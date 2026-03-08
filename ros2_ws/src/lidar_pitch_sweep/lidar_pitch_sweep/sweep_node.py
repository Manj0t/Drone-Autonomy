import math
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

TOPIC = "/model/x500_lidar_2d_0/joint/LidarPitchJoint/cmd_pos"

PUB_HZ = 200
AMP_RAD = 1
FREQ_HZ = 1.0
PHI = math.pi / 2

class LidarPitchSweep(Node):
    def __init__(self):
        super().__init__("lidar_pitch_sweep")                   # Can be any name, maintain consistency 

        self.pub = self.create_publisher(Float64, TOPIC, 10)    # (message type, topic, buffer/queue size)

        self.t0 = time.perf_counter()                           # Gets current time to a high precision
        self.timer = self.create_timer(1.0 / PUB_HZ, self.tick) # Runs function tick() ever 1.0 / PUB_HZ seconds. In this case 1/200 = 0.005 seconds or 5 ms.

    def tick(self):
        """ Sinusoidal motion eq: q(t) = A sin(2π * f * t + φ) + C
                                         A : amplitude (How far it moves from center)
                                         f : Oscillaiton Frequency
                                         2π : works in radiance, converts frequency into angular motion (2π * f)
                                         φ : Phase shift. Shifts the starting pos of the wave (0=center start, π/2=max start)
                                         C : Vertical offset, 0 used here
        """
        t1 = time.perf_counter()
        t = t1 - self.t0
        period = 1 / FREQ_HZ

        angle = 2 * AMP_RAD / math.pi * math.asin(math.sin(2 * math.pi * t / period))
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