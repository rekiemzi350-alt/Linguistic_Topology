
def get_mandarin_len(n):
    # Characters: 
    # 0: 零 (1)
    # 1-10: 一 二 三 四 五 六 七 八 九 十 (1 char each)
    # 11-19: 十一 (2 chars)
    # 20: 二十 (2 chars)
    # 21: 二十一 (3 chars)
    # 100: 一百 (2 chars)
    
    if n == 0: return 1 # 零
    if n == 100: return 2 # 一百
    if n > 100: 
        # Simplified logic for >100 to catch trends
        # 101: 一百零一 (4)
        # 111: 一百一十一 (5)
        # 200: 二百 (2)
        base = 2 # X hundred
        rem = n % 100
        if rem == 0: return base
        if rem < 10: return base + 2 # ling X
        return base + get_mandarin_len(rem) # simple append

    if n <= 10: return 1
    if n < 20: return 2 # 11-19 (Shi-Yi)
    if n % 10 == 0: return 2 # 20, 30... (Er-Shi)
    return 3 # 21-99 (Er-Shi-Yi)

def get_arabic_len(n):
    # Approximate length of Arabic script representation (Letters)
    # 0: صفر (3)
    # 1: واحد (4)
    # 2: اثنان (5)
    # 3: ثلاثة (5)
    # 4: أربعة (5)
    # 5: خمسة (4)
    # 6: ستة (3)
    # 7: سبعة (4)
    # 8: ثمانية (6)
    # 9: تسعة (4)
    # 10: عشرة (4)
    
    units = [0, 4, 5, 5, 5, 4, 3, 4, 6, 4] # 1-9
    
    if n == 0: return 3
    if n < 10: return units[n]
    if n == 10: return 4
    
    # 11-19: ahad ashar (approx 3+3=6 to 5+3=8)
    # simple approx: unit + 3 ('ashar')
    if n < 20:
        u = n % 10
        if u == 1: return 7 # ahada 'ashar
        if u == 2: return 8 # ithna 'ashar
        return units[u] + 3
        
    # Tens: 20 (ishrun - 5), 30 (thalathun - 6), 40 (arba'un - 6)...
    tens_len = [0, 0, 5, 6, 6, 6, 4, 5, 6, 5] 
    
    if n < 100:
        t = n // 10
        u = n % 10
        if u == 0: return tens_len[t]
        # "Wahid wa ishrun" -> Unit + 1 (wa) + Ten
        return units[u] + 1 + tens_len[t]
        
    return 5 # "Miah" (100) approx

def analyze_language(lang_name, len_func):
    paths = {}
    
    # Run 0-100
    for start in range(101):
        path = []
        curr = start
        while curr < 300: # Limit
            path.append(curr)
            length = len_func(curr)
            curr = curr + length
        paths[start] = path

    # Group
    unique_rivers = []
    groups = {}
    
    for start in range(101):
        my_path = paths[start]
        my_tail = my_path[-5:]
        
        found = False
        for rid, rtail in enumerate(unique_rivers):
            if my_tail == rtail:
                if rid not in groups: groups[rid] = []
                groups[rid].append(start)
                found = True
                break
        if not found:
            unique_rivers.append(my_tail)
            groups[len(unique_rivers)-1] = [start]

    print(f"LANGUAGE: {lang_name}")
    print(f"Distinct Rivers: {len(unique_rivers)}")
    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
    for rid, members in sorted_groups:
        count = len(members)
        print(f"  River: {count}% of numbers. Ends in... {unique_rivers[rid][-5:]}")
    print("-" * 40)

print("--- EASTERN LANGUAGE ANALYSIS ---")
analyze_language("MANDARIN (Characters)", get_mandarin_len)
analyze_language("ARABIC (Approx Script)", get_arabic_len)
