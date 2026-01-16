import os

LANG_DIR = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"

def apply_patch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Check if 11 exists
    if any(line.strip().startswith("11:") for line in lines):
        return False

    # Extract rules for 1-9 and 10
    rules = {}
    for line in lines:
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            val = parts[1].strip()
            if key.isdigit():
                rules[int(key)] = val
    
    if 10 not in rules:
        return False # Can't patch if we don't know 10
        
    # Generate 11-19
    new_lines = []
    ten = rules[10]
    
    # Try to find a separator if defined
    sep = " "
    for line in lines:
        if "ten_sep:" in line:
            sep = line.split(":", 1)[1].strip().strip("'")
            break
            
    for i in range(1, 10):
        if i in rules:
            # Generic logic: 10 + sep + unit
            val = f"{ten}{sep}{rules[i]}"
            new_lines.append(f"{10+i}: {val} # Auto-Generated Generic Patch\n")
            
    # Insert
    idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("10:"):
            idx = i + 1
            break
    if idx == -1: idx = len(lines)
    
    lines[idx:idx] = new_lines
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return True

def main():
    files = [f for f in os.listdir(LANG_DIR) if f.endswith('.lang')]
    count = 0
    for f in files:
        if apply_patch(os.path.join(LANG_DIR, f)):
            count += 1
    print(f"Generic Patch Applied to {count} languages.")

if __name__ == "__main__":
    main()
