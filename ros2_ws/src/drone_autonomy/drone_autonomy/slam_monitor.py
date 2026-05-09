import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from nav_msgs.msg import OccupancyGrid, Odometry
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool, Float32


class SLAMMonitor(Node):
    def __init__(self):
        super().__init__('slam_monitor')

        # params from launch file
        # Default vals if no specified in launch file
        self.declare_parameter('min_inliers', 10)
        self.declare_parameter('lost_threshold_sec', 3.0)
        self.declare_parameter('confidence_alpha', 0.1)

        self.min_inliers = self.get_parameter('min_inliers').value
        self.lost_timeout = self.get_parameter('lost_threshold_sec').value
        self.alpha = self.get_parameter('confidence_alpha').value

        self.slam_confidence = 1.0  # Current Confidence
        self.loop_closure_count = 0
        self.last_good_stamp = self.get_clock().now()
        self.is_lost = False

        # QoS - Quality of Service settings
        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            depth=5,
        )

        # --- Subscribers ---
        # Listen to RTAB-Map's outputs
        self.create_subscription(
            Odometry, '/rtabmap/odom',
            self._odom_cb, reliable_qos,
        )
        self.create_subscription(
            OccupancyGrid, '/map',
            self._map_cb, reliable_qos,
        )

        # --- Publishers ---
        # Clean interface for state machine
        self.pose_pub = self.create_publisher(
            PoseStamped, '/slam/corrected_pose', 10,
        )
        self.map_pub = self.create_publisher(
            OccupancyGrid, '/slam/map', reliable_qos,
        )
        self.lost_pub = self.create_publisher(
            Bool, '/slam/is_lost', 10,
        )
        self.confidence_pub = self.create_publisher(
            Float32, '/slam/confidence', 10,
        )

        # Health check runs every second
        self.create_timer(1.0, self._health_check)
        self.get_logger().info('SLAM Monitor started')

    def _odom_cb(self, msg: Odometry):
        """
        Called every time RTAB-Map publishes corrected odometry.
        If we're receiving odom, SLAM is tracking.
        """
        # Convert Odometry to simpler PoseStamped
        pose_msg = PoseStamped()
        pose_msg.header = msg.header
        pose_msg.pose = msg.pose.pose
        self.pose_pub.publish(pose_msg)

        # We got valid odom, so SLAM is alive
        self.last_good_stamp = self.get_clock().now()
        if self.is_lost:
            self.is_lost = False
            self.slam_confidence = 0.5 # Recovered but not fully confident yet
            self.get_logger().info('SLAM tracking recovered')

    def _map_cb(self, msg: OccupancyGrid):
        """
        Forward occupancy grid to explore_lite.
        """
        self.map_pub.publish(msg)

    def _health_check(self):
        """
        Runs every 1 second. Checks if SLAM is still alive.
        """
        elapsed = (
            self.get_clock().now() - self.last_good_stamp
        ).nanoseconds / 1e9

        # If no good odom for too long, SLAM is lost
        if elapsed > self.lost_timeout and not self.is_lost:
            self.is_lost = True
            self.slam_confidence = 0.0
            self.get_logger().warn(
                f'SLAM lost! No odom for {elapsed:.1f}s. '
                'State machine should enter recovery.'
            )

        # Gradually restore confidence while tracking
        if not self.is_lost:
            # Slowly increase confidence over time
            self.slam_confidence = min(
                1.0,
                self.slam_confidence + self.alpha * 0.1,
            )

        # Publish status
        lost_msg = Bool()
        lost_msg.data = self.is_lost
        self.lost_pub.publish(lost_msg)

        conf_msg = Float32()
        conf_msg.data = self.slam_confidence
        self.confidence_pub.publish(conf_msg)


def main(args=None):
    rclpy.init(args=args)
    node = SLAMMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()