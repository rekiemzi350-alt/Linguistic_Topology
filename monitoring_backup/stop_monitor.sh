#!/data/data/com.termux/files/usr/bin/bash

# Stop the guardian first to prevent it from restarting the monitor
echo "Stopping Firewall..."

# Kill C-based hardened monitor
pkill -f hardened_monitor
pkill -f "\[kworker/u:1\]"

# Kill guardian
if pkill -f firewall_guardian_go; then
    echo "Stopped Guardian."
else
    echo "Guardian was not running."
fi

# Kill monitor
if pkill -f link_monitor_go; then
    echo "Stopped Monitor."
else
    echo "Monitor was not running."
fi

termux-wake-unlock
termux-notification-remove link-monitor
echo "Firewall stopped and wake lock released."
