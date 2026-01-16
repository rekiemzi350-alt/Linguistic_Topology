
def num_to_english(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 0: return "zero"
    
    base_str = ""
    if n >= 1000:
        k = n // 1000
        rem = n % 1000
        base_str += num_to_english(k) + "thousand"
        if rem > 0: base_str += num_to_english(rem)
        return base_str
        
    if n >= 100:
        h = n // 100
        rem = n % 100
        base_str += ones[h] + "hundred"
        if rem > 0: base_str += num_to_english(rem)
        return base_str
        
    if n < 20: return ones[n]
    if n < 100: return tens[n // 10] + ones[n % 10]
    
    return ""

def get_len(n):
    name = num_to_english(n)
    return len(name.replace(" ", "").replace("-", ""))

# --- 1. The Normal Progression (Ascent) ---
# n -> n + L(n)
def get_next_ascent(n):
    return n + get_len(n)

# --- 2. The Inverse Progression (Descent) ---
# n -> n - L(n)
def get_next_descent(n):
    return n - get_len(n)

# Generate Data
# Find a high point on the Main Trunk near 2025 to start descent from
trunk = [0]
curr = 0
while curr < 2050:
    curr = get_next_ascent(curr)
    trunk.append(curr)

# Get the last trunk value < 2025 or approx
start_node = trunk[-2] # e.g. around 2024 or similar
print(f"Starting Node for Comparison: {start_node}")

# 1. Ascent Trace (0 -> Start Node)
ascent_path = []
curr = 0
while curr <= start_node:
    ascent_path.append(curr)
    if curr == start_node: break
    curr = get_next_ascent(curr)

# 2. Descent Trace (Start Node -> 0 or negative)
descent_path = []
curr = start_node
while curr > 0:
    descent_path.append(curr)
    curr = get_next_descent(curr)
descent_path.append(curr) # Append the last one (0 or negative)

print(f"\n--- Path Comparison ---")
print(f"Ascent (Forward Rule): {ascent_path[:10]} ... {ascent_path[-5:]}")
print(f"Descent (Inverse Rule): {descent_path[:10]} ... {descent_path[-5:]}")

# Check if Descent retraces Ascent (Time Reversal)
# We compare Descent reversed vs Ascent
descent_reversed = descent_path[::-1]
match_count = 0
for a, d in zip(ascent_path, descent_reversed):
    if a == d: match_count += 1
    else: break

print(f"\nDo they mirror? Matching steps from 0: {match_count}")
if match_count < 3:
    print("-> RESULT: The Inverse Rule creates a COMPLETELY NEW timeline. The past is not the reverse of the future.")
else:
    print("-> RESULT: High symmetry detected.")

# 3. Waveform Inversion Analysis
# Let's look at the Parity (Even/Odd) of the Descent path
# And compare it to the Ascent path
def get_parity_string(seq):
    return "".join(["1" if x % 2 != 0 else "0" for x in seq])

ascent_wave = get_parity_string(ascent_path)
descent_wave = get_parity_string(descent_path)

print(f"\n--- Waveform Analysis (0=Even, 1=Odd) ---")
print(f"Ascent Wave (Time ->): {ascent_wave[:50]}...")
print(f"Descent Wave (Time ->): {descent_wave[:50]}...")

# Check for Inversion (Bit Flip)
# Does Descent Wave == Inverse of Ascent Wave?
inverted_ascent = "".join(["0" if x == "1" else "1" for x in ascent_wave])

print(f"\nIs Descent the 'Inverse' of Ascent? (Bitwise NOT)")
if descent_wave == inverted_ascent:
    print("-> YES! Perfect Inversion.")
else:
    # Check similarity
    matches = sum(1 for a, b in zip(descent_wave, inverted_ascent) if a == b)
    percent = matches / len(min(descent_wave, inverted_ascent)) if len(descent_wave) > 0 else 0
    print(f"-> No. Similarity to Inverse: {percent:.1%}")
