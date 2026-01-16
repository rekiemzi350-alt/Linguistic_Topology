import os
import sys
import subprocess
import time
import re
import math
import shutil

# --- Configuration ---
TEST_DOCS_DIR = "test_documents"
REPORT_FILE = "FULL_TLA_TEST_REPORT_2026.txt"
LOG_FILE = "tla_test_log.txt"

def log(message):
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def write_report(content):
    with open(REPORT_FILE, "a") as f:
        f.write(content + "\n")

# --- 1. Environment & Data Check ---
def check_environment():
    log("=== 1. Environment Check & Data Retrieval ===")
    if not os.path.exists(TEST_DOCS_DIR):
        log(f"WARNING: '{TEST_DOCS_DIR}' not found. Creating and generating dummy data...")
        os.makedirs(TEST_DOCS_DIR)
        create_dummy_corpus()
    else:
        log(f"SUCCESS: '{TEST_DOCS_DIR}' found.")
        files = os.listdir(TEST_DOCS_DIR)
        log(f"Found {len(files)} files in corpus.")
        write_report(f"Environment: OK. Corpus Size: {len(files)} files.")

def create_dummy_corpus():
    with open(os.path.join(TEST_DOCS_DIR, "authentic_sample.txt"), "w") as f:
        f.write("In the beginning God created the heaven and the earth. " * 50)
    with open(os.path.join(TEST_DOCS_DIR, "hoax_sample.txt"), "w") as f:
        f.write("This is a fake text designed to simulate a modern forgery. " * 50)
    log("Generated dummy corpus files.")

# --- 2. Core Topological Analysis (Unity/Fracture) ---
def run_core_topology_tests():
    log("\n=== 2. Running Core Topological Analysis ===")
    write_report("\n--- Core Topology Test Results ---")
    
    # Updated to use verified language files
    languages = ["english.lang", "ancient_hebrew_gematria.lang"]
    
    for lang in languages:
        if os.path.exists(lang):
            log(f"Testing Language: {lang}")
            try:
                result = subprocess.run(
                    ["python", "linguistic_topology_app.py", lang],
                    capture_output=True, text=True, timeout=30
                )
                output = result.stdout
                rivers = re.search(r"(\d+) Distinct River", output)
                river_count = rivers.group(1) if rivers else "Unknown"
                
                log(f"  -> {lang}: {river_count} Rivers")
                write_report(f"Language: {lang:<30} | Rivers: {river_count}")
                
            except Exception as e:
                log(f"  -> Error testing {lang}: {e}")
                write_report(f"Language: {lang:<30} | Status: FAILED ({e})")
        else:
            log(f"  -> SKIPPING {lang} (File not found)")

# --- 3. Forensic & Hoax Detection ---
def run_forensic_tests():
    log("\n=== 3. Forensic & Hoax Detection Benchmarks ===")
    write_report("\n--- Forensic Analysis (Weight & Variance) ---")
    
    try:
        log("Running 'master_forensic_topology.py'...")
        result = subprocess.run(
            ["python", "master_forensic_topology.py"],
            capture_output=True, text=True, timeout=60
        )
        
        if "Report generated" in result.stdout:
            report_path = "forensic_master_report.txt"
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    content = f.read()
                    lines = content.split('\n')
                    anomalies = [line for line in lines if "ALERT" in line]
                    write_report(f"Forensic Scan Completed. Found {len(anomalies)} anomalies.")
                    for a in anomalies[:5]: 
                        write_report(f"  -> {a}")
            else:
                write_report("Forensic Script ran but produced no report file.")
        else:
            write_report(f"Forensic Script Output:\n{result.stdout[:200]}...")
            
    except Exception as e:
        log(f"Error running forensic script: {e}")
        write_report(f"Forensic Test Failed: {e}")

# --- 4. Persistence Barcode (Topological Resilience) ---
def calculate_simple_barcode(text):
    def get_val(word):
        return sum(ord(c.lower()) - 96 for c in word if 'a' <= c.lower() <= 'z')

    words = re.findall(r'\b[a-z]+\b', text.lower())[:100]
    if not words: return []
    
    path_lengths = []
    current_val = 0
    for word in words:
        val = get_val(word)
        if val == 0: continue
        current_val += val
        path_lengths.append(current_val % 101) 
        
    return path_lengths

def wasserstein_distance_sim(barcode1, barcode2):
    if not barcode1 or not barcode2: return 999.0
    hist1 = sorted(barcode1)
    hist2 = sorted(barcode2)
    min_len = min(len(hist1), len(hist2))
    hist1 = hist1[:min_len]
    hist2 = hist2[:min_len]
    diff = sum(abs(u - v) for u, v in zip(hist1, hist2))
    return diff / min_len

def run_persistence_tests():
    log("\n=== 4. Persistence Barcode Testing (Translation Resilience) ===")
    write_report("\n--- Persistence Barcode Results ---")
    
    files = [f for f in os.listdir(TEST_DOCS_DIR) if f.endswith(".txt")]
    if not files:
        write_report("No files to test persistence.")
        return

    # Prefer one of our new downloads if available
    target_file = None
    for priority in ["frankenstein.txt", "sherlock_holmes.txt", "the_prince.txt"]:
        if priority in files:
            target_file = os.path.join(TEST_DOCS_DIR, priority)
            break
    
    if not target_file:
        target_file = os.path.join(TEST_DOCS_DIR, files[0])

    try:
        with open(target_file, "r", encoding='utf-8', errors='ignore') as f:
            content = f.read(2000)
            
        barcode_original = calculate_simple_barcode(content)
        translated_content = "".join([chr(ord(c)+1) if c.isalpha() else c for c in content])
        barcode_translated = calculate_simple_barcode(translated_content)
        
        distance = wasserstein_distance_sim(barcode_original, barcode_translated)
        
        log(f"Tested file: {os.path.basename(target_file)}")
        log(f"Persistence Distance (Wasserstein): {distance:.4f}")
        
        write_report(f"File: {os.path.basename(target_file)}")
        write_report(f"  -> Original vs Simulated Translation Distance: {distance:.4f}")
        if distance < 20.0:
            write_report("  -> RESULT: HIGH PERSISTENCE. Topology survives transformation.")
        else:
            write_report("  -> RESULT: LOW PERSISTENCE. Topology fragile to translation.")
            
    except Exception as e:
        log(f"Persistence test error: {e}")

# --- 5. Weighted Topology (Feature Analysis) ---
def run_weighted_topology_tests():
    log("\n=== 5. Weighted Topology (Feature Analysis) ===")
    write_report("\n--- Weighted Topology (Alphabet vs Frequency) ---")
    try:
        result = subprocess.run(
            ["python", "analyze_weighted_topology.py"],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        for line in output.split('\n'):
            if "Distinct River" in line or "Main Trunk" in line:
                write_report(f"  {line.strip()}")
    except Exception as e:
        log(f"Weighted topology error: {e}")

# --- Main Driver ---
if __name__ == "__main__":
    with open(REPORT_FILE, "w") as f:
        f.write("GEMINI TLA - FULL SYSTEM TEST REPORT\n")
        f.write("====================================\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d')}\n")
    
    check_environment()
    run_core_topology_tests()
    run_forensic_tests()
    run_persistence_tests()
    run_weighted_topology_tests()
    
    log("\n=== TEST SUITE COMPLETE ===")
    log(f"Final detailed report written to: {REPORT_FILE}")
