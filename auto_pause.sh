#!/data/data/com.termux/files/usr/bin/bash

# Periodically check if gemini CLI is running and pause security tools
while true; do
    # Check for gemini processes
    if pgrep -f "node.*gemini" > /dev/null; then
        # Check if security tools are currently running
        if pgrep -f "firewall_guardian_go" > /dev/null; then
            echo "[$(date)] Gemini CLI detected. Pausing security suite..."
            /data/data/com.termux/files/home/gemini/pause_monitor.sh
        fi
    fi
    sleep 10
done
