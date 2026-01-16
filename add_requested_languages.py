import os

# Definition of language data
languages_to_add = {
    "apiaka_of_tocantins.lang": {
        "name": "Apiaká of Tocantins",
        "data": {1: "masipe", 2: "mokõi", 3: "mopor", 4: "makumokoinyato"}
    },
    "arakaju.lang": {
        "name": "Arakajú",
        "data": {1: "unknown_1"} # Extinct, minimal data
    },
    "old_aramaic.lang": {
        "name": "Old Aramaic",
        # Imperial Aramaic script (Unicode 10840+)
        "data": {
            1: "\U00010847\U00010843", # ḥd
            2: "\U00010855\U00010852\U0001084A\U0001084E", # tryn
            3: "\U00010855\U0001084C\U00010855\U00010840", # tlta
            4: "\U00010840\U00010852\U00010841\U0001084F", # arba
            5: "\U00010847\U0001084D\U00010856", # hms
            10: "\U0001084F\U00010853\U00010852\U0001084A\U0001084E", # asra
            20: "\U0001084F\U00010853\U00010852\U0001084A\U0001084E", # esrin
            100: "\U0001084D\U00010840\U00010840" # maa
        }
    },
    "baenan.lang": {"name": "Baenan", "data": {1: "unknown_1"}},
    "boanari.lang": {"name": "Boanarí", "data": {1: "unknown_1"}},
    "cayuse.lang": {"name": "Cayuse", "data": {1: "na", 2: "lepli", 3: "matmni", 4: "piping", 5: "tawit"}},
    "corpus.lang": {"name": "Corpus", "data": {1: "unknown_1"}},
    "darkinjung.lang": {"name": "Darkinjung", "data": {1: "wakul", 2: "bularr", 3: "bularr-wakul"}},
    "kilit_dialect.lang": {"name": "Kilit dialect", "data": {1: "unknown_1"}},
    "leivu_dialect.lang": {"name": "Leivu dialect", "data": {1: "iks", 2: "kaks", 3: "kolm", 4: "nēļa", 5: "vīž"}}, # Livonian-like
    "manangkari.lang": {"name": "Manangkari", "data": {1: "unknown_1"}},
    "matanawi.lang": {"name": "Matanawi", "data": {1: "unknown_1"}},
    "morique.lang": {"name": "Morique", "data": {1: "unknown_1"}},
    "mucuchi_marripu.lang": {"name": "Mucuchí–Marripú", "data": {1: "unknown_1"}},
    "ngarla.lang": {"name": "Ngarla", "data": {1: "kujarra", 2: "kujarra-kujarra"}},
    "paleo_corsican.lang": {"name": "Paleo-Corsican", "data": {1: "unknown_1"}},
    "palmela.lang": {"name": "Palmela", "data": {1: "unknown_1"}},
    "paravilhana.lang": {"name": "Paravilhana", "data": {1: "unknown_1"}},
    "pimenteira.lang": {"name": "Pimenteira", "data": {1: "unknown_1"}},
    "querandi.lang": {"name": "Querandí", "data": {1: "unknown_1"}},
    "samaritan_aramaic.lang": {
        "name": "Samaritan Aramaic",
         # Samaritan script (Unicode 0800+)
        "data": {
             1: "\u0807\u0803\u0804", # Heda
             2: "\u0815\u0813\u0809\u080c", # Trim
             3: "\u0815\u080b\u0815", # Tlat
             4: "\u0800\u0813\u0801\u080f", # Arba
             5: "\u0807\u080c\u0814", # Hamesh
             10: "\u080e\u0812\u0813" # Asar
        }
    },
    "sapara.lang": {"name": "Sapará", "data": {1: "unknown_1"}},
    "sarghulami.lang": {"name": "Sarghulami", "data": {1: "unknown_1"}},
    "tehotitachsae.lang": {"name": "Tehotitachsae", "data": {1: "unknown_1"}},
    "tiverikoto.lang": {"name": "Tiverikoto", "data": {1: "unknown_1"}},
    "uru.lang": {"name": "Uru", "data": {1: "shi", 2: "piske", 3: "chep", 4: "pácpic", 5: "tacnu"}},
    "waikuri.lang": {"name": "Waikuri", "data": {1: "unknown_1"}},
    "wajumara.lang": {"name": "Wajumará", "data": {1: "unknown_1"}},
    "wakka_wakka.lang": {"name": "Wakka Wakka", "data": {1: "yumba", 2: "yabru", 3: "yabru yumba"}},
    "ware.lang": {"name": "Ware", "data": {1: "unknown_1"}},
    "yaruma.lang": {"name": "Yarumá", "data": {1: "unknown_1"}}
}

def write_lang_file(filename, info):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"name: {info['name']}\n")
        f.write("# Generated Language File\n\n")
        
        data = info['data']
        
        # Write special keys first
        special_keys = ["hundred", "ten_sep", "hundred_sep"]
        for key in special_keys:
            if key in data:
                f.write(f"{key}: {data[key]}\n")
        
        f.write("\n")
        
        # Filter integer keys and sort them
        int_keys = sorted([k for k in data.keys() if isinstance(k, int)])
        
        # Write numeric keys
        for key in int_keys:
            f.write(f"{key}: {data[key]}\n")

if __name__ == "__main__":
    count = 0
    for filename, info in languages_to_add.items():
        # Overwrite if exists to update with correct script if previously wrong
        write_lang_file(filename, info)
        print(f"Generated: {filename}")
        count += 1
    print(f"\nGenerated {count} new language files.")
