#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

import math
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

from std_msgs.msg import Float64

import numpy as np

PI = math.pi
MAX_POINTS = 100000
L = 0.26

def cos(x):
    return math.cos(x)

def sin(x):
    return math.sin(x)

class ScanPrinter(Node):
    def __init__(self):
        super().__init__('scan_printer')
        self.create_subscription(
            LaserScan, # Idk, can be anything maybe lonag as consistnet? Not sure
            '/world/default/model/x500_lidar_2d_0/link/link/sensor/lidar_2d_v2/scan', # Subscirbes to the 2d lidar
            self.on_scan,
            10
        )
        self.create_subscription(
            Float64,
            "/model/x500_lidar_2d_0/joint/LidarPitchJoint/cmd_pos",
            self.on_pitch,
            10
        )

        self.current_pitch = 0.0
        self.marker_pub = self.create_publisher(Marker, 'lidar_points', 10) # Create Publisher for RVIZ to subscribe to
        self.fov_pub = self.create_publisher(Marker, 'lidar_fov', 10)


        self.marker = Marker()
        self.marker.header.frame_id = 'world'
        # Tell RVIZ how to map these points
        self.marker.type = Marker.POINTS

        # Unique identifiers
        self.marker.action = Marker.ADD
        self.marker.ns = "lidar"
        self.marker.id = 0

        self.marker.pose.orientation.w = 1.0  # orientation

        # RGB
        self.marker.color.r = 1.0
        self.marker.color.g = 1.0
        self.marker.color.b = 1.0
        self.marker.color.a = 1.0  # Opacity

        # Point size (0.3 == 3cm)
        self.marker.scale.x = 0.01
        self.marker.scale.y = 0.01
    
    def on_pitch(self, msg: Float64) -> None:
        self.current_pitch = msg.data

    def get_points(self, r: float, angle: float, pitch: float) -> Point:
        p = Point()

        x_local = r * math.cos(angle)
        y_local = r * math.sin(angle)

        
        # Rotate the point based on the LiDAR pitch
        gamma = PI/2 - pitch

        P_0 = np.array([0 + L * math.sin(pitch), 0, 0 + L * math.cos(pitch)])

        N = np.array([cos(gamma), 0, sin(gamma)])

        a = np.array([cos(PI - pitch), 0, sin(PI - pitch)])
        b = np.array([0.0, 1.0, 0.0])

        world_vec = P_0 + x_local * a + y_local * b

        p.x, p.y, p.z = world_vec

        return p
    

    def on_scan(self, msg: LaserScan) -> None:
        self.marker.header.stamp = self.get_clock().now().to_msg() # Not entirely sure why

        thet: float = self.current_pitch
        angle: float = msg.angle_min

        for r in msg.ranges:
            # If no object is hit, don't map
            if math.isfinite(r):
                p = self.get_points(r, angle, thet)
                
                self.marker.points.append(p)

                if len(self.marker.points) > MAX_POINTS:
                    self.marker.points.pop(0)          

            angle += msg.angle_increment

        # Publish points for RVIZ
        self.marker_pub.publish(self.marker)



        ########## IGNORE BELOW
        # temp
        m = Marker()
        m.header.frame_id = "world" # msg.header.frame_id or "
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "lidar"
        m.id = 1
        m.action = Marker.ADD
        m.type = Marker.LINE_LIST
        m.pose.orientation.w = 1.0

        m.scale.x = 0.005  # line thickness (meters)

        # Color
        m.color.r = 0.0
        m.color.g = 1.0
        m.color.b = 0.0
        m.color.a = 0.25  # transparent rays

        max_r = msg.range_max
        angle = msg.angle_min

        step = 10  # draw every 10th beam so it isn't a solid blob
        for i, r in enumerate(msg.ranges):
            if i % step != 0:
                angle += msg.angle_increment
                continue

            # origin
            p0 = Point(x=0.0, y=0.0, z=0.0)

            # endpoint at max range (this shows the sweep even if no hit)
            p1 = Point()
            p1.x = max_r * math.cos(angle)
            p1.y = max_r * math.sin(angle)
            p1.z = 0.0

            m.points.append(p0)
            m.points.append(p1)

            angle += msg.angle_increment

        self.fov_pub.publish(m)




        self.get_logger().info(f"Got scan with {len(msg.ranges)} ranges")




def main():
    rclpy.init()
    node = ScanPrinter()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
