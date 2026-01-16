# --- Linguistic Topology App (LTA) v2.1 - Convergence Edition ---
# This application analyzes the "Waveform" or "River" structure
# of different languages based on the "Erik Convergence" algorithm.
#
# This version runs the simulation until a true convergence point (a loop or
# termination) is found, with safety breaks for exceptionally long paths.

import sys
import re
from language_math import get_processor

# --- 1. The Core Analysis Engine ---

def analyze_language(lang_data):
    """Runs the simulation for a given language's rules until convergence."""
    paths = {}
    
    for start_num in range(101):
        path = []
        seen_in_path = set()
        curr = start_num
        
        # Run until convergence with safety limits - pushed for full unity
        while curr < 100000000 and len(path) < 10000:
            if curr in seen_in_path:
                path.append(f"LOOP_TO_{curr}")
                break # Loop detected
            
            path.append(curr)
            seen_in_path.add(curr)
            
            try:
                length = lang_data["get_len_func"](curr, lang_data["rules"])
                if length == 0: 
                    break # Path terminated
                curr += length
            except Exception:
                break # Error in length calculation
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

    print(f"\n--- Full Convergence Analysis for: {lang_data['name']} ---")
    print(f"Structure: {len(unique_rivers)} Distinct River(s) found for integers 0-100.")
    print("-" * 40)
    
    sorted_groups = sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
    
    for i, (river_id, members) in enumerate(sorted_groups):
        count = len(members)
        percent = count
        tail_preview = unique_rivers[river_id]
        
        # Format the tail preview to be more readable
        formatted_tail = []
        for item in tail_preview:
            if isinstance(item, str) and "LOOP" in item:
                formatted_tail.append(f"-> {item}")
            else:
                formatted_tail.append(str(item))

        print(f"  River #{i+1}: {percent}% of numbers converge here.")
        print(f"     -> Ends in pattern: ...{' -> '.join(formatted_tail[-3:])}")

# --- 2. Language-Specific Naming & Parsing ---

def validate_script(text, lang_name):
    return True

def parse_lang_file(filepath):
    rules = {"direct": {}, "tens": [""] * 10}
    name = "Custom Language"
    lines = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            lines.append(line)
            if line.strip().startswith('name:'):
                name = line.split(':', 1)[1].strip()
    rules["meta_name"] = name
    
    for line in lines:
        line = line.strip()
        if line.startswith('#') or ':' not in line: continue
        key, value = line.split(':', 1)
        key = key.strip()
        if '#' in value: value = value.split('#', 1)[0]
        value = value.strip()
        if key == 'name': continue
        if not validate_script(value, name): raise ValueError(f"Validation Error for {name}")
        if key.isdigit():
            num = int(key)
            rules["direct"][num] = value
            if 20 <= num <= 90 and num % 10 == 0: rules["tens"][num // 10] = value
        elif key in ["hundred", "ten_sep", "hundred_sep"]: rules[key] = value

    math_type = "western"
    name_lower = name.lower()
    if "sumerian" in name_lower: math_type = "sumerian"
    elif "hebrew" in name_lower:
        if "gematria" in name_lower: math_type = "hebrew_gematria"
        else: math_type = "hebrew"
    
    processor = get_processor(math_type, name, rules)
    return {"name": name, "get_len_func": lambda n, r: processor.get_length(n), "rules": rules}


# --- 3. Main Execution ---

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_to_convergence.py <lang.lang>")
        sys.exit(1)
    try:
        lang_data = parse_lang_file(sys.argv[1])
        analyze_language(lang_data)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
