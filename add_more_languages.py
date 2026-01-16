# Language Definitions for new languages

def create_russian():
    content = """# Language Definition for Russian
name: Russian

# --- Direct Numbers 0-19 ---
0: ноль
1: один
2: два
3: три
4: четыре
5: пять
6: шесть
7: семь
8: восемь
9: девять
10: десять
11: одиннадцать
12: двенадцать
13: тринадцать
14: четырнадцать
15: пятнадцать
16: шестнадцать
17: семнадцать
18: восемнадцать
19: девятнадцать

# --- Tens ---
20: двадцать
30: тридцать
40: сорок
50: пятьдесят
60: шестьдесят
70: семьдесят
80: восемьдесят
90: девяносто

# --- Keywords ---
hundred: сто
ten_sep:  
"""
    with open("russian.lang", "w", encoding="utf-8") as f:
        f.write(content)

def create_italian():
    content = """# Language Definition for Italian
name: Italian

# --- Direct Numbers 0-19 ---
0: zero
1: uno
2: due
3: tre
4: quattro
5: cinque
6: sei
7: sette
8: otto
9: nove
10: dieci
11: undici
12: dodici
13: tredici
14: quattordici
15: quindici
16: sedici
17: diciassette
18: diciotto
19: diciannove

# --- Tens ---
20: venti
30: trenta
40: quaranta
50: cinquanta
60: sessanta
70: settanta
80: ottanta
90: noventa

# --- Keywords ---
hundred: cento
ten_sep: 
# Note: Italian drops vowel for 1 and 8, handled in app logic usually.
# But for now we use basic additive.
"""
    with open("italian.lang", "w", encoding="utf-8") as f:
        f.write(content)

def create_hebrew():
    content = """# Language Definition for Hebrew
name: Hebrew

# --- Direct Numbers 0-19 (Feminine Absolute) ---
0: אפס
1: אחת
2: שתים
3: שלוש
4: ארבע
5: חמש
6: שש
7: שבע
8: שמונה
9: תשע
10: עשר
11: אחת עשרה
12: שתים עשרה
13: שלוש עשרה
14: ארבע עשרה
15: חמש עשרה
16: שש עשרה
17: שבע עשרה
18: שמונה עשרה
19: תשע עשרה

# --- Tens ---
20: עשרים
30: שלושים
40: ארבעים
50: חמשים
60: ששים
70: שבעים
80: שמונים
90: תשעים

# --- Keywords ---
hundred: מאה
ten_sep: ו
"""
    with open("hebrew.lang", "w", encoding="utf-8") as f:
        f.write(content)

def create_japanese():
    content = """# Language Definition for Japanese
name: Japanese

# --- Direct Numbers 0-19 (Hiragana) ---
0: ぜろ
1: いち
2: に
3: さん
4: よん
5: ご
6: ろく
7: なな
8: はち
9: きゅう
10: じゅう
11: じゅういち
12: じゅうに
13: じゅうさん
14: じゅうよん
15: じゅうご
16: じゅうろく
17: じゅうなな
18: じゅうはち
19: じゅうきゅう

# --- Tens ---
20: にじゅう
30: さんじゅう
40: よんじゅう
50: ごじゅう
60: ろくじゅう
70: ななじゅう
80: はちじゅう
90: きゅうじゅう

# --- Keywords ---
hundred: ひゃく
ten_sep: 
"""
    with open("japanese.lang", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    create_russian()
    create_italian()
    create_hebrew()
    create_japanese()
    print("Added Russian, Italian, Hebrew, and Japanese .lang files.")
