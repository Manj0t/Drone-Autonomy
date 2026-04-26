#!/usr/bin/env bash
# ==============================================================================
# start_bridges.sh — Launch all Gazebo <-> ROS 2 bridges
#
# Usage:  ./start_bridges.sh
# Stop:   Ctrl+C
#
# HOW TO ADD BRIDGES:
#   Add a `_launch` call below in the BRIDGES section.
#   Format: _launch "description" ros2 run ros_gz_bridge parameter_bridge <topic@ROS_type[gz_type>
# ==============================================================================

set -o pipefail

source /opt/ros/jazzy/setup.bash
source ~/drone-autonomy/ros2_ws/install/setup.bash

declare -a _PIDS=()
declare -a _LABELS=()

_launch() {
    local label="$1"; shift
    echo "[START] $label"
    "$@" &
    _PIDS+=("$!")
    _LABELS+=("$label")
}

_cleanup() {
    echo ""
    echo "[STOP] Shutting down bridges..."
    local i
    for i in "${!_PIDS[@]}"; do
        local pid="${_PIDS[$i]}"
        if kill -0 "$pid" 2>/dev/null; then
            echo "  stopping: ${_LABELS[$i]} (pid $pid)"
            kill "$pid" 2>/dev/null
        fi
    done
    wait 2>/dev/null
    echo "[DONE] All bridges stopped."
}
trap _cleanup EXIT INT TERM

# ==============================================================================
# BRIDGES
# ==============================================================================

_launch "Micro XRCE-DDS Agent (PX4 <-> ROS 2)" \
    micro-xrce-dds-agent udp4 -p 8888

sleep 2

_launch "LaserScan bridge — 2D lidar scan" \
    ros2 run ros_gz_bridge parameter_bridge \
    /world/default/model/x500_lidar_2d_0/link/link/sensor/lidar_2d_v2/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan

sleep 1

_launch "Float64 bridge — LidarPitchJoint cmd_pos" \
    ros2 run ros_gz_bridge parameter_bridge \
    /model/x500_lidar_2d_0/joint/LidarPitchJoint/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double

sleep 1

_launch "Camera image bridge" \
    ros2 run ros_gz_bridge parameter_bridge \
    /world/default/model/x500_lidar_2d_0/link/camera_link/sensor/IMX214/image@sensor_msgs/msg/Image[gz.msgs.Image

sleep 1

_launch "Camera info bridge" \
    ros2 run ros_gz_bridge parameter_bridge \
    /world/default/model/x500_lidar_2d_0/link/camera_link/sensor/IMX214/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo

sleep 1

_launch "Camera IMU bridge" \
    ros2 run ros_gz_bridge parameter_bridge \
    /world/default/model/x500_lidar_2d_0/link/camera_link/sensor/camera_imu/imu@sensor_msgs/msg/Imu[gz.msgs.IMU

sleep 1

_launch "Depth point cloud bridge" \
    ros2 run ros_gz_bridge parameter_bridge \
    /depth_camera/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked

sleep 1

_launch "3D lidar point cloud bridge" \
    ros2 run ros_gz_bridge parameter_bridge \
    /world/default/model/x500_lidar_2d_0/link/lidar_sensor_link/sensor/lidar/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked

sleep 1

_launch "Odometry with covariance bridge" \
    ros2 run ros_gz_bridge parameter_bridge \
    /model/x500_lidar_2d_0/odometry_with_covariance@nav_msgs/msg/Odometry[gz.msgs.OdometryWithCovariance

sleep 1

_launch "Clock bridge — Gazebo sim time" \
      ros2 run ros_gz_bridge parameter_bridge \
      /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock

sleep 1

_launch "Model TF bridge — drone link transforms" \
      ros2 run ros_gz_bridge parameter_bridge \
      /world/default/dynamic_pose/info@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V

# --- Add future bridges below this line ---


# ==============================================================================
# STATUS + WAIT
# ==============================================================================
echo ""
echo "============================================"
echo " All bridges running. Ctrl+C to stop all."
echo "============================================"
printf "  %-6s  %s\n" "PID" "Label"
printf "  %-6s  %s\n" "------" "-----"
for i in "${!_PIDS[@]}"; do
    printf "  %-6s  %s\n" "${_PIDS[$i]}" "${_LABELS[$i]}"
done
echo ""

wait
