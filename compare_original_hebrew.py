import math
import re

# Hebrew Weights (Standard Aleph=1... Tav=22)
HEB_STD = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    'כ': 11, 'ל': 12, 'מ': 13, 'נ': 14, 'ס': 15, 'ע': 16, 'פ': 17, 'צ': 18, 'ק': 19, 'ר': 20, 'ש': 21, 'ת': 22,
    'ך': 11, 'ם': 13, 'ן': 14, 'ף': 17, 'ץ': 18
}

def analyze_hebrew(word_list):
    std_weights = []
    tech_weights = []
    
    for word in word_list:
        s_w = sum(HEB_STD.get(c, 0) for c in word)
        if s_w > 0: std_weights.append(s_w)
        
        t_w = len(word) * 8
        if t_w > 0: tech_weights.append(t_w)
        
    return std_weights, tech_weights

def get_stats(weights):
    if not weights: return 0, 0
    mean = sum(weights) / len(weights)
    variance = sum((x - mean) ** 2 for x in weights) / len(weights)
    return mean, math.sqrt(variance)

# Extract words from biblical_hebrew.lang
words = []
try:
    with open("biblical_hebrew.lang", "r", encoding="utf-8") as f:
        for line in f:
            if ':' in line and not line.strip().startswith(('name', '#', 'hundred', 'ten_sep', 'hundred_sep')):
                val = line.split(':', 1)[1].strip()
                clean_val = "".join(re.findall(r'[\u0590-\u05FF]', val))
                if clean_val: words.append(clean_val)

    std_ws, tech_ws = analyze_hebrew(words)

    m_s, d_s = get_stats(std_ws)
    m_t, d_t = get_stats(tech_ws)

    print(f"--- Analysis of Original Biblical Hebrew ({len(words)} words) ---")
    print(f"Standard (Gematria Values): Mean={m_s:.2f}, StdDev={d_s:.2f}, CV={d_s/m_s:.4f}")
    print(f"Tech (Bitcode/Word Len):    Mean={m_t:.2f}, StdDev={d_t:.2f}, CV={d_t/m_t:.4f}")

    if (d_s/m_s) > (d_t/m_t):
        print("\nConclusion: The Standard Language File is MORE accurate for the original language.")
    else:
        print("\nConclusion: The Tech Language File is MORE accurate for the original language.")
except Exception as e:
    print(f"Error: {e}")
