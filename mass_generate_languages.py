import os

languages = {
    "old_english.lang": {
        "name": "Old English",
        "data": {
            1: "ān", 2: "twā", 3: "þrēo", 4: "fēower", 5: "fīf", 6: "siex", 7: "seofon", 8: "eahta", 9: "nigon", 10: "tīen",
            11: "endleofan", 12: "twelf", 13: "þrēotīene", 14: "fēowertīene", 15: "fīftīene", 16: "siextīene", 17: "seofontīene", 18: "eahtatīene", 19: "nigontīene",
            20: "twentig", 30: "þrītig", 40: "fēowertig", 50: "fīftig", 60: "siextig", 70: "hundseofontig", 80: "hundeahtatig", 90: "hundnigontig",
            "hundred": "hundred", "ten_sep": " ond "
        }
    },
    "anglo_saxon.lang": {
        "name": "Anglo-Saxon",
        "data": {
            1: "ān", 2: "twēgen", 3: "þrīe", 4: "fēower", 5: "fīf", 6: "siex", 7: "seofon", 8: "eahta", 9: "nigon", 10: "tīen",
            20: "twentig", 30: "þrītig", 40: "fēowertig", 50: "fīftig", 60: "siextig", 100: "hund",
            "hundred": "hund", "ten_sep": " ond "
        }
    },
    "yiddish.lang": {
        "name": "Yiddish",
        "data": {
            0: "נול", 1: "אײנס", 2: "צװײ", 3: "דרײַ", 4: "פֿיר", 5: "פֿינף", 6: "זעקס", 7: "זיבן", 8: "אכט", 9: "נײַן", 10: "צען",
            11: "עלף", 12: "צוועלף", 20: "צוואַנציק", 30: "דרײַסיק", 40: "פערציק", 50: "פופציק", 60: "זעכציק", 70: "זיבעציק", 80: "אַכציק", 90: "נײַנציק",
            "hundred": "הונדערט", "ten_sep": " און "
        }
    },
    "afrikaans.lang": {
        "name": "Afrikaans",
        "data": {
            0: "nul", 1: "een", 2: "twee", 3: "drie", 4: "vier", 5: "vyf", 6: "ses", 7: "sewe", 8: "agt", 9: "nege", 10: "tien",
            20: "twintig", 30: "dertig", 40: "veertig", 50: "vyftig", 60: "sestig", 70: "sewentig", 80: "tagtig", 90: "negentig",
            "hundred": "honderd", "ten_sep": " en "
        }
    },
    "old_norse.lang": {
        "name": "Old Norse",
        "data": {
            1: "einn", 2: "tveir", 3: "þrír", 4: "fjórir", 5: "fimm", 6: "sex", 7: "sjau", 8: "átta", 9: "níu", 10: "tíu",
            11: "ellifu", 12: "tólf", 20: "tuttugu", 30: "þrír tigir", 40: "fjórir tigir", 50: "fimm tigir", 60: "sex tigir",
            "hundred": "tíu tigir", "ten_sep": " ok "
        }
    },
    "danish.lang": {
        "name": "Danish",
        "data": {
            0: "nul", 1: "en", 2: "to", 3: "tre", 4: "fire", 5: "fem", 6: "seks", 7: "syv", 8: "otte", 9: "ni", 10: "ti",
            20: "tyve", 30: "tredive", 40: "fyrre", 50: "halvtreds", 60: "tres", 70: "halvfjerds", 80: "firs", 90: "halvfems",
            "hundred": "hundrede", "ten_sep": "og"
        }
    },
    "swedish.lang": {
        "name": "Swedish",
        "data": {
            0: "noll", 1: "en", 2: "två", 3: "tre", 4: "fyra", 5: "fem", 6: "sex", 7: "sju", 8: "åtta", 9: "nio", 10: "tio",
            20: "tjugo", 30: "trettio", 40: "fyrtio", 50: "femtio", 60: "sextio", 70: "sjuttio", 80: "åttio", 90: "nittio",
            "hundred": "hundra", "ten_sep": ""
        }
    },
    "norwegian.lang": {
        "name": "Norwegian",
        "data": {
            0: "null", 1: "en", 2: "to", 3: "tre", 4: "fire", 5: "fem", 6: "seks", 7: "sju", 8: "åtte", 9: "ni", 10: "ti",
            20: "tjue", 30: "tretti", 40: "førti", 50: "femti", 60: "seksti", 70: "sytti", 80: "åtti", 90: "nitti",
            "hundred": "hundre", "ten_sep": ""
        }
    },
    "cymric.lang": {
        "name": "Cymric (Welsh)",
        "data": {
            0: "dim", 1: "un", 2: "dau", 3: "tri", 4: "pedwar", 5: "pump", 6: "chwech", 7: "saith", 8: "wyth", 9: "naw", 10: "deg",
            20: "ugain", 30: "deg ar hugain", 40: "deugain", 50: "hanner cant", 60: "trigain", 70: "deg a thrigain", 80: "pedwar ugain", 90: "deg a phedwar ugain",
            "hundred": "cant", "ten_sep": " a "
        }
    },
    "erse.lang": {
        "name": "Erse (Irish)",
        "data": {
            0: "náid", 1: "haon", 2: "dó", 3: "trí", 4: "ceathair", 5: "cúig", 6: "sé", 7: "seacht", 8: "hocht", 9: "naoi", 10: "deich",
            11: "haon déag", 20: "fiche", 30: "tríocha", 40: "daichead", 50: "caoga", 60: "seasca", 70: "seachtó", 80: "ochtó", 90: "nócha",
            "hundred": "céad", "ten_sep": " a "
        }
    },
    "gaelic.lang": {
        "name": "Gaelic (Scottish)",
        "data": {
            0: "neoni", 1: "aon", 2: "dhà", 3: "trì", 4: "ceithir", 5: "còig", 6: "sia", 7: "seachd", 8: "ochd", 9: "naoi", 10: "deich",
            20: "fichead", 30: "trithead", 40: "ceathrad", 50: "caogad", 60: "siagad", 70: "seachad", 80: "ochdad", 90: "naochad",
            "hundred": "ceud", "ten_sep": " air "
        }
    },
    "provencal.lang": {
        "name": "Provencal",
        "data": {
            0: "zèro", 1: "un", 2: "dos", 3: "tres", 4: "quatre", 5: "cinc", 6: "sièis", 7: "sèt", 8: "uèch", 9: "nòu", 10: "dètz",
            20: "vint", 30: "trenta", 40: "quaranta", 50: "cinquanta", 60: "seissanta", 70: "setanta", 80: "ochanta", 90: "nonanta",
            "hundred": "cent", "ten_sep": " e "
        }
    },
    "romanian.lang": {
        "name": "Romanian",
        "data": {
            0: "zero", 1: "unu", 2: "doi", 3: "trei", 4: "patru", 5: "cinci", 6: "șase", 7: "șapte", 8: "opt", 9: "nouă", 10: "zece",
            20: "douăzeci", 30: "treizeci", 40: "patruzeci", 50: "cincizeci", 60: "șaizeci", 70: "șaptezeci", 80: "optzeci", 90: "nouăzeci",
            "hundred": "sută", "ten_sep": " și "
        }
    },
    "attic_greek.lang": {
        "name": "Attic Greek",
        "data": {
            1: "εἷς", 2: "δύο", 3: "τρεῖς", 4: "τέτταρες", 5: "πέντε", 6: "ἕξ", 7: "ἑπτά", 8: "ὀκτώ", 9: "ἐννέα", 10: "δέκα",
            20: "εἴκοσι", 30: "τριάκοντα", 100: "ἑκατόν", "hundred": "ἑκατόν", "ten_sep": " καὶ "
        }
    },
    "ionic_greek.lang": {
        "name": "Ionic Greek",
        "data": {
            1: "εἷς", 2: "δύο", 3: "τρεῖς", 4: "τέσσερες", 5: "πέντε", 10: "δέκα",
            20: "εἴκοσι", 100: "ἑκατόν", "hundred": "ἑκατόν", "ten_sep": " καὶ "
        }
    },
    "doric_greek.lang": {
        "name": "Doric Greek",
        "data": {
            1: "εἷς", 2: "δύο", 3: "τρεῖς", 4: "τέτορες", 5: "πέντε", 10: "δέκα",
            20: "ϝείκατι", 100: "ἑκατόν", "hundred": "ἑκατόν", "ten_sep": " καὶ "
        }
    },
    "koine_greek.lang": {
        "name": "Koine Greek",
        "data": {
            1: "εἷς", 2: "δύο", 3: "τρεῖς", 4: "τέσσαρες", 5: "πέντε", 10: "δέκα",
            20: "εἴκοσι", 100: "ἑκατόν", "hundred": "ἑκατόν", "ten_sep": " καὶ "
        }
    },
    "belorussian.lang": {
        "name": "Belorussian",
        "data": {
            0: "нуль", 1: "адзін", 2: "два", 3: "тры", 4: "чатыры", 5: "пяць", 6: "шэсць", 7: "сем", 8: "восем", 9: "дзевяць", 10: "дзесяць",
            20: "дваццаць", 30: "трыццаць", 40: "сорак", 50: "пяцьдзесят", 60: "шэсцьдзесят", 70: "семдзесят", 80: "восемдзесят", 90: "дзевяноста",
            "hundred": "сто", "ten_sep": " "
        }
    },
    "ukrainian.lang": {
        "name": "Ukrainian",
        "data": {
            0: "нуль", 1: "один", 2: "два", 3: "три", 4: "чотири", 5: "п'ять", 6: "шість", 7: "сім", 8: "вісім", 9: "дев'ять", 10: "десять",
            20: "двадцять", 30: "тридцять", 40: "сорок", 50: "п'ятдесят", 60: "шістдесят", 70: "сімдесят", 80: "вісімдесят", 90: "дев'яносто",
            "hundred": "сто", "ten_sep": " "
        }
    },
    "polish.lang": {
        "name": "Polish",
        "data": {
            0: "zero", 1: "jeden", 2: "dwa", 3: "trzy", 4: "cztery", 5: "pięć", 6: "sześć", 7: "siedem", 8: "osiem", 9: "dziewięć", 10: "dziesięć",
            20: "dwadzieścia", 30: "trzydzieści", 40: "czterdzieści", 50: "pięćdziesiąt", 60: "sześćdziesiąt", 70: "siedemdziesiąt", 80: "osiemdziesiąt", 90: "dziewięćdziesiąt",
            "hundred": "sto", "ten_sep": " "
        }
    },
    "czech.lang": {
        "name": "Czech",
        "data": {
            0: "nula", 1: "jeden", 2: "dva", 3: "tři", 4: "čtyři", 5: "pět", 6: "šest", 7: "sedm", 8: "osm", 9: "devět", 10: "deset",
            20: "dvacet", 30: "třicet", 40: "čtyřicet", 50: "padesát", 60: "šedesát", 70: "sedmdesát", 80: "osmdesát", 90: "devadesát",
            "hundred": "sto", "ten_sep": " "
        }
    },
    "slovak.lang": {
        "name": "Slovak",
        "data": {
            0: "nula", 1: "jeden", 2: "dva", 3: "tri", 4: "štyri", 5: "päť", 6: "šest", 7: "sedem", 8: "osem", 9: "deväť", 10: "desať",
            20: "dvadsat", 30: "tridsat", 40: "štyridsat", 50: "päťdesiat", 60: "šestdesiat", 70: "sedemdesiat", 80: "osemdesiat", 90: "deväťdesiat",
            "hundred": "sto", "ten_sep": " "
        }
    },
    "slovenian.lang": {
        "name": "Slovenian",
        "data": {
            0: "nič", 1: "ena", 2: "dve", 3: "tri", 4: "štiri", 5: "pet", 6: "šest", 7: "sedem", 8: "osem", 9: "devet", 10: "deset",
            20: "dvajset", 30: "trideset", 40: "štirideset", 50: "petdeset", 60: "šestdeset", 70: "sedemdeset", 80: "osemdeset", 90: "devetdeset",
            "hundred": "sto", "ten_sep": " "
        }
    },
    "macedonian.lang": {
        "name": "Macedonian",
        "data": {
            0: "нула", 1: "еден", 2: "два", 3: "три", 4: "четири", 5: "пет", 6: "шест", 7: "седум", 8: "осум", 9: "девет", 10: "десет",
            20: "дваесет", 30: "триесет", 40: "четириесет", 50: "педесет", 60: "шеесет", 70: "седумдесет", 80: "осумдесет", 90: "деведесет",
            "hundred": "сто", "ten_sep": " "
        }
    },
    "serbo_croatian.lang": {
        "name": "Serbo-Croatian",
        "data": {
            0: "nula", 1: "jedan", 2: "dva", 3: "tri", 4: "četiri", 5: "pet", 6: "šest", 7: "sedam", 8: "osam", 9: "devet", 10: "deset",
            20: "dvadeset", 30: "trideset", 40: "četrdeset", 50: "pedeset", 60: "šezdeset", 70: "sedamdeset", 80: "osamdeset", 90: "devedeset",
            "hundred": "sto", "ten_sep": " "
        }
    },
    "bulgarian.lang": {
        "name": "Bulgarian",
        "data": {
            0: "нула", 1: "едно", 2: "две", 3: "три", 4: "четири", 5: "пет", 6: "шест", 7: "седем", 8: "осем", 9: "девет", 10: "десет",
            20: "двадесет", 30: "тридесет", 40: "четиридесет", 50: "петдесет", 60: "шестдесет", 70: "седемдесет", 80: "осемдесет", 90: "деветдесет",
            "hundred": "сто", "ten_sep": " "
        }
    },
    "lithuanian.lang": {
        "name": "Lithuanian",
        "data": {
            0: "nulis", 1: "vienas", 2: "du", 3: "trys", 4: "keturi", 5: "penki", 6: "šeši", 7: "septyni", 8: "aštuoni", 9: "devyni", 10: "dešimt",
            20: "dvidešimt", 30: "trisdešimt", 40: "keturiasdešimt", 50: "penkiasdešimt", 60: "šešiasdešimt", 70: "septyniasdešimt", 80: "aštuoniasdešimt", 90: "devyniasdešimt",
            "hundred": "šimtas", "ten_sep": " "
        }
    },
    "latvian.lang": {
        "name": "Latvian",
        "data": {
            0: "nulle", 1: "viens", 2: "divi", 3: "trīs", 4: "četri", 5: "pieci", 6: "seši", 7: "septiņi", 8: "astoņi", 9: "deviņi", 10: "desmit",
            20: "divdesmit", 30: "trīsdesmit", 40: "četrdesmit", 50: "piecdesmit", 60: "sešdesmit", 70: "septiņdesmit", 80: "astoņdesmit", 90: "deviņdesmit",
            "hundred": "simts", "ten_sep": " "
        }
    },
    "old_persian.lang": {
        "name": "Old Persian",
        "data": {
            1: "aiva", 2: "duva", 3: "thraya", 4: "chathwara", 5: "pancha", 6: "khshvash", 7: "hapta", 8: "ashta", 9: "nava", 10: "datha",
            20: "vithati", 100: "thahata", "hundred": "thahata", "ten_sep": " "
        }
    }
}

def write_lang_file(filename, info):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"name: {info['name']}\n")
        f.write("# Generated Language File\n\n")
        data = info['data']
        special_keys = ["hundred", "ten_sep", "hundred_sep"]
        for key in special_keys:
            if key in data:
                f.write(f"{key}: {data[key]}\n")
        f.write("\n")
        int_keys = sorted([k for k in data.keys() if isinstance(k, int)])
        for key in int_keys:
            f.write(f"{key}: {data[key]}\n")

if __name__ == "__main__":
    for filename, info in languages.items():
        write_lang_file(filename, info)
    print(f"Generated {len(languages)} language files.")
