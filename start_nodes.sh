#!/usr/bin/env bash
# ==============================================================================
# start_nodes.sh — Launch all ROS 2 nodes
#
# Usage:  ./start_nodes.sh
# Stop:   Ctrl+C
#
# HOW TO ADD NODES:
#   Add a `_launch` call below in the ROS NODES section.
#   Format: _launch "description" ros2 run <package> <executable>
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
    echo "[STOP] Shutting down nodes..."
    local i
    for i in "${!_PIDS[@]}"; do
        local pid="${_PIDS[$i]}"
        if kill -0 "$pid" 2>/dev/null; then
            echo "  stopping: ${_LABELS[$i]} (pid $pid)"
            kill "$pid" 2>/dev/null
        fi
    done
    wait 2>/dev/null
    echo "[DONE] All nodes stopped."
}
trap _cleanup EXIT INT TERM

# ==============================================================================
# ROS NODES
# ==============================================================================

_launch "Lidar pitch sweep" \
    ros2 run lidar_pitch_sweep sweep_node

sleep 1

_launch "Point cloud collector" \
    ros2 run spinning_lidar collect_points

# --- Add future nodes below this line ---


# ==============================================================================
# STATUS + WAIT
# ==============================================================================
echo ""
echo "============================================"
echo " All nodes running. Ctrl+C to stop all."
echo "============================================"
printf "  %-6s  %s\n" "PID" "Label"
printf "  %-6s  %s\n" "------" "-----"
for i in "${!_PIDS[@]}"; do
    printf "  %-6s  %s\n" "${_PIDS[$i]}" "${_LABELS[$i]}"
done
echo ""

wait
