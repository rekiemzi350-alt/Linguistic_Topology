import os
import sys
import re
import math

# --- CONFIGURATION ---
LANG_DIR = "linguistic_topology_repo/languages"
OUTPUT_DIR = "OEIS_B_Files"
MAX_STEPS = 100000
HARD_LIMIT = 500000 # Safety brake for non-converging infinite loops

# Extended Large Number Keywords (Simplified)
LARGE_KEYWORDS = {
    "English": {1000: "thousand", 1000000: "million", 1000000000: "billion"},
    "Spanish": {1000: "mil", 1000000: "millon", 1000000000: "milmillones"},
    "French": {1000: "mille", 1000000: "million", 1000000000: "milliard"},
    "German": {1000: "tausend", 1000000: "million", 1000000000: "milliarde"},
    "Latin": {1000: "mille", 1000000: "million", 1000000000: "milliard"},
    "Ancient_Greek": {1000: "chilioi", 10000: "myrioi"},
    "Hebrew": {1000: "elef", 1000000: "milyon"},
}

def parse_lang_file(filepath):
    rules = {"direct": {}, "tens": [""] * 10}
    name = "Unknown"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            
            if line.startswith('name:'):
                name = line.split(':', 1)[1].strip()
                rules["meta_name"] = name
                continue
            
            if ':' in line:
                key_part, val = line.split(':', 1)
                key_part = key_part.strip()
                val = val.split('#')[0].strip()
                
                if key_part.isdigit():
                    num = int(key_part)
                    rules["direct"][num] = val
                    if 20 <= num <= 90 and num % 10 == 0:
                        rules["tens"][num // 10] = val
                elif key_part in ["hundred", "thousand", "million", "ten_sep", "hundred_sep", "thousand_sep"]:
                    rules[key_part] = val
                    
    # Inject guessed large keywords
    if name in LARGE_KEYWORDS:
        for val, word in LARGE_KEYWORDS[name].items():
            if val not in rules["direct"]:
                rules["direct"][val] = word
            if val == 1000 and "thousand" not in rules:
                rules["thousand"] = word

    return {"name": name, "rules": rules}

def get_sumerian_len(n, rules):
    if n == 0: return 0
    signs = 0
    temp = n
    shar = temp // 3600
    temp %= 3600
    if shar > 0: signs += shar 
    gesh = temp // 60
    temp %= 60
    if gesh > 0: signs += gesh 
    tens = temp // 10
    units = temp % 10
    signs += tens + units
    return signs

def get_name_length(n, lang_data):
    rules = lang_data["rules"]
    name = lang_data["name"]
    
    if "Sumerian" in name:
        return get_sumerian_len(n, rules)
    
    if "TECH" in name:
        return len(bin(n)[2:])

    if n == 0:
        return len(rules["direct"].get(0, "zero").replace(" ", ""))
        
    def construct_len(num):
        if num == 0: return 0
        if num in rules["direct"]:
            return len(rules["direct"][num].replace(" ", "").replace("-", ""))
        
        if num >= 1000:
            thousand_word = rules.get("thousand", "thousand")
            thousand_sep = rules.get("thousand_sep", " ")
            k = num // 1000
            rem = num % 1000
            l = construct_len(k) + len(thousand_word.replace(" ", ""))
            if rem > 0:
                l += len(thousand_sep.replace(" ", "")) + construct_len(rem)
            return l

        if num >= 100:
            hundred_word = rules.get("hundred", "hundred")
            hundred_sep = rules.get("hundred_sep", " ")
            h = num // 100
            rem = num % 100
            l = construct_len(h) + len(hundred_word.replace(" ", ""))
            if rem > 0:
                l += len(hundred_sep.replace(" ", "")) + construct_len(rem)
            return l
            
        if num >= 20:
            tens = (num // 10) * 10
            unit = num % 10
            sep = rules.get("ten_sep", "")
            l = len(rules["direct"].get(tens, "X").replace(" ", ""))
            if unit > 0:
                l += len(sep.replace(" ", "")) + len(rules["direct"].get(unit, "X").replace(" ", ""))
            return l
            
        if num > 10:
            return len(rules["direct"].get(10, "X")) + len(rules["direct"].get(num % 10, "X"))
        
        return len(rules["direct"].get(num, "X"))

    return construct_len(n)

def generate_b_file(lang_path):
    lang_data = parse_lang_file(lang_path)
    name = lang_data["name"].replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    
    curr = 0
    if 0 not in lang_data["rules"]["direct"] and "TECH" not in lang_data["name"]:
        curr = 1
        
    trajectory = [curr]
    seen = {curr: 0}
    
    converged_at = -1
    loop_start = -1
    
    for i in range(MAX_STEPS):
        length = get_name_length(curr, lang_data)
        if length == 0: break
        
        next_val = curr + length
        
        if next_val in seen:
            loop_start = seen[next_val]
            converged_at = i + 1
            trajectory.append(next_val)
            break
            
        trajectory.append(next_val)
        seen[next_val] = len(trajectory) - 1
        curr = next_val
        
        if curr > 10**12: break

    out_name = f"b_file_{name}.txt"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"# {lang_data['name']} Trajectory\n")
        if converged_at != -1:
            f.write(f"# Converged at step {converged_at} to loop starting at index {loop_start}\n")
        f.write(f"# n a(n)\n")
        for j, val in enumerate(trajectory):
            f.write(f"{j} {val}\n")
            
    return len(trajectory), converged_at

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    files = sorted([f for f in os.listdir(LANG_DIR) if f.endswith('.lang')])
    print(f"Found {len(files)} languages.")
    
    summary_path = os.path.join(OUTPUT_DIR, "convergence_summary.txt")
    with open(summary_path, 'w') as summary:
        summary.write("Language | Terms | Converged At\n")
        summary.write("---|---|---\n")
        
        for f in files:
            path = os.path.join(LANG_DIR, f)
            count, conv = generate_b_file(path)
            summary.write(f"{f} | {count} | {conv if conv != -1 else 'No'}\n")
            print(f"Processed: {f} ({count} terms, Conv: {conv})")

if __name__ == "__main__":
    main()
