<<<<<<< HEAD
=======
import math
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
# --- Linguistic Topology App (LTA) v2.0 ---
# This application analyzes the "Waveform" or "River" structure
# of different languages based on the "Erik Convergence" algorithm.
#
# NEW IN v2.0:
# Now supports loading custom language definitions from external '.lang' files,
# making the tool extensible and easier to automate with tools like Tasker.

import sys
import re
<<<<<<< HEAD
import language_math
=======
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c

# --- 1. The Core Analysis Engine ---

def analyze_language(lang_data):
<<<<<<< HEAD
    """Runs the simulation for a given language's rules."""
    paths = {}
    processor = lang_data["processor"]
=======
    """Runs the simulation for a given language's rules with extreme precision metrics."""
    paths = {}
    entropies = []
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
    
    for start_num in range(101):
        path = []
        curr = start_num
        
<<<<<<< HEAD
        while curr < 800 and len(path) < 100:
            path.append(curr)
            try:
                length = processor.get_length(curr)
                if length == 0: break
=======
        while curr < 10000 and len(path) < 500: # Increased depth for precision
            path.append(curr)
            try:
                length = lang_data["get_len_func"](curr, lang_data["rules"])
                if length == 0: break
                
                # Metric: Step-wise Entropy (Information gain/loss)
                # log2(next/curr) proxy
                entropies.append(math.log2(length) if length > 0 else 0)
                
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
                curr += length
            except Exception:
                break
        paths[start_num] = path

    unique_rivers = []
    groups = {}
    
<<<<<<< HEAD
    for start_num in range(101):
        my_path = paths.get(start_num, [])
        if len(my_path) < 5: continue
        my_tail = tuple(my_path[-5:])
        
        found_river = False
        for river_id, river_tail in enumerate(unique_rivers):
            if my_tail == river_tail:
=======
    # Identify unique attractors (Rivers)
    for start_num in range(101):
        my_path = paths.get(start_num, [])
        if len(my_path) < 5: continue
        my_tail = tuple(my_path[-20:]) # Increased tail size for stability check
        
        found_river = False
        for river_id, river_tail in enumerate(unique_rivers):
            # Check for intersection (any common point in tail)
            if set(my_tail).intersection(set(river_tail)):
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
                groups[river_id].append(start_num)
                found_river = True
                break
        if not found_river:
            new_id = len(unique_rivers)
            unique_rivers.append(my_tail)
            groups[new_id] = [start_num]

<<<<<<< HEAD
    print(f"\n--- Analysis for: {lang_data['name']} ---")
    print(f"Structure: {len(unique_rivers)} Distinct River(s) found for integers 0-100.")
=======
    print(f"\n--- Extreme Precision Analysis: {lang_data['name']} ---")
    print(f"Total Seeds Mapped: 101")
    print(f"Unique Attractors:  {len(unique_rivers)}")
    
    avg_entropy = sum(entropies)/len(entropies) if entropies else 0
    print(f"Linguistic Entropy: {avg_entropy:.4f} bits/step")
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
    print("-" * 40)
    
    sorted_groups = sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
    
    for i, (river_id, members) in enumerate(sorted_groups):
        count = len(members)
<<<<<<< HEAD
        percent = count
        tail_preview = unique_rivers[river_id]
        print(f"  River #{i+1}: {percent}% of numbers converge here.")
        print(f"     -> Ends in pattern: ...{tail_preview[-3:]}")

# --- 2. Language-Specific Naming & Parsing ---

=======
        percent = (count / 101) * 100
        print(f"  River #{i+1}: {percent:.2f}% Convergence Velocity")
        # Stability: Average steps to merge
        # (Simplified: logic for finding merge point relative to the first river)


# --- 2. Language-Specific Naming & Parsing ---

