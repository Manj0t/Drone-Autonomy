#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

import math
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

class ScanPrinter(Node):
    def __init__(self):
        super().__init__('scan_printer')
        self.create_subscription(
            LaserScan, # Idk, can be anything maybe lonag as consistnet? Not sure
            '/world/default/model/x500_lidar_2d_0/link/link/sensor/lidar_2d_v2/scan', # Subscirbes to the 2d lidar
            self.on_scan,
            10
        )
        self.marker_pub = self.create_publisher(Marker, 'lidar_points', 10) # Create Publisher for RVIZ to subscribe to
        self.fov_pub = self.create_publisher(Marker, 'lidar_fov', 10)

    def on_scan(self, msg):
        marker = Marker()
        marker.header.frame_id = 'link'
        marker.header.stamp = self.get_clock().now().to_msg() # Not entirely sure why
        # Tell RVIZ how to map these points
        marker.type = Marker.POINTS

        # Unique identifiers
        marker.action = Marker.ADD
        marker.ns = "lidar"
        marker.id = 0

        marker.pose.orientation.w = 1.0  # valid orientation

        # RGB
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0  # Opacity

        # Point size (0.3 == 3cm)
        marker.scale.x = 0.01
        marker.scale.y = 0.01

        angle = msg.angle_min
        for r in msg.ranges:
            # If no object is hit, don't map
            if math.isfinite(r):
                p = Point()
                # Map to cartesian points
                p.x = r * math.cos(angle)
                p.y = r * math.sin(angle)
                p.z = 0.0
                marker.points.append(p)

            angle += msg.angle_increment

        # Publish points for RVIZ
        self.marker_pub.publish(marker)


        # temp
        m = Marker()
        m.header.frame_id = msg.header.frame_id or "link"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "lidar"
        m.id = 1
        m.action = Marker.ADD
        m.type = Marker.LINE_LIST
        m.pose.orientation.w = 1.0

        m.scale.x = 0.005  # line thickness (meters)

        # Color (alpha is crucial)
        m.color.r = 0.0
        m.color.g = 1.0
        m.color.b = 0.0
        m.color.a = 0.25  # transparent rays

        max_r = msg.range_max
        angle = msg.angle_min

        step = 10  # draw every 10th beam so it isn't a solid blob (tune this)
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
