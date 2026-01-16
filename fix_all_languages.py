import os
import sys

# Add repo to path to reuse the validation logic if needed
sys.path.append('/data/data/com.termux/files/home/coffee/linguistic_topology_repo')

def validate_line(key, value, lang_name):
    # Minimal validation to catch obvious junk
    # We are not re-implementing the full regex engine here, just sanity checks
    if not key or not value: return False
    return True

def fix_language_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_lines = []
        name = "Unknown"
        changed = False
        
        for line in lines:
            stripped = line.strip()
            
            # Keep Name
            if stripped.lower().startswith("name:"):
                name = stripped.split(":", 1)[1].strip()
                fixed_lines.append(line)
                continue
                
            # Keep Comments
            if stripped.startswith("#") or not stripped:
                fixed_lines.append(line)
                continue
                
            # Handle Key-Value pairs
            if ":" in stripped:
                parts = stripped.split(":", 1)
                key = parts[0].strip()
                val = parts[1].strip()
                
                # Fix: Remove inline comments that might have triggered validation
                if "#" in val:
                    val = val.split("#")[0].strip()
                    changed = True
                    
                # Fix: Tech languages should strictly be 0/1 if they are "binary"
                # But some might be "7g" (error seen in logs).
                # If the key is '7g', it's likely a typo for '7'.
                if key.endswith('g') and key[:-1].isdigit():
                    key = key[:-1]
                    changed = True
                    
                # Reconstruct line
                fixed_lines.append(f"{key}: {val}\n")
            else:
                # Discard malformed lines
                changed = True
                
        if changed:
            print(f"Repaired: {filepath}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            return True
        else:
            return False

    except Exception as e:
        print(f"Failed to process {filepath}: {e}")
        return False

def main():
    lang_dir = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"
    files = [f for f in os.listdir(lang_dir) if f.endswith('.lang')]
    
    print(f"Scanning {len(files)} language files for repairs...")
    count = 0
    for f in files:
        if fix_language_file(os.path.join(lang_dir, f)):
            count += 1
            
    print(f"Repair run complete. Modified {count} files.")

if __name__ == "__main__":
    main()
