#!/data/data/com.termux/files/usr/bin/bash

# Firewall Guardian - Keeps the monitor running in the background
# Survives crashes and attempts to stay active across user sessions

cd "$(dirname "$0")"

# Ensure wake lock is active
termux-wake-lock

echo "Firewall Guardian started. Monitoring link_monitor.py..."

while true; do
    # Check if link_monitor_go is already running
    if ! pgrep -x "link_monitor_go" > /dev/null; then
        echo "[$(date)] Go Link Monitor not found. Starting..."
        ./link_monitor_go >> monitor_debug.log 2>&1
    fi
    sleep 30
done
