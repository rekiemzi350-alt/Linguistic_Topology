
def get_navajo_len(n):
    # Navajo (Diné) Number System
    # Counts distinct letters (unicode chars).
    # Glottal stop (ʼ) counts as a letter.
    # Diacritics are part of the letter (precomposed) or ignored if counting bytes, 
    # but python len() on unicode string counts 1 char per visual glyph usually.
    
    # Basic Units (1-9)
    # 0: ádin
    # 1: tʼááłáʼí
    # 2: naaki
    # 3: tááʼ
    # 4: dį́į́ʼ
    # 5: ashdlaʼ
    # 6: hastą́ą́
    # 7: tsostsʼid
    # 8: tseebíí
    # 9: náhástʼéí
    # 10: neeznáá

    units = ["", "tʼááłáʼí", "naaki", "tááʼ", "dį́į́ʼ", "ashdlaʼ", "hastą́ą́", "tsostsʼid", "tseebíí", "náhástʼéí"]
    
    if n == 0: return 4 # ádin
    if n < 10: return len(units[n])
    
    # Teens (11-19)
    # Suffix: -tsʼáadah
    # 11: łaʼtsʼáadah (Special 'one')
    if n == 11: return len("łaʼtsʼáadah")
    if n < 20:
        base = units[n % 10]
        # Some slight spelling changes exist in dialects, but we stick to standard additive for approx
        return len(base + "tsʼáadah")

    # Tens (20-90)
    # 20: naadiin
    # 30: tádiin
    # 40: dízdiin
    # 50: ashdladiin
    # 60: hastą́ądiin
    # 70: tsostsʼidiin
    # 80: tseebíidiin
    # 90: náhástʼéidiin
    
    tens_map = {
        2: "naadiin",
        3: "tádiin",
        4: "dízdiin",
        5: "ashdladiin",
        6: "hastą́ądiin",
        7: "tsostsʼidiin",
        8: "tseebíidiin",
        9: "náhástʼéidiin"
    }

    if n == 100: return len("neeznáádiin") # or tʼááłáʼídi neeznáadiin

    if n < 100:
        t = n // 10
        u = n % 10
        
        base = tens_map[t]
        
        if u == 0: return len(base)
        
        # Compound: Tens + Unit
        # e.g., 21: naadiin tʼááłáʼí
        return len(base + units[u])
        
    return 11 # Default fallback for >100 (neeznáádiin)

def analyze(name, func):
    rivers = []
    groups = {}

    for start in range(101):
        path = []
        curr = start
        while curr < 600: # Navajo grows FAST, need higher ceiling
            path.append(curr)
            l = func(curr)
            curr = curr + l
        
        # Identify by tail
        tail = path[-5:]
        found = False
        for i, r in enumerate(rivers):
            if tail == r:
                if i not in groups: groups[i] = []
                groups[i].append(start)
                found = True
                break
        if not found:
            rivers.append(tail)
            groups[len(rivers)-1] = [start]

    print(f"LANGUAGE: {name}")
    print(f"Distinct Rivers: {len(rivers)}")
    
    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
    
    for rid, mems in sorted_groups:
        count = len(mems)
        pct = (count / 101) * 100
        print(f"  River: {int(pct)}% of numbers. Ends in... {rivers[rid][-3:]}")
    print("-" * 30)

print("--- CODE TALKER ANALYSIS ---")
analyze("NAVAJO (Diné)", get_navajo_len)
