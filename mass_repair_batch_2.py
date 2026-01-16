import os

LANG_DIR = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"

# Comprehensive dictionary for Batch 2 (11-19)
repairs = {
    "punjabi": {11:"ਗਿਆਰਾਂ", 12:"ਬਾਰਾਂ", 13:"ਤੇਰਾਂ", 14:"ਚੌਦਾਂ", 15:"ਪੰਦਰਾਂ", 16:"ਸੋਲਾਂ", 17:"ਸਤਾਰਾਂ", 18:"ਅਠਾਰਾਂ", 19:"ਉੱਨੀ"},
    "romanian": {11:"unsprezece", 12:"doisprezece", 13:"treisprezece", 14:"paisprezece", 15:"cincisprezece", 16:"șaisprezece", 17:"șaptesprezece", 18:"optsprezece", 19:"nouăsprezece"},
    "russian": {11:"одиннадцать", 12:"двенадцать", 13:"тринадцать", 14:"четырнадцать", 15:"пятнадцать", 16:"шестнадцать", 17:"семнадцать", 18:"восемнадцать", 19:"девятнадцать"},
    "serbian": {11:"једанаест", 12:"дванаест", 13:"тринаест", 14:"четрнаест", 15:"петнаест", 16:"шеснаест", 17:"седамнаест", 18:"осамнаест", 19:"деветнаест"},
    "serbo_croatian": {11:"jedanaest", 12:"dvanaest", 13:"trinaest", 14:"četrnaest", 15:"petnaest", 16:"šesnaest", 17:"sedamnaest", 18:"osamnaest", 19:"devetnaest"},
    "slovak": {11:"jedenásť", 12:"dvanásť", 13:"trinásť", 14:"štrnásť", 15:"pätnásť", 16:"šestnásť", 17:"sedemnásť", 18:"osemnásť", 19:"devätnásť"},
    "slovenian": {11:"enajst", 12:"dvanajst", 13:"trinajst", 14:"štirinajst", 15:"petnajst", 16:"šestnajst", 17:"sedemnajst", 18:"osemnajst", 19:"devetnajst"},
    "somali": {11:"kow iyo toban", 12:"laba iyo toban", 13:"saddex iyo toban", 14:"afar iyo toban", 15:"shan iyo toban", 16:"lix iyo toban", 17:"toddoba iyo toban", 18:"siddeed iyo toban", 19:"sagaal iyo toban"},
    "spanish": {11:"once", 12:"doce", 13:"trece", 14:"catorce", 15:"quince", 16:"dieciséis", 17:"diecisiete", 18:"dieciocho", 19:"diecinueve"},
    "swahili": {11:"kumi na moja", 12:"kumi na mbili", 13:"kumi na tatu", 14:"kumi na nne", 15:"kumi na tano", 16:"kumi na sita", 17:"kumi na saba", 18:"kumi na nane", 19:"kumi na tisa"},
    "swedish": {11:"elva", 12:"tolv", 13:"tretton", 14:"fjorton", 15:"femton", 16:"sexton", 17:"sjutton", 18:"arton", 19:"nitton"},
    "tagalog": {11:"labing-isa", 12:"labing-dalawa", 13:"labing-tatlo", 14:"labing-apat", 15:"labing-lima", 16:"labing-anim", 17:"labing-pito", 18:"labing-walo", 19:"labing-siyam"},
    "tamil": {11:"பதினொன்று", 12:"பன்னிரண்டு", 13:"பதின்மூன்று", 14:"பதினான்கு", 15:"பதினைந்து", 16:"பதினாறு", 17:"பதினேழு", 18:"பதினெட்டு", 19:"பத்தொன்பது"},
    "telugu": {11:"పదకొండు", 12:"పన్నెండు", 13:"పதమూడు", 14:"పద్నాలుగు", 15:"పదిహేను", 16:"పదహారు", 17:"పదిహేడు", 18:"పద్దెనిమిది", 19:"పంతొమ్మిది"},
    "thai": {11:"สิบเอ็ด", 12:"สิบสอง", 13:"สิบสาม", 14:"สิบสี่", 15:"สิบห้า", 16:"สิบหก", 17:"สิบเจ็ด", 18:"สิบแปด", 19:"สิบเก้า"},
    "tibetan": {11:"བཅུ་གཅིག", 12:"བཅུ་གཉིས", 13:"བཅུ་གསུམ", 14:"བཅུ་བཞི", 15:"བཅོ་ལྔ", 16:"བཅུ་དྲུག", 17:"བཅུ་བདུན", 18:"བཅོ་བརྒྱད", 19:"བཅུ་དགུ"},
    "tigrinya": {11:"ዓሰርተ ሓደ", 12:"ዓሰርተ ክልተ", 13:"ዓሰርተ ሰለስተ", 14:"ዓሰርተ ኣርባዕተ", 15:"ዓሰርተ ሓሙሽተ", 16:"ዓሰርተ ሽዱሽተ", 17:"ዓሰርተ ሸውዓተ", 18:"ዓሰርተ ሸሞንተ", 19:"ዓሰርተ ትሽዓተ"},
    "turkish": {11:"on bir", 12:"on iki", 13:"on üç", 14:"on dört", 15:"on beş", 16:"on altı", 17:"on yedi", 18:"on sekiz", 19:"on dokuz"},
    "ukrainian": {11:"одинадцять", 12:"дванадцять", 13:"тринадцять", 14:"чотирнадцять", 15:"п'ятнадцять", 16:"шістнадцять", 17:"сімнадцять", 18:"вісімнадцять", 19:"дев'ятнадцять"},
    "urdu": {11:"گیارہ", 12:"بارہ", 13:"تیرہ", 14:"چودہ", 15:"پندرہ", 16:"سولہ", 17:"سترہ", 18:"اٹھارہ", 19:"انیس"},
    "uzbek": {11:"o'n bir", 12:"o'n ikki", 13:"o'n uch", 14:"o'n to'rt", 15:"o'n besh", 16:"o'n olti", 17:"o'n yetti", 18:"o'n sakkiz", 19:"o'n to'qqiz"},
    "vietnamese": {11:"mười một", 12:"mười hai", 13:"mười ba", 14:"mười bốn", 15:"mười lăm", 16:"mười sáu", 17:"mười bảy", 18:"mười tám", 19:"mười chín"},
    "wolof": {11:"fukk ak benn", 12:"fukk ak ñaar", 13:"fukk ak ñett", 14:"fukk ak ñeent", 15:"fukk ak juróom", 16:"fukk ak juróom benn", 17:"fukk ak juróom ñaar", 18:"fukk ak juróom ñett", 19:"fukk ak juróom ñeent"},
    "yiddish": {11:"עלף", 12:"צוועלף", 13:"דרײַצן", 14:"פערצן", 15:"פֿופֿצן", 16:"זעכצן", 17:"זיבעצן", 18:"אַכצן", 19:"נײַנצן"},
    "yoruba": {11:"ọkànlá", 12:"èjìlá", 13:"ètàlá", 14:"ẹ̀rinlá", 15:"ẹ̀dógún", 16:"ẹ̀rìndínlógún", 17:"ètàdínlógún", 18:"èjìdínlógún", 19:"ọkàndínlógún"},
    "cymric": {11:"un ar ddeg", 12:"deuddeg", 13:"tri ar ddeg", 14:"pedwar ar ddeg", 15:"pymtheg", 16:"un ar bymtheg", 17:"dau ar bymtheg", 18:"deunaw", 19:"pedwar ar ddeg"}
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
        
print(f"Batch 2 Repair Complete: {count} languages updated.")
