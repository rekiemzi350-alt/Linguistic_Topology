import os

# Define basic number names for common languages for placeholder generation
# This is simplified and primarily for ensuring the script runs without KeyError.
# Actual, accurate language files should replace these placeholders for precise results.

LANG_TEMPLATES = {
    "german": {
        "name": "German",
        "rules": {
            0: "null", 1: "eins", 2: "zwei", 3: "drei", 4: "vier", 5: "fuenf",
            6: "sechs", 7: "sieben", 8: "acht", 9: "neun", 10: "zehn",
            11: "elf", 12: "zwoelf", 20: "zwanzig", 30: "dreissig", 40: "vierzig",
            50: "fuenfzig", 60: "sechzig", 70: "siebzig", 80: "achtzig", 90: "neunzig",
            100: "einhundert", "hundred": "hundert",
            1000: "eintausend", "thousand": "tausend",
            1000000: "eine million", "million": "million",
            "ten_sep": "", "hundred_sep": ""
        }
    },
    "polish": {
        "name": "Polish",
        "rules": {
            0: "zero", 1: "jeden", 2: "dwa", 3: "trzy", 4: "cztery", 5: "piec",
            6: "szesc", 7: "siedem", 8: "osiem", 9: "dziewiec", 10: "dziesiec",
            11: "jedenascie", 12: "dwanascie", 20: "dwadziescia", 30: "trzydziesci",
            40: "czterdziesci", 50: "piecdziesiat", 60: "szescdziesiat",
            70: "siedemdziesiat", 80: "osiemdziesiat", 90: "dziewiecdziesiat",
            100: "sto", "hundred": "sto",
            1000: "tysiac", "thousand": "tysiac",
            1000000: "milion", "million": "milion",
            "ten_sep": "", "hundred_sep": ""
        }
    },
    "french": {
        "name": "French",
        "rules": {
            0: "zero", 1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq",
            6: "six", 7: "sept", 8: "huit", 9: "neuf", 10: "dix",
            11: "onze", 12: "douze", 20: "vingt", 30: "trente", 40: "quarante",
            50: "cinquante", 60: "soixante", 70: "soixante-dix", 80: "quatre-vingts",
            90: "quatre-vingt-dix",
            100: "cent", "hundred": "cent",
            1000: "mille", "thousand": "mille",
            1000000: "million", "million": "million",
            "ten_sep": "-", "hundred_sep": " "
        }
    },
    "italian": {
        "name": "Italian",
        "rules": {
            0: "zero", 1: "uno", 2: "due", 3: "tre", 4: "quattro", 5: "cinque",
            6: "sei", 7: "sette", 8: "otto", 9: "nove", 10: "dieci",
            11: "undici", 12: "dodici", 20: "venti", 30: "trenta", 40: "quaranta",
            50: "cinquanta", 60: "sessanta", 70: "settanta", 80: "ottanta", 90: "novanta",
            100: "cento", "hundred": "cento",
            1000: "mille", "thousand": "mille",
            1000000: "milione", "million": "milione",
            "ten_sep": "", "hundred_sep": ""
        }
    },
    "russian": {
        "name": "Russian",
        "rules": {
            0: "nol", 1: "odin", 2: "dva", 3: "tri", 4: "chetyre", 5: "pyat",
            6: "shest", 7: "sem", 8: "vosem", 9: "devyat", 10: "desyat",
            11: "odinnadtsat", 12: "dvenadtsat", 20: "dvadtsat", 30: "tridtsat",
            40: "sorok", 50: "pyatdesyat", 60: "shestdyesyat", 70: "semdesyat",
            80: "vosemdesyat", 90: "devyanosto",
            100: "sto", "hundred": "sto",
            1000: "tysyacha", "thousand": "tysyacha",
            1000000: "million", "million": "million",
            "ten_sep": "", "hundred_sep": ""
        }
    },
    "czech": {
        "name": "Czech",
        "rules": {
            0: "nula", 1: "jeden", 2: "dva", 3: "tri", 4: "ctyri", 5: "pet",
            6: "sest", 7: "sedm", 8: "osm", 9: "devet", 10: "deset",
            11: "jedenact", 12: "dvanact", 20: "dvacet", 30: "tricet",
            40: "ctyricet", 50: "padesat", 60: "sedesat", 70: "sedmdesat",
            80: "osmdesat", 90: "devadesat",
            100: "sto", "hundred": "sto",
            1000: "tisic", "thousand": "tisic",
            1000000: "milion", "million": "milion",
            "ten_sep": "", "hundred_sep": ""
        }
    },
    "finnish": {
        "name": "Finnish",
        "rules": {
            0: "nolla", 1: "yksi", 2: "kaksi", 3: "kolme", 4: "nelja", 5: "viisi",
            6: "kuusi", 7: "seitseman", 8: "kahdeksan", 9: "yhdeksan", 10: "kymmenen",
            11: "yksitoista", 12: "kaksitoista", 20: "kaksikymmenta", 30: "kolmekymmenta",
            40: "neljakymmenta", 50: "viisikymmenta", 60: "kuusikymmenta",
            70: "seitsemankymmenta", 80: "kahdeksankymmenta", 90: "yhdeksankymmenta",
            100: "sata", "hundred": "sata",
            1000: "tuhat", "thousand": "tuhat",
            1000000: "miljoona", "million": "miljoona",
            "ten_sep": "", "hundred_sep": ""
        }
    },
    "hungarian": {
        "name": "Hungarian",
        "rules": {
            0: "nulla", 1: "egy", 2: "ketto", 3: "harom", 4: "negy", 5: "ot",
            6: "hat", 7: "het", 8: "nyolc", 9: "kilenc", 10: "tiz",
            11: "tizenegy", 12: "tizenketto", 20: "husz", 30: "harminc",
            40: "negyven", 50: "otven", 60: "hatvan", 70: "hetven",
            80: "nyolcvan", 90: "kilencven",
            100: "szaz", "hundred": "szaz",
            1000: "ezer", "thousand": "ezer",
            1000000: "millio", "million": "millio",
            "ten_sep": "", "hundred_sep": ""
        }
    },
}

