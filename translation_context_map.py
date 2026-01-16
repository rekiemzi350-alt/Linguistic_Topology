import sys

# --- 1. Ancient Hebrew (Biblical/Masoretic) ---
def get_hebrew_len(n):
    # Length of native Hebrew words (Masculine form for abstract counting)
    if n == 0: return 0 # No zero in ancient thought usually, but for algo we use 0
    
    units_len = {
        0: 0, 1: 3, 2: 4, 3: 4, 4: 4, 5: 4, 6: 3, 7: 4, 8: 4, 9: 4, 10: 3
    }
    tens_len = {
        20: 4, 30: 5, 40: 5, 50: 5, 60: 4, 70: 5, 80: 5, 90: 5
    }

    if n <= 10: return units_len[n]
    if n < 20:
        if n == 11: return 6 # achad-asar
        if n == 12: return 7 # shneim-asar
        return units_len[n-10] + 3 # unit + asar
    
    if n < 100:
        t = (n // 10) * 10
        u = n % 10
        if u == 0: return tens_len[t]
        return tens_len[t] + 1 + units_len[u] # tens + ve + unit
        
    if n < 1000:
        h = n // 100
        rem = n % 100
        # Hundreds base
        base = 0
        if h == 1: base = 3 # me'a
        elif h == 2: base = 5 # matayim
        else: base = units_len[h] + 4 # unit + me'ot
        
        if rem == 0: return base
        return base + 1 + get_hebrew_len(rem) # hundred + ve + remainder
    return 0

# --- 2. Aramaic (Imperial/Syriac) ---
def get_aramaic_len(n):
    if n == 0: return 0
    units = [0, 4, 5, 5, 4, 6, 5, 4, 6, 4] # khad, trein, tlata...
    tens = [0, 4, 5, 6, 6, 7, 6, 4, 6, 6] # asar, esrin...
    
    if n < 10: return units[n]
    if n < 20: return units[n-10] + 4 # unit + asar (approx)
    
    if n < 100:
        t = n // 10
        u = n % 10
        if u == 0: return tens[t]
        return tens[t] + 1 + units[u] # tens + w + unit
    return 0

# --- 3. Koine Greek ---
def get_greek_len(n):
    if n == 0: return 0
    units = [0, 4, 3, 5, 8, 5, 3, 5, 4, 5] # heis, duo, treis...
    tens = [0, 4, 6, 9, 12, 10, 8, 12, 10, 9] # deka, eikosi...
    
    if n < 10: return units[n]
    if n == 10: return 4
    if n < 20: 
        if n == 11: return 6 # endeka
        if n == 12: return 6 # dodeka
        return units[n-10] + 3 + 4 # unit + kai + deka
        
    if n < 100:
        t = n // 10
        u = n % 10
        if u == 0: return tens[t]
        return tens[t] + 3 + units[u] # tens + kai + unit
    return 0

# --- 4. American English ---
def get_english_len(n):
    if n == 0: return 4 # zero
    units = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
             "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n < 20: return len(units[n])
    if n < 100:
        t = n // 10
        u = n % 10
        if u == 0: return len(tens[t])
        return len(tens[t] + units[u]) # No hyphen in char count usually? Standard is no space for counting?
        # Actually standard: twenty-one (10 chars). 
        # Let's count letters only: twentyone (9). 
        # Hyphens/spaces usually ignored in this numerology unless specified. 
        # The prompt says "context". Standard Gematria ignores symbols. 
        # But let's check other scripts. They usually count letters.
        return len(tens[t] + units[u])
        
    if n < 1000:
        h = n // 100
        rem = n % 100
        base = units[h] + "hundred"
        if rem == 0: return len(base)
        return len(base) + get_english_len(rem) # onehundredtwentyone
    return 0

def analyze(name, func):
    paths = {}
    limit = 800
    
    # Analyze 1-100 (skip 0 as ancient langs often lack it)
    for start in range(1, 101):
        path = []
        curr = start
        while curr < limit and len(path) < 100:
            path.append(curr)
            l = func(curr)
            if l == 0: break
            curr += l
        paths[start] = path

    groups = {}
    unique_rivers = []
    
    for start in range(1, 101):
        my_path = paths.get(start, [])
        if len(my_path) < 5: continue
        my_tail = tuple(my_path[-5:])
        
        found = False
        for i, r in enumerate(unique_rivers):
            if my_tail == r:
                groups[i].append(start)
                found = True
                break
        if not found:
            unique_rivers.append(my_tail)
            groups[len(unique_rivers)-1] = [start]
            
    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
    
    print(f"\n{name.upper()}")
    print(f"Total Rivers: {len(unique_rivers)}")
    for i, (rid, mems) in enumerate(sorted_groups):
        pct = len(mems)
        print(f"  River {i+1}: {pct}%")
        
    return len(unique_rivers), sorted_groups[0][1] if sorted_groups else []

print("MAPPING TRANSLATION LOSS VIA LINGUISTIC TOPOLOGY")
print("================================================")

h_rivers, h_main = analyze("Ancient Hebrew", get_hebrew_len)
a_rivers, a_main = analyze("Aramaic", get_aramaic_len)
g_rivers, g_main = analyze("Koine Greek", get_greek_len)
e_rivers, e_main = analyze("American English", get_english_len)

print("\n--- CONTEXT LOSS REPORT ---")
print(f"Original Unity (Hebrew): {100//h_rivers if h_rivers else 0}% Cohesion (1 River = 100%)")
print(f"Original Unity (Aramaic): {100//a_rivers if a_rivers else 0}% Cohesion")
print(f"Original Unity (Greek): {100//g_rivers if g_rivers else 0}% Cohesion")
print(f"Target Unity (English): {100//e_rivers if e_rivers else 0}% Cohesion")

if e_rivers > h_rivers:
    print(f"\nResult: FRACTURE DETECTED.")
    print(f"The translation from Hebrew (1 unified outcome) to English ({e_rivers} outcomes)")
    print(f"suggests a loss of deterministic context. The English language introduces")
    print(f"logical forks/ambiguities that did not exist in the source.")
elif e_rivers < h_rivers:
    print(f"\nResult: SIMPLIFICATION DETECTED.")
    print("English merges distinct ancient concepts into fewer paths.")
else:
    print(f"\nResult: TOPOLOGICAL PRESERVATION.")
    print("The logical flow of meaning is structurally preserved.")
