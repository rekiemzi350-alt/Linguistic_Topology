import math
import re

# Standard English (A=1, B=2...)
STD_WEIGHTS = {chr(ord('a') + i): i + 1 for i in range(26)}

def analyze(text, method="std"):
    words = re.findall(r'[a-z]+', text.lower())
    weights = []
    for w in words:
        if method == "std":
            weight = sum(STD_WEIGHTS.get(c, 0) for c in w)
        else: # tech (English)
            # English Tech is length * 8
            weight = len(w) * 8
        if weight > 0: weights.append(weight)
        
    if not weights: return 0, 0
    
    mean = sum(weights) / len(weights)
    variance = sum((x - mean) ** 2 for x in weights) / len(weights)
    std_dev = math.sqrt(variance)
    return mean, std_dev

try:
    with open("talmud_sample.txt", "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    m_std, s_std = analyze(text, "std")
    m_tech, s_tech = analyze(text, "tech")

    print(f"--- Analysis of Talmud Translation ---")
    print(f"Standard (Letter Values):   Mean={m_std:.2f}, StdDev={s_std:.2f}")
    print(f"    -> Coeff of Variation:  {s_std/m_std:.4f}")
    print(f"Tech (Bitcode/Word Len):    Mean={m_tech:.2f}, StdDev={s_tech:.2f}")
    print(f"    -> Coeff of Variation:  {s_tech/m_tech:.4f}")

    print("\nObservation:")
    if (s_std/m_std) > (s_tech/m_tech):
        print("The Standard Language File (Letter Values) provides significantly higher distinctiveness (Entropy).")
        print("For detecting stylistic fingerprints in English translations, the NORMAL file is more accurate.")
    else:
        print("The Tech Language File provides higher distinctiveness.")
except Exception as e:
    print(f"Error: {e}")
