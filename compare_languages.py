def get_english_name(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 0: return "zero"
    
    if n >= 100:
        h = n // 100
        rem = n % 100
        base = ones[h] + "hundred"
        if rem == 0: return base
        return base + get_english_name(rem)

    if n < 20: return ones[n]
    if n < 100: return tens[n // 10] + ones[n % 10]
    return ""

def get_spanish_name(n):
    if n == 0: return "cero"
    
    uniques = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
               "once", "doce", "trece", "catorce", "quince"]
    tens_prefix = ["", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
    hundreds = ["", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]

    if n == 100: return "cien"
    
    if n >= 100:
        h = n // 100
        rem = n % 100
        base = hundreds[h]
        if rem == 0: return base
        return base + get_spanish_name(rem)

    if n < 16: return uniques[n]
    if n < 20: return "dieci" + uniques[n-10]
    if n == 20: return "veinte"
    if n < 30: return "veinti" + uniques[n-20]
    
    t = n // 10
    o = n % 10
    base = tens_prefix[t]
    if o == 0: return base
    return base + "y" + uniques[o]

def get_german_name(n):
    if n == 0: return "null"
    
    ones = ["", "eins", "zwei", "drei", "vier", "fuenf", "sechs", "sieben", "acht", "neun", "zehn",
            "elf", "zwoelf"]
    tens_names = ["", "", "zwanzig", "dreissig", "vierzig", "fuenfzig", "sechzig", "siebzig", "achtzig", "neunzig"]
    
    if n >= 100:
        h = n // 100
        rem = n % 100
        base = ones[h] + "hundert"
        if h == 1: base = "einhundert"
        if rem == 0: return base
        return base + get_german_name(rem)

    if n < 13: return ones[n]
    if n < 20:
        base = ones[n % 10]
        if n == 16: base = "sech"
        if n == 17: base = "sieb"
        return base + "zehn"
    
    t = n // 10
    o = n % 10
    if o == 0: return tens_names[t]
    
    one_str = ones[o]
    if o == 1: one_str = "ein"
    return one_str + "und" + tens_names[t]

def get_french_name(n):
    if n == 0: return "zero"
    
    ones = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix",
            "onze", "douze", "treize", "quatorze", "quinze", "seize"]
    tens_map = {
        10: "dix", 20: "vingt", 30: "trente", 40: "quarante", 50: "cinquante", 
        60: "soixante", 70: "soixantedix", 80: "quatrevingts", 90: "quatrevingtdix"
    }

    if n >= 100:
        h = n // 100
        rem = n % 100
        if h == 1: base = "cent"
        else: base = ones[h] + "cent" 
        if rem == 0: return base
        return base + get_french_name(rem)
    
    if n < 17: return ones[n]
    if n < 20: return "dix" + ones[n-10]
    
    t = (n // 10) * 10
    rem = n % 10
    
    if t == 70:
        base = "soixante"
        rem = n - 60
    elif t == 90:
        base = "quatrevingt"
        rem = n - 80
    else:
        base = tens_map[t]
    
    if rem == 0: return base
    
    if (n % 10 == 1 and n < 70) or n == 71:
        return base + "et" + get_french_name(rem)
    
    if rem < 17: suffix = ones[rem]
    else: suffix = "dix" + ones[rem-10]
    
    return base + suffix

def analyze_language(lang_name, func):
    # Track "Rivers"
    paths = {}
    
    # Analyze 0-100
    for start in range(101):
        path = []
        curr = start
        while curr < 800: # Go high enough to let them merge
            path.append(curr)
            name = func(curr)
            length = len(name.replace(" ", "").replace("-", ""))
            curr = curr + length
        paths[start] = path

    # Group by destination (River)
    groups = {} 
    unique_rivers = []
    
    for start in range(101):
        my_path = paths[start]
        my_tail = my_path[-5:] # Identify river by its tail
        
        found_river = False
        for river_id, river_tail in enumerate(unique_rivers):
            if my_tail == river_tail:
                if river_id not in groups: groups[river_id] = []
                groups[river_id].append(start)
                found_river = True
                break
        
        if not found_river:
            unique_rivers.append(my_tail)
            river_id = len(unique_rivers) - 1
            groups[river_id] = [start]

    print("--------------------------------------------------")
    print(f"LANGUAGE: {lang_name}")
    print(f"Structure: {len(unique_rivers)} Distinct River(s) found for 0-100")
    
    # Sort groups by size (largest river first)
    sorted_groups = sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
    
    for i, (rid, members) in enumerate(sorted_groups):
        count = len(members)
        percent = count
        tail_preview = str(unique_rivers[rid][-3:])
        print(f"  River #{i+1}: {count}% of numbers (Ends in ...{tail_preview})")
        
        if i == 0:
            print(f"     -> The 'Main Trunk' (Includes {members[:10]}...)")
        else:
            print(f"     -> Tributary (Includes {members})")

print("analyzing...")
analyze_language("ENGLISH", get_english_name)
analyze_language("SPANISH", get_spanish_name)
analyze_language("GERMAN", get_german_name)
analyze_language("FRENCH", get_french_name)