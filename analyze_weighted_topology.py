# analyze_weighted_topology.py
# This script tests two new weighting systems for the Erik Convergence algorithm
# to determine if the topology is sensitive to informational or symbolic letter weights.

import sys

# --- 1. Weighting Systems ---

def get_weight_maps():
    """Generates the dictionaries for frequency and alphabetical weights."""
    # Standard English letter frequency order (most to least common)
    freq_order = "etaoinshrdlcumwfgypbvkjxqz"
    
    freq_weights = {letter: i + 1 for i, letter in enumerate(freq_order)}
    alpha_weights = {chr(ord('a') + i): i + 1 for i in range(26)}
    
    return freq_weights, alpha_weights

FREQ_WEIGHTS, ALPHA_WEIGHTS = get_weight_maps()

# --- 2. Core Algorithm Logic ---

def num_to_english(n):
    """Converts a number to its English name string."""
    if n > 9999: return "numbertoolarge"
    
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 0: return "zero"
    
    parts = []
    if n >= 1000:
        parts.append(num_to_english(n // 1000) + "thousand")
        n %= 1000
    if n >= 100:
        parts.append(ones[n // 100] + "hundred")
        n %= 100
    if n >= 20:
        parts.append(tens[n // 10])
        n %= 10
    if n > 0:
        parts.append(ones[n])
        
    return "".join(parts)

def get_word_weight(word, weight_map):
    """Calculates the total weight of a word based on a given weight map."""
    return sum(weight_map.get(char, 0) for char in word)

# --- 3. Topology Simulation Engine ---

def run_simulation(name, weight_map):
    """Analyzes the topology for a given weighting system."""
    print(f"\n--- Analyzing Topology for: {name} ---")

    paths = {}
    
    for start_num in range(101):
        path = []
        curr = start_num
        
        # Limit steps to prevent infinite loops, which are more likely with large weights. 
        for _ in range(100): 
            path.append(curr)
            word = num_to_english(curr)
            weight = get_word_weight(word, weight_map)
            if weight == 0 and curr != 0: break
            curr += weight
        paths[start_num] = path

    # Group the paths into "rivers" based on their endpoints
    unique_rivers = []
    groups = {}
    
    for start_num in range(101):
        my_path = paths.get(start_num, [])
        if len(my_path) < 3: continue
        my_tail = tuple(my_path[-3:]) # Identify river by its last 3 steps
        
        found_river = False
        for river_id, river_tail in enumerate(unique_rivers):
            if my_tail == river_tail:
                groups.setdefault(river_id, []).append(start_num)
                found_river = True
                break
        if not found_river:
            new_id = len(unique_rivers)
            unique_rivers.append(my_tail)
            groups[new_id] = [start_num]

    print(f"Structure: {len(unique_rivers)} Distinct River(s) found for integers 0-100.")
    print("-" * 50)
    
    sorted_groups = sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
    
    # Print the first few terms of the Main Trunk (starting at 0)
    main_trunk_path = paths.get(0, [])
    print(f"Main Trunk Sequence (first 5 terms):")
    print(" -> ".join(map(str, main_trunk_path[:5])))
    
    print("\nRiver Distribution:")
    for i, (river_id, members) in enumerate(sorted_groups):
        count = len(members)
        percent = (count / 101) * 100
        tail_preview = unique_rivers[river_id]
        print(f"  River #{i+1}: {percent:.1f}% of numbers converge here.")
        if i == 0:
            print(f"     -> This is the Main Trunk, containing {count} numbers.")
        else:
            print(f"     -> Tributary containing {count} numbers.")

if __name__ == "__main__":
    print("Running simulations for new weighting systems...")
    
    # System 1: Frequency-Based Weighting
    run_simulation("Frequency-Based Weights (e=1, t=2...)", FREQ_WEIGHTS)
    
    # System 2: Alphabetical-Based Weighting (A=1, B=2...)
    run_simulation("Alphabetical Weights (a=1, b=2...)", ALPHA_WEIGHTS)
