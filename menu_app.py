import os
import sys
import subprocess
import glob
import time
import lta_converters

# --- Configuration & Constants ---
APP_TITLE = "LTA Toolkit"
APP_VERSION = "3.2" # Incremented version
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
SEARCH_PATHS = [BASE_DIR]

# --- Helper Functions ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 50)
    print(f"{APP_TITLE} v{APP_VERSION}")
    print("=" * 50)
    print("CORE MANDATES:")
    print("1. NO TRANSLITERATION: All analysis uses native scripts.")
    print("2. NO ANACHRONISMS: Ancient systems respect their era.")
    print("3. TEMPORAL ACCURACY: Waveforms match historical context.")
    print("-" * 50)

def pause():
    input("\nPress Enter to return to menu...")

def list_files(pattern):
    """Legacy helper for .lang files in base dir."""
    return sorted(glob.glob(pattern))

def request_setup():
    """
    1) Requests permission (simulation/user prompt).
    2) Asks for search directories.
    """
    global SEARCH_PATHS
    print_header()
    print("INITIAL SETUP & PERMISSIONS")
    print("-" * 50)
    print("1. PERMISSION CHECK:")
    print("   Please ensure this application has access to read all files.")
    print("   (On Android/Termux, run 'termux-setup-storage' if needed.)")
    input("\n   Press Enter to confirm permissions are granted...")

    print("\n2. CONFIGURE SEARCH DIRECTORIES:")
    print("   Enter the full paths to the folders you wish to scan for documents.")
    print("   Separate multiple paths with a comma.")
    print(f"   (Default: {BASE_DIR})")
    
    user_input = input("\n   Paths > ").strip()
    
    if user_input:
        paths = [p.strip() for p in user_input.split(',')]
        valid_paths = []
        for p in paths:
            exp_p = os.path.expanduser(p)
            if os.path.isdir(exp_p):
                valid_paths.append(exp_p)
            else:
                print(f"   [WARNING] Path not found, ignoring: {p}")
        
        if valid_paths:
            SEARCH_PATHS = valid_paths
            print(f"\n   -> Updated search paths: {SEARCH_PATHS}")
        else:
            print("\n   -> No valid paths provided. Keeping default.")
    else:
        print("\n   -> Keeping default path.")
    time.sleep(1)

