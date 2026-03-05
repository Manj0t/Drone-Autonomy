#!/usr/bin/env python3
import math
import time
import subprocess

TOPIC = "/model/x500_lidar_2d_0/joint/LidarPitchJoint/cmd_pos"
AMP_RAD = 0.5     # +/- radians (~34 deg)
FREQ_HZ = 1.0     # sweeps per second
DT = 0.01         # command update period (50 Hz)

def publish(angle: float) -> None:
    subprocess.run(
        ["gz", "topic", "-t", TOPIC, "-m", "gz.msgs.Double", "-p", f"data: {angle}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

def main():
    t = 0.0
    while True:
        angle = AMP_RAD * math.sin(2 * math.pi * FREQ_HZ * t)
        publish(angle)
        time.sleep(DT)
        t += DT

if __name__ == "__main__":
    main()
