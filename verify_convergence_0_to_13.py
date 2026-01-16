# verify_convergence_0_to_13.py
# This script demonstrates the convergence paths for starting integers 0-13
# to show the formation of the Main Trunk, as requested by Erik Mize for the OEIS submission.

def num_to_english(n):
    """Converts a number to its English name, handling numbers up to the thousands."""
    if n > 9999: return "numbertoolarge" # Safety break for this test
    
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 0: return "zero"
    
    parts = []
    if n >= 1000:
        k = n // 1000
        n %= 1000
        parts.append(num_to_english(k) + "thousand")
    if n >= 100:
        h = n // 100
        n %= 100
        parts.append(ones[h] + "hundred")
    if n >= 20:
        t = n // 10
        n %= 10
        parts.append(tens[t])
    if n > 0:
        parts.append(ones[n])
        
    return "".join(parts)

def get_len(word):
    return len(word.replace(" ","").replace("-",""))

# First, generate the Main Trunk (the sequence from 0) as our reference
main_trunk_list = []
main_trunk_set = set()
curr = 0
for _ in range(50):
    main_trunk_list.append(curr)
    main_trunk_set.add(curr)
    curr += get_len(num_to_english(curr))

print("--- Verifying Convergence for Seeds 0-13 ---")
print(f"Reference Main Trunk: {main_trunk_list[:10]}...")
print("-" * 50)

# Now, trace each seed from 0 to 13
for seed in range(14):
    path = []
    curr = seed
    
    # Check if the seed is already on the trunk
    if curr in main_trunk_set:
        merge_point = curr
        path_str = f"Seed {seed} starts on the Main Trunk at value {merge_point}."
    else:
        # Trace the path until it merges
        while curr not in main_trunk_set:
            path.append(str(curr))
            curr += get_len(num_to_english(curr))
        
        merge_point = curr
        path.append(f"-> {merge_point}")
        path_str = f"Seed {seed}: " + " -> ".join(path)
    
    print(path_str)

print("-" * 50)
print("Conclusion: All integers from 0 to 13 converge to the Main Trunk.")
