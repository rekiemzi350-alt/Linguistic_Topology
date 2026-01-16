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

# Generate Main Trunk (from 0)
main_trunk = set()
curr = 0
for _ in range(50):
    main_trunk.add(curr)
    curr = get_next(curr)

# Analyze 0-100
rivers = {}
for start in range(101):
    curr = start
    path = [curr]
    # Run until we hit the main trunk or go very high
    steps = 0
    merged = False
    while steps < 100:
        if curr in main_trunk:
            merged = True
            break
        curr = get_next(curr)
        path.append(curr)
        steps += 1
    
    if merged:
        key = "Main Trunk"
    else:
        # If not merged, identify by the path tail
        key = f"Rebel Stream (Tail: {path[-3:]})"

    if key not in rivers:
        rivers[key] = []
    rivers[key].append(start)

print(f"Rivers found: {len(rivers)}")
for key, seeds in rivers.items():
    print(f"{key}: {len(seeds)} seeds. Seeds: {seeds}")