import os
import sys
import linguistic_topology_app

LANG_DIR = "./linguistic_topology_repo/languages/"

def list_languages():
    print(f"Scanning {LANG_DIR}...")
    count = 0
    for root, dirs, files in os.walk(LANG_DIR):
        for file in files:
            if file.endswith(".lang"):
                print(f" - {file}")
                count += 1
    print(f"Total: {count} languages found.")

def validate_all():
    print(f"Validating languages in {LANG_DIR}...")
    success = 0
    failed = 0
    
    for root, dirs, files in os.walk(LANG_DIR):
        for file in files:
            if file.endswith(".lang"):
                path = os.path.join(root, file)
                try:
                    linguistic_topology_app.parse_lang_file(path)
                    # print(f"[OK] {file}")
                    success += 1
                except Exception as e:
                    print(f"[FAIL] {file}: {e}")
                    failed += 1
    
    print("-" * 30)
    print(f"Validation Complete: {success} Passed, {failed} Failed.")

def set_math_type(lang_name, math_type):
    # Find the file
    target_file = None
    for root, dirs, files in os.walk(LANG_DIR):
        if f"{lang_name}.lang" in files:
            target_file = os.path.join(root, f"{lang_name}.lang")
            break
            
    if not target_file:
        print(f"Error: Language file for '{lang_name}' not found.")
        return

    print(f"Updating {target_file} to use math_type: {math_type}")
    
    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    has_math_type = False
    
    for line in lines:
        if line.strip().startswith("math_type:"):
            new_lines.append(f"math_type: {math_type}\n")
            has_math_type = True
        else:
            new_lines.append(line)
            
    if not has_math_type:
        # Insert after 'name:' if possible, else at top
        inserted = False
        final_lines = []
        for line in new_lines:
            final_lines.append(line)
            if line.strip().startswith("name:") and not inserted:
                final_lines.append(f"math_type: {math_type}\n")
                inserted = True
        if not inserted:
            final_lines.insert(0, f"math_type: {math_type}\n")
        new_lines = final_lines

    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print("Update complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_languages.py list")
        print("  python manage_languages.py validate")
        print("  python manage_languages.py set_math <lang_name> <math_type>")
        sys.exit(1)
        
    cmd = sys.argv[1]
    
    if cmd == "list":
        list_languages()
    elif cmd == "validate":
        validate_all()
    elif cmd == "set_math":
        if len(sys.argv) != 4:
            print("Usage: python manage_languages.py set_math <lang_name> <math_type>")
        else:
            set_math_type(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
