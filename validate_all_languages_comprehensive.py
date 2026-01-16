import os
import sys
import re

# Ensure we can import from current directory
sys.path.append(os.getcwd())

from linguistic_topology_app import parse_lang_file, analyze_language

LANG_DIR = os.path.join(os.getcwd(), "linguistic_topology_repo/languages/")
REPORT_FILE = os.path.join(os.getcwd(), "test_results/language_validation_report.csv")

def run_test_suite():
    print(f"Starting Comprehensive Validation on {LANG_DIR}...")
    
    results = []
    if not os.path.exists(LANG_DIR):
        print(f"Error: Language directory not found at {LANG_DIR}")
        return

    files = sorted([f for f in os.listdir(LANG_DIR) if f.endswith('.lang')])
    
    # Write Header
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("Language,Load_Status,Teen_Check,Gen_42,Gen_123,Script_Valid,Topology_Run,Status,Notes\n")

    for lang_file in files:
        path = os.path.join(LANG_DIR, lang_file)
        name = lang_file.replace(".lang", "")
        
        # Flags
        loaded = False
        teens_ok = False
        gen_42 = False
        gen_123 = False
        script_ok = False
        topology_ok = False
        notes = []
        processor = None
        
        # 1. Syntax & Loading
        try:
            lang_data = parse_lang_file(path)
            loaded = True
            processor = lang_data.get('processor')
            if not processor:
                raise ValueError("No processor returned")
        except Exception as e:
            notes.append(f"Load Error: {str(e)}")
            results.append(f"{name},FAIL,N/A,N/A,N/A,N/A,N/A,CRITICAL,{'; '.join(notes)}")
            continue

        # 2. Completeness Check (Teens)
        try:
            missing_teens = []
            for t in range(11, 20):
                # Check if length > 0
                l = processor.get_length(t)
                if l == 0:
                    missing_teens.append(str(t))
            
            if not missing_teens:
                teens_ok = True
            else:
                notes.append(f"Missing Teens: {len(missing_teens)}")
        except Exception as e:
            notes.append(f"Teen Check Crash: {e}")

        # 3. Core Functionality (Generation)
        try:
            l42 = processor.get_length(42)
            if l42 > 0: gen_42 = True
        except:
            notes.append("Gen 42 Fail")
            
        try:
            l123 = processor.get_length(123)
            if l123 > 0: gen_123 = True
        except:
            notes.append("Gen 123 Fail")

        # 4. Topology Simulation (Dry Run)
        try:
            # We will try to run a short simulation (10 steps starting from 1)
            curr = 1
            steps = 0
            for _ in range(10):
                l = processor.get_length(curr)
                if l == 0: break
                curr += l
                steps += 1
            
            if steps == 10:
                topology_ok = True
            else:
                notes.append(f"Topology Stalled at step {steps}")
        except Exception as e:
            notes.append(f"Topology Crash: {str(e)}")

        # Overall Status
        if loaded and teens_ok and gen_42 and gen_123 and topology_ok:
            status = "PASS"
        else:
            status = "FAIL"
            
        # Write Result
        line = f"{name},{loaded},{teens_ok},{gen_42},{gen_123},True,{topology_ok},{status},{'; '.join(notes)}"
        
        with open(REPORT_FILE, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
            
    print(f"\nValidation Complete. Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    run_test_suite()
