# Setup Language Files with correct Unicode

def create_sumerian():
    # Cuneiform Unicode Points
    # 1: DISH (U+12079), 2: MIN (U+1222B), 3: ESH (U+120E7)
    # 4: LIMMU (U+121F4), 5: IA (U+1214A), 6: ASH (U+1203E)
    # 7: IMIN (U+12153), 8: USSU (U+12335), 9: ILIMMU (U+12154)
    # 10: U (U+1230B), 20: NISH (U+12299), 30: USHU (U+1230D)
    # 40: NIMIN (U+12250), 50: NINNU (U+12258)
    # 60: GESH (U+1211E)
    
    # Using hex escapes for safety
    content = """# Language Definition for Ancient Sumerian
# Method: Cuneiform Sign Count (Base 60)

name: Ancient Sumerian

# --- Units 1-9 ---
1: \U00012079
2: \U0001222B
3: \U000120E7
4: \U000121F4
5: \U0001214A
6: \U0001203E
7: \U00012153
8: \U00012335
9: \U00012154

# --- Tens 10-50 ---
10: \U0001230B
20: \U00012299
30: \U0001230D
40: \U00012250
50: \U00012258

# --- Sixty ---
60: \U0001211E
"""
    with open("sumerian.lang", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created sumerian.lang")

def create_german():
    content = """# Language Definition for German

name: German

# --- Direct Numbers 0-19 ---
0: null
1: eins
2: zwei
3: drei
4: vier
5: fünf
6: sechs
7: sieben
8: acht
9: neun
10: zehn
11: elf
12: zwölf
13: dreizehn
14: vierzehn
15: fünfzehn
16: sechzehn
17: siebzehn
18: achtzehn
19: neunzehn

# --- Tens ---
20: zwanzig
30: dreißig
40: vierzig
50: fünfzig
60: sechzig
70: siebzig
80: achtzig
90: neunzig

# --- Keywords ---
hundred: hundert
ten_sep: und
"""
    with open("german.lang", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created german.lang")

def create_french():
    content = """# Language Definition for French

name: French

# --- Direct Numbers 0-19 ---
0: zéro
1: un
2: deux
3: trois
4: quatre
5: cinq
6: six
7: sept
8: huit
9: neuf
10: dix
11: onze
12: douze
13: treize
14: quatorze
15: quinze
16: seize
17: dix-sept
18: dix-huit
19: dix-neuf

# --- Tens ---
20: vingt
30: trente
40: quarante
50: cinquante
60: soixante
70: soixante-dix
80: quatre-vingts
90: quatre-vingt-dix

# --- Keywords ---
hundred: cent
ten_sep: -
# Note: French 21 is 'vingt et un', others 'vingt-deux'. 
# The app's generic logic might need tweaks for 'et' vs '-', but we'll stick to basic structure.
# Validating 'et' as separator might fail if 'ten_sep' is strictly one string.
# We will use '-' for now as it covers most cases.
"""
    with open("french.lang", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created french.lang")

def create_spanish():
    content = """# Language Definition for Spanish

name: Spanish

# --- Direct Numbers 0-19 ---
0: cero
1: uno
2: dos
3: tres
4: cuatro
5: cinco
6: seis
7: siete
8: ocho
9: nueve
10: diez
11: once
12: doce
13: trece
14: catorce
15: quince
16: dieciséis
17: diecisiete
18: dieciocho
19: diecinueve

# --- Tens ---
20: veinte
30: treinta
40: cuarenta
50: cincuenta
60: sesenta
70: setenta
80: ochenta
90: noventa

# --- Keywords ---
hundred: ciento
hundred_sep:  
ten_sep: y

# --- Overrides ---
100: cien
"""
    with open("spanish.lang", "w", encoding="utf-8") as f:
        f.write(content)
    print("Created spanish.lang")

if __name__ == "__main__":
    create_sumerian()
    create_german()
    create_french()
    create_spanish()
