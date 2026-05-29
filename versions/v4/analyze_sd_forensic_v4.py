import os
import re
import math
import json

# Configuration
INPUT_DIR = "/data/data/com.termux/files/home/coffee/test_documents/"
OUTPUT_DIR = "/data/data/com.termux/files/home/coffee/test_results/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

REBEL_SEEDS = {83, 84, 93, 94}

def get_word_weight(word):
    return sum(ord(c) - 96 for c in word.lower() if 'a' <= c <= 'z')

def calculate_unity(stream, window=1000):
    """Calculates convergence velocity / unity of a number stream."""
    if len(stream) < window: return 0.0
    # Unity is defined here as 1 - CV (Coefficient of Variation)
    # As the stream converges, variance should stabilize.
    sample = stream[:window]
    mean = sum(sample) / len(sample)
    variance = sum((x - mean)**2 for x in sample) / len(sample)
    if mean == 0: return 0.0
    cv = math.sqrt(variance) / mean
    return max(0.0, 1.0 - cv)

def analyze_forensic(text, label):
    sentences = re.split(r'(?<=[.!?]["”])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
    
    if not sentences: return None
    
    seeds = []
    word_counts = []
    weights = []
    waveform = [] # 1 for even, -1 for odd (peak/valley) 
    
    for s in sentences:
        letters = re.sub(r'[^a-zA-Z]', '', s)
        words = s.split()
        if not words: continue
        
        seed = len(letters)
        seeds.append(seed)
        word_counts.append(len(words))
        waveform.append(1 if seed % 2 == 0 else -1)
        
        for w in words:
            wt = get_word_weight(w)
            if wt > 0: weights.append(wt)
            
    mean_weight = sum(weights) / len(weights) if weights else 0
    unity = calculate_unity(weights)
    
    return {
        "label": label,
        "count": len(sentences),
        "avg_words": sum(word_counts) / len(word_counts),
        "rebel_rate": sum(1 for s in seeds if s in REBEL_SEEDS) / len(seeds) * 100,
        "mean_weight": mean_weight,
        "unity": unity,
        "waveform_balance": sum(waveform) / len(waveform) # Near 0 is balanced
    }

def run_sd_full_v4():
    volumes = [
        "Secret_Doctrine_Vol1.txt",
        "Secret_Doctrine_Vol2.txt",
        "Secret_Doctrine_Vol3.txt",
        "Secret_Doctrine_Vol4.txt"
    ]
    
    reports = []
    
    for vol in volumes:
        path = os.path.join(INPUT_DIR, vol)
        if not os.path.exists(path): continue
        
        print(f"Deep Forensic Analysis: {vol}")
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Split into broad categories using regex
        preface_match = re.search(r'PREFACE.*?(?=INTRODUCTORY|PROEM|PART I)', content, re.S | re.I)
        intro_match = re.search(r'INTRODUCTORY.*?(?=PROEM|PART I)', content, re.S | re.I)
        
        # Quotes: anything inside " " or “ ” or indented blocks
        # We'll extract all quotes and the remainder as "Main"
        quotes = re.findall(r'["“].*?["”]', content, re.S)
        main_text = re.sub(r'["“].*?["”]', '', content, flags=re.S)
        
        reports.append(analyze_forensic(content, f"{vol} - FULL"))
        if preface_match:
            reports.append(analyze_forensic(preface_match.group(), f"{vol} - PREFACE"))
        if intro_match:
            reports.append(analyze_forensic(intro_match.group(), f"{vol} - INTRO"))
        
        reports.append(analyze_forensic(" ".join(quotes), f"{vol} - QUOTES"))
        reports.append(analyze_forensic(main_text, f"{vol} - MAIN (NO QUOTES)"))

    # Final Summary Report
    reports = [r for r in reports if r is not None]
    report_path = os.path.join(OUTPUT_DIR, "SD_V4_Final_Forensic.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=== THE SECRET DOCTRINE: V4 COMPREHENSIVE FORENSIC REPORT ===\n\n")
        f.write(f"{ 'Section Label':<40} | { 'Sents':<7} | { 'Words':<5} | { 'Rebel%':<7} | { 'Weight':<7} | { 'Unity':<7} | {'Wave'}\n")
        f.write("-" * 100 + "\n")
        
        for r in reports:
            if not r: continue
            f.write(f"{r['label']:<40} | {r['count']:<7} | {r['avg_words']:<5.1f} | {r['rebel_rate']:<7.2f} | {r['mean_weight']:<7.2f} | {r['unity']:<7.4f} | {r['waveform_balance']:+.4f}\n")
            
        f.write("\n=== HOAX DETECTION SUMMARY ===\n")
        # Compare Vol 1 Main vs Vol 1 Quotes
        v1_main = next((r for r in reports if "Vol1" in r['label'] and "MAIN" in r['label']), None)
        v1_quote = next((r for r in reports if "Vol1" in r['label'] and "QUOTES" in r['label']), None)
        
        if v1_main and v1_quote:
            diff = abs(v1_main['mean_weight'] - v1_quote['mean_weight'])
            f.write(f"Weight Distance (Vol 1): {diff:.4f}\n")
            if diff < 0.2:
                f.write("Result: Style identity detected. High risk of author rewrite/hoax.\n")
            else:
                f.write("Result: Stylistic distinctiveness preserved.\n")

    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    run_sd_full_v4()
