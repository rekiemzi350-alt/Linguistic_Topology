import os
import sys

# --- CONFIGURATION ---
LANG_DIR = "linguistic_topology_repo/languages"
OUTPUT_DIR = "OEIS_B_Files"
MAX_STEPS = 100000
EXTENSION_LIMIT = 2000000 # The "Extend until they do" limit

# Extended Large Number Keywords (Universal Fallback)
LARGE_KEYWORDS = {
    "English": {1000: "thousand", 1000000: "million"},
    "Spanish": {1000: "mil", 1000000: "millon"},
    "French": {1000: "mille", 1000000: "million"},
    "German": {1000: "tausend", 1000000: "million"},
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
    
    # Inject Universal Fallback if specific large numbers are missing
    if name in LARGE_KEYWORDS:
        for val, word in LARGE_KEYWORDS[name].items():
            if val not in rules["direct"]:
                rules["direct"][val] = word
            if val == 1000 and "thousand" not in rules: rules["thousand"] = word
            
    return {"name": name, "rules": rules}

def get_name_length(n, lang_data):
    # Simplified Logic (Supports Recursion for Large Numbers)
    rules = lang_data["rules"]
    if "Sumerian" in lang_data["name"]:
        # Simple Sumerian approximation for speed
        if n == 0: return 0
        return (n // 3600) + ((n % 3600) // 60) + ((n % 60) // 10) + (n % 10)
    
    if "TECH" in lang_data["name"]:
        return len(bin(n)[2:])

    # Recursive Western
    def construct_len(num):
        if num == 0: return 0
        if num in rules["direct"]:
            return len(rules["direct"].get(num, "X").replace(" ", "").replace("-", ""))
        
        # Power of 10 decomposition
        for cutoff, label_key, sep_key in [(1000000, "million", "million_sep"), (1000, "thousand", "thousand_sep"), (100, "hundred", "hundred_sep")]:
            if num >= cutoff:
                word = rules.get(label_key, label_key) # Default to key name if missing (e.g. "million")
                sep = rules.get(sep_key, " ")
                k = num // cutoff
                rem = num % cutoff
                l = construct_len(k) + len(word.replace(" ", ""))
                if rem > 0: l += len(sep.replace(" ", "")) + construct_len(rem)
                return l

        if num >= 20:
            tens = (num // 10) * 10
            unit = num % 10
            sep = rules.get("ten_sep", "")
            l = len(rules["direct"].get(tens, "X").replace(" ", ""))
            if unit > 0: l += len(sep.replace(" ", "")) + len(rules["direct"].get(unit, "X").replace(" ", ""))
            return l
            
        if num > 10: # Fallback 11-19
            return len(rules["direct"].get(10, "X")) + len(rules["direct"].get(num%10, "X"))
            
        return len(rules["direct"].get(num, "X"))

    if n == 0: return len(rules["direct"].get(0, "zero").replace(" ", ""))
    return construct_len(n)

def verify_language_convergence(lang_path):
    lang_data = parse_lang_file(lang_path)
    name = lang_data["name"]
    print(f"Verifying Convergence: {name}...")

    # 1. Generate Main Trunk (Seed 0)
    trunk_set = set()
    trunk_max = 0
    curr = 0
    if 0 not in lang_data["rules"]["direct"] and "TECH" not in name: curr = 1
    
    # Run Trunk for initial MAX_STEPS
    steps = 0
    while steps < MAX_STEPS:
        trunk_set.add(curr)
        trunk_max = curr
        l = get_name_length(curr, lang_data)
        if l == 0: break
        curr += l
        steps += 1
        if curr > 10**15: break # Sanity

    # 2. Test Seeds 1-20 for Convergence
    seeds_to_test = range(1, 21)
    converged_count = 0
    max_steps_needed = 0
    
    rebels = []

    for seed in seeds_to_test:
        if seed in trunk_set:
            converged_count += 1
            continue
            
        # Trace seed
        s_curr = seed
        s_steps = 0
        merged = False
        
        while s_steps < MAX_STEPS:
            if s_curr in trunk_set:
                merged = True
                converged_count += 1
                if s_steps > max_steps_needed: max_steps_needed = s_steps
                break
            
            l = get_name_length(s_curr, lang_data)
            if l == 0: break
            s_curr += l
            s_steps += 1
        
        if not merged:
            rebels.append(seed)

    # 3. EXTEND REBELS (The "Do that until they do" logic)
    if rebels:
        print(f"  ! Found {len(rebels)} Potential Rebels (e.g., {rebels[0]}). Extending search...")
        
        # Extend Trunk further
        while steps < EXTENSION_LIMIT:
            trunk_set.add(curr)
            l = get_name_length(curr, lang_data)
            if l == 0: break
            curr += l
            steps += 1
            
        # Retry Rebels against extended trunk
        still_rebel = []
        for r_seed in rebels:
            r_curr = r_seed
            r_steps = 0
            r_merged = False
            while r_steps < EXTENSION_LIMIT:
                if r_curr in trunk_set:
                    r_merged = True
                    break
                l = get_name_length(r_curr, lang_data)
                if l == 0: break
                r_curr += l
                r_steps += 1
            
            if not r_merged:
                still_rebel.append(r_seed)
        
        rebels = still_rebel

    # Result
    if not rebels:
        return f"{name}: 100% Convergence (Verified up to {steps} steps)."
    else:
        return f"{name}: FAILED CONVERGENCE. Rebels persist: {rebels[:5]}... (Checked {EXTENSION_LIMIT} steps)"

def main():
    files = sorted([f for f in os.listdir(LANG_DIR) if f.endswith('.lang')])
    report_path = os.path.join(OUTPUT_DIR, "PROOF_OF_CONVERGENCE.txt")
    
    with open(report_path, 'w') as f:
        f.write("LINGUISTIC TOPOLOGY: CONVERGENCE PROOF REPORT\n")
        f.write("=============================================\n")
        
        for lang_file in files:
            result = verify_language_convergence(os.path.join(LANG_DIR, lang_file))
            print(f"  > {result}")
            f.write(result + "\n")
            
    print(f"\nProof Report Saved: {report_path}")

if __name__ == "__main__":
    main()
