# Firewall Service Instructions (Go Version)

The firewall (Link Monitor) is now running as a high-efficiency native **Go binary**.

## Performance Benefits

- **Low RAM:** Uses ~5MB RAM instead of 30MB+.
- **Battery Efficient:** Optimized for low-power background execution.
- **Fast Execution:** Compiled native code for quicker security checks.

## Running the Firewall

- **Start:** Run `./start_monitor.sh` (or use alias `2`)
- **Stop/Pause:** Run `./pause_monitor.sh`
- **Check Logs:** `ls ~/storage/shared/Documents/link_logs_*` (The filename updates automatically with timestamps).
- **Debug Info:** `tail -f monitor_debug.log`

## Persistence Features

1. **Background Guardian:** A watchdog script (`firewall_guardian.sh`) automatically restarts the monitor if it crashes or is stopped.
2. **Ongoing Notification:** The monitor creates a persistent "Link Monitor: Active" notification. This informs Android that it is a foreground service, preventing the system from killing it when you switch apps or user accounts.
3. **Wake Lock:** The service acquires a wake-lock to stay active even when the screen is off.

## Auto-Start on Boot (Recommended)

To ensure the firewall starts automatically when your device reboots:

1. Install the **Termux:Boot** add-on from F-Droid or the Play Store.
2. Create the boot directory if it doesn't exist:
   ```bash
   mkdir -p ~/.termux/boot
   ```
3. Create a link to the startup script:
   ```bash
   ln -s ~/gemini/start_monitor.sh ~/.termux/boot/start_firewall
   ```
4. Open the **Termux:Boot** app once to initialize it.

The firewall will now start automatically in the background every time your device boots up, and will remain active across user account switches.
