
def num_to_english(n):
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

def get_next(n):
    return n + len(num_to_english(n))

main_trunk = set()
curr = 0
for _ in range(5000):
    main_trunk.add(curr)
    curr = get_next(curr)

for start in [83, 84, 93, 94]:
    curr = start
    for i in range(5000):
        if curr in main_trunk:
            print(f"Seed {start} merged at {curr} after {i} steps.")
            break
        curr = get_next(curr)
    else:
        print(f"Seed {start} did not merge within 5000 steps.")
