# --- Aramaic Linguistic Topology Verification ---
# This script uses a more accurate, non-approximated model for
# Aramaic number names to verify the "River" convergence rate.

import sys

def get_aramaic_len_accurate(n):
    """
    Calculates the length of the transliterated Aramaic name for n.
    This version uses specific names for 11-19 instead of an approximation.
    Apostrophes (') representing glottal stops are removed for the count.
    """
    if n > 100: return 0 # Out of scope for this function

    # Based on Syriac Aramaic transliterations
    if n == 0: return 4  # sfer
    
    units = {
        1: "khad", 2: "trein", 3: "tlata", 4: "arba", 5: "khamsha", 
        6: "eshta", 7: "shva", 8: "tmanya", 9: "tsha"
    }
    teens = {
        11: "khad'asar", 12: "tre'asar", 13: "tlat'asar", 14: "arba'asar",
        15: "khamesh'asar", 16: "esht'asar", 17: "shva'asar", 18: "tmanya'asar",
        19: "tsha'asar"
    }
    tens = {
        10: "asra", 20: "esrin", 30: "tlatin", 40: "arbain", 50: "khamshin",
        60: "eshtin", 70: "shvin", 80: "tmanin", 90: "tishin"
    }

    if n in units: return len(units[n])
    if n in teens: return len(teens[n].replace("'", ""))
    if n in tens: return len(tens[n])
    
    if n > 20 and n < 100:
        t = (n // 10) * 10
        u = n % 10
        # e.g., esrin w'khad (21)
        return len(tens[t] + "w" + units[u])
        
    if n == 100: return 3 # ma

    return 0 # Should not be reached for 0-100

def analyze_language(lang_name, len_func):
    """
    Runs the simulation for a given language's rules.
    """
    paths = {}
    
    for start_num in range(101):
        path = []
        curr = start_num
        
        while curr < 500 and len(path) < 100: # Increased limit for better accuracy
            path.append(curr)
            length = len_func(curr)
            if length == 0 and curr !=0: break
            curr += length
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

    print(f"--- Analysis for: {lang_name} ---")
    print(f"Structure: {len(unique_rivers)} Distinct River(s) found.")
    
    sorted_groups = sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
    
    main_trunk_size = 0
    if sorted_groups:
        main_trunk_size = len(sorted_groups[0][1])

    print(f"Main Trunk Convergence: {main_trunk_size}% of integers converge into the largest river.")
    print("-" * 40)


if __name__ == "__main__":
    analyze_language("Aramaic (Accurate)", get_aramaic_len_accurate)