def create_or_update_lang_file(lang_code, template):
    filepath = f"{lang_code}.lang"
    current_rules = {}

    # Read existing rules if file exists
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if ":" in line and not line.startswith('#'):
                    key, val = line.split(":", 1)
                    current_rules[key.strip()] = val.strip()

    # Apply template, prioritizing existing rules
    final_rules = {**template["rules"], **current_rules}
    
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(f"name: {template['name']}\n")
        
        # Write direct number names
        sorted_direct_keys = sorted([k for k in final_rules if isinstance(k, int)])
        for num in sorted_direct_keys:
            f.write(f"{num}: {final_rules[num]}\n")
        
        # Write other rules
        for key in ["hundred", "thousand", "million", "ten_sep", "hundred_sep"]:
            if key in final_rules:
                f.write(f"{key}: {final_rules[key]}\n")
    print(f"Created/Updated {filepath}")

if __name__ == "__main__":
    for lang_code, template in LANG_TEMPLATES.items():
        create_or_update_lang_file(lang_code, template)
    
    # Ensure our specific English and Dutch files also have thousand/million
    # Read existing english_us.lang
    with open("english_us.lang", 'r', encoding='utf-8') as f:
        us_content = f.read()
    if "thousand:" not in us_content:
        us_content += "\nthousand: thousand\n"
    if "million:" not in us_content:
        us_content += "million: million\n"
    with open("english_us.lang", 'w', encoding='utf-8') as f:
        f.write(us_content)
    print("Updated english_us.lang with thousand/million")

    # Read existing english_uk.lang
    with open("english_uk.lang", 'r', encoding='utf-8') as f:
        uk_content = f.read()
    if "thousand:" not in uk_content:
        uk_content += "\nthousand: thousand\n"
    if "million:" not in uk_content:
        uk_content += "million: million\n"
    with open("english_uk.lang", 'w', encoding='utf-8') as f:
        f.write(uk_content)
    print("Updated english_uk.lang with thousand/million")

    # Read existing dutch_hist.lang
    with open("dutch_hist.lang", 'r', encoding='utf-8') as f:
        nl_content = f.read()
    if "thousand:" not in nl_content:
        nl_content += "\nthousand: duizend\n"
    if "million:" not in nl_content:
        nl_content += "million: miljoen\n"
    with open("dutch_hist.lang", 'w', encoding='utf-8') as f:
        f.write(nl_content)
    print("Updated dutch_hist.lang with thousand/million")