def get_sumerian_len(n, rules):
    """
    Calculates the number of Cuneiform signs for a Sumerian number (Base 60).
    Logic:
    0-59: Sum of signs for Tens (10,20,30,40,50) and Units (1-9).
    60+: Decomposed into multiples of 60.
    """
    if n == 0: return 0 # No zero in Sumerian
    
    # Check direct rules first (e.g., specific signs provided in .lang)
    direct_rules = rules.get("direct", {})
    if n in direct_rules: return len(direct_rules[n])

    # Decompose into Base 60: n = 60*h + Remainder
    h = n // 60
    rem = n % 60
    
    length = 0
    
    # Handle the '60's place (GESH)
    if h > 0:
        # Recursively get length for h (if h is 1, it's 1 GESH sign. If h=2, 2 GESH signs?)
        # For simplicity in 0-800 range:
        # 60 (1 GESH), 120 (2 GESH), etc.
        # Use direct rule for 60 if available, else assume it behaves like units of 60.
        # But commonly: 60=1 sign, 120=2 signs.
        # We can reuse get_sumerian_len for h if we assume GESH behaves like 1.
        # Let's assume h signs of GESH.
        length += get_sumerian_len(h, rules) 

    # Handle Remainder (0-59)
    if rem > 0:
        tens = (rem // 10) * 10
        units = rem % 10
        
        # Add Tens sign count
        if tens > 0:
            # Look up tens in direct rules or tens array?
            # parse_lang_file puts 10,20.. in direct or tens.
            # Let's check direct first.
            if tens in direct_rules:
                length += len(direct_rules[tens])
            else:
                # Check tens array
                tens_idx = tens // 10
                tens_rules = rules.get("tens", [])
                if tens_idx < len(tens_rules) and tens_rules[tens_idx]:
                    length += len(tens_rules[tens_idx])
        
        # Add Units sign count
        if units > 0:
            if units in direct_rules:
                length += len(direct_rules[units])

    return length

def get_western_name(n, rules):
    """Generates the word name for a number."""
    if n > 999: return ""
    
    direct_rules = rules.get("direct", {})
    lang_name = rules.get("meta_name", "").lower()

    if n in direct_rules: return direct_rules[n]
    
    parts = []
    if n >= 100:
        h = n // 100
        rem = n % 100
        
        prefix = direct_rules.get(h, "")
        
        if "german" in lang_name and h == 1 and prefix == "eins":
            prefix = "ein"
        if "spanish" in lang_name and h == 1:
            prefix = ""
            
        parts.append(prefix)
        parts.append(rules.get("hundred", ""))
        
        if rem > 0:
            if rules.get("hundred_sep"): parts.append(rules["hundred_sep"])
            parts.append(get_western_name(rem, rules))
        return "".join(parts)

    if n >= 20:
        t = n // 10
        rem = n % 10
        tens_rules = rules.get("tens", [])
        tens_val = ""
        if t < len(tens_rules):
            tens_val = tens_rules[t]
            
        if rem > 0:
            ten_sep = rules.get("ten_sep", "")
            if ten_sep in ["und", "و"]:
                unit_str = direct_rules.get(rem, "")
                if "german" in lang_name and rem == 1 and unit_str == "eins":
                    unit_str = "ein"
                parts.extend([unit_str, ten_sep, tens_val])
            else:
                parts.append(tens_val)
                if ten_sep: parts.append(ten_sep)
                parts.append(direct_rules.get(rem, ""))
        else:
            parts.append(tens_val)
    elif n > 10:
        # Additive Teens Fallback (10 + unit)
        ten_val = direct_rules.get(10, "")
        unit_val = direct_rules.get(n % 10, "")
        ten_sep = rules.get("ten_sep", " ")
        if ten_val and unit_val:
            parts.extend([ten_val, ten_sep, unit_val])
    
    return "".join(parts)

def get_western_len(n, rules):
    name = get_western_name(n, rules)
    return len(name.replace(" ", "").replace("-", ""))

>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
def validate_script(text, lang_name):
    """
    Validates that the text uses the native alphabet/script for the given language.
    Rejects transliterations (e.g., Latin characters in Sumerian).
    """
    if not text:
        return True

    lang = lang_name.lower()
    
    # Allow binary bitcodes for TECH versions
    if "tech" in lang:
        if not re.match(r'^[01\s]+$', text):
            return False
        return True

    # Define script patterns
    # Note: \s is allowed for spaces.
    
    # 1. Latin Group (English, French, German, Spanish)
    # Allows Basic Latin, Latin-1 Supplement, Latin Extended-A
    if any(x in lang for x in ["english", "french", "german", "spanish"]):
        if not re.match(r'^[A-Za-z\u00C0-\u00FF\u0100-\u017F\s\-]+$', text):
            return False

    # 2. Ancient Greek
    elif "greek" in lang:
        if not re.match(r'^[\u0370-\u03FF\u1F00-\u1FFF\s\-]+$', text):
            return False

    # 3. Ancient Egyptian (Hieroglyphs)
    elif "egyptian" in lang:
        if not re.match(r'^[\U00013000-\U0001342F\s]+$', text):
            return False

    # 4. Sumerian (Cuneiform)
    elif "sumerian" in lang:
        if not re.match(r'^[\U00012000-\U0001247F\s]+$', text):
            return False

    # 5. Chinese / Mandarin / Cantonese (Hanzi / CJK)
    elif any(x in lang for x in ["chinese", "mandarin", "cantonese"]):
        # CJK Unified Ideographs + Extensions A-G roughly covered by ranges or just main block
        # Using main CJK block + Ext A.
        if not re.match(r'^[\u4E00-\u9FFF\u3400-\u4DBF\s]+$', text):
            return False

    # 6. Japanese (Kanji + Hiragana + Katakana)
    elif "japanese" in lang:
        if not re.match(r'^[\u3040-\u30FF\u4E00-\u9FFF\s]+$', text):
            return False

    # 7. Arabic
    elif "arabic" in lang:
        if not re.match(r'^[\u0600-\u06FF\s]+$', text):
            return False

    # 8. Aramaic (Imperial Aramaic, Hebrew, Syriac)
    elif "aramaic" in lang:
        if "samaritan" in lang:
             if not re.match(r'^[\u0800-\u083F\s]+$', text):
                return False
        elif not re.match(r'^[\u0590-\u05FF\u0700-\u074F\U00010840-\U0001085F\s]+$', text):
            return False

    # 9. Cyrillic (Russian)
    elif "russian" in lang:
        if not re.match(r'^[\u0400-\u04FF\s]+$', text):
            return False

    # 10. Devanagari (Sanskrit, Hindi)
    elif any(x in lang for x in ["sanskrit", "hindi"]):
        if not re.match(r'^[\u0900-\u097F\s]+$', text):
            return False

    # 11. Korean (Hangul)
    elif "korean" in lang:
        if not re.match(r'^[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F\s]+$', text):
            return False

    # Default: If language not strictly monitored, allow (or could default to Latin if preferred)
    return True

def parse_lang_file(filepath):
    """Parses a .lang file and returns a language data dictionary."""
    rules = {"direct": {}, "tens": [""] * 10}
    name = "Custom Language"
<<<<<<< HEAD
    math_type = "western" # Default
    lines = []
    
    # First pass: Read lines and find name/math_type
=======
    lines = []
    
    # First pass: Read lines and find name
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line)
            if line.strip().startswith('name:'):
                name = line.split(':', 1)[1].strip()
