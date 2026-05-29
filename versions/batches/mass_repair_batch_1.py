import os

LANG_DIR = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"

# Comprehensive dictionary for Batch 1 (11-19)
repairs = {
    "amharic": {11:"አስራ አንድ", 12:"አስራ ሁለት", 13:"አስራ ሶስት", 14:"አስራ አራት", 15:"አስራ አምስት", 16:"አስራ ስድስት", 17:"አስራ ሰባት", 18:"አስራ ስምንት", 19:"አስራ ዘጠኝ"},
    "armenian_eastern": {11:"տասնմեկ", 12:"տասներկու", 13:"տասներեք", 14:"տասնչորս", 15:"տասնհինգ", 16:"տասնվեց", 17:"տասնյոթ", 18:"տասնութ", 19:"տասնինը"},
    "azerbaijani": {11:"on bir", 12:"on iki", 13:"on üç", 14:"on dörd", 15:"on beş", 16:"on altı", 17:"on yeddi", 18:"on səkkiz", 19:"on doqquz"},
    "belorussian": {11:"адзінаццаць", 12:"дванаццаць", 13:"трынаццаць", 14:"чатырнаццаць", 15:"пятнаццаць", 16:"шаснаццаць", 17:"семнаццаць", 18:"वासімнаццаць", 19:"дзевятнаццаць"},
    "bengali": {11:"এগারো", 12:"বারো", 13:"তেরো", 14:"চৌদ্দ", 15:"পনেরো", 16:"ষোলো", 17:"সতেরো", 18:"আঠারো", 19:"উনিশ"},
    "bosnian": {11:"jedanaest", 12:"dvanaest", 13:"trinaest", 14:"četrnaest", 15:"petnaest", 16:"šesnaest", 17:"sedamnaest", 18:"osamnaest", 19:"devetnaest"},
    "bulgarian": {11:"единадесет", 12:"дванадесет", 13:"тринадесет", 14:"четиринадесет", 15:"петнадесет", 16:"шестнадесет", 17:"седемнадесет", 18:"осемнадесет", 19:"деветнадесет"},
    "burmese": {11:"ဆယ့်တစ်", 12:"ဆယ့်နှစ်", 13:"ဆယ့်သုံး", 14:"ဆယ့်လေး", 15:"ဆယ့်ငါး", 16:"ဆယ့်ခြောက်", 17:"ဆယ့်ခုနစ်", 18:"ဆယ့်ရှစ်", 19:"ဆယ့်ကိုး"},
    "cebuano": {11:"napulog-usa", 12:"napulog-duha", 13:"napulog-tulo", 14:"napulog-upat", 15:"napulog-lima", 16:"napulog-unom", 17:"napulog-pito", 18:"napulog-walo", 19:"napulog-siyam"},
    "chinese_simplified": {11:"十一", 12:"十二", 13:"十三", 14:"十四", 15:"十五", 16:"十六", 17:"十七", 18:"十八", 19:"十九"},
    "chinese_traditional": {11:"十一", 12:"十二", 13:"十三", 14:"十四", 15:"十五", 16:"十六", 17:"十七", 18:"十八", 19:"十九"},
    "croatian": {11:"jedanaest", 12:"dvanaest", 13:"trinaest", 14:"četrnaest", 15:"petnaest", 16:"šesnaest", 17:"sedamnaest", 18:"osamnaest", 19:"devetnaest"},
    "czech": {11:"jedenáct", 12:"dvanáct", 13:"třináct", 14:"čtrnáct", 15:"patnáct", 16:"šestnáct", 17:"sedmnáct", 18:"osmnáct", 19:"devatenáct"},
    "danish": {11:"elleve", 12:"tolv", 13:"tretten", 14:"fjorten", 15:"femten", 16:"seksten", 17:"sytten", 18:"atten", 19:"nitten"},
    "dutch": {11:"elf", 12:"twaalf", 13:"dertien", 14:"veertien", 15:"vijftien", 16:"zestien", 17:"zeventien", 18:"achttien", 19:"negentien"},
    "estonian": {11:"üksteist", 12:"kaksteist", 13:"kolmteist", 14:"neliteist", 15:"viisteist", 16:"kuusteist", 17:"seitseteist", 18:"kaheksateist", 19:"üheksateist"},
    "farsi": {11:"یازده", 12:"دوازده", 13:"سیزده", 14:"چهارده", 15:"پانزده", 16:"شانزده", 17:"هفده", 18:"هجده", 19:"نوزده"},
    "finnish": {11:"yksitoista", 12:"kaksitoista", 13:"kolmetoista", 14:"neljätoista", 15:"viisitoista", 16:"kuusitoista", 17:"seitsemäntoista", 18:"kahdeksantoista", 19:"yhdeksäntoista"},
    "french": {11:"onze", 12:"douze", 13:"treize", 14:"quatorze", 15:"quinze", 16:"seize", 17:"dix-sept", 18:"dix-huit", 19:"dix-neuf"},
    "georgian": {11:"თერთმეტი", 12:"თორმეტი", 13:"ცამეტი", 14:"თოთხმეტი", 15:"თხუთმეტი", 16:"თექვსმეტი", 17:"ჩვიდმეტი", 18:"თვრამეტი", 19:"ცხრამეტი"},
    "german": {11:"elf", 12:"zwölf", 13:"dreizehn", 14:"vierzehn", 15:"fünfzehn", 16:"sechzehn", 17:"siebzehn", 18:"achtzehn", 19:"neunzehn"},
    "gujarati": {11:"અગિયાર", 12:"બાર", 13:"તેર", 14:"ચૌદ", 15:"પંદર", 16:"સોળ", 17:"સત્તર", 18:"અઢાર", 19:"ઓગણીસ"},
    "haitian_creole": {11:"onz", 12:"douz", 13:"trèz", 14:"katòz", 15:"kenz", 16:"sèz", 17:"disèt", 18:"dizwit", 19:"diznèf"},
    "hindi": {11:"ग्यारह", 12:"बारह", 13:"तेरह", 14:"चौदह", 15:"पंद्रह", 16:"सोलह", 17:"सत्रह", 18:"अठारह", 19:"उन्नीस"},
    "hmong": {11:"kaum ib", 12:"kaum ob", 13:"kaum peb", 14:"kaum plaub", 15:"kaum tsib", 16:"kaum rau", 17:"kaum xya", 18:"kaum yim", 19:"kaum cuaj"},
    "hungarian": {11:"tizenegy", 12:"tizenkettő", 13:"tizenhárom", 14:"tizennégy", 15:"tizenöt", 16:"tizenhat", 17:"tizenhét", 18:"tizennyolc", 19:"tizenkilenc"},
    "icelandic": {11:"ellefu", 12:"tólf", 13:"þrettán", 14:"fjórtán", 15:"fimmtán", 16:"sextán", 17:"sjöttán", 18:"átján", 19:"nítján"},
    "igbo": {11:"iri na otu", 12:"iri na abụọ", 13:"iri na atọ", 14:"iri na anọ", 15:"iri na ise", 16:"iri na isii", 17:"iri na asaa", 18:"iri na asatọ", 19:"iri na itoolu"},
    "indonesian": {11:"sebelas", 12:"dua belas", 13:"tiga belas", 14:"empat belas", 15:"lima belas", 16:"enam belas", 17:"tujuh belas", 18:"delapan belas", 19:"sembilan belas"},
    "italian": {11:"undici", 12:"dodici", 13:"tredici", 14:"quattordici", 15:"quindici", 16:"sedici", 17:"diciassette", 18:"diciotto", 19:"diciannove"},
    "japanese": {11:"十一", 12:"十二", 13:"十三", 14:"十四", 15:"十五", 16:"十六", 17:"十七", 18:"十八", 19:"十九"},
    "javanese": {11:"sewelas", 12:"rolas", 13:"telulas", 14:"patbelas", 15:"limalas", 16:"nembelas", 17:"pitulas", 18:"wolulas", 19:"sangalas"},
    "kannada": {11:"ಹನ್ನೊಂದು", 12:"ಹನ್ನೆರಡು", 13:"ಹದಿಮೂರು", 14:"ಹದಿನಾಲ್ಕು", 15:"ಹದಿನೈದು", 16:"ಹದಿನಾರು", 17:"ಹದಿನೇಳು", 18:"ಹದಿನೆಂಟು", 19:"ಹತ್ತೊಂಬತ್ತು"},
    "kazakh": {11:"он бір", 12:"он екі", 13:"он үш", 14:"он төрт", 15:"он бес", 16:"он алты", 17:"он жеті", 18:"он сегіз", 19:"он тоғыз"},
    "khmer": {11:"ដប់មួយ", 12:"ដប់ពីរ", 13:"ដប់បី", 14:"ដប់បួន", 15:"ដប់ប្រាំ", 16:"ដប់ប្រាំមួយ", 17:"ដប់ប្រាំពីរ", 18:"ដប់ប្រាំបី", 19:"ដប់ប្រាំបួន"},
    "korean": {11:"열하나", 12:"열둘", 13:"열셋", 14:"열넷", 15:"열다섯", 16:"열여섯", 17:"열일곱", 18:"열여덟", 19:"열아홉"},
    "kurdish_kurmanji": {11:"yanzdeh", 12:"duvazdeh", 13:"sêzdeh", 14:"çardeh", 15:"panzdeh", 16:"shanzdeh", 17:"hifdeh", 18:"hijdeh", 19:"nozdeh"},
    "kyrgyz": {11:"он бир", 12:"он эки", 13:"он үч", 14:"он төрт", 15:"он беш", 16:"он алты", 17:"он жети", 18:"он сегиз", 19:"он тогуз"},
    "lao": {11:"ສິບເອັດ", 12:"ສິບສອງ", 13:"ສິບສາມ", 14:"ສິບສີ່", 15:"ສິບຫ້າ", 16:"ສິບຫົກ", 17:"ສິບເຈັດ", 18:"ສິບແປດ", 19:"ສິບເກົ້າ"},
    "latvian": {11:"vienpadsmit", 12:"divpadsmit", 13:"trīspadsmit", 14:"četrpadsmit", 15:"piecpadsmit", 16:"sešpadsmit", 17:"septiņpadsmit", 18:"astoņpadsmit", 19:"deviņpadsmit"},
    "lithuanian": {11:"vienuolika", 12:"dvylika", 13:"trylika", 14:"keturiolika", 15:"penkiolika", 16:"šešiolika", 17:"septyniolika", 18:"aštuoniolika", 19:"devyniolika"},
    "macedonian": {11:"единаесет", 12:"дванаесет", 13:"тринаесет", 14:"четиринаесет", 15:"петнаесет", 16:"шеснаесет", 17:"седумнаесет", 18:"осумнаесет", 19:"деветнаесет"},
    "malay": {11:"sebelas", 12:"dua belas", 13:"tiga belas", 14:"empat belas", 15:"lima belas", 16:"enam belas", 17:"tujuh belas", 18:"delapan belas", 19:"sembilan belas"},
    "malayalam": {11:"പതിനൊന്ന്", 12:"പന്ത്രണ്ട്", 13:"പതിമൂന്ന്", 14:"പതിനാല്", 15:"പതിനഞ്ച്", 16:"പതിനാറ്", 17:"പതിനേഴ്", 18:"പതിനെട്ട്", 19:"പത്തൊമ്പത്"},
    "marathi": {11:"अकरा", 12:"बारा", 13:"तेरा", 14:"चौदा", 15:"पंधरा", 16:"सोळा", 17:"सतरा", 18:"अठरा", 19:"एकोणीस"},
    "mongolian": {11:"арван нэг", 12:"арван хоёр", 13:"арван гурав", 14:"арван дөрөв", 15:"арван тав", 16:"арван зургаа", 17:"арван долоо", 18:"арван найм", 19:"арван ес"},
    "nepali": {11:"एघार", 12:"बाह्र", 13:"तेह्र", 14:"चौध", 15:"पन्ध्र", 16:"सोह्र", 17:"सत्र", 18:"अठार", 19:"उन्नाइस"},
    "norwegian": {11:"elleve", 12:"tolv", 13:"tretten", 14:"fjorten", 15:"femten", 16:"seksten", 17:"sytten", 18:"atten", 19:"nitten"},
    "polish": {11:"jedenaście", 12:"dwanaście", 13:"trzynaście", 14:"czternaście", 15:"piętnaście", 16:"szesnaście", 17:"siedemnaście", 18:"osiemnaście", 19:"dziewiętnaście"},
    "portuguese": {11:"onze", 12:"doze", 13:"treze", 14:"quatorze", 15:"quinze", 16:"dezesseis", 17:"dezessete", 18:"dezoito", 19:"dezenove"}
}

def update_lang_file(name, data):
    path = os.path.join(LANG_DIR, name + ".lang")
    if not os.path.exists(path):
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Check if 11 is already there
    if any(line.strip().startswith("11:") for line in lines):
        return False
        
    # Find insertion point (after 10:)
    idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("10:"):
            idx = i + 1
            break
            
    if idx == -1: idx = len(lines)
    
    new_lines = [f"{k}: {v}\n" for k, v in data.items()]
    lines[idx:idx] = new_lines
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return True

count = 0
for name, data in repairs.items():
    if update_lang_file(name, data):
        count += 1
        
print(f"Batch 1 Repair Complete: {count} languages updated.")
