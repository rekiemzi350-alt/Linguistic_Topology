# advanced_stylometry_analyzer.py
# An advanced tool for linguistic forensics that attempts to separate a
# translator's introduction from the main body of a text to perform
# differential stylometric analysis.

import sys
import re
import math
from collections import Counter

# --- Configuration ---
INTRO_KEYWORDS = [
    'introduction', 'preface', 'foreword', "translator's note", "translator's preface",
    'contents', 'errata', 'addenda'
]
BODY_START_KEYWORDS = [
    'book i', 'chapter i', 'part i', 'part one', 'canto i'
]

# --- Core Analysis Functions (from the original detector) ---

def get_alpha_weights():
    return {chr(ord('a') + i): i + 1 for i in range(26)}

ALPHA_WEIGHTS = get_alpha_weights()

def get_word_weight(word, weight_map):
    return sum(weight_map.get(char, 0) for char in word.lower())

def generate_fingerprint(text_chunk, name):
    """Computes the statistical fingerprint for a given chunk of text."""
    words = re.findall(r'\b[a-zA-Z]+\b', text_chunk.lower())
    if not words:
        return None

    number_stream = [get_word_weight(word, ALPHA_WEIGHTS) for word in words]
    n = len(number_stream)
    if n < 2: return None # Need at least 2 words to calculate variance

    mean = sum(number_stream) / n
    variance = sum((x - mean) ** 2 for x in number_stream) / n
    std_dev = math.sqrt(variance)
    
    sorted_stream = sorted(number_stream)
    mid = n // 2
    median = (sorted_stream[mid - 1] + sorted_stream[mid]) / 2 if n % 2 == 0 else sorted_stream[mid]
    
    skew = (mean - median) / std_dev if std_dev > 0 else 0

    return {
        "Name": name,
        "Mean Word Weight": mean,
        "Std Deviation": std_dev,
        "Median Word Weight": median,
        "Style Skewness": skew
    }

def print_fingerprint(fp):
    """Prints a formatted fingerprint report."""
    if not fp: return
    print(f"\n--- Fingerprint: {fp['Name']} ---")
    print(f"  > Mean Word Weight:   {fp['Mean Word Weight']:.2f}")
    print(f"  > Style Variance:     {fp['Std Deviation']:.2f}")
    print(f"  > Median Word Weight: {fp['Median Word Weight']:.2f}")
    print(f"  > Style Skewness:     {fp['Style Skewness']:.2f}")

# --- Advanced Differential Analysis ---

def find_split_point(text):
    """
    Uses heuristics to find the likely split point between the introduction
    and the main body of the text.
    """
    lower_text = text.lower()
    last_intro_pos = -1
    
    # Find the last occurrence of any introductory keyword
    for keyword in INTRO_KEYWORDS:
        pos = lower_text.rfind(keyword)
        if pos > last_intro_pos:
            last_intro_pos = pos
            
    # Look for an explicit start of the main body after the last intro keyword
    first_body_pos = -1
    search_area = text[last_intro_pos:] if last_intro_pos != -1 else text
    
    for keyword in BODY_START_KEYWORDS:
        pos = search_area.lower().find(keyword)
        if pos != -1:
            # Adjust position to be absolute
            absolute_pos = pos + (last_intro_pos if last_intro_pos != -1 else 0)
            if first_body_pos == -1 or absolute_pos < first_body_pos:
                first_body_pos = absolute_pos

    if first_body_pos != -1:
        return first_body_pos
        
    # If no body keyword is found, but an intro keyword was, guess the split
    # is some distance after it (e.g., end of paragraph).
    if last_intro_pos != -1:
        # Find the next double newline, a common paragraph break
        para_break = text.find('\n\n', last_intro_pos)
        if para_break != -1:
            return para_break
            
    # Fallback: if no keywords found, split the text 15% of the way in.
    return int(len(text) * 0.15)


def run_advanced_analysis(filepath):
    """Performs the full differential analysis on a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"\nError: File not found at '{filepath}'")
        return

    split_point = find_split_point(full_text)
    
    intro_text = full_text[:split_point]
    body_text = full_text[split_point:]
    
    print(f"\n========================================================")
    print(f"ADVANCED ANALYSIS: {filepath}")
    print(f"Detected split @ ~{int((split_point / len(full_text)) * 100)}% into the document.")
    print(f"========================================================")
    
    intro_fp = generate_fingerprint(intro_text, "Translator's Introduction (PRESUMED)")
    body_fp = generate_fingerprint(body_text, "Main Body (PRESUMED)")
    
    if not intro_fp or not body_fp:
        print("\nCould not generate one or both fingerprints. The text may be too short or lack clear structure.")
        return
        
    print_fingerprint(intro_fp)
    print_fingerprint(body_fp)
    
    # --- Calculate Stylistic Distance ---
    # A simple Euclidean distance between the two fingerprint vectors
    
    vec1 = [intro_fp['Mean Word Weight'], intro_fp['Std Deviation'], intro_fp['Median Word Weight']]
    vec2 = [body_fp['Mean Word Weight'], body_fp['Std Deviation'], body_fp['Median Word Weight']]
    
    distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))
    
    print("\n--- BIAS ANALYSIS ---")
    print(f"  > Stylistic Distance: {distance:.2f}")
    print("  > Interpretation:")
    if distance > 10:
        print("    A HIGH distance suggests the main body's style is very different from the translator's.")
        print("    This implies a strong 'ghost' of the original author's style may be present.")
    elif distance > 3:
        print("    A MODERATE distance suggests a mix of translator and author style.")
    else:
        print("    A LOW distance suggests the translator's style heavily dominates the main work.")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python advanced_stylometry_analyzer.py <file1.txt> [file2.txt] ...")
        print("Description: Performs a differential analysis by splitting a text into 'introduction' and 'main body' to detect translator bias.")
    else:
        for filepath in sys.argv[1:]:
            run_advanced_analysis(filepath)