def scan_files(allowed_extensions):
    """
    Scans SEARCH_PATHS for files matching a set of extensions.
    Returns a sorted list of absolute file paths.
    """
    found_files = []
    print("\n[Scanning directories...]")
    
    for path in SEARCH_PATHS:
        for root, dirs, files in os.walk(path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in allowed_extensions:
                    found_files.append(os.path.join(root, file))
    
    return sorted(found_files)

def select_file(prompt_text="Select File", allowed_extensions=ALL_EXTENSIONS):
    """
    Helper to list and select a file from the scanned set.
    """
    docs = scan_files(allowed_extensions)
    if not docs:
        print("\nNo matching files found in configured paths.")
        return None

    print(f"\nAvailable Files ({len(docs)} found):")
    max_display = 50
    for i, doc in enumerate(docs):
        if i >= max_display:
            print(f"... and {len(docs) - max_display} more.")
            break
        display_name = doc
        for sp in SEARCH_PATHS:
            if doc.startswith(sp):
                display_name = os.path.relpath(doc, sp)
                break
        print(f"{i+1}. {display_name}")
    
    sel = input(f"\n{prompt_text} (Number): ").strip()
    if sel.isdigit() and 1 <= int(sel) <= len(docs):
        return docs[int(sel)-1]
    return None

def view_file(filepath):
    """Safely prints the content of a text file to the console."""
    if not os.path.exists(filepath):
        print(f"\nError: Documentation file '{filepath}' not found.")
        pause()
        return
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            clear_screen()
            print(f"--- Viewing: {filepath} ---\n")
            print(f.read())
            print("\n--- End of File ---")
    except Exception as e:
        print(f"Error reading file: {e}")
    
    pause()

def run_script(script_name, args=None):
    if not os.path.exists(script_name):
        print(f"\nError: Script '{script_name}' not found.")
        pause()
        return

    cmd = [sys.executable, script_name]
    if args:
        cmd.extend(args)
    
    print(f"\n[EXEC] Running: {' '.join(cmd)}\n")
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nExecution Error: {e}")
    
    pause()

# --- Menu Functions ---

def menu_topology():
    while True:
        print_header()
        print("TOPOLOGY & CONVERGENCE")
        print("1. Analyze Language Structure (.lang files)")
        print("2. Compare Foundational Languages (Hardcoded)")
        print("3. Run Extended Trace (Sumerian/Greek)")
        print("4. Analyze Corporate Topology")
        print("5. Verify Convergence for Seeds 0-13")
        print("B. Back")
        
        choice = input("\nSelect Option: ").strip().upper()
        
        if choice == '1':
            langs = list_files("*.lang")
            if not langs:
                print("\nNo .lang files found.")
                pause()
                continue
            print("\nAvailable Languages:")
            for i, l in enumerate(langs): print(f"{i+1}. {l}")
            sel = input("\nSelect Language Number: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(langs):
                run_script("linguistic_topology_app.py", [langs[int(sel)-1]])
        elif choice == '2':
            run_script("compare_languages.py")
        elif choice == '3':
            run_script("extended_topology.py")
        elif choice == '4':
            run_script("analyze_corporate_topology.py")
        elif choice == '5':
            run_script("verify_convergence_0_to_13.py")
        elif choice == 'B':
            break

def menu_forensics():
    """Menu for stylometry and code breaking."""
    while True:
        print_header()
        print("LINGUISTIC FORENSICS")
        print("1. Quick Fingerprint (Hoax/Root Source Detector)")
        print("2. Advanced Bias Detector")
        print("3. Topological Stylometry Analyzer (Multi-Vector)")
        print("4. Code Breaker Simulation")
        print("B. Back")

        choice = input("\nSelect Option: ").strip().upper()
        if choice == 'B': break

        if choice in ['1', '2', '3']:
            doc = select_file("Select File for Analysis", allowed_extensions=DOC_EXTENSIONS)
            if not doc:
                pause()
                continue

            script_map = {
                '1': "hoax_root_source_detector.py",
                '2': "advanced_stylometry_analyzer.py",
                '3': "comprehensive_stylometry.py"
            }
            script_to_run = script_map[choice]

            # Handle EPUB extraction if needed
            if doc.lower().endswith(".epub"):
                 print("\n[INFO] EPUB detected. Extracting text for analysis...")
                 lta_converters.convert_document_to_text(doc)
                 doc = os.path.splitext(doc)[0] + ".txt"

            run_script(script_to_run, [doc])
        
        elif choice == '4':
            run_script("test_code_breaker.py")

def menu_conversion():
    """Menu for file conversion tools."""
    while True:
        print_header()
        print("FILE CONVERSION TOOLS")
        print("1. Convert Document to Plain Text (PDF, DOCX, EPUB)")
        print("2. Convert Image Format (e.g., JPG to PNG)")
        print("B. Back")
        
        choice = input("\nSelect Option: ").strip().upper()
        
        if choice == '1':
            doc = select_file("Select Document to Convert", allowed_extensions={'.pdf', '.docx', '.epub'})
            if doc:
                lta_converters.convert_document_to_text(doc)
            pause()
        
        elif choice == '2':
            img = select_file("Select Image to Convert", allowed_extensions=IMG_EXTENSIONS)
            if img:
                print("\nSupported output formats: PNG, JPG, BMP, GIF, WEBP")
                fmt = input("Enter desired output format: ").strip().lower()
                if fmt:
                    lta_converters.convert_image_format(img, fmt)
                else:
                    print("No format entered.")
            pause()
            
        elif choice == 'B':
            break

def menu_theory():
    """Menu to view the theoretical documents."""
    while True:
        print_header()
        print("THEORY & DOCUMENTATION")
        print("1. View Algorithm Explanation")
        print("2. View Formal Definition of the Sequence")
        print("3. View Evolution of the Theory")
        print("4. View OEIS Submission Draft (v3)")
        print("B. Back")
        
        choice = input("\nSelect Option: ").strip().upper()

        if choice == '1': view_file("Algorithm_Explanation.txt")
        elif choice == '2': view_file("Formal_Definition.txt")
        elif choice == '3': view_file("Theory_Evolution.md")
        elif choice == '4': view_file("OEIS_Submission_v3.txt")
        elif choice == 'B': break

def menu_settings():
    """Menu to adjust application settings."""
    while True:
        print_header()
        print("SETTINGS")
        print(f"Current Search Paths: {SEARCH_PATHS}")
        print("-" * 50)
        print("1. Change Search Directories")
        print("B. Back")
        
        choice = input("\nSelect Option: ").strip().upper()
        
        if choice == '1': request_setup()
        elif choice == 'B': break

def main_menu():
    # Initial Setup Call
    request_setup()

    while True:
        print_header()
        print("MAIN MENU")
        print("1. Linguistic Topology Analysis")
        print("2. Linguistic Forensics (Hoax ID)")
        print("3. File Conversion Tools")
        print("4. Theory & Documentation")
        print("5. Settings")
        print("H. Help")
        print("X. Exit")
        
        choice = input("\nSelect Option: ").strip().upper()
        
        if choice == '1': menu_topology()
        elif choice == '2': menu_forensics()
        elif choice == '3': menu_conversion()
        elif choice == '4': menu_theory()
        elif choice == '5': menu_settings()
        elif choice == 'H': view_file("help.txt")
        elif choice == 'X':
            clear_screen()
            print(f"Exiting {APP_TITLE}.")
            break
        else:
            print("\nInvalid option.")
            time.sleep(1)

if __name__ == "__main__":
    # Check for BeautifulSoup and install if missing
    try:
        import bs4
    except ImportError:
        print("BeautifulSoup4 not found. Attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
        except Exception as e:
            print(f"Fatal: Failed to install 'beautifulsoup4'. Please install it manually. Error: {e}")
            sys.exit(1)
            
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
