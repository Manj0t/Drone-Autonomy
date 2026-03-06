import math
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

TOPIC = "/model/x500_lidar_2d_0/joint/LidarPitchJoint/cmd_pos"

AMP_RAD = 0.5   # +/- min/max angle
FREQ_HZ = 1.0   # 1 sweep per second
PUB_HZ  = 200   # smoother motion

class LidarPitchSweep(Node):
    def __init__(self):
        super().__init__("lidar_pitch_sweep")
        self.pub = self.create_publisher(Float64, TOPIC, 10)

        self.t0 = time.perf_counter()
        self.dt = 1.0 / PUB_HZ
        self.timer = self.create_timer(self.dt, self.tick)

    def tick(self):
        t = time.perf_counter() - self.t0
        angle = AMP_RAD * math.sin(2 * math.pi * FREQ_HZ * t)
        print(angle)

        msg = Float64()
        msg.data = angle
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = LidarPitchSweep()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()