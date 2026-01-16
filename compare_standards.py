import os
import re
import math

def get_word_weight(word):
    return sum(ord(c) - 96 for c in word.lower() if 'a' <= c <= 'z')

def analyze(filepath):
    if not os.path.exists(filepath): return None
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    words = re.findall(r'[a-zA-Z]+', text)
    if not words: return None
    weights = [get_word_weight(w) for w in words if len(w) > 1]
    mean = sum(weights) / len(weights)
    variance = sum((x - mean)**2 for x in weights) / len(weights)
    return {"mean": mean, "std": math.sqrt(variance), "count": len(weights)}

sd_path = "/data/data/com.termux/files/home/coffee/test_documents/Secret_Doctrine_Vol1.txt"
modern_path = "/data/data/com.termux/files/home/coffee/test_documents/the_QURAN-abdel-haleem-ebook-english.txt"

sd_stats = analyze(sd_path)
modern_stats = analyze(modern_path)

print("=== HISTORICAL VS MODERN TRANSLATION STANDARDS ===")
if sd_stats:
    print(f"Secret Doctrine (1888/1893): Mean={sd_stats['mean']:.2f}, StdDev={sd_stats['std']:.2f}")
if modern_stats:
    print(f"Modern Quran (Abdel Haleem): Mean={modern_stats['mean']:.2f}, StdDev={modern_stats['std']:.2f}")

if sd_stats and modern_stats:
    diff = abs(sd_stats['mean'] - modern_stats['mean'])
    print(f"Linguistic Weight Delta: {diff:.4f}")
    if diff > 2.0:
        print("Conclusion: Significant shift in translation weight detected over 130 years.")
    else:
        print("Conclusion: Consistent linguistic weights maintained across historical/modern standards.")
