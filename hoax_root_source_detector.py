# stylometric_analyzer.py
# A basic tool for linguistic forensics to identify potential authorship or translation artifacts.

import sys
import re
from collections import Counter

# --- Configuration ---
# Function words are often language-specific and used unconsciously by native speakers.
# We will check the frequency of some common English function words.
ENGLISH_FUNCTION_WORDS = [
    'the', 'a', 'an', 'in', 'on', 'at', 'of', 'to', 'for', 'with', 'and', 'but', 'or', 'is', 'are', 'was', 'were'
]

def analyze_text(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().lower()
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        return

    # 1. Tokenize the text (split into words)
    words = re.findall(r'\b[a-z]+\b', text)
    if not words:
        print("No words found in the text.")
        return

    total_words = len(words)
    word_counts = Counter(words)

    # 2. Vocabulary Richness (Type-Token Ratio)
    # A simple measure of how many unique words are used.
    # Translations or texts by non-native speakers sometimes have lower TTR.
    unique_words = len(word_counts)
    ttr = (unique_words / total_words) * 100 if total_words > 0 else 0

    # 3. Function Word Frequency
    # How often do common "glue" words appear? This is a strong stylistic fingerprint.
    function_word_count = sum(word_counts.get(fw, 0) for fw in ENGLISH_FUNCTION_WORDS)
    function_word_freq = (function_word_count / total_words) * 100 if total_words > 0 else 0
    
    # 4. Sentence Analysis
    # Split text into sentences. A simple regex for sentence boundaries.
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    num_sentences = len(sentences)
    
    if num_sentences > 0:
        # Average sentence length
        avg_sentence_len = total_words / num_sentences
        
        # Sentence length variance (a measure of sentence structure complexity)
        sentence_lengths = [len(re.findall(r'\b[a-z]+\b', s)) for s in sentences]
        mean_len = sum(sentence_lengths) / num_sentences
        variance = sum((l - mean_len) ** 2 for l in sentence_lengths) / num_sentences
    else:
        avg_sentence_len = 0
        variance = 0

    # --- Print Report ---
    print(f"\n--- STYLOMETRIC ANALYSIS: {filepath} ---")
    print(f"Total Words: {total_words}")
    print(f"Unique Words: {unique_words}")
    print("-" * 40)
    print(f"Vocabulary Richness (TTR): {ttr:.2f}%")
    print(f"Function Word Frequency:   {function_word_freq:.2f}% (e.g., 'the', 'a', 'of')")
    print(f"Average Sentence Length:   {avg_sentence_len:.2f} words")
    print(f"Sentence Length Variance:  {variance:.2f} (Higher means more complex structures)")
    print("-" * 40)
    print("\nInterpretation:")
    print("- Native English often has a TTR between 40-50% and high sentence variance.")
    print("- Hoaxes or texts by non-native speakers may show lower TTR, anomalous function word frequencies, and lower sentence variance.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python stylometric_analyzer.py <path_to_text_file.txt>")
        print("This tool performs a basic stylometric analysis on a text file to identify linguistic patterns.")
    else:
        analyze_text(sys.argv[1])
