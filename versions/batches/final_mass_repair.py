import os
import re

LANG_DIR = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"

def get_tech_representation(num, base_val):
    # Heuristic for TECH: bitstring or hex-like
    # If base_val is binary, 11-19 should be binary
    if re.match(r'^[01\s]+$', base_val):
        return bin(num)[2:]
    return hex(num)[2:]

def repair_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    rules = {}
    name = ""
    for line in lines:
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            val = parts[1].strip()
            if key.isdigit():
                rules[int(key)] = val

    if not rules: return False
    
    # Check if 11 is missing
    if 11 in rules: return False
    
    # Determine Repair Strategy
    new_lines = []
    
    if "TECH" in name or "TECH" in filepath:
        # Strategy: Use bitstrings/hex
        base_val = rules.get(1, rules.get(10, "0"))
        for i in range(11, 20):
            val = get_tech_representation(i, base_val)
            new_lines.append(f"{i}: {val} # Auto-Repair TECH\n")
    elif 10 in rules:
        # Strategy: Decimal Aggregation {10}{1}
        ten = rules[10]
        one = rules.get(1, "")
        sep = " " # Default
        for line in lines:
            if "ten_sep:" in line:
                sep = line.split(":", 1)[1].strip().strip("'”)
        
        for i in range(1, 10):
            if i in rules:
                val = f"{ten}{sep}{rules[i]}"
                new_lines.append(f"{10+i}: {val} # Auto-Repair Aggregate\n")
    else:
        # Strategy: Last Resort - use a placeholder or skip
        return False

    # Insert after 10: or at end
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
        if repair_file(os.path.join(LANG_DIR, f)):
            count += 1
    print(f"Repair Complete. Fixed {count} languages.")

if __name__ == "__main__":
    main()
