package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"strings"
	"sync"
	"syscall"
	"time"
)

// Constants and Configuration
const (
	StateFile = "monitor_state.json"
)

var (
	LogDir        = os.ExpandEnv("$HOME/storage/shared/Documents")
	SessionStart  = time.Now().Format("2006-01-02_15-04-05")
	DownloadDirs  = []string{"/sdcard/Download", os.ExpandEnv("$HOME/downloads")}
	ProxyProcs    = []string{"ssh", "sshd", "ngrok", "frp", "proxy", "tunnel", "tor", "vpn", "androRAT", "reverse", "payload", "nc", "netcat", "ncat", "socat", "metasploit"}
	WhitelistProcs = []string{"link_monitor", "firewall_guardian", "gemini"}
	KillProactive = true
	SecurityKeys  = []string{"sign-in", "login", "security", "verify", "code", "alert", "account", "access", "unusual", "password"}
	CurrentLogPath string
	LogMutex       sync.Mutex
)

type State struct {
	Notifications []string `json:"notifications"`
	Connections   []string `json:"connections"`
	SMS           []string `json:"sms"`
	USB           []string `json:"usb"`
	Neighbors     []string `json:"neighbors"`
	BSSID         string   `json:"bssid"`
	Cell          string   `json:"cell"`
}

var currentState State
var knownNotifications map[string]bool
var knownSMS map[string]bool
var knownNeighbors map[string]bool
var knownUSB map[string]bool

// Utility Functions

func runCommand(command string) string {
	cmd := exec.Command("sh", "-c", command)
	out, err := cmd.Output()
	if err != nil {
		return ""
	}
	return strings.TrimSpace(string(out))
}

func getJSON(command string, v interface{}) error {
	out := runCommand(command)
	if out == "" {
		return fmt.Errorf("empty output")
	}
	return json.Unmarshal([]byte(out), v)
}

