
def get_sumerian_len(n):
    # Sumerian (Base 60, but we trace 0-100 using standard notation)
    # 1: dis, 2: min, 3: es, 4: limmu, 5: ia, 6: as, 7: imin, 8: ussu, 9: ilimmu, 10: u
    # 20: nis, 30: usu, 40: nimin, 50: ninnu, 60: gis
    
    if n == 0: return 0 # Concept didn't exist in same way, return 0 length (stop)
    
    units = ["", "dis", "min", "es", "limmu", "ia", "as", "imin", "ussu", "ilimmu"]
    tens = ["", "u", "nis", "usu", "nimin", "ninnu", "gis", "gis-u", "gis-nis", "gis-usu"] # 10, 20... 90 (approx)

    if n < 10: return len(units[n])
    
    if n < 60:
        t = n // 10
        u = n % 10
        base = tens[t]
        if u == 0: return len(base)
        return len(base + units[u]) # e.g. u-dis
        
    if n >= 60:
        # 60 is 'gis'
        # 61 is 'gis dis'
        # 70 is 'gis u'
        val = n - 60
        base = "gis"
        if val == 0: return len(base)
        # recursive simple
        return len(base) + get_sumerian_len(val)

def get_egyptian_len(n):
    # Middle Egyptian Transliteration (approx)
    # 1: wa, 2: senu, 3: khemet, 4: fedu, 5: diu, 6: sisu, 7: sefekh, 8: khemenu, 9: pesdj, 10: medju
    
    if n == 0: return 3 # 'nfr' (zero/completion)
    
    units = ["", "wa", "senu", "khemet", "fedu", "diu", "sisu", "sefekh", "khemenu", "pesdj"]
    tens = ["", "medju", "djewati", "maba", "hem", "diiu", "sisu", "sefekhu", "khemenu", "pesdju"] # Approx reconstruction
    
    if n < 10: return len(units[n])
    if n < 100:
        t = n // 10
        u = n % 10
        base = tens[t]
        if u == 0: return len(base)
        return len(base + units[u])
    return 3 # 'shet' (100)

def get_greek_len(n):
    # Ancient Greek
    if n == 0: return 5 # ouden
    
    units = ["", "heis", "duo", "treis", "tettares", "pente", "hex", "hepta", "okto", "ennea"]
    tens = ["", "deka", "eikosi", "triakonta", "tessarakonta", "pentekonta", "hexakonta", "hebdomekonta", "ogdoekonta", "enenekonta"]
    
    if n < 10: return len(units[n])
    
    if n < 20: # 11-19: endeka, dodeka...
        if n == 11: return 6 # endeka
        if n == 12: return 6 # dodeka
        return len(units[n-10] + "kai" + "deka") # simplified composite
        
    if n < 100:
        t = n // 10
        u = n % 10
        base = tens[t]
        if u == 0: return len(base)
        return len(base + "kai" + units[u]) # eikosi kai duo
        
    return 7 # hekaton

def get_aramaic_len(n):
    # Syriac/Aramaic
    if n == 0: return 4 # sfer
    
    units = ["", "khad", "trein", "tlata", "arba", "khamsha", "lshta", "shva", "tmanya", "tish"]
    tens = ["", "asar", "esrin", "tlatin", "arbain", "khamshin", "ishtin", "shvin", "tmanin", "tishin"]
    
    if n < 10: return len(units[n])
    if n < 20: return len("khad" + "asar") # approx teens
    
    if n < 100:
        t = n // 10
        u = n % 10
        base = tens[t]
        if u == 0: return len(base)
        return len(base + "w" + units[u]) # Esrin w khad
    return 4 # mwa

def get_quechua_len(n):
    # Inca
    if n == 0: return 3 # chusaq
    
    units = ["", "huk", "iskay", "kimsa", "tawa", "pichqa", "suqta", "qanchis", "pusaq", "isqun"]
    
    if n < 10: return len(units[n])
    if n == 10: return 6 # chunka
    
    if n < 100:
        t = n // 10
        u = n % 10
        # 11: chunka hukniyuq
        # 20: iskay chunka
        # 21: iskay chunka hukniyuq
        
        base_ten = "chunka"
        if t > 1: base_ten = units[t] + "chunka"
        
        if u == 0: return len(base_ten)
        return len(base_ten + units[u] + "niyuq")
        
    return 5 # pachak

def get_aymara_len(n):
    # Lake Titicaca
    if n == 0: return 4 # ch'usa
    
    units = ["", "maya", "paya", "kimsa", "pusi", "phisqa", "suxta", "paqallqu", "kimsaqallqu", "llatunka"]
    
    if n < 10: return len(units[n])
    if n == 10: return 5 # tunka
    
    if n < 100:
        t = n // 10
        u = n % 10
        
        base_ten = "tunka"
        if t > 1: base_ten = units[t] + "tunka"
        
        if u == 0: return len(base_ten)
        return len(base_ten + units[u] + "ni") # tunka mayani
        
    return 5 # pataka

def analyze(name, func):
    rivers = []
    groups = {}
    
    for start in range(101):
        path = []
        curr = start
        while curr < 300:
            path.append(curr)
            l = func(curr)
            if l == 0: break # stop
            curr = curr + l
            
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
        print(f"  River: {len(mems)}% ends in {rivers[rid][-3:]}")
    print("-" * 30)

print("--- ANCIENT & INDIGENOUS ANALYSIS ---")
analyze("SUMERIAN (First Writing)", get_sumerian_len)
analyze("ANCIENT EGYPTIAN", get_egyptian_len)
analyze("ANCIENT GREEK", get_greek_len)
analyze("ARAMAIC (Language of Jesus)", get_aramaic_len)
analyze("QUECHUA (Inca)", get_quechua_len)
analyze("AYMARA (Lake Titicaca)", get_aymara_len)
