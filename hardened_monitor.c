#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <ctype.h>

// Configuration
#define SCAN_INTERVAL 5 // Seconds
#define LOG_FILE "hardened_security.log"

const char *blocked_patterns[] = {
    "ssh", "sshd", "ngrok", "frp", "nc", "netcat", "ncat", "socat", 
    "reverse", "payload", "androRAT", "metasploit", "tunnel", "proxy", "tor"
};

const char *whitelist[] = {
    "hardened_monitor", "firewall_guardian_go", "link_monitor_go", "gemini", "bash", "sh", "clang", "gcc", "[kworker", "node", "python"
};

void log_event(const char *msg) {
    FILE *f = fopen(LOG_FILE, "a");
    if (f) {
        time_t now = time(NULL);
        char *t = ctime(&now);
        if (t) {
            t[strlen(t)-1] = '\0'; // Remove newline
            fprintf(f, "[%s] %s\n", t, msg);
        } else {
            fprintf(f, "[UNKNOWN TIME] %s\n", msg);
        }
        fclose(f);
    }
    printf("%s\n", msg);
}

int is_whitelisted(const char *comm) {
    for (int i = 0; i < sizeof(whitelist)/sizeof(whitelist[0]); i++) {
        if (strcmp(comm, whitelist[i]) == 0 || strstr(comm, whitelist[i])) return 1;
    }
    return 0;
}

void scan_and_neutralize() {
    DIR *dir;
    struct dirent *entry;
    dir = opendir("/proc");
    if (!dir) return;

    while ((entry = readdir(dir)) != NULL) {
        if (!isdigit(entry->d_name[0])) continue;

        int pid = atoi(entry->d_name);
        if (pid == getpid() || pid == getppid()) continue;

        char path[256];
        snprintf(path, sizeof(path), "/proc/%d/comm", pid);
        
        FILE *f = fopen(path, "r");
        if (f) {
            char comm[256];
            if (fgets(comm, sizeof(comm), f)) {
                // Safely remove trailing newline or carriage return
                size_t len = strlen(comm);
                while (len > 0 && (comm[len-1] == '\n' || comm[len-1] == '\r')) {
                    comm[--len] = '\0';
                }
                
                if (is_whitelisted(comm)) {
                    fclose(f);
                    continue;
                }

                for (int i = 0; i < sizeof(blocked_patterns)/sizeof(blocked_patterns[0]); i++) {
                    // Check for blocked patterns, but avoid false positives like "monitor" matching "tor"
                    // We can check if it's a whole word or use more specific logic
                    const char *match = strstr(comm, blocked_patterns[i]);
                    if (match) {
                        // Basic false positive prevention for "monitor" matching "tor"
                        if (strcmp(blocked_patterns[i], "tor") == 0 && strstr(comm, "monitor")) {
                            continue;
                        }

                        char msg[512];
                        snprintf(msg, sizeof(msg), "NEUTRALIZED unauthorized process: %s (PID: %d)", comm, pid);
                        log_event(msg);
                        kill(pid, SIGKILL);
                        break;
                    }
                }
            }
            fclose(f);
        }
    }
    closedir(dir);
}

int main(int argc, char *argv[]) {
    // Self-renaming for stealth (simple version)
    if (argc > 0) {
        memset(argv[0], 0, strlen(argv[0]));
        strcpy(argv[0], "[kworker/u:1]");
    }

    log_event("HARDENED C-CORE MONITOR STARTED (High Efficiency Mode)");
    
    // Daemonize
    if (fork() != 0) exit(0);
    setsid();

    while (1) {
        scan_and_neutralize();
        sleep(SCAN_INTERVAL);
    }

    return 0;
}
