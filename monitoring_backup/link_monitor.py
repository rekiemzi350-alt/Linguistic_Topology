import subprocess
import json
import time
import os
import threading
from datetime import datetime

LOG_DIR = os.path.expanduser("~/storage/shared/Documents")
SESSION_START = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
CURRENT_LOG_PATH = None
STATE_FILE = "monitor_state.json"
DOWNLOAD_DIRS = ["/sdcard/Download", "/data/data/com.termux/files/home/downloads"]

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            return None
        return result.stdout.strip()
    except Exception as e:
        return None

def get_json(command):
    output = run_command(command)
    if output:
        try:
            return json.loads(output)
        except:
            return None
    return None

def log(message):
    global CURRENT_LOG_PATH
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Create/Update filename with session start and last update time
    update_time = now.strftime("%H-%M-%S")
    new_filename = f"link_logs_started_{SESSION_START}_last_updated_{update_time}.txt"
    new_path = os.path.join(LOG_DIR, new_filename)
    
    # Rename the file if it already exists to update the "last_updated" part of the name
    if CURRENT_LOG_PATH and os.path.exists(CURRENT_LOG_PATH):
        try:
            os.rename(CURRENT_LOG_PATH, new_path)
        except:
            new_path = CURRENT_LOG_PATH # Fallback if rename fails
            
    CURRENT_LOG_PATH = new_path
    
    with open(CURRENT_LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def panic_alert(message, critical=False):
    log(f"🚨 PANIC ALERT: {message}")
    # Physical Alert (Vibration)
    duration = 1000 if critical else 500
    run_command(f"termux-vibrate -d {duration}")
    # Audio Alert (TTS)
    safe_msg = message.replace('"', '').replace("'", "")
    run_command(f"termux-tts-speak 'Alert: {safe_msg}'")
    # Screen Notification
    run_command(f"termux-notification -t 'SECURITY ALERT' -c '{message}' --priority high")

SECURITY_KEYWORDS = ["sign-in", "login", "security", "verify", "code", "alert", "account", "access", "unusual", "password"]
PROXY_PROCESSES = ["ssh", "ngrok", "frp", "proxy", "tunnel", "tor", "vpn"]

def is_security_alert(text):
    if not text: return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in SECURITY_KEYWORDS)

def check_proxy_processes():
    ps = run_command("ps -e")
    if ps:
        for line in ps.splitlines():
            if any(proxy in line.lower() for proxy in PROXY_PROCESSES):
                if "link_monitor.py" not in line:
                    msg = f"PROXY/TUNNEL PROCESS DETECTED: {line.split()[-1]}"
                    panic_alert(msg, critical=True)
                    log(f"   Level of Access: Potential Remote Tunnel/Proxy")

def file_monitor_thread():
    log(f"Starting File Monitor on: {', '.join(DOWNLOAD_DIRS)}")
    # Check if directories exist before monitoring
    valid_dirs = [d for d in DOWNLOAD_DIRS if os.path.exists(d)]
    if not valid_dirs:
        log("No valid download directories found for monitoring.")
        return

    cmd = f"inotifywait -m -r -e create,moved_to {' '.join(valid_dirs)}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    while True:
        line = process.stdout.readline()
        if not line:
            break
        parts = line.split()
        if len(parts) >= 3:
            directory, event, filename = parts[0], parts[1], parts[2]
            msg = f"NEW DOWNLOAD: {filename}"
            log(f"📥 {msg} (Event: {event})")
            log(f"   Level of Access: File System Write")
            # Vibration only for downloads
            run_command("termux-vibrate -d 200")

def update_status(message):
    log(f"Status: {message}")
    # Update persistent notification to prevent Android from killing the process
    safe_msg = message.replace('"', '').replace("'", "")
    run_command(f"termux-notification -t 'Link Monitor: Active' -c '{safe_msg}' --id link-monitor --ongoing --priority low")

