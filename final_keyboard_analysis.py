import sys
import re
import math

# --- Language Mappings (Alphabet Bitcodes) ---

def get_english_weights():
    # a=1, b=2, ... z=26
    return {chr(ord('a') + i): i + 1 for i in range(26)}

def get_arabic_weights():
    # Standard Arabic Alphabet (28 letters)
    arabic_chars = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
    weights = {}
    for i, char in enumerate(arabic_chars):
        weights[char] = i + 1
    
    # Handling common variations / extras
    extras = {
        'أ': 1, 'إ': 1, 'آ': 1, 'ء': 1, 'ؤ': 1, 'ئ': 1, # Alif/Hamza variants -> 1
        'ة': 26, # Ta Marbuta -> often treated like Ha (26) or Ta (3)
        'ى': 28, # Alif Maqsura -> Ya (28)
    }
    weights.update(extras)
    return weights

def analyze_document(filepath, weight_map, script_regex, label):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().lower()
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return None

    words = re.findall(script_regex, text)
    if not words: return None

    word_weights = []
    for word in words:
        weight = sum(weight_map.get(c, 0) for c in word)
        if weight > 0:
            word_weights.append(weight)

    if not word_weights: return None

    n = len(word_weights)
    mean = sum(word_weights) / n
    variance = sum((x - mean) ** 2 for x in word_weights) / n
    std_dev = math.sqrt(variance)
    sorted_w = sorted(word_weights)
    mid = n // 2
    median = (sorted_w[mid-1] + sorted_w[mid]) / 2 if n % 2 == 0 else sorted_w[mid]
    skew = (mean - median) / std_dev if std_dev > 0 else 0

    print(f"\n--- {label} (Bitcode Analysis) ---")
    print(f"  > Mean Word Weight:   {mean:.2f}")
    print(f"  > Weight Deviation:   {std_dev:.2f}")
    print(f"  > Median Weight:      {median:.2f}")
    print(f"  > Style Skewness:     {skew:.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python final_keyboard_analysis.py <lang: eng|ara> <file>")
        sys.exit(1)
        
    lang = sys.argv[1]
    file = sys.argv[2]
    
    if lang == "eng":
        analyze_document(file, get_english_weights(), r'[a-z]+', "ENGLISH TRANSLATION")
    elif lang == "ara":
        analyze_document(file, get_arabic_weights(), r'[\u0600-\u06FF]+', "ARABIC ORIGINAL")