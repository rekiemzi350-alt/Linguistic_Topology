#!/data/data/com.termux/files/usr/bin/bash

# Ensure we are in the right directory
cd "$(dirname "$0")"

# Acquire wake lock to prevent the system from sleeping
termux-wake-lock

# Start the ultra-efficient C-based hardened monitor
echo "Starting Hardened C-Core Monitor..."
./hardened_monitor

echo "Starting Go Firewall Guardian in background..."
nohup ./firewall_guardian_go > /dev/null 2>&1 &

echo "Firewall started and guarded. PID: $!"
echo "A persistent notification should appear shortly."
echo "Check link_logs.txt for activity."
