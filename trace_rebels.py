def get_english_name(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 0: return "zero"
    
    if n >= 1000: # Simple support for larger numbers to track long convergences
        k = n // 1000
        rem = n % 1000
        base = get_english_name(k) + "thousand"
        if rem == 0: return base
        return base + get_english_name(rem)
        
    if n >= 100:
        h = n // 100
        rem = n % 100
        base = ones[h] + "hundred"
        if rem == 0: return base
        return base + get_english_name(rem)

    if n < 20: return ones[n]
    if n < 100: return tens[n // 10] + ones[n % 10]
    return ""

def trace_path(start_num, limit=50):
    path = []
    curr = start_num
    for _ in range(limit):
        path.append(curr)
        name = get_english_name(curr)
        length = len(name.replace(" ", "").replace("-", ""))
        curr = curr + length
    return path

# Trace Main Trunk (0) and Rebel (83)
trunk_path = trace_path(0, 100)
rebel_path = trace_path(83, 100)

print("--- The Divergence Analysis ---")

# Find if they merge
merge_point = -1
for num in rebel_path:
    if num in trunk_path:
        merge_point = num
        break

print(f"Main Trunk (Start 0): {trunk_path[:10]} ...")
print(f"Rebel Path (Start 83): {rebel_path[:10]} ...")

if merge_point != -1:
    print(f"\nCONCLUSION: They MERGE at number: {merge_point}")
    
    # Calculate distance
    trunk_index = trunk_path.index(merge_point)
    rebel_index = rebel_path.index(merge_point)
    print(f" - The Main Trunk reaches {merge_point} in {trunk_index} steps.")
    print(f" - The Rebel Path reaches {merge_point} in {rebel_index} steps.")
else:
    print("\nCONCLUSION: They do NOT merge within 100 steps. They are truly separate streams.")

# Let's verify 93, 84, 94 too
print("\n--- Checking the other Rebels ---")
rebels = [84, 93, 94]
for r in rebels:
    path = trace_path(r, 20)
    print(f"Start {r}: {path[:6]}...")