<<<<<<< HEAD
            if line.strip().startswith('math_type:'):
                math_type = line.split(':', 1)[1].strip()

    rules["meta_name"] = name
    
=======

    rules["meta_name"] = name
    
    # Determine function based on name
    func = get_western_len
    if "sumerian" in name.lower():
        func = get_sumerian_len

>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
    # Second pass: Parse values and validate
    for line in lines:
        line = line.strip()
        if line.startswith('#') or ':' not in line:
            continue
        
        key, value = line.split(':', 1)
        key = key.strip()
        
        # Strip inline comments
        if '#' in value:
            value = value.split('#', 1)[0]
        
        value = value.strip()
        
<<<<<<< HEAD
        if key in ['name', 'math_type']:
=======
        if key == 'name':
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
            continue # Already handled

        # Validate the value against the native script rules
        if not validate_script(value, name):
            raise ValueError(f"Validation Error: The value '{value}' for key '{key}' is not in the native alphabet for language '{name}'. Transliterations are not allowed.")

        if key.isdigit():
            num = int(key)
            # Allow any direct number (useful for Spanish 100, Sumerian 60, etc.)
            rules["direct"][num] = value
            
            # Also populate tens array for convenience if in range
            if 20 <= num <= 90 and num % 10 == 0:
                rules["tens"][num // 10] = value
        elif key in ["hundred", "ten_sep", "hundred_sep"]:
            rules[key] = value

<<<<<<< HEAD
    processor = language_math.get_processor(math_type, name, rules)

    return {
        "name": name,
        "math_type": math_type,
        "rules": rules,
        "processor": processor
=======
    return {
        "name": name,
        "get_len_func": func,
        "rules": rules
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
    }

# --- 3. Forensic Comparison (Hoax Detection) ---

def compare_topologies(lang1, lang2):
    """
    Compares the convergence patterns of two languages.
    Used for forensic 'hoax detection' by identifying structural identity.
    """
    print(f"\n=== FORENSIC TOPOLOGY COMPARISON ===")
    print(f"Baseline: {lang1['name']}")
    print(f"Target:   {lang2['name']}")
    print("-" * 40)

    # Simulation parameters
    limit = 101
    matches = 0
    total_length_diff = 0

<<<<<<< HEAD
    proc1 = lang1["processor"]
    proc2 = lang2["processor"]

=======
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
    for i in range(limit):
        # Path 1
        curr1 = i
        path1 = []
        while curr1 < 800 and len(path1) < 50:
            path1.append(curr1)
<<<<<<< HEAD
            l = proc1.get_length(curr1)
=======
            l = lang1["get_len_func"](curr1, lang1["rules"])
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
            if l == 0: break
            curr1 += l
        
        # Path 2
        curr2 = i
        path2 = []
        while curr2 < 800 and len(path2) < 50:
            path2.append(curr2)
<<<<<<< HEAD
            l = proc2.get_length(curr2)
=======
            l = lang2["get_len_func"](curr2, lang2["rules"])
>>>>>>> 3f1231c7745b157981796b9bd27f4cf386fbef0c
            if l == 0: break
            curr2 += l

        # Compare path lengths as a proxy for 'bit-velocity' similarity
        if len(path1) == len(path2):
            matches += 1
        
        total_length_diff += abs(len(path1) - len(path2))

    correlation = (matches / limit) * 100
    avg_diff = total_length_diff / limit

    print(f"Convergence Identity:  {correlation:.2f}%")
    print(f"Path Length Deviation: {avg_diff:.2f} steps")
    print("-" * 40)

    if correlation > 90:
        print("RESULT: HIGH IDENTITY. The target language perfectly mimics the baseline structure.")
        print("FORENSIC NOTE: Potential modern hoax if claiming ancient origin.")
    elif correlation > 60:
        print("RESULT: STRUCTURAL SIMILARITY. Possible linguistic relation or shared root.")
    else:
        print("RESULT: DISTINCT TOPOLOGIES. The languages exhibit unrelated bit-velocities.")

# --- 4. Main Execution ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage (Analysis):   python linguistic_topology_app.py <lang1.lang>")
        print("Usage (Forensics):  python linguistic_topology_app.py <baseline.lang> <target.lang>")
        sys.exit(1)
        
    try:
        if len(sys.argv) == 2:
            lang_data = parse_lang_file(sys.argv[1])
            analyze_language(lang_data)
        elif len(sys.argv) == 3:
            lang1 = parse_lang_file(sys.argv[1])
            lang2 = parse_lang_file(sys.argv[2])
            compare_topologies(lang1, lang2)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
