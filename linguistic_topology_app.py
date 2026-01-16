# --- Linguistic Topology App (LTA) v2.0 ---
# This application analyzes the "Waveform" or "River" structure
# of different languages based on the "Erik Convergence" algorithm.
#
# NEW IN v2.0:
# Now supports loading custom language definitions from external '.lang' files,
# making the tool extensible and easier to automate with tools like Tasker.

import sys
import re
import language_math

# --- 1. The Core Analysis Engine ---

def analyze_language(lang_data):
    """Runs the simulation for a given language's rules."""
    paths = {}
    processor = lang_data["processor"]
    
    for start_num in range(101):
        path = []
        curr = start_num
        
        while curr < 800 and len(path) < 100:
            path.append(curr)
            try:
                length = processor.get_length(curr)
                if length == 0: break
                curr += length
            except Exception:
                break
        paths[start_num] = path

    unique_rivers = []
    groups = {}
    
    for start_num in range(101):
        my_path = paths.get(start_num, [])
        if len(my_path) < 5: continue
        my_tail = tuple(my_path[-5:])
        
        found_river = False
        for river_id, river_tail in enumerate(unique_rivers):
            if my_tail == river_tail:
                groups[river_id].append(start_num)
                found_river = True
                break
        if not found_river:
            new_id = len(unique_rivers)
            unique_rivers.append(my_tail)
            groups[new_id] = [start_num]

    print(f"\n--- Analysis for: {lang_data['name']} ---")
    print(f"Structure: {len(unique_rivers)} Distinct River(s) found for integers 0-100.")
    print("-" * 40)
    
    sorted_groups = sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
    
    for i, (river_id, members) in enumerate(sorted_groups):
        count = len(members)
        percent = count
        tail_preview = unique_rivers[river_id]
        print(f"  River #{i+1}: {percent}% of numbers converge here.")
        print(f"     -> Ends in pattern: ...{tail_preview[-3:]}")

# --- 2. Language-Specific Naming & Parsing ---

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
    math_type = "western" # Default
    lines = []
    
    # First pass: Read lines and find name/math_type
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line)
            if line.strip().startswith('name:'):
                name = line.split(':', 1)[1].strip()
            if line.strip().startswith('math_type:'):
                math_type = line.split(':', 1)[1].strip()

    rules["meta_name"] = name
    
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
        
        if key in ['name', 'math_type']:
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

    processor = language_math.get_processor(math_type, name, rules)

    return {
        "name": name,
        "math_type": math_type,
        "rules": rules,
        "processor": processor
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

    proc1 = lang1["processor"]
    proc2 = lang2["processor"]

    for i in range(limit):
        # Path 1
        curr1 = i
        path1 = []
        while curr1 < 800 and len(path1) < 50:
            path1.append(curr1)
            l = proc1.get_length(curr1)
            if l == 0: break
            curr1 += l
        
        # Path 2
        curr2 = i
        path2 = []
        while curr2 < 800 and len(path2) < 50:
            path2.append(curr2)
            l = proc2.get_length(curr2)
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
