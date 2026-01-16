def num_to_english(n):
    ones = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n < 20: return ones[n]
    if n < 100:
        res = tens[n // 10]
        if n % 10 > 0: res += ones[n % 10]
        return res
    if n < 1000:
        res = ones[n // 100] + "hundred"
        if n % 100 > 0: res += num_to_english(n % 100)
        return res
    return str(n)

def get_next_val(curr):
    name = num_to_english(curr)
    length = len(name.replace(" ", "").replace("-", ""))
    # Parity logic: Even = Positive, Odd = Negative
    val = length if curr % 2 == 0 else -length
    return curr + length, val

# Track sequences for starting numbers 0 to 9
starts = range(10)
timelines = {s: [] for s in starts}
values = {s: [] for s in starts}

steps = 15

# Initialize
currents = {s: s for s in starts}

# Run simulation
for _ in range(steps):
    for s in starts:
        curr = currents[s]
        next_n, val = get_next_val(curr)
        
        timelines[s].append(curr)
        values[s].append(val)
        
        currents[s] = next_n

print("\n--- SYNCHRONIZATION TEST: DO NUMBERS MIRROR ZERO? ---")
print("Tracking the first 10 numbers. Do they merge into Zero's path?\n")

# Header
header = "Step |"
for s in starts:
    header += f" Start {s} |"
print(header)
print("-" * len(header))

# Rows
zero_path = timelines[0]

for i in range(steps):
    row = f"{i:4} |"
    for s in starts:
        val = values[s][i]
        curr = timelines[s][i]
        
        # Check if this number has merged with Zero's path at this step
        # Note: Merging means hitting the same number.
        # But here we just want to see if the WAVEFORM (Value) syncs.
        
        # Simple visual:
        # If the current number matches Zero's current number -> "SYNC"
        # If not -> Show Value
        
        is_synced = (curr == zero_path[i])
        
        val_str = f"{val:2}" # e.g. " 4" or "-5"
        if val > 0: val_str = f"+{val}"
        
        if is_synced and s != 0:
            display = "  ~ " # Tilde indicates merged
        else:
            display = f"{val_str:3} ({curr})"
            
        row += f" {display:<8}|"
    print(row)

print("\nLEGEND:")
print("Val (Num): The waveform value (+/- length) and the current number.")
print("   ~     : Indicates the timeline has MERGED perfectly with Start 0.")
