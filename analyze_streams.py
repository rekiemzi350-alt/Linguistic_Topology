
def num_to_english(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n < 20:
        return ones[n]
    if n < 100:
        return tens[n // 10] + ones[n % 10]
    if n < 1000:
        base = ones[n // 100] + "hundred"
        remainder = n % 100
        if remainder == 0:
            return base
        elif remainder < 20:
            return base + ones[remainder]
        else:
            return base + tens[remainder // 10] + ones[remainder % 10]
    return ""

def get_next(n):
    if n == 0: return 4 # "zero"
    word = num_to_english(n)
    length = len(word)
    return n + length

# 1. Generate the "Main Trunk" starting from 0
main_trunk = []
current = 0
while current < 300:
    if current not in main_trunk:
        main_trunk.append(current)
    current = get_next(current)

# 2. Analyze 0-100
streams = dict() # Key: Merge Point, Value: List of starting numbers

for start_num in range(101):
    curr = start_num
    
    # Trace path until we hit the Main Trunk
    while curr < 500:
        if curr in main_trunk:
            # We found the entry point
            entry_point = curr
            if entry_point not in streams:
                streams[entry_point] = []
            streams[entry_point].append(start_num)
            break
        curr = get_next(curr)

# 3. Format Output for the User
print("CLASSIFICATION OF INTEGERS 0-100 BY MAIN TRUNK ENTRY POINT")
print("==========================================================")
print("Main Trunk Sequence: " + str(main_trunk[:15]) + "...\n")

sorted_keys = sorted(streams.keys())
for key in sorted_keys:
    stream_name = "Entry Node " + str(key)
    nums = streams[key]
    print("[" + stream_name + "] (Count: " + str(len(nums)) + ")")
    print("  Numbers: " + str(nums))
    print("-" * 60)
