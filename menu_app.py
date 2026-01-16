
import os
import sys
import glob
import subprocess
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_languages():
    return sorted(glob.glob("linguistic_topology_repo/languages/*.lang") + glob.glob("*.lang"))

def run_wrapper(lang_file):
    print(f"\n[Analysing {lang_file} with lta_wrapper...]")
    subprocess.run(["python", "lta_wrapper.py", lang_file])
    input("\nPress Enter to continue...")

def run_forensics():
    langs = get_languages()
    if len(langs) < 2:
        print("Not enough language files found.")
        return

    print("\nSelect Baseline Language:")
    for i, l in enumerate(langs):
        print(f"{i+1}. {l}")
    
    try:
        b_idx = int(input("Choice: ")) - 1
        base = langs[b_idx]
        
        print("\nSelect Target Language:")
        t_idx = int(input("Choice: ")) - 1
        target = langs[t_idx]
        
        print(f"\n[Comparing {base} vs {target}]")
        # Wrapper doesn't support 2 args yet, calling python app directly for now or updating wrapper
        # The wrapper I wrote only takes 1 arg. I should probably update the wrapper later, 
        # but for now calling the python app directly for forensics is safe as Go core handles single lang analysis.
        subprocess.run(["python", "linguistic_topology_app.py", base, target])
        input("\nPress Enter to continue...")
        
    except (ValueError, IndexError):
        print("Invalid selection.")
        time.sleep(1)

def main_menu():
    while True:
        clear_screen()
        print("==========================================")
        print("   GEMINI LINGUISTIC TOOLKIT (v4.0)       ")
        print("==========================================")
        print("1. Analyze a Language (Turbo Mode)")
        print("2. Forensic Topology Comparison")
        print("3. Language Management (List/Validate)")
        print("4. Corpus Management")
        print("5. Exit")
        print("==========================================")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            langs = get_languages()
            print("\nAvailable Languages:")
            for i, l in enumerate(langs):
                print(f"{i+1}. {os.path.basename(l)}")
            try:
                idx = int(input("\nSelect Language Number: ")) - 1
                if 0 <= idx < len(langs):
                    run_wrapper(langs[idx])
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input.")
                
        elif choice == '2':
            run_forensics()
            
        elif choice == '3':
            print("\n1. List Languages")
            print("2. Validate Languages")
            sub = input("Choice: ")
            if sub == '1':
                subprocess.run(["python", "manage_languages.py", "list"])
            elif sub == '2':
                subprocess.run(["python", "manage_languages.py", "validate"])
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            print("\n1. List Corpus Files")
            print("2. Import Abbyy XML")
            print("3. Segment Text (Bias Isolation)")
            sub = input("Choice: ")
            if sub == '1':
                subprocess.run(["python", "manage_corpus.py", "list"])
            elif sub == '2':
                xml_in = input("Input XML path: ")
                txt_out = input("Output TXT path: ")
                subprocess.run(["python", "manage_corpus.py", "import_abbyy", xml_in, txt_out])
            elif sub == '3':
                fpath = input("File to segment: ")
                subprocess.run(["python", "manage_corpus.py", "segment", fpath])
            input("\nPress Enter to continue...")

        elif choice == '5':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
