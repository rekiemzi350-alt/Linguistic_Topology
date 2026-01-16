import sys
import re
import math

# --- English Tech Mapping (Bit-Velocity) ---
# We use this to measure the "Physical Entropy" of the English text.
BIT_MAP = {
    'f': 2, 'j': 2, 'd': 3, 'k': 3, 's': 3, 'l': 3, 
    'a': 4, 'g': 4, 'h': 4, ';': 4, "'": 4,
    'r': 4, 'u': 4, 'e': 5, 'i': 5, 'w': 5, 'o': 5, 
    't': 5, 'y': 5, 'q': 6, 'p': 6, '[': 6, ']': 6,
    'v': 5, 'm': 5, 'c': 6, 'n': 6, 'x': 6, 
    'b': 6, 'z': 6, ',': 6, '.': 6, '/': 6,
    ' ': 1 # Space is very fast (1 bit)
}

def get_word_weight(word):
    # Calculate the total bit-cost of typing the word
    return sum(BIT_MAP.get(c, 8) for c in word.lower())

def analyze_segment(text_segment):
    words = re.findall(r'[a-z]+', text_segment.lower())
    if len(words) < 3: return None # Too short to analyze
    
    weights = [get_word_weight(w) for w in words]
    
    mean = sum(weights) / len(weights)
    variance = sum((x - mean) ** 2 for x in weights) / len(weights)
    std_dev = math.sqrt(variance)
    
    # Coefficient of Variation (CV) is our "Fingerprint"
    # Ancient (Hebrew/Aramaic) ~ 0.20 - 0.30
    # Modern (English) ~ 0.55 - 0.65
    cv = std_dev / mean if mean > 0 else 0
    return cv

def scan_document(filepath):
    print(f"\n--- HOAX SCANNER REPORT: {filepath} ---")
    print(f"{'SEGMENT (First 50 chars)':<55} | {'CV SCORE':<10} | {'VERDICT'}")
    print("-" * 85)
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        
    # Split into sentences or paragraphs
    segments = re.split(r'(?<=[.!?])\s+', text)
    
    ancient_count = 0
    modern_count = 0
    
    for seg in segments:
        seg = seg.strip()
        if not seg: continue
        
        cv = analyze_segment(seg)
        if cv is None: continue
        
        # Classification Logic
        # Adjusted thresholds based on our previous findings
        if cv < 0.45:
            verdict = "ANCIENT (Likely Source)"
            ancient_count += 1
        elif cv > 0.55:
            verdict = "MODERN (English/Hoax?)"
            modern_count += 1
        else:
            verdict = "MIXED / TRANSITIONAL"
            
        print(f"{seg[:50].replace(chr(10), ' '):<55} | {cv:.4f}     | {verdict}")

    print("-" * 85)
    print(f"SUMMARY:")
    print(f"  > Ancient/Faithful Sections: {ancient_count}")
    print(f"  > Modern/Suspicious Sections: {modern_count}")
    if modern_count > ancient_count:
        print("\n[!] WARNING: Document shows predominantly MODERN structural variance.")
        print("    View with SKEPTICISM if it claims to be a direct ancient translation.")
    else:
        print("\n[OK] Document retains significant ANCIENT structural characteristics.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hoax_scanner.py <text_file>")
    else:
        scan_document(sys.argv[1])
