#!/usr/bin/env bash
# ==============================================================================
# start_all.sh — Launch everything: sim, bridges, and ROS 2 nodes
#
# Usage:  ./start_all.sh
# Stop:   Ctrl+C  (kills every process started by this script, nothing else)
#
# This script launches the three component scripts in separate terminals.
# Requires a display / terminal emulator (gnome-terminal used by default).
# ==============================================================================

set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

_open_terminal() {
    local title="$1"
    local script="$2"

    if command -v gnome-terminal &>/dev/null; then
        gnome-terminal --title="$title" -- bash -c "\"$script\"; exec bash" &
    elif command -v xterm &>/dev/null; then
        xterm -title "$title" -e bash -c "\"$script\"; exec bash" &
    else
        echo "[WARN] No supported terminal emulator found. Running $script in background."
        bash "$script" &
    fi
}

echo "[START] Launching sim environment (PX4 SITL, RViz, QGroundControl)..."
_open_terminal "Sim (SITL + RViz + QGC)" "$SCRIPT_DIR/start_sim.sh"

echo "Waiting 10 s for sim to initialize before starting bridges..."
sleep 10

echo "[START] Launching bridges..."
_open_terminal "Bridges" "$SCRIPT_DIR/start_bridges.sh"

echo "Waiting 5 s for bridges to connect before starting nodes..."
sleep 5

echo "[START] Launching ROS 2 nodes..."
_open_terminal "Nodes" "$SCRIPT_DIR/start_nodes.sh"

echo ""
echo "============================================"
echo " All windows launched."
echo " Close individual terminals to stop each."
echo "============================================"
