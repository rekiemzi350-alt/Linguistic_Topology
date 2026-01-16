def num_to_english(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 0: return "zero"
    
    parts = []
    
    if n >= 1000000:
        parts.append(num_to_english(n // 1000000) + "million")
        n %= 1000000
        
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

def get_trajectory(start, steps):
    traj = [start]
    curr = start
    for _ in range(steps):
        curr = get_next(curr)
        traj.append(curr)
    return traj

# Main trunk starting from 0
main_trunk = set()
curr = 0
for _ in range(1000):
    main_trunk.add(curr)
    curr = get_next(curr)

print("Analyzing trajectory of 83:")
curr = 83
path = []
for i in range(2000):
    if curr in main_trunk:
        print(f"83 merged into main trunk at {curr} after {i} steps.")
        break
    path.append(curr)
    curr = get_next(curr)
else:
    print("83 did not merge within 2000 steps.")

if rebel_seeds:
    print(f"\nRebel Seeds found: {rebel_seeds}")
    # Let's see if the rebels merge with each other
    seed0 = rebel_seeds[0]
    rebel_trunk = set()
    curr = seed0
    for _ in range(2000):
        rebel_trunk.add(curr)
        curr = get_next(curr)
    
    for seed in rebel_seeds[1:]:
        curr = seed
        merged = False
        for _ in range(100):
            if curr in rebel_trunk:
                merged = True
                break
            curr = get_next(curr)
        if merged:
            print(f"Seed {seed} merges into Rebel Trunk (starting {seed0})")
        else:
            print(f"Seed {seed} is independent even from Rebel Trunk!")

    # Check for eventual merge between Main and Rebel
    print("\nChecking for long-term merge between Main Trunk and Rebel Trunk...")
    main_list = sorted(list(main_trunk))
    rebel_list = sorted(list(rebel_trunk))
    
    # Extend both
    m_curr = max(main_list)
    r_curr = max(rebel_list)
    
    main_set = main_trunk.copy()
    rebel_set = rebel_trunk.copy()
    
    for _ in range(5000):
        m_curr = get_next(m_curr)
        main_set.add(m_curr)
        r_curr = get_next(r_curr)
        rebel_set.add(r_curr)
        
    intersection = main_set.intersection(rebel_set)
    if intersection:
        print(f"MERGE DETECTED at {min(intersection)}")
    else:
        print("No merge detected after 6000+ total steps.")
