def num_to_english(n):
    # Standard English implementation
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
    name = num_to_english(n)
    length = len(name.replace(" ", "").replace("-", ""))
    return n + length

def verify_sequence():
    print("--- VERIFICATION OF 'ERIK CONVERGENCE' ---")
    trunk = [0]
    curr = 0
    for _ in range(15):
        curr = get_next(curr)
        trunk.append(curr)
    print(f"Main Trunk (Calculated): {trunk}")

    rebel_start = 83
    rebel_path = [rebel_start]
    curr = rebel_start
    merged = False
    
    main_set = set()
    t = 0
    while t < 2000:
        main_set.add(t)
        t = get_next(t)
        
    for _ in range(50):
        curr = get_next(curr)
        rebel_path.append(curr)
        if curr in main_set:
            print(f"MERGE DETECTED for 83 at value: {curr}")
            merged = True
            break
            
    if not merged:
        print(f"Rebel Stream (83) did NOT merge in first {len(rebel_path)} steps.")
        print(f"Rebel Path start: {rebel_path[:10]}...")

    # Verify 0-100 Convergence Rate
    merged_count = 0
    rebels = []
    for i in range(101):
        curr = i
        steps = 0
        is_merged = False
        while steps < 500:
            if curr in main_set:
                merged_count += 1
                is_merged = True
                break
            curr = get_next(curr)
            steps += 1
        if not is_merged:
            rebels.append(i)
            
    print(f"Convergence Stat: {merged_count}/101 numbers ({merged_count/101*100:.1f}%) merged.")
    print(f"Non-merging numbers (0-100): {rebels}")

if __name__ == "__main__":
    verify_sequence()