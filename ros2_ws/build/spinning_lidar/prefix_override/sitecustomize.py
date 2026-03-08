import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sandhm1/Drone-Autonomy/ros2_ws/install/spinning_lidar'
