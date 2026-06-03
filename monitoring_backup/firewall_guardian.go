package main

import (
	"log"
	"os"
	"os/exec"
	"time"
)

func isProcessRunning(name string) bool {
	cmd := exec.Command("pgrep", "-f", name)
	err := cmd.Run()
	return err == nil
}

func main() {
	logFile, err := os.OpenFile("guardian_start.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		// Fallback to stderr if log file can't be opened
		log.SetOutput(os.Stderr)
	} else {
		log.SetOutput(logFile)
		defer logFile.Close()
	}

	log.Println("Go Firewall Guardian started.")

	for {
		if !isProcessRunning("link_monitor_go") {
			log.Println("Go Link Monitor not found. Starting...")
			
			// We use a background command to start the monitor
			// but we don't want the guardian to wait for it.
			startCmd := exec.Command("./link_monitor_go")
			
			// Redirect monitor output to its own log
			monitorLog, err := os.OpenFile("monitor_debug.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
			if err == nil {
				startCmd.Stdout = monitorLog
				startCmd.Stderr = monitorLog
				// monitorLog will be closed when the process finishes, 
				// but here we are starting it and moving on.
				// Since we don't wait, we might leak the file descriptor if we are not careful,
				// but in Termux/Go this is generally handled by the OS when the child starts.
			}

			err = startCmd.Start()
			if err != nil {
				log.Printf("Failed to start link_monitor_go: %v\n", err)
			} else {
				log.Printf("Started link_monitor_go (PID: %d)\n", startCmd.Process.Pid)
			}
		}
		time.Sleep(10 * time.Second)
	}
}
