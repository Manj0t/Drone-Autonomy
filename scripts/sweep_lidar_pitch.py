#!/usr/bin/env python3
import math
import time
import subprocess
from gz.transport13 import Node  # sometimes transport11/12/13 depending on install
from gz.msgs.double_pb2 import Double

TOPIC = "/model/x500_lidar_2d_0/joint/LidarPitchJoint/cmd_pos"
AMP_RAD = 0.5     # +/- radians (~34 deg)
FREQ_HZ = 1.0     # sweeps per second
DT = 0.01         # command update period (50 Hz)
PUB_HZ = 200

def publish(angle: float) -> None:
    subprocess.run(
        ["gz", "topic", "-t", TOPIC, "-m", "gz.msgs.Double", "-p", f"data: {angle}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

def main():
    node = Node()
    pub = node.advertise(TOPIC, Double)

    t0 = time.perf_counter()
    dt = 1.0/PUB_HZ

    while True:
        t = time.perf_counter() - t0
        angle = AMP_RAD * math.sin(2 * math.pi * FREQ_HZ * t)

        msg = Double()
        msg.data = angle
        pub.publish(msg)

        time.sleep(dt)
        print(angle)

if __name__ == "__main__":
    main()
