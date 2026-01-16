
def num_to_english(n):
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

def get_next(n):
    return n + len(num_to_english(n))

# Generate Main Trunk
main_trunk = []
curr = 0
while curr <= 3000: # Go past the expected 2827 merge
    main_trunk.append(curr)
    curr = get_next(curr)

# Generate Rebel Stream from 83
rebel_val = 83
rebel_path = []
while rebel_val <= 3000:
    rebel_path.append(rebel_val)
    rebel_val = get_next(rebel_val)

# Find merge point
merge_point = None
main_set = set(main_trunk)
for val in rebel_path:
    if val in main_set:
        merge_point = val
        break

print(f"Merge Point: {merge_point}")

# Format for OEIS (comma separated)
print("Sequence Data:")
print(",".join(map(str, main_trunk)))
