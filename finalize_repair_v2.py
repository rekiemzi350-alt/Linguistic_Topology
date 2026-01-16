import os

LANG_DIR = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"

# High-Precision Fixes for Stall Points > 10
stalls_to_fix = {
    "albanian": {70: "shtatëdhjetë", 80: "tetëdhjetë", 90: "nëntëdhjetë", 100: "njëqind"},
    "amharic": {40: "አርባ", 50: "ሃምሳ", 60: "สิดสา", 70: "ሰባ", 80: "ሰማንያ", 90: "ዘጠና"},
    "anglo_saxon": {90: "hundnigontig", 100: "hundred"},
    "armenian_eastern": {20: "քսան", 30: "երեսուն", 40: "քառասուն", 50: "հիսուն", 60: "վաթսուն", 70: "յոթանասուն", 80: "ութսուն", 90: "իննสուն"},
    "armenian_western": {40: "քառասուն", 50: "յيسون", 60: "վաթսուն", 70: "եօթանասուն", 80: "ութսուն", 90: "իննսուն"},
    "finnish": {20: "kaksikymmentä", 30: "kolmekymmentä", 40: "neljäkymmentä", 50: "viisikymmentä", 60: "kuusikymmentä", 70: "seitsemänkymmentä", 80: "kahdeksankymmentä", 90: "yhdeksänkymmentä"},
    "thai": {20: "ยี่สิบ", 30: "สามสิบ", 40: "สี่สิบ", 50: "ห้าสิบ", 60: "หกสิบ", 70: "เจ็ดสิบ", 80: "แปดสิบ", 90: "เก้าสิบ"},
    "indonesian": {20: "dua puluh", 30: "tiga puluh", 40: "empat puluh", 50: "lima puluh", 60: "enam puluh", 70: "tujuh puluh", 80: "delapan puluh", 90: "sembilan puluh"},
    "malay": {20: "dua puluh", 30: "tiga puluh", 40: "empat puluh", 50: "lima puluh", 60: "enam puluh", 70: "tujuh puluh", 80: "delapan puluh", 90: "sembilan puluh"},
    "vietnamese": {40: "bốn mươi", 50: "năm mươi", 60: "sáu mươi", 70: "bảy mươi", 80: "tám mươi", 90: "chín mươi"},
    "turkish": {20: "yirmi", 30: "otuz", 40: "kırk", 50: "elli", 60: "altmış", 70: "yetmiş", 80: "seksen", 90: "doksan"},
    "somali": {40: "afartan", 50: "konton", 60: "lixdan", 70: "toddobaatan", 80: "sideettan", 90: "sagaashan"},
    "serbian": {40: "четрдесет", 50: "педесет", 60: "шездесет", 70: "седамдесет", 80: "осамдесет", 90: "деведесет"}
}

def apply_fix(name, fixes):
    path = os.path.join(LANG_DIR, name + ".lang")
    if not os.path.exists(path): return
    with open(path, 'a', encoding='utf-8') as f:
        for k, v in sorted(fixes.items()):
            f.write(f"{k}: {v} # Stall Fix\n")

for name, fixes in stalls_to_fix.items():
    apply_fix(name, fixes)
