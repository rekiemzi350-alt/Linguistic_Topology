import os
import re
import nltk
from collections import Counter
import math
import json

# Ensure NLTK data is available
# (Already checked in previous step)

def get_word_weight(word):
    return sum(ord(c) - 96 for c in word.lower() if 'a' <= c <= 'z')

def calculate_unity(stream):
    if not stream: return 0.0
    mean = sum(stream) / len(stream)
    if mean == 0: return 0.0
    variance = sum((x - mean)**2 for x in stream) / len(stream)
    cv = math.sqrt(variance) / mean
    return max(0.0, 1.0 - cv)

def analyze_text_extreme(text, label):
    if not text or len(text.strip()) < 100:
        return None

    # Tokenize
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)
    words_alpha = [w.lower() for w in words if w.isalpha()]
    
    if not words_alpha: return None

    # POS Tagging
    tagged = nltk.pos_tag(words, tagset='universal')
    pos_counts = Counter(tag for word, tag in tagged)
    total_pos = sum(pos_counts.values())
    
    # Stylometry
    ttr = len(set(words_alpha)) / len(words_alpha) if words_alpha else 0
    avg_sent_len = len(words) / len(sentences) if sentences else 0
    
    # Topology Waveform (Even=1, Odd=-1)
    # Based on sentence lengths (in characters, excluding whitespace)
    waveform = []
    for s in sentences:
        clean_s = re.sub(r'\s+', '', s)
        length = len(clean_s)
        waveform.append(1 if length % 2 == 0 else -1)
    
    balance = sum(waveform) / len(waveform) if waveform else 0
    
    # Weights
    weights = [get_word_weight(w) for w in words_alpha]
    unity = calculate_unity(weights)

    return {
        "Label": label,
        "Word Count": len(words),
        "Sentence Count": len(sentences),
        "TTR (Vocabulary Richness)": ttr,
        "Avg Sentence Length": avg_sent_len,
        "Noun Density": pos_counts.get('NOUN', 0) / total_pos,
        "Verb Density": pos_counts.get('VERB', 0) / total_pos,
        "Adj Density": pos_counts.get('ADJ', 0) / total_pos,
        "Adv Density": pos_counts.get('ADV', 0) / total_pos,
        "Unity (Convergence)": unity,
        "Waveform Balance": balance
    }

def process_volumes():
    input_dir = "test_documents"
    volumes = ["Secret_Doctrine_Vol1.txt", "Secret_Doctrine_Vol2.txt", "Secret_Doctrine_Vol3.txt", "Secret_Doctrine_Vol4.txt"]
    
    full_report = {}

    for vol in volumes:
        path = os.path.join(input_dir, vol)
        if not os.path.exists(path):
            print(f"Skipping {vol}, file not found.")
            continue
            
        print(f"Processing {vol}...")
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Section Extraction
        preface_match = re.search(r'PREFACE.*?(?=INTRODUCTORY|PROEM|PART I)', content, re.S | re.I)
        intro_match = re.search(r'INTRODUCTORY.*?(?=PROEM|PART I)', content, re.S | re.I)
        
        # Quote Extraction (simplified)
        quotes = re.findall(r'["“].*?["”]', content, re.S)
        main_text = re.sub(r'["“].*?["”]', '', content, flags=re.S)

        vol_data = {}
        vol_data["Full"] = analyze_text_extreme(content, f"{vol} Full")
        vol_data["Preface"] = analyze_text_extreme(preface_match.group(), f"{vol} Preface") if preface_match else None
        vol_data["Intro"] = analyze_text_extreme(intro_match.group(), f"{vol} Intro") if intro_match else None
        vol_data["Quotes"] = analyze_text_extreme(" ".join(quotes), f"{vol} Quotes") if quotes else None
        vol_data["Main"] = analyze_text_extreme(main_text, f"{vol} Main (No Quotes)")
        
        full_report[vol] = vol_data

    # Output Report
    report_path = "test_results/sd_extreme_forensic_report.json"
    os.makedirs("test_results", exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(full_report, f, indent=4)
    
    print(f"\nExtremely precise forensic report saved to {report_path}")

    # Print a summary comparison for Vol 1
    if "Secret_Doctrine_Vol1.txt" in full_report:
        v1 = full_report["Secret_Doctrine_Vol1.txt"]
        print("\n--- Summary Comparison (Volume 1) ---")
        for section in ["Preface", "Intro", "Quotes", "Main"]:
            data = v1.get(section)
            if data:
                print(f"\nSection: {section}")
                print(f"  Noun Density: {data['Noun Density']:.4f}")
                print(f"  Verb Density: {data['Verb Density']:.4f}")
                print(f"  Unity:        {data['Unity (Convergence)']:.4f}")
                print(f"  Waveform Bal: {data['Waveform Balance']:.4f}")

if __name__ == "__main__":
    process_volumes()