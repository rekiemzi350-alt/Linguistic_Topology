import os
# author_fingerprint_analyzer.py
# A tool to compute the "Topological Fingerprint" of a text based on
# the alphabetical weighting of its words. This is a novel stylometric method
# proposed by Erik Mize to test for authorship signals across translations.

import sys
import re
import math
from collections import Counter

# --- 1. Weighting System ---

def get_alpha_weights():
    """Generates the dictionary for alphabetical weights (a=1, b=2...)."""
    return {chr(ord('a') + i): i + 1 for i in range(26)}

ALPHA_WEIGHTS = get_alpha_weights()

def get_word_weight(word, weight_map):
    """Calculates the total alphabetical weight of a word."""
    return sum(weight_map.get(char, 0) for char in word.lower())

# --- 2. Fingerprint Generation ---

def generate_fingerprint(filepath):
    """Reads a text file and computes its statistical fingerprint with extreme precision."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except FileNotFoundError:
        return None

    # 1. Word Analysis
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    if not words: return None
    
    number_stream = [get_word_weight(word, ALPHA_WEIGHTS) for word in words]
    n = len(number_stream)
    
    mean = sum(number_stream) / n
    variance = sum((x - mean) ** 2 for x in number_stream) / n
    std_dev = math.sqrt(variance)
    
    # 2. Syntactic Friction (Sentence Length Variance)
    sentences = re.split(r'[.!?]+', text)
    sent_lengths = [len(s.split()) for s in sentences if len(s.split()) > 3]
    if sent_lengths:
        avg_sent = sum(sent_lengths) / len(sent_lengths)
        sent_friction = math.sqrt(sum((x - avg_sent) ** 2 for x in sent_lengths) / len(sent_lengths))
    else:
        avg_sent, sent_friction = 0, 0

    # 3. Zipf Distribution (Vocabulary Richness)
    counts = Counter(words).most_common(100)
    # Simple Zipf proxy: correlation of frequency to rank
    # (Simplified for fingerprint)
    zipf_coeff = sum(1/i for i in range(1, len(counts)+1)) / len(counts) if counts else 0

    fingerprint = {
        "File": filepath,
        "Mean Word Weight": mean,
        "Style Volatility (SD)": std_dev,
        "Syntactic Friction": sent_friction,
        "Avg Sentence Length": avg_sent,
        "Vocabulary Density": zipf_coeff
    }
    
    return fingerprint

def print_fingerprint(fp):
    """Prints a formatted high-precision fingerprint report."""
    if not fp: return
    
    print(f"\n--- AUTHOR FINGERPRINT: {os.path.basename(fp['File'])} ---")
    print(f"  > Weight Center:    {fp['Mean Word Weight']:.4f}")
    print(f"  > Style Volatility: {fp['Style Volatility (SD)']:.4f}")
    print(f"  > Syntactic Friction: {fp['Syntactic Friction']:.4f}")
    print(f"  > Sentence Avg:     {fp['Avg Sentence Length']:.2f}")
    print(f"  > Vocab Density:    {fp['Vocabulary Density']:.4f}")
    print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python author_fingerprint_analyzer.py <file1.txt> [file2.txt] ...")
        print("Description: Analyzes text files to generate a 'Topological Fingerprint' for each.")
        print("This can be used to compare writing styles, even across translations.")
    else:
        import segment_text
        print("Generating authorial fingerprints...")
        
        for filepath in sys.argv[1:]:
            print(f"\n[{os.path.basename(filepath)}]")
            
            # Auto-Segment first
            segments = []
            try:
                segments = segment_text.segment_file(filepath)
            except Exception as e:
                print(f"Segmentation warning: {e}")
            
            if segments and len(segments) > 1:
                print(f"Auto-Segmentation Active: Analyzing {len(segments)} isolated sections...")
                print("*" * 60)
                
                # Analyze segments
                for seg_path in segments:
                    # Optional: Clean up name for display
                    seg_name = os.path.basename(seg_path)
                    fingerprint = generate_fingerprint(seg_path)
                    if fingerprint:
                        print_fingerprint(fingerprint)
            else:
                # Fallback to original if no distinct segments found
                print("No distinct bias sections found. Analyzing full text...")
                fingerprint = generate_fingerprint(filepath)
                if fingerprint:
                    print_fingerprint(fingerprint)
                    
            print("=" * 60)
