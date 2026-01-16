import os

# Definition of language data
languages = {
    # --- Modern Languages ---
    "english.lang": {
        "name": "English",
        "data": {
            0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
            11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
            16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
            20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
            60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety",
            "hundred": "hundred",
            "ten_sep": "-",
            "hundred_sep": " and "
        }
    },
    "spanish.lang": {
        "name": "Spanish",
        "data": {
            0: "cero", 1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco",
            6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez",
            11: "once", 12: "doce", 13: "trece", 14: "catorce", 15: "quince",
            16: "dieciseis", 17: "diecisiete", 18: "dieciocho", 19: "diecinueve",
            20: "veinte", 21: "veintiuno", 22: "veintidos", 23: "veintitres", 
            24: "veinticuatro", 25: "veinticinco", 26: "veintiseis", 27: "veintisiete", 
            28: "veintiocho", 29: "veintinueve",
            30: "treinta", 40: "cuarenta", 50: "cincuenta",
            60: "sesenta", 70: "setenta", 80: "ochenta", 90: "noventa",
            "hundred": "cien", 
            100: "cien",
            "ten_sep": " y ",
            "hundred_sep": "to " 
        }
    },
    "french.lang": {
        "name": "French",
        "data": {
            0: "zero", 1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq",
            6: "six", 7: "sept", 8: "huit", 9: "neuf", 10: "dix",
            11: "onze", 12: "douze", 13: "treize", 14: "quatorze", 15: "quinze",
            16: "seize", 17: "dix-sept", 18: "dix-huit", 19: "dix-neuf",
            20: "vingt", 30: "trente", 40: "quarante", 50: "cinquante",
            60: "soixante", 70: "soixante-dix", 80: "quatre-vingts", 90: "quatre-vingt-dix",
            "hundred": "cent",
            "ten_sep": "-",
            "hundred_sep": " "
        }
    },
    "german.lang": {
        "name": "German",
        "data": {
            0: "null", 1: "eins", 2: "zwei", 3: "drei", 4: "vier", 5: "funf",
            6: "sechs", 7: "sieben", 8: "acht", 9: "neun", 10: "zehn",
            11: "elf", 12: "zwolf", 13: "dreizehn", 14: "vierzehn", 15: "funfzehn",
            16: "sechzehn", 17: "siebzehn", 18: "achtzehn", 19: "neunzehn",
            20: "zwanzig", 30: "dreissig", 40: "vierzig", 50: "funfzig",
            60: "sechzig", 70: "siebzig", 80: "achtzig", 90: "neunzig",
            "hundred": "hundert",
            "ten_sep": "und", 
            "hundred_sep": ""
        }
    },
    "italian.lang": {
        "name": "Italian",
        "data": {
            0: "zero", 1: "uno", 2: "due", 3: "tre", 4: "quattro", 5: "cinque",
            6: "sei", 7: "sette", 8: "otto", 9: "nove", 10: "dieci",
            11: "undici", 12: "dodici", 13: "tredici", 14: "quattordici", 15: "quindici",
            16: "sedici", 17: "diciassette", 18: "diciotto", 19: "diciannove",
            20: "venti", 30: "trenta", 40: "quaranta", 50: "cinquanta",
            60: "sessanta", 70: "settanta", 80: "ottanta", 90: "novanta",
            "hundred": "cento",
            "ten_sep": "",
            "hundred_sep": ""
        }
    },
    "portuguese.lang": {
        "name": "Portuguese",
        "data": {
            0: "zero", 1: "um", 2: "dois", 3: "tres", 4: "quatro", 5: "cinco",
            6: "seis", 7: "sete", 8: "oito", 9: "nove", 10: "dez",
            11: "onze", 12: "doze", 13: "treze", 14: "catorze", 15: "quinze",
            16: "dezasseis", 17: "dezassete", 18: "dezoito", 19: "dezanove",
            20: "vinte", 30: "trinta", 40: "quarenta", 50: "cinquenta",
            60: "sessenta", 70: "setenta", 80: "oitenta", 90: "noventa",
            "hundred": "cem",
            100: "cem",
            "ten_sep": " e ",
            "hundred_sep": " e "
        }
    },
    "russian.lang": {
        "name": "Russian",
        "data": {
            0: "ноль", 1: "один", 2: "два", 3: "три", 4: "четыре", 5: "пять",
            6: "шесть", 7: "семь", 8: "восемь", 9: "девять", 10: "десять",
            11: "одиннадцать", 12: "двенадцать", 13: "тринадцать", 14: "четырнадцать", 15: "пятнадцать",
            16: "шестнадцать", 17: "семнадцать", 18: "восемнадцать", 19: "девятнадцать",
            20: "двадцать", 30: "тридцать", 40: "сорок", 50: "пятьдесят",
            60: "шестьдесят", 70: "семьдесят", 80: "восемьдесят", 90: "девяносто",
            "hundred": "сто",
            "ten_sep": " ",
            "hundred_sep": " "
        }
    },
    "chinese_simplified.lang": {
        "name": "Chinese (Mandarin)",
        "data": {
            0: "零", 1: "一", 2: "二", 3: "三", 4: "四", 5: "五",
            6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
            11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五",
            16: "十六", 17: "十七", 18: "十八", 19: "十九",
            20: "二十", 30: "三十", 40: "四十", 50: "五十",
            60: "六十", 70: "七十", 80: "八十", 90: "九十",
            "hundred": "百",
            "ten_sep": "",
            "hundred_sep": ""
        }
    },
    "japanese.lang": {
        "name": "Japanese",
        "data": {
            0: "零", 1: "一", 2: "二", 3: "三", 4: "四", 5: "五",
            6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
            11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五",
            16: "十六", 17: "十七", 18: "十八", 19: "十九",
            20: "二十", 30: "三十", 40: "四十", 50: "五十",
            60: "六十", 70: "七十", 80: "八十", 90: "九十",
            "hundred": "百",
            "ten_sep": "",
            "hundred_sep": ""
        }
    },
    "korean.lang": {
        "name": "Korean (Sino)",
        "data": {
            0: "영", 1: "일", 2: "이", 3: "삼", 4: "사", 5: "오",
            6: "육", 7: "칠", 8: "팔", 9: "구", 10: "십",
            11: "십일", 12: "십이", 13: "십삼", 14: "십사", 15: "십오",
            16: "십육", 17: "십칠", 18: "십팔", 19: "십구",
            20: "이십", 30: "삼십", 40: "사십", 50: "오십",
            60: "육십", 70: "칠십", 80: "팔십", 90: "구십",
            "hundred": "백",
            "ten_sep": "",
            "hundred_sep": ""
        }
    },
    "arabic.lang": {
        "name": "Arabic",
        "data": {
            0: "صفر", 1: "واحد", 2: "اثنان", 3: "ثلاثة", 4: "أربعة", 5: "خمسة",
            6: "ستة", 7: "سبعة", 8: "ثمانية", 9: "تسعة", 10: "عشرة",
            11: "أحد عشر", 12: "اثنا عشر", 13: "ثلاثة عشر", 14: "أربعة عشر", 15: "خمسة عشر",
            16: "ستة عشر", 17: "سبعة عشر", 18: "ثمانية عشر", 19: "تسعة عشر",
            20: "عشرون", 30: "ثلاثون", 40: "أربعون", 50: "خمسون",
            60: "ستون", 70: "سبعون", 80: "ثمانون", 90: "تسعون",
            "hundred": "مائة",
            "ten_sep": "و", 
            "hundred_sep": " و "
        }
    },
    "hindi.lang": {
        "name": "Hindi",
        "data": {
            0: "शून्य", 1: "एक", 2: "दो", 3: "तीन", 4: "चार", 5: "पाँच",
            6: "छह", 7: "सात", 8: "आठ", 9: "नौ", 10: "दस",
            11: "ग्यारह", 12: "बारह", 13: "तेरह", 14: "चौदह", 15: "पंद्रह",
            16: "सोलह", 17: "सत्रह", 18: "अठारह", 19: "उन्नीस",
            20: "बीस", 30: "तीस", 40: "चालीस", 50: "पचास",
            60: "साठ", 70: "सत्तर", 80: "अस्सी", 90: "नब्बे",
            "hundred": "सौ",
            "ten_sep": " ",
            "hundred_sep": " "
        }
    },
    "turkish.lang": {
        "name": "Turkish",
        "data": {
            0: "sifir", 1: "bir", 2: "iki", 3: "uc", 4: "dort", 5: "bes",
            6: "alti", 7: "yedi", 8: "sekiz", 9: "dokuz", 10: "on",
            11: "on bir", 12: "on iki", 13: "on uc", 14: "on dort", 15: "on bes",
            16: "on alti", 17: "on yedi", 18: "on sekiz", 19: "on dokuz",
            20: "yirmi", 30: "otuz", 40: "kirk", 50: "elli",
            60: "altmis", 70: "yetmis", 80: "seksen", 90: "doksan",
            "hundred": "yuz",
            "ten_sep": " ",
            "hundred_sep": " "
        }
    },
     "dutch.lang": {
        "name": "Dutch",
        "data": {
            0: "nul", 1: "een", 2: "twee", 3: "drie", 4: "vier", 5: "vijf",
            6: "zes", 7: "zeven", 8: "acht", 9: "negen", 10: "tien",
            11: "elf", 12: "twaalf", 13: "dertien", 14: "veertien", 15: "vijftien",
            16: "zestien", 17: "zeventien", 18: "achttien", 19: "negentien",
            20: "twintig", 30: "dertig", 40: "veertig", 50: "vijftig",
            60: "zestig", 70: "zeventig", 80: "tachtig", 90: "negentig",
            "hundred": "honderd",
            "ten_sep": "en", 
            "hundred_sep": ""
        }
    },
    # --- Ancient Languages ---
    "latin.lang": {
        "name": "Latin",
        "data": {
            0: "nulla", 1: "unus", 2: "duo", 3: "tres", 4: "quattuor", 5: "quinque",
            6: "sex", 7: "septem", 8: "octo", 9: "novem", 10: "decem",
            11: "undecim", 12: "duodecim", 13: "tredecim", 14: "quattuordecim", 15: "quindecim",
            16: "sedecim", 17: "septendecim", 18: "duodeviginti", 19: "undeviginti",
            20: "viginti", 30: "triginta", 40: "quadraginta", 50: "quinquaginta",
            60: "sexaginta", 70: "septuaginta", 80: "octoginta", 90: "nonaginta",
            "hundred": "centum",
            "ten_sep": " et ",
            "hundred_sep": " "
        }
    },
    "ancient_greek.lang": {
        "name": "Ancient Greek",
        "data": {
            0: "μηδέν", 1: "εἷς", 2: "δύο", 3: "τρεῖς", 4: "τέσσαρες", 5: "πέντε",
            6: "ἕξ", 7: "ἑπτά", 8: "ὀκτώ", 9: "ἐννέα", 10: "δέκα",
            11: "ἕνδεκα", 12: "δώδεκα", 13: "τρεῖς καὶ δέκα", 14: "τέσσαρες καὶ δέκα", 15: "πεντεκαίδεκα",
            20: "εἴκοσι", 30: "τριάκοντα", 40: "τεσσαράκοντα", 50: "πεντήκοντα",
            60: "ἑξήκοντα", 70: "ἑβδομήκοντα", 80: "ὀγδοήκοντα", 90: "ἐνενήκοντα",
            "hundred": "ἑκατόν",
            "ten_sep": " καὶ ",
            "hundred_sep": " "
        }
    },
    "biblical_hebrew.lang": {
        "name": "Biblical Hebrew (Aramaic Script)",
        "data": {
            0: "אפס", 1: "אחד", 2: "שניים", 3: "שלושה", 4: "ארבעה", 5: "חמישה",
            6: "שישה", 7: "שבעה", 8: "שמונה", 9: "תשעה", 10: "עשרה",
            11: "אחד עשר", 12: "שנים עשר", 13: "שלושה עשר",
            20: "עשרים", 30: "שלושים", 40: "ארבעים", 50: "חמישים",
            60: "שישים", 70: "שבעים", 80: "שמונים", 90: "תשעים",
            "hundred": "מאה",
            "ten_sep": " ו",
            "hundred_sep": " "
        }
    },
    "sanskrit.lang": {
        "name": "Sanskrit", 
        "data": {
            0: "शून्य", 1: "एक", 2: "द्वि", 3: "त्रि", 4: "चतुर्", 5: "पञ्च",
            6: "षष्", 7: "सप्त", 8: "अष्ट", 9: "नव", 10: "दश",
            11: "एकादश", 12: "द्वादश", 13: "त्रयोदश", 14: "चतुर्दश", 15: "पञ्चदश",
            20: "विंशति", 30: "त्रिंशत्", 40: "चत्वारिंशत्", 50: "पञ्चाशत्",
            60: "षष्टि", 70: "सप्तति", 80: "अशीति", 90: "नवति",
            "hundred": "शत",
            "ten_sep": "",
            "hundred_sep": ""
        }
    },
    "sumerian.lang": {
        "name": "Sumerian",
        "data": {
            1: "𒁹", 2: "𒁹𒁹", 3: "𒁹𒁹𒁹", 4: "𒁹𒁹𒁹𒁹", 5: "𒁹𒁹𒁹𒁹𒁹",
            6: "𒁹𒁹𒁹𒁹𒁹𒁹", 7: "𒁹𒁹𒁹𒁹𒁹𒁹𒁹", 8: "𒁹𒁹𒁹𒁹𒁹𒁹𒁹𒁹", 9: "𒁹𒁹𒁹𒁹𒁹𒁹𒁹𒁹𒁹",
            10: "𒌋", 20: "𒌋𒌋", 30: "𒌋𒌋𒌋", 40: "𒌋𒌋𒌋𒌋", 50: "𒌋𒌋𒌋𒌋𒌋",
            60: "𒁹",
            "hundred": "NotUsedInBase60" 
        }
    }
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

    print(f"Generated: {filename}")

if __name__ == "__main__":
    for filename, info in languages.items():
        write_lang_file(filename, info)
