#!/usr/bin/env bash
# ==============================================================================
# start_sim.sh — Launch PX4 SITL (gz_x500_lidar_2d), RViz2, and QGroundControl
#
# Usage:  ./start_sim.sh
# Stop:   Ctrl+C
# ==============================================================================

set -o pipefail

source /opt/ros/jazzy/setup.bash

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
    echo "[STOP] Shutting down..."
    local i
    for i in "${!_PIDS[@]}"; do
        local pid="${_PIDS[$i]}"
        if kill -0 "$pid" 2>/dev/null; then
            echo "  stopping: ${_LABELS[$i]} (pid $pid)"
            kill "$pid" 2>/dev/null
        fi
    done
    wait 2>/dev/null
    echo "[DONE] All processes stopped."
}
trap _cleanup EXIT INT TERM

# ------------------------------------------------------------------------------
# PX4 SITL — gz_x500_lidar_2d
# ------------------------------------------------------------------------------
_launch "PX4 SITL (gz_x500_lidar_2d)" \
    bash -c "cd ~/drone-autonomy/PX4-Autopilot && make px4_sitl gz_x500_lidar_2d"

sleep 5   # give Gazebo time to come up before launching RViz / QGC

# ------------------------------------------------------------------------------
# RViz2
# ------------------------------------------------------------------------------
_launch "RViz2" rviz2

sleep 2

# ------------------------------------------------------------------------------
# QGroundControl
# ------------------------------------------------------------------------------
_launch "QGroundControl" ~/Downloads/QGroundControl-x86_64.AppImage


# ==============================================================================
# STATUS + WAIT
# ==============================================================================
echo ""
echo "============================================"
echo " All sim processes running. Ctrl+C to stop."
echo "============================================"
printf "  %-6s  %s\n" "PID" "Label"
printf "  %-6s  %s\n" "------" "-----"
for i in "${!_PIDS[@]}"; do
    printf "  %-6s  %s\n" "${_PIDS[$i]}" "${_LABELS[$i]}"
done
echo ""

wait
