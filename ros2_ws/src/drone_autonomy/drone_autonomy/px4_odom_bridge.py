#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

from px4_msgs.msg import VehicleOdometry
from nav_msgs.msg import Odometry
from rosgraph_msgs.msg import Clock
from geometry_msgs.msg import TransformStamped
import tf2_ros


# Static quaternions for NED/FRD → ENU/FLU conversion
# q_ned_to_enu: 180° around axis [1/√2, 1/√2, 0] — maps North→East, East→North, Down→Up
_S2 = math.sqrt(2) / 2
_Q_NED_TO_ENU = (_S2, _S2, 0.0, 0.0)  # (x, y, z, w) scipy convention

# q_frd_to_flu: 180° around forward (X) axis — maps Right→Left, Down→Up
_Q_FRD_TO_FLU = (1.0, 0.0, 0.0, 0.0)  # (x, y, z, w)


def _quat_mul(a, b):
    """Quaternion multiply (x,y,z,w) convention."""
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (
        aw*bx + ax*bw + ay*bz - az*by,
        aw*by - ax*bz + ay*bw + az*bx,
        aw*bz + ax*by - ay*bx + az*bw,
        aw*bw - ax*bx - ay*by - az*bz,
    )


def _quat_conj(q):
    x, y, z, w = q
    return (-x, -y, -z, w)


def _px4_to_ros_quat(q_px4_wxyz):
    """Convert PX4 quaternion [w,x,y,z] NED/FRD to ROS [x,y,z,w] ENU/FLU."""
    w, x, y, z = q_px4_wxyz
    q = (x, y, z, w)  # repack to (x,y,z,w)
    q_result = _quat_mul(_Q_NED_TO_ENU, _quat_mul(q, _quat_conj(_Q_FRD_TO_FLU)))
    return q_result  # (x, y, z, w)


class PX4OdomBridge(Node):
    def __init__(self):
        super().__init__('px4_odom_bridge')

        px4_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.sim_time = None
        self.create_subscription(Clock, '/clock', self._clock_cb, 10)

        self.sub = self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self._cb,
            px4_qos,
        )
        self.pub = self.create_publisher(Odometry, '/odom', 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.get_logger().info('PX4 odom bridge started')

    def _clock_cb(self, msg: Clock):
        self.sim_time = msg.clock

    def _cb(self, msg: VehicleOdometry):
        if self.sim_time is None or any(math.isnan(v) for v in msg.position):
            return

        odom = Odometry()
        odom.header.stamp = self.sim_time  # Gazebo sim time, matches sensor topics
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        # Position: NED → ENU
        odom.pose.pose.position.x = float(msg.position[1])   # East
        odom.pose.pose.position.y = float(msg.position[0])   # North
        odom.pose.pose.position.z = float(-msg.position[2])  # Up

        # Orientation: PX4 [w,x,y,z] FRD/NED → ROS [x,y,z,w] FLU/ENU
        if not math.isnan(msg.q[0]):
            qx, qy, qz, qw = _px4_to_ros_quat(msg.q)
            odom.pose.pose.orientation.x = qx
            odom.pose.pose.orientation.y = qy
            odom.pose.pose.orientation.z = qz
            odom.pose.pose.orientation.w = qw

        # Velocity: NED → ENU
        if not math.isnan(msg.velocity[0]):
            odom.twist.twist.linear.x = float(msg.velocity[1])
            odom.twist.twist.linear.y = float(msg.velocity[0])
            odom.twist.twist.linear.z = float(-msg.velocity[2])

        # Angular velocity: FRD → FLU (flip Y and Z)
        if not math.isnan(msg.angular_velocity[0]):
            odom.twist.twist.angular.x = float(msg.angular_velocity[0])
            odom.twist.twist.angular.y = float(-msg.angular_velocity[1])
            odom.twist.twist.angular.z = float(-msg.angular_velocity[2])

        self.pub.publish(odom)

        # Publish odom -> base_link TF (rtabmap needs this alongside the topic)
        tf = TransformStamped()
        tf.header.stamp = odom.header.stamp
        tf.header.frame_id = 'odom'
        tf.child_frame_id = 'base_link'
        tf.transform.translation.x = odom.pose.pose.position.x
        tf.transform.translation.y = odom.pose.pose.position.y
        tf.transform.translation.z = odom.pose.pose.position.z
        tf.transform.rotation = odom.pose.pose.orientation
        self.tf_broadcaster.sendTransform(tf)


def main(args=None):
    rclpy.init(args=args)
    node = PX4OdomBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        try:
            rclpy.shutdown()
        except Exception:
            pass


if __name__ == '__main__':
    main()
