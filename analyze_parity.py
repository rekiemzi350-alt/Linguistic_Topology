def num_to_english(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n < 20: return ones[n]
    if n < 100: return tens[n // 10] + ones[n % 10]
    if n < 1000:
        base = ones[n // 100] + "hundred"
        rem = n % 100
        if rem == 0: return base
        if rem < 20: return base + ones[rem]
        return base + tens[rem // 10] + ones[rem % 10]
    
    # Handle larger numbers simply for the sake of the loop
    # We will just append "thousand" etc. approximations if needed, 
    # but let's stick to < 100000 logic for the trace
    if n < 1000000:
        k = n // 1000
        rem = n % 1000
        base = num_to_english(k) + "thousand"
        if rem == 0: return base
        return base + num_to_english(rem)
        
    return ""

def get_next(n):
    if n == 0: return 4
    name = num_to_english(n)
    length = len(name.replace(" ", "").replace("-", ""))
    return n + length

def analyze_stream_parity(start_num, steps=100):
    sequence = []
    parity_seq = []
    curr = start_num
    
    for _ in range(steps):
        sequence.append(curr)
        parity_seq.append(curr % 2) # 0 for Even, 1 for Odd
        curr = get_next(curr)
        
    return sequence, parity_seq

# Analyze Main Trunk
trunk_vals, trunk_parity = analyze_stream_parity(0, steps=100)

# Analyze Rebel Stream (83)
rebel_vals, rebel_parity = analyze_stream_parity(83, steps=100)

# Print visualization
print("--- Parity Analysis (0=Even, 1=Odd) ---")

def print_wave(name, parity_data):
    print(f"\n{name} Waveform (First 60 steps):")
    # visual representation
    vis = ""
    for p in parity_data[:60]:
        if p == 0: vis += "_" # Low/Even
        else: vis += "-"      # High/Odd
    print(vis)
    print(parity_data[:60])
    
    # Check for stabilization (flatlining)
    # Check last 20
    tail = parity_data[-20:]
    if all(x == 0 for x in tail):
        print("-> STATUS: Flats to EVEN")
    elif all(x == 1 for x in tail):
        print("-> STATUS: Flats to ODD")
    else:
        # Check for oscillation
        is_oscillating = True
        for i in range(len(tail)-1):
            if tail[i] == tail[i+1]:
                is_oscillating = False
                break
        if is_oscillating:
            print("-> STATUS: Oscillates (Frequency constant)")
        else:
            print("-> STATUS: Irregular / Complex Pattern")

print_wave("Main Trunk (Start 0)", trunk_parity)
print_wave("Rebel Stream (Start 83)", rebel_parity)

# Check specifically if they match
print("\n--- Comparison ---")
# Find where they merge in parity pattern (even if numbers are different)
# Just simple observational output
