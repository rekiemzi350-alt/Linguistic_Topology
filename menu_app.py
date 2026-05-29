import os
import sys
import glob
import subprocess
import time
import lta_config

# --- Configuration & Constants ---
APP_TITLE = "GEMINI LINGUISTIC TOOLKIT"
APP_VERSION = "4.0"
BASE_DIR = lta_config.BASE_DIR

# Allowed File Extensions
DOC_EXTENSIONS = {
    '.txt', '.doc', '.docx', '.html', '.epub', '.pdf', 
    '.djvu', '.fb2', '.mobi', '.azw', '.xps'
}
IMG_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp'
}
ALL_EXTENSIONS = DOC_EXTENSIONS.union(IMG_EXTENSIONS)

# Global State for Search Paths
SEARCH_PATHS = [BASE_DIR, lta_config.DEFAULT_DOCS_DIR]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 50)
    print(f"   {APP_TITLE} (v{APP_VERSION})")
    print("=" * 50)
    print(f"SESSION ID: {lta_config.get_session_id()}")
    print(f"OUTPUT DIR: {lta_config.get_output_dir()}")
    print("-" * 50)

def pause():
    input("\nPress Enter to continue...")

def get_languages():
    # Look in local languages dir and current dir
    langs = glob.glob(os.path.join(lta_config.DEFAULT_LANGS_DIR, "*.lang"))
    langs += glob.glob("*.lang")
    return sorted(list(set(langs)))

def run_script(script_name, args=None):
    if not os.path.exists(script_name):
        # Try finding it in the repo root if it's not in the current dir
        potential_path = os.path.join(BASE_DIR, script_name)
        if os.path.exists(potential_path):
            script_name = potential_path
        else:
            print(f"\nError: Script '{script_name}' not found.")
            pause()
            return

    env = os.environ.copy()
    env["LTA_OUTPUT_DIR"] = lta_config.get_output_dir()
    env["PYTHONPATH"] = BASE_DIR + (os.pathsep + env.get("PYTHONPATH", "") if env.get("PYTHONPATH") else "")

    cmd = [sys.executable, script_name]
    if args:
        cmd.extend(args)
    
    print(f"\n[EXEC] Running: {' '.join(cmd)}\n")
    try:
        subprocess.run(cmd, env=env, check=False)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nExecution Error: {e}")
    
    pause()

def scan_files(allowed_extensions):
    found_files = []
    for path in SEARCH_PATHS:
        if not os.path.exists(path): continue
        for root, dirs, files in os.walk(path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in allowed_extensions:
                    found_files.append(os.path.join(root, file))
    return sorted(list(set(found_files)))

def select_file(prompt_text="Select File", allowed_extensions=ALL_EXTENSIONS):
    docs = scan_files(allowed_extensions)
    if not docs:
        print("\nNo matching files found.")
        return None

    print(f"\nAvailable Files ({len(docs)} found):")
    for i, doc in enumerate(docs):
        print(f"{i+1}. {os.path.basename(doc)} ({os.path.dirname(doc)})")
    
    sel = input(f"\n{prompt_text} (Number): ").strip()
    if sel.isdigit() and 1 <= int(sel) <= len(docs):
        return docs[int(sel)-1]
    return None

# --- Menu Functions ---

def menu_topology():
    while True:
        print_header()
        print("TOPOLOGY & CONVERGENCE")
        print("1. Analyze Language Structure (.lang)")
        print("2. Forensic Topology Comparison (Baseline vs Target)")
        print("3. Language Management (List/Validate)")
        print("4. Extended Topology (Sumerian/Greek/Corporate)")
        print("B. Back")
        
        choice = input("\nSelect Option: ").strip().upper()
        
        if choice == '1':
            langs = get_languages()
            if not langs:
                print("\nNo .lang files found.")
                pause()
                continue
            for i, l in enumerate(langs): print(f"{i+1}. {os.path.basename(l)}")
            try:
                idx = int(input("\nSelect Language Number: ")) - 1
                if 0 <= idx < len(langs):
                    run_script("lta_wrapper.py", [langs[idx]])
            except ValueError: pass
        elif choice == '2':
            langs = get_languages()
            if len(langs) < 2:
                print("Not enough language files found.")
                pause()
                continue
            print("\nSelect Baseline Language:")
            for i, l in enumerate(langs): print(f"{i+1}. {os.path.basename(l)}")
            try:
                b_idx = int(input("Choice: ")) - 1
                print("\nSelect Target Language:")
                t_idx = int(input("Choice: ")) - 1
                run_script("linguistic_topology_app.py", [langs[b_idx], langs[t_idx]])
            except (ValueError, IndexError): pass
        elif choice == '3':
            print("\n1. List Languages")
            print("2. Validate Languages")
            sub = input("Choice: ")
            if sub == '1': run_script("manage_languages.py", ["list"])
            elif sub == '2': run_script("manage_languages.py", ["validate"])
        elif choice == '4':
            print("\n1. Extended Topology (Historical)")
            print("2. Corporate Topology")
            sub = input("Choice: ")
            if sub == '1': run_script("extended_topology.py")
            elif sub == '2': run_script("analyze_corporate_topology.py")
        elif choice == 'B':
            break

def menu_forensics():
    while True:
        print_header()
        print("LINGUISTIC FORENSICS")
        print("1. Quick Fingerprint (Hoax/Root Source Detector)")
        print("2. Advanced Bias Detector")
        print("3. Topological Stylometry Analyzer")
        print("4. Analyze Book Structure (Large Scale)")
        print("B. Back")

        choice = input("\nSelect Option: ").strip().upper()
        if choice == 'B': break

        if choice in ['1', '2', '3', '4']:
            doc = select_file("Select File for Analysis", allowed_extensions=DOC_EXTENSIONS)
            if not doc: continue

            script_map = {
                '1': "hoax_root_source_detector.py",
                '2': "advanced_stylometry_analyzer.py",
                '3': "comprehensive_stylometry.py",
                '4': "analyze_book_structure.py"
            }
            run_script(script_map[choice], [doc])

def menu_corpus():
    while True:
        print_header()
        print("CORPUS MANAGEMENT")
        print("1. List Corpus Files")
        print("2. Import Abbyy XML")
        print("3. Segment Text (Bias Isolation)")
        print("B. Back")
        
        choice = input("\nSelect Option: ").strip().upper()
        if choice == 'B': break
        
        if choice == '1': run_script("manage_corpus.py", ["list"])
        elif choice == '2':
            xml_in = input("Input XML path: ")
            txt_out = input("Output TXT path: ")
            run_script("manage_corpus.py", ["import_abbyy", xml_in, txt_out])
        elif choice == '3':
            fpath = input("File to segment: ")
            run_script("manage_corpus.py", ["segment", fpath])

def main_menu():
    while True:
        print_header()
        print("MAIN MENU")
        print("1. Topology & Convergence")
        print("2. Forensic Analysis (Hoax ID)")
        print("3. Corpus Management")
        print("4. Settings & Paths")
        print("X. Exit")
        
        choice = input("\nSelect Option: ").strip().upper()
        
        if choice == '1': menu_topology()
        elif choice == '2': menu_forensics()
        elif choice == '3': menu_corpus()
        elif choice == '4':
            print(f"\nSearch Paths: {SEARCH_PATHS}")
            print(f"Output Directory: {lta_config.get_output_dir()}")
            pause()
        elif choice == 'X':
            break

if __name__ == "__main__":
    main_menu()
