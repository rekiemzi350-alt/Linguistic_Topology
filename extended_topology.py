import sys

# --- 1. Sumerian Logic (Cuneiform Sign Count) ---
def get_sumerian_signs(n):
    # Base 60 Place Value System
    # Digit Sign Count: (digit // 10) + (digit % 10)
    # Exceptions: 0 is 0 signs (empty). 
    # But for the number 0 itself, we usually return something to keep the loop going or 0.
    # The prompt implies "trajectory of 0". If len(0) is 0, it stays at 0. 
    # sumerian.lang said 0:1. I will use 1 for n=0.
    
    if n == 0: return 1
    
    count = 0
    # Convert to base 60 digits
    temp_n = n
    digits = []
    if temp_n == 0: digits = [0]
    while temp_n > 0:
        digits.append(temp_n % 60)
        temp_n //= 60
    
    # Sum signs for each digit
    for d in digits:
        if d == 0:
            # In place value, an empty place is 0 signs.
            # Unless it's the only digit (handled above).
            count += 0 
        else:
            # 1 = 1 (dis)
            # 10 = 1 (u)
            # 11 = 2 (u dis)
            # 59 = 5(u) + 9(dis) = 14 signs
            count += (d // 10) + (d % 10)
            
    # If the number is > 0 but signs is 0 (e.g. n=0 handled, but n=3600 -> 1,0,0 -> 1+0+0=1)
    if count == 0: return 1 # Fallback, though 3600 is 1 sign. 
    
    return count

# --- 2. Ancient Greek Logic (Greek Letter Count) ---
# Estimates the number of letters in the Ancient Greek spelling.
# Removes 'h' (rough breathing).
# Treats 'ph', 'th', 'ch', 'ps', 'xi' as 1 letter (phi, theta, chi, psi, xi).
# Standard Attic/Ionic names.

def get_greek_letter_count(n):
    if n == 0: return 5 # ouden (o-u-d-e-n)
    
    # 1-9
    # heis -> eis (3)
    # duo -> duo (3)
    # treis -> treis (5)
    # tessares -> tessares (8) (Attic: tettares -> 8)
    # pente -> pente (5)
    # hex -> ex (2)
    # hepta -> epta (4)
    # okto -> okto (4)
    # ennea -> ennea (5)
    units_len = [0, 3, 3, 5, 8, 5, 2, 4, 4, 5]
    
    # 10-90
    # deka (4)
    # eikosi (6)
    # triakonta (9)
    # tessarakonta (12)
    # pentekonta (10)
    # hexakonta -> exakonta (8)
    # hebdomekonta -> ebdomekonta (11)
    # ogdoekonta (10)
    # enenekonta (10)
    tens_len = [0, 4, 6, 9, 12, 10, 8, 11, 10, 10]
    
    # 100-900
    # hekaton -> ekaton (6)
    # diakosioi (9)
    # triakosioi (10)
    # tetrakosioi (11)
    # pentakosioi (11)
    # hexakosioi -> exakosioi (9)
    # heptakosioi -> eptakosioi (10)
    # oktakosioi (10)
    # enakosioi (9)
    hundreds_len = [0, 6, 9, 10, 11, 11, 9, 10, 10, 9]

    parts_len = 0
    
    # Extract periods (myriads are 10,000)
    # Greek uses Myriad (M) = 10,000.
    # We will process chunks of 10,000.
    # e.g. 20,000 is "dis myrioi" (2 * 10000).
    
    # Simplified Logic for Large Numbers:
    # Just sum the lengths of components.
    # 1234 -> chilioi diakosioi triakonta tessares
    
    # We'll handle up to 9999 for simplicity in the loop, assuming growth is slow.
    # If > 9999, we'll approximate or use "myrioi".
    
    if n >= 10000:
        # Recursive Myriads
        m = n // 10000
        rem = n % 10000
        # "m myriads"
        # myrioi (6) or myrias (6)
        parts_len += get_greek_letter_count(m) + 6
        if rem > 0:
            parts_len += get_greek_letter_count(rem) # "kai" usually implied or added
        return parts_len

    # 1000-9999
    if n >= 1000:
        k = n // 1000
        rem = n % 1000
        # 1000: chilioi (6) (chi-i-l-i-o-i) -> ch is 1 letter (chi). So c-h-i-l-i-o-i is 1+1+1+1+1+1 = 6?
        # chilioi -> chi, iota, lambda, iota, omicron, iota. 6 letters.
        # 2000: dischilioi (10)
        # General: "k thousands"
        if k == 1:
            parts_len += 6 # chilioi
        else:
            # adverbial multiplier? dis, tris...
            # Simplified: just use get_greek(k) + chilioi?
            # Or "duo chilioi". 
            # I'll add length of K and length of Chilioi (6).
            parts_len += get_greek_letter_count(k) + 6
            
        if rem > 0:
            parts_len += get_greek_letter_count(rem)
        return parts_len

    # 100-999
    if n >= 100:
        h = n // 100
        rem = n % 100
        parts_len += hundreds_len[h]
        if rem > 0:
            parts_len += 3 # "kai" (kappa-alpha-iota = 3 letters)
            parts_len += get_greek_letter_count(rem)
        return parts_len
        
    # 20-99
    if n >= 20:
        t = n // 10
        u = n % 10
        parts_len += tens_len[t]
        if u > 0:
            parts_len += 3 # "kai"
            parts_len += units_len[u]
        return parts_len
        
    # 0-19
    # 11-19 special
    # 11: endeka (6)
    # 12: dodeka (6)
    # 13: treiskaideka (3+3+4 = 10)
    # 14: tessareskaideka (8+3+4 = 15)
    # 15: pentekaideka (5+3+4 = 12)
    # 16: hekkaideka (ex + kai + deka = 2+3+4 = 9)
    # 17: heptakaideka (4+3+4 = 11)
    # 18: oktokaideka (4+3+4 = 11)
    # 19: enneakaideka (5+3+4 = 12)
    
    if n >= 11 and n <= 19:
        if n == 11: return 6
        if n == 12: return 6
        if n == 16: return 9
        # others are unit + kai + deka
        u = n - 10
        return units_len[u] + 3 + 4

    # 10
    if n == 10: return 4 # deka

    # 1-9
    return units_len[n]


# --- 3. Analysis Engine ---

def run_simulation(name, func, seed_limit=100, step_limit=1000000, unity_threshold=0.5):
    print(f"\nAnalyzing {name}...")
    print(f"Algorithm: n -> n + length_in_native_script(n)")
    print(f"Limits: {step_limit} steps, Stop at {unity_threshold:.0%} Unity")
    
    paths = {}
    main_trunk_set = set()
    
    # 1. Trace the Main Trunk (Seed 0) first
    curr = 0
    main_trunk_set.add(curr)
    steps = 0
    while steps < step_limit:
        l = func(curr)
        if l == 0 and curr != 0: break 
        curr += l
        main_trunk_set.add(curr)
        steps += 1
        
    # 2. Trace other seeds
    merged_count = 0
    total_seeds = seed_limit + 1 # 0 to 100
    
    # We already know 0 is in main trunk
    merged_count = 1 
    
    for seed in range(1, total_seeds):
        curr = seed
        steps = 0
        merged = False
        while steps < step_limit:
            if curr in main_trunk_set:
                merged = True
                break
            l = func(curr)
            curr += l
            steps += 1
            
        if merged:
            merged_count += 1
            
    unity = merged_count / total_seeds
    print(f"Unity (Convergence to Main Trunk): {unity:.2%} ({merged_count}/{total_seeds})")
    
    if unity >= unity_threshold:
        print(f"-> SUCCESS: Reached minimum unity of {unity_threshold:.0%}")
    else:
        print(f"-> RESULT: Remained fractured after {step_limit} calculations.")

if __name__ == "__main__":
    # Sumerian
    run_simulation("Sumerian (Cuneiform Signs)", get_sumerian_signs, step_limit=1000000)
    
    # Ancient Greek
    run_simulation("Ancient Greek (Native Letter Count)", get_greek_letter_count, step_limit=1000000)
