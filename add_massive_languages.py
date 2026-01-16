import os

# Definition of language data
languages_to_add = {
    # --- European & Near East ---
    "albanian.lang": {
        "name": "Albanian",
        "data": {1: "një", 2: "dy", 3: "tre", 4: "katër", 5: "pesë", 6: "gjashtë", 7: "shtatë", 8: "tetë", 9: "nëntë", 10: "dhjetë", 20: "njëzet", 30: "tridhjetë", 40: "dyzet", 50: "pesëdhjetë", 100: "njëqind", "ten_sep": " e "},
    },
    "bosnian.lang": {
        "name": "Bosnian",
        "data": {1: "jedan", 2: "dva", 3: "tri", 4: "četiri", 5: "pet", 6: "šest", 7: "sedam", 8: "osam", 9: "devet", 10: "deset", 11: "jedanaest", 20: "dvadeset", 100: "sto", "ten_sep": " "},
    },
    "estonian.lang": {
        "name": "Estonian",
        "data": {1: "üks", 2: "kaks", 3: "kolm", 4: "neli", 5: "viis", 6: "kuus", 7: "seitse", 8: "kaheksa", 9: "üheksa", 10: "kümme", 11: "üksteist", 20: "kakskümmend", 100: "sada", "ten_sep": " "},
    },
    "finnish.lang": {
        "name": "Finnish",
        "data": {1: "yksi", 2: "kaksi", 3: "kolme", 4: "neljä", 5: "viisi", 6: "kuusi", 7: "seitsemän", 8: "kahdeksan", 9: "yhdeksän", 10: "kymmenen", 11: "yksitoista", 20: "kaksikymmentä", 100: "sata", "ten_sep": ""},
    },
    "georgian.lang": {
        "name": "Georgian",
        "data": {1: "ერთი", 2: "ორი", 3: "სამი", 4: "ოთხი", 5: "ხუთი", 6: "ექვსი", 7: "შვიდი", 8: "რვა", 9: "ცხრა", 10: "ათი", 11: "თერთმეტი", 20: "ოცი", 30: "ოცდაათი", 40: "ორმოცი", 100: "ასი", "ten_sep": "და"},
    },
    "greek_modern.lang": {
        "name": "Greek",
        "data": {1: "ένα", 2: "δύο", 3: "τρία", 4: "τέσσερα", 5: "πέντε", 6: "έξι", 7: "επτά", 8: "οκτώ", 9: "εννέα", 10: "δέκα", 11: "έντεκα", 20: "είκοσι", 100: "εκατό", "ten_sep": " "},
    },
    "hungarian.lang": {
        "name": "Hungarian",
        "data": {1: "egy", 2: "kettő", 3: "három", 4: "négy", 5: "öt", 6: "hat", 7: "hét", 8: "nyolc", 9: "kilenc", 10: "tíz", 11: "tizenegy", 20: "húsz", 21: "huszonegy", 30: "harminc", 100: "száz", "ten_sep": ""},
    },
    "icelandic.lang": {
        "name": "Icelandic",
        "data": {1: "einn", 2: "tveir", 3: "þrír", 4: "fjórir", 5: "fimm", 6: "sex", 7: "sjö", 8: "átta", 9: "níu", 10: "tíu", 11: "ellefu", 20: "tuttugu", 30: "þrjátíu", 100: "hundrað", "ten_sep": " og "},
    },
    # --- Asian ---
    "armenian_eastern.lang": {"name": "Armenian (Eastern)", "data": {1: "մեկ", 2: "երկու", 3: "երեք", 4: "չորս", 5: "հինգ", 6: "վեց", 7: "յոթ", 8: "ութ", 9: "ինը", 10: "տասը", 11: "տասնմեկ", 20: "քսան", 100: "հարյուր", "ten_sep": ""}},
    "armenian_western.lang": {"name": "Armenian (Western)", "data": {1: "մէկ", 2: "երկու", 3: "երեք", 4: "չորս", 5: "հինգ", 6: "վեց", 7: "եօթ", 8: "ութ", 9: "ինը", 10: "տասը", 20: "քսան", 100: "հարիւր", "ten_sep": ""}},
    "azerbaijani.lang": {"name": "Azerbaijani", "data": {1: "bir", 2: "iki", 3: "üç", 4: "dörd", 5: "beş", 6: "altı", 7: "yeddi", 8: "səkkiz", 9: "doqquz", 10: "on", 20: "iyirmi", 100: "yüz", "ten_sep": " "}},
    "bengali.lang": {"name": "Bengali", "data": {1: "এক", 2: "দুই", 3: "তিন", 4: "চার", 5: "পাঁচ", 6: "ছয়", 7: "সাত", 8: "আট", 9: "নয়", 10: "দশ", 20: "বিশ", 100: "একশো", "ten_sep": " "}},
    "burmese.lang": {"name": "Burmese", "data": {1: "တစ်", 2: "နှစ်", 3: "သုံး", 4: "လေး", 5: "ငါး", 6: "ခြောက်", 7: "ခုနစ်", 8: "ရှစ်", 9: "ကိုး", 10: "ဆယ်", 20: "နှစ်ဆယ်", 100: "တစ်ရာ", "ten_sep": " "}},
    "chinese_traditional.lang": {"name": "Chinese (Traditional)", "data": {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十", 20: "二十", 100: "一百", "ten_sep": ""}},
    "khmer.lang": {"name": "Khmer", "data": {1: "មួយ", 2: "ពីរ", 3: "បី", 4: "បួន", 5: "ប្រាំ", 6: "ប្រាំមួយ", 7: "ប្រាំពីរ", 8: "ប្រាំបី", 9: "ប្រាំបួន", 10: "ដប់", 20: "ម្ភៃ", 30: "សាមសិប", 100: "មួយរយ", "ten_sep": " "}},
    "cebuano.lang": {"name": "Cebuano", "data": {1: "usa", 2: "duha", 3: "tulo", 4: "upat", 5: "lima", 6: "unom", 7: "pito", 8: "walo", 9: "siyam", 10: "napulo", 20: "kawhaan", 100: "usa ka gatos", "ten_sep": " ug "}},
    "dari.lang": {"name": "Dari", "data": {1: "یک", 2: "دو", 3: "سه", 4: "چهار", 5: "پنج", 6: "شش", 7: "هفت", 8: "هشت", 9: "نه", 10: "ده", 20: "بیست", 100: "صد", "ten_sep": " و "}},
    "farsi.lang": {"name": "Farsi", "data": {1: "یک", 2: "دو", 3: "سه", 4: "چهار", 5: "پنج", 6: "شش", 7: "هفت", 8: "هشت", 9: "نه", 10: "ده", 20: "بیست", 100: "صد", "ten_sep": " و "}},
    "gujarati.lang": {"name": "Gujarati", "data": {1: "એક", 2: "બે", 3: "ત્રણ", 4: "ચાર", 5: "પાંચ", 6: "છ", 7: "સાત", 8: "આઠ", 9: "નવ", 10: "દસ", 20: "વીસ", 100: "સો", "ten_sep": " "}},
    "hakka.lang": {"name": "Hakka", "data": {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十", 20: "二十", 100: "百", "ten_sep": ""}},
    "hmong.lang": {"name": "Hmong", "data": {1: "Ib", 2: "Ob", 3: "Peb", 4: "Plaub", 5: "Tsib", 6: "Rau", 7: "Xya", 8: "Yim", 9: "Cuaj", 10: "Kaum", 20: "Nees nkaum", 30: "Peb caug", 100: "Ib puas", "ten_sep": " "}},
    "ilocano.lang": {"name": "Ilocano", "data": {1: "maysa", 2: "dua", 3: "tallo", 4: "uppat", 5: "lima", 6: "innem", 7: "pito", 8: "walo", 9: "siam", 10: "sangapulo", 20: "duapulo", 100: "sangagasut", "ten_sep": " ket "}},
    "ilonggo.lang": {"name": "Ilonggo", "data": {1: "isa", 2: "duha", 3: "tatlo", 4: "apat", 5: "lima", 6: "anum", 7: "pito", 8: "walo", 9: "siyam", 10: "napulo", 20: "duha ka pulo", 100: "isa ka gatos", "ten_sep": " kag "}},
    "indonesian.lang": {"name": "Indonesian", "data": {1: "satu", 2: "dua", 3: "tiga", 4: "empat", 5: "lima", 6: "enam", 7: "tujuh", 8: "delapan", 9: "sembilan", 10: "sepuluh", 11: "sebelas", 20: "dua puluh", 100: "seratus", "ten_sep": " "}},
    "javanese.lang": {"name": "Javanese", "data": {1: "siji", 2: "loro", 3: "telu", 4: "papat", 5: "lima", 6: "enem", 7: "pitu", 8: "wolu", 9: "sanga", 10: "sepuluh", 20: "rong puluh", 21: "selikur", 25: "selawé", 50: "sèket", 60: "suwidha", 100: "satus", "ten_sep": " "}},
    "kannada.lang": {"name": "Kannada", "data": {1: "ಒಂದು", 2: "ಎರಡು", 3: "ಮೂರು", 4: "ನಾಲ್ಕು", 5: "ಐದು", 6: "ಆರು", 7: "ಏಳು", 8: "ಎಂಟು", 9: "ಒಂಬತ್ತು", 10: "ಹತ್ತು", 20: "ಇಪ್ಪತ್ತು", 100: "ನೂರು", "ten_sep": " "}},
    "kazakh.lang": {"name": "Kazakh", "data": {1: "Бір", 2: "Екі", 3: "Үш", 4: "Төрт", 5: "Бес", 6: "Алты", 7: "Жеті", 8: "Сегіз", 9: "Тоғыз", 10: "Он", 20: "Жиырма", 100: "Жүз", "ten_sep": " "}},
    "kurdish_kurmanji.lang": {"name": "Kurdish (Kurmanji)", "data": {1: "yek", 2: "du", 3: "sê", 4: "çar", 5: "pênc", 6: "şeş", 7: "heft", 8: "heşt", 9: "neh", 10: "deh", 20: "bîst", 100: "sed", "ten_sep": " û "}},
    "kurdish_sorani.lang": {"name": "Kurdish (Sorani)", "data": {1: "یه‌ك", 2: "دوو", 3: "سێ", 4: "چوار", 5: "پێنج", 6: "شەش", 7: "حەوت", 8: "هەشت", 9: "نۆ", 10: "ده", 20: "بیست", 100: "سەد", "ten_sep": " و "}},
    "kyrgyz.lang": {"name": "Kyrgyz", "data": {1: "Бир", 2: "Эки", 3: "Үч", 4: "Төрт", 5: "Беш", 6: "Алты", 7: "Жети", 8: "Сегиз", 9: "Тогуз", 10: "Он", 20: "Жыйырма", 100: "Жүз", "ten_sep": " "}},
    "lao.lang": {"name": "Lao", "data": {1: "ຫນຶ່ງ", 2: "ສອງ", 3: "ສາມ", 4: "ສີ່", 5: "ຫ້າ", 6: "ຫົກ", 7: "ເຈັດ", 8: "ແປດ", 9: "ເກົ້າ", 10: "ສິບ", 20: "ຊາວ", 100: "ຮ້ອຍ", "ten_sep": " "}},
    "malay.lang": {"name": "Malay", "data": {1: "satu", 2: "dua", 3: "tiga", 4: "empat", 5: "lima", 6: "enam", 7: "tujuh", 8: "lapan", 9: "sembilan", 10: "sepuluh", 11: "sebelas", 20: "dua puluh", 100: "seratus", "ten_sep": " "}},
    "marathi.lang": {"name": "Marathi", "data": {1: "एक", 2: "दोन", 3: "तीन", 4: "चार", 5: "पाच", 6: "सहा", 7: "सात", 8: "आठ", 9: "नऊ", 10: "दहा", 20: "वीस", 100: "शंभर", "ten_sep": " "}},
    "mongolian.lang": {"name": "Mongolian", "data": {1: "нэг", 2: "хоёр", 3: "гурав", 4: "дөрөв", 5: "тав", 6: "зургаа", 7: "долоо", 8: "найм", 9: "ес", 10: "арав", 20: "хорь", 30: "гуч", 100: "зуу", "ten_sep": " "}},
    "nepali.lang": {"name": "Nepali", "data": {1: "एक", 2: "दुई", 3: "तिन", 4: "चार", 5: "पाँच", 6: "छ", 7: "सात", 8: "आठ", 9: "नौ", 10: "दस", 20: "बिस", 100: "सय", "ten_sep": " "}},
    "pashto.lang": {"name": "Pashto", "data": {1: "يو", 2: "دوه", 3: "درې", 4: "څلور", 5: "پنځه", 6: "شپږ", 7: "اووه", 8: "اته", 9: "نهه", 10: "لس", 20: "شل", 30: "دیرش", 100: "سل", "ten_sep": " "}},
    "punjabi.lang": {"name": "Punjabi", "data": {1: "ਇੱਕ", 2: "ਦੋ", 3: "ਤਿੰਨ", 4: "ਚਾਰ", 5: "ਪੰਜ", 6: "ਛੇ", 7: "ਸੱਤ", 8: "ਅੱਠ", 9: "ਨੌਂ", 10: "ਦਸ", 20: "ਵੀਹ", 100: "ਸੌ", "ten_sep": " "}},
    "rohingya.lang": {"name": "Rohingya", "data": {1: "ek", 2: "dui", 3: "tin", 4: "sair", 5: "fañs", 6: "só", 7: "háñt", 8: "añctho", 9: "no", 10: "doc", 20: "bis", 100: "ek-cót", "ten_sep": " "}},
    "serbian.lang": {"name": "Serbian", "data": {1: "један", 2: "два", 3: "три", 4: "четири", 5: "пет", 6: "шест", 7: "седам", 8: "осам", 9: "девет", 10: "десет", 20: "двадесет", 100: "сто", "ten_sep": " "}},
    "tagalog.lang": {"name": "Tagalog", "data": {1: "isa", 2: "dalawa", 3: "tatlo", 4: "apat", 5: "lima", 6: "anim", 7: "pito", 8: "walo", 9: "siyam", 10: "sampu", 11: "labing-isa", 20: "dalawampu", 100: "isang daan", "ten_sep": "'t "}},
    "tamil.lang": {"name": "Tamil", "data": {1: "ஒன்று", 2: "இரண்டு", 3: "மூன்று", 4: "நான்கு", 5: "ஐந்து", 6: "ஆறு", 7: "ஏழு", 8: "எட்டு", 9: "ஒன்பது", 10: "பத்து", 20: "இருபது", 100: "நூறு", "ten_sep": " "}},
    "telugu.lang": {"name": "Telugu", "data": {1: "ఒకటి", 2: "రెండు", 3: "మూడు", 4: "నాలుగు", 5: "ఐదు", 6: "ఆరు", 7: "ఏడు", 8: "ఎనిమిది", 9: "తొమ్మిది", 10: "పది", 20: "ఇరవై", 100: "వంద", "ten_sep": " "}},
    "thai.lang": {"name": "Thai", "data": {1: "หนึ่ง", 2: "สอง", 3: "สาม", 4: "สี่", 5: "ห้า", 6: "หก", 7: "เจ็ด", 8: "แปด", 9: "เก้า", 10: "สิบ", 11: "สิบเอ็ด", 20: "ยี่สิบ", 100: "หนึ่งร้อย", "ten_sep": ""}},
    "tibetan.lang": {"name": "Tibetan", "data": {1: "གཅིག་", 2: "གཉིས་", 3: "གསུམ་", 4: "བཞི་", 5: "ལྔ་", 6: "དྲུག་", 7: "བདུན་", 8: "བརྒྱད་", 9: "དགུ་", 10: "བཅུ་", 20: "ཉི་ཤུ་", 30: "སུམ་ཅུ", 100: "བརྒྱ་", "ten_sep": "རྩ་"}},
    "urdu.lang": {"name": "Urdu", "data": {1: "ایک", 2: "دو", 3: "تین", 4: "چار", 5: "پانچ", 6: "چھ", 7: "سات", 8: "آٹھ", 9: "نو", 10: "دس", 20: "بیس", 100: "سو", "ten_sep": " "}},
    "uzbek.lang": {"name": "Uzbek", "data": {1: "bir", 2: "ikki", 3: "uch", 4: "to'rt", 5: "besh", 6: "olti", 7: "yetti", 8: "sakkiz", 9: "to'qqiz", 10: "o'n", 20: "yigirma", 100: "yuz", "ten_sep": " "}},
    "vietnamese.lang": {"name": "Vietnamese", "data": {1: "một", 2: "hai", 3: "ba", 4: "bốn", 5: "năm", 6: "sáu", 7: "bảy", 8: "tám", 9: "chín", 10: "mười", 20: "hai mươi", 21: "hai mươi mốt", 100: "một trăm", "ten_sep": " "}},
    # --- African ---
    "amharic.lang": {"name": "Amharic", "data": {1: "አንድ", 2: "ሁለት", 3: "ሦስት", 4: "አራት", 5: "አምስት", 6: "ስድስት", 7: "ሰባት", 8: "ስምንት", 9: "ዘጠኝ", 10: "አስር", 20: "ሃያ", 100: "መቶ", "ten_sep": " "}},
    "fulani.lang": {"name": "Fulani", "data": {1: "Go'o", 2: "Ɗiɗi", 3: "Tati", 4: "Nay", 5: "Jowi", 6: "Jeego", 7: "Jeeɗiɗi", 8: "Jeetati", 9: "Jeenay", 10: "Sappo", 20: "Nogas", 100: "Teemerre", "ten_sep": " e "}},
    "igbo.lang": {"name": "Igbo", "data": {1: "otu", 2: "abụọ", 3: "atọ", 4: "anọ", 5: "ise", 6: "isii", 7: "asaa", 8: "asatọ", 9: "itoolu", 10: "iri", 20: "iri abụọ", 100: "otu narị", "ten_sep": " na "}},
    "kinyarwanda.lang": {"name": "Kinyarwanda", "data": {1: "rimwe", 2: "kabiri", 3: "gatatu", 4: "kane", 5: "gatanu", 6: "gatandatu", 7: "karindwi", 8: "umunane", 9: "icyenda", 10: "icumi", 20: "makumyabiri", 100: "ijana", "ten_sep": " na "}},
    "oromo.lang": {"name": "Oromo", "data": {1: "tokko", 2: "lama", 3: "sadi", 4: "afur", 5: "shan", 6: "jaha", 7: "torba", 8: "saddeet", 9: "sagal", 10: "kudhan", 20: "digdama", 100: "dhibba", "ten_sep": " "}},
    "somali.lang": {"name": "Somali", "data": {1: "Kow", 2: "Labo", 3: "Saddex", 4: "Afar", 5: "Shan", 6: "Lix", 7: "Toddoba", 8: "Sideed", 9: "Sagaal", 10: "Toban", 20: "Labataan", 100: "Boqol", "ten_sep": " iyo "}},
    "swahili.lang": {"name": "Swahili", "data": {1: "moja", 2: "mbili", 3: "tatu", 4: "nne", 5: "tano", 6: "sita", 7: "saba", 8: "nane", 9: "tisa", 10: "kumi", 20: "ishirini", 100: "mia moja", "ten_sep": " na "}},
    "tigrinya.lang": {"name": "Tigrinya", "data": {1: "ሓደ", 2: "ክልተ", 3: "ሰለስተ", 4: "ኣርባዕተ", 5: "ሓሙሽተ", 6: "ሽዱሽተ", 7: "ሸውዓተ", 8: "ሸሞንተ", 9: "ትሽዓተ", 10: "ዓሰርተ", 20: "ዕስራ", 100: "ሚእቲ", "ten_sep": " "}},
    "wolof.lang": {"name": "Wolof", "data": {1: "benn", 2: "ñaar", 3: "ñett", 4: "ñent", 5: "juróom", 6: "juróom benn", 7: "juróom ñaar", 8: "juróom ñett", 9: "juróom ñent", 10: "fukk", 20: "ñaar fukk", 100: "teeméer", "ten_sep": " ak "}},
    "yoruba.lang": {"name": "Yoruba", "data": {1: "Ọ̀kan", 2: "Èjì", 3: "Ẹta", 4: "Ẹrin", 5: "Àrún", 6: "Ẹfà", 7: "Èje", 8: "Ẹjọ", 9: "Ẹsan", 10: "Ẹwà", 20: "Ogún", 30: "Ọgbọ̀n", 100: "Ọgọ́rùn", "ten_sep": " "}},
    # --- Americas & Creoles ---
    "haitian_creole.lang": {"name": "Haitian Creole", "data": {1: "En", 2: "De", 3: "Twa", 4: "Kat", 5: "Senk", 6: "Sis", 7: "Sèt", 8: "Uit", 9: "Nèf", 10: "Dis", 20: "Ven", 30: "Trant", 80: "Katreven", 100: "San", "ten_sep": ""}},
    "navajo.lang": {"name": "Navajo", "data": {1: "Tʼááłáʼí", 2: "Naakí", 3: "Tááʼ", 4: "Dį́į́ʼ", 5: "Áshdlaʼ", 6: "Hastą́ą́", 7: "Tsostsʼid", 8: "Tseebíí", 9: "Náhástʼéí", 10: "Neeznáá", 11: "łaʼtsʼáadah", 20: "Naadiin", 100: "neeznádiin", "ten_sep": " dóó baʼaan "}},
    # --- Other ---
    "braille.lang": {"name": "Braille", "data": {1: "⠼⠁", 2: "⠼⠃", 3: "⠼⠉", 4: "⠼⠙", 5: "⠼⠑", 6: "⠼⠋", 7: "⠼⠛", 8: "⠼⠓", 9: "⠼⠊", 0: "⠼⠚", "hundred": "⠼⠁⠚⠚", "ten_sep": ""}},
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
        # Write numeric keys, ensuring 0 is handled correctly if present
        int_keys = sorted([k for k in data.keys() if isinstance(k, int)])
        for key in int_keys:
            f.write(f"{key}: {data[key]}\n")

if __name__ == "__main__":
    count = 0
    for filename, info in languages_to_add.items():
        if not os.path.exists(filename):
            write_lang_file(filename, info)
            print(f"Generated: {filename}")
            count += 1
    print(f"\nGenerated {count} new language files.")