func logMessage(message string) {
	LogMutex.Lock()
	defer LogMutex.Unlock()

	now := time.Now()
	timestamp := now.Format("2006-01-02 15:04:05")
	updateTime := now.Format("15-04-05")
	
	newFilename := fmt.Sprintf("link_logs_started_%s_last_updated_%s.txt", SessionStart, updateTime)
	newPath := filepath.Join(LogDir, newFilename)

	if CurrentLogPath != "" && CurrentLogPath != newPath {
		os.Rename(CurrentLogPath, newPath)
	}
	CurrentLogPath = newPath

	f, err := os.OpenFile(CurrentLogPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err == nil {
		f.WriteString(fmt.Sprintf("[%s] %s\n", timestamp, message))
		f.Close()
	}
	fmt.Printf("[%s] %s\n", timestamp, message)
}

func updateStatus(message string) {
	logMessage("Status: " + message)
	safeMsg := strings.ReplaceAll(message, "'", "")
	safeMsg = strings.ReplaceAll(safeMsg, "\"", "")
	runCommand(fmt.Sprintf("termux-notification -t 'Link Monitor: Active' -c '%s' --id link-monitor --ongoing --priority low", safeMsg))
}

func notifyUser(title, message string, critical bool) {
	logMessage(fmt.Sprintf("[%s] %s", title, message))
	
	// Tactile: Vibration
	duration := 300
	if critical {
		duration = 800
	}
	runCommand(fmt.Sprintf("termux-vibrate -d %d", duration))
	
	// Visual: Notification (No --sound flag ensures silence)
	safeTitle := strings.ReplaceAll(title, "'", "")
	safeMsg := strings.ReplaceAll(message, "'", "")
	priority := "default"
	if critical {
		priority = "high"
	}
	runCommand(fmt.Sprintf("termux-notification -t '%s' -c '%s' --priority %s", safeTitle, safeMsg, priority))
}

func panicAlert(message string, critical bool) {
	notifyUser("SECURITY ALERT", message, critical)
}

func isSecurityAlert(text string) bool {
	lower := strings.ToLower(text)
	for _, k := range SecurityKeys {
		if strings.Contains(lower, k) {
			return true
		}
	}
	return false
}

func checkProxyProcesses() {
	ps := runCommand("ps -e")
	lines := strings.Split(ps, "\n")
	for _, line := range lines {
		lower := strings.ToLower(line)
		isWhitelisted := false
		for _, w := range WhitelistProcs {
			if strings.Contains(lower, strings.ToLower(w)) {
				isWhitelisted = true
				break
			}
		}

		if isWhitelisted {
			continue
		}

		for _, proxy := range ProxyProcs {
			if strings.Contains(lower, strings.ToLower(proxy)) {
				parts := strings.Fields(line)
				if len(parts) > 0 {
					procName := parts[len(parts)-1]
					pid := parts[0]
					msg := "PROXY/TUNNEL/RAT DETECTED: " + procName
					if KillProactive {
						runCommand("kill -9 " + pid)
						msg = "NEUTRALIZED: " + procName + " (PID: " + pid + ")"
					}
					panicAlert(msg, true)
				}
			}
		}
	}
}

func fileMonitor() {
	validDirs := []string{}
	for _, d := range DownloadDirs {
		if _, err := os.Stat(d); err == nil {
			validDirs = append(validDirs, d)
		}
	}
	if len(validDirs) == 0 {
		return
	}

	for {
		line := runCommand("inotifywait -q -e create,moved_to --format '%f' " + strings.Join(validDirs, " "))
		if line != "" {
			notifyUser("New Download", "File: "+line, false)
		}
		time.Sleep(1 * time.Second)
	}
}

func main() {
	// Initialize state
	knownNotifications = make(map[string]bool)
	knownSMS = make(map[string]bool)
	knownNeighbors = make(map[string]bool)
	knownUSB = make(map[string]bool)

	data, err := ioutil.ReadFile(StateFile)
	if err == nil {
		json.Unmarshal(data, &currentState)
		for _, v := range currentState.Notifications { knownNotifications[v] = true }
		for _, v := range currentState.SMS { knownSMS[v] = true }
		for _, v := range currentState.Neighbors { knownNeighbors[v] = true }
		for _, v := range currentState.USB { knownUSB[v] = true }
	}

	logMessage("Starting GO-ACTIVATED PANIC MONITOR (High Efficiency)...")
	updateStatus("Monitoring for threats...")

	// Start file monitor in background
	go fileMonitor()

	// Handle signals for clean shutdown
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		<-sigs
		logMessage("Monitor stopping...")
		runCommand("termux-notification-remove link-monitor")
		os.Exit(0)
	}()

	// Periodic checks
	ticker := time.NewTicker(10 * time.Second)
	for range ticker.C {
		checkProxyProcesses()

		// Notifications
		var ntfs []map[string]interface{}
		if err := getJSON("termux-notification-list", &ntfs); err == nil {
			for _, n := range ntfs {
				pkg := fmt.Sprint(n["packageName"])
				title := fmt.Sprint(n["title"])
				content := fmt.Sprint(n["content"])
				id := pkg + "|" + title + "|" + content
				if !knownNotifications[id] {
					msg := fmt.Sprintf("[%s] %s: %s", pkg, title, content)
					if isSecurityAlert(title) || isSecurityAlert(content) {
						panicAlert(msg, true)
					} else {
						notifyUser("New Notification", msg, false)
					}
					knownNotifications[id] = true
					currentState.Notifications = append(currentState.Notifications, id)
				}
			}
		}

		// SMS
		var sms []map[string]interface{}
		if err := getJSON("termux-sms-list -l 5", &sms); err == nil {
			for _, m := range sms {
				num := fmt.Sprint(m["number"])
				body := fmt.Sprint(m["body"])
				received := fmt.Sprint(m["received"])
				id := num + "|" + received + "|" + body
				if !knownSMS[id] {
					if isSecurityAlert(body) {
						panicAlert("Sensitive SMS from "+num+": "+body, true)
					} else {
						notifyUser("New SMS", "From "+num+": "+body, false)
					}
					knownSMS[id] = true
					currentState.SMS = append(currentState.SMS, id)
				}
			}
		}

		// Network Neighbors
		neigh := runCommand("ip neigh show")
		lines := strings.Split(neigh, "\n")
		for _, line := range lines {
			if strings.Contains(line, "REACHABLE") || strings.Contains(line, "STALE") {
				parts := strings.Fields(line)
				if len(parts) > 0 {
					ip := parts[0]
					if !knownNeighbors[ip] {
						notifyUser("Network Activity", "New device: "+ip, false)
						knownNeighbors[ip] = true
						currentState.Neighbors = append(currentState.Neighbors, ip)
					}
				}
			}
		}

		// USB
		var usb []string
		if err := getJSON("termux-usb -l", &usb); err == nil {
			for _, u := range usb {
				if !knownUSB[u] {
					panicAlert("USB Hardware Connected: "+u, true)
					knownUSB[u] = true
					currentState.USB = append(currentState.USB, u)
				}
			}
		}

		// WiFi
		var wifi map[string]interface{}
		if err := getJSON("termux-wifi-connectioninfo", &wifi); err == nil {
			bssid := fmt.Sprint(wifi["bssid"])
			if bssid != currentState.BSSID && bssid != "<nil>" {
				notifyUser("WiFi Changed", fmt.Sprintf("Linked to %v (%s)", wifi["ssid"], bssid), false)
				currentState.BSSID = bssid
				updateStatus("Connected to " + fmt.Sprint(wifi["ssid"]))
			}
		}

		// Save State
		saveData, _ := json.Marshal(currentState)
		ioutil.WriteFile(StateFile, saveData, 0644)
	}
}