def monitor():
    log("Starting ACTIVATED PANIC MONITOR (Tactile/Audio Defense)...")
    update_status("Monitoring for threats...")
    
    # Start file monitor in a separate thread
    threading.Thread(target=file_monitor_thread, daemon=True).start()

    known_notifications = set()
    known_connections = set()
    known_sms = set()
    known_usb = set()
    known_neighbors = set()
    current_bssid = None
    current_cell = None
    
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                known_notifications = set(state.get("notifications", []))
                known_connections = set(state.get("connections", []))
                known_sms = set(state.get("sms", []))
                known_usb = set(state.get("usb", []))
                known_neighbors = set(state.get("neighbors", []))
                current_bssid = state.get("bssid")
                current_cell = state.get("cell")
        except:
            pass

    try:
        while True:
            try:
                # 1. Check Proxy Processes
                check_proxy_processes()

                # 2. Monitor Notifications (Apps/Texts/Emails/Account Access)
                notifications = get_json("termux-notification-list")
                if notifications:
                    for n in notifications:
                        pkg = n.get('packageName', '')
                        title = n.get('title', '')
                        content = n.get('content', '')
                        n_id = f"{pkg}|{title}|{content}"
                        
                        if n_id not in known_notifications:
                            msg = f"[{pkg}] {title}: {content}"
                            
                            # Detect Account Access Info
                            account_info = ""
                            level = "Notification Visibility"
                            if "com.google.android.gm" in pkg:
                                account_info = " (Account: Gmail)"
                                level = "Account Data Access"
                            elif "com.android.vending" in pkg:
                                account_info = " (Account: Play Store)"
                                level = "App Management Access"
                            
                            if is_security_alert(title) or is_security_alert(content):
                                panic_alert(f"Security Alert{account_info}", critical=True)
                                log(f"⚠️ {msg}")
                                log(f"   Level of Access: {level} (Sensitive)")
                            else:
                                log(f"NEW NOTIFICATION: {msg}")
                                log(f"   Level of Access: {level}")
                                
                            known_notifications.add(n_id)

                # 3. Monitor SMS
                sms_list = get_json("termux-sms-list -l 5")
                if sms_list:
                    for msg in sms_list:
                        number = msg.get('number')
                        body = msg.get('body', '')
                        sms_id = f"{number}|{msg.get('received')}|{body}"
                        
                        if sms_id not in known_sms:
                            if is_security_alert(body):
                                panic_alert(f"Sensitive SMS from {number}", critical=True)
                                log(f"⚠️ SECURITY SMS from {number}: {body}")
                            else:
                                log(f"NEW SMS from {number}: {body}")
                                log(f"   Level of Access: SMS Reading")
                            known_sms.add(sms_id)

                # 4. Monitor Network Connections (Neighbors)
                neighbors = run_command("ip neigh show")
                if neighbors:
                    active_neighbors = set()
                    for line in neighbors.splitlines():
                        if any(s in line for s in ["REACHABLE", "STALE", "DELAY"]):
                            parts = line.split()
                            if parts:
                                ip = parts[0]
                                active_neighbors.add(ip)
                    
                    new_neighbors = active_neighbors - known_neighbors
                    for ip in new_neighbors:
                        panic_alert(f"New Device on Network: {ip}")
                        log(f"🔗 Details: {run_command(f'ip neigh show {ip}')}")
                    known_neighbors = active_neighbors

                # 5. Monitor USB & ADB
                usb_list = get_json("termux-usb -l")
                if usb_list:
                    current_usb = set(usb_list)
                    new_usb = current_usb - known_usb
                    for device in new_usb:
                        panic_alert(f"USB Hardware Connected: {device}", critical=True)
                        log(f"🔌 Level of Access: Physical Hardware Link")
                    known_usb = current_usb

                # 6. WiFi/Cellular Location Mapping
                wifi = get_json("termux-wifi-connectioninfo")
                if wifi and wifi.get("bssid") != current_bssid:
                    log(f"📍 WIFI LINKED: {wifi.get('ssid')} ({wifi.get('bssid')})")
                    current_bssid = wifi.get("bssid")
                    update_status(f"Connected to {wifi.get('ssid')}")

                cells = get_json("termux-telephony-cellinfo")
                if cells:
                    for cell in cells:
                        if cell.get("registered"):
                            cell_id = f"{cell.get('type')}|{cell.get('ci')}"
                            if cell_id != current_cell:
                                log(f"📍 CELLULAR LINKED: {cell.get('type')} ID:{cell.get('ci')}")
                                current_cell = cell_id

                # Save state
                with open(STATE_FILE, "w") as f:
                    json.dump({
                        "notifications": list(known_notifications),
                        "connections": list(known_connections),
                        "sms": list(known_sms),
                        "usb": list(known_usb),
                        "neighbors": list(known_neighbors),
                        "bssid": current_bssid,
                        "cell": current_cell
                    }, f)
            except Exception as e:
                log(f"Error in monitor loop: {e}")
            
            time.sleep(10) 
    except KeyboardInterrupt:
        log("Monitor stopped.")
        run_command("termux-notification-remove link-monitor")


if __name__ == "__main__":
    monitor()
