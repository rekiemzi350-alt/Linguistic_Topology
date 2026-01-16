import sys
import os
import math
import csv
import nltk
from collections import Counter

def parse_lang_file(lang_filepath):
    """Loads letter values from a .lang file."""
    values = {}
    with open(lang_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or ':' not in line or line.startswith('name'):
                continue
            key, val = line.split(':', 1)
            key = key.strip()
            if key.isdigit():
                # For alphabetic numeral systems like Coptic/Greek
                # The "value" is the number, the "name" is the letter
                # But for topology, we want the *character's* value, not what it represents.
                # This requires a different mapping. For now, we use unicode value as a proxy.
                pass # This part is for the convergence engine, not fingerprinting.

    # If the lang file doesn't define explicit weights, fall back to unicode value
    # This is a neutral way to assign a unique value to each character.
    # We will use the lang file to identify valid characters.
    valid_chars = set()
    with open(lang_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or ':' not in line: continue
            _, val = line.split(':', 1)
            val = val.split('#')[0].strip()
            for char in val:
                valid_chars.add(char)
    
    # Create a consistent value map based on unicode value for fingerprinting
    # This makes no assumptions about frequency, treating each character as a unique atomic element.
    value_map = {char: ord(char) for char in valid_chars}
    return value_map

def analyze_text_forensically(text_filepath, lang_filepath):
    """
    Generates a full forensic deconstruction of a text file using a specified language definition.
    """
    # 1. Load Language & Text
    letter_values = parse_lang_file(lang_filepath)
    with open(text_filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 2. Calculate Word Frequencies for Track 2
    all_words_in_text = [w.lower() for w in nltk.word_tokenize(text) if w.isalpha()]
    word_counts = Counter(all_words_in_text)
    # Rank words by frequency (most common = rank 1)
    word_ranks = {word: i + 1 for i, (word, count) in enumerate(word_counts.most_common())}

    # 3. Define Value Functions
    def get_letter_val(char):
        return letter_values.get(char, 0)

    def get_word_track1(word):
        return sum(get_letter_val(c) for c in word)

    def get_word_track2(word, t1_val):
        rank = word_ranks.get(word.lower(), len(word_ranks) + 1)
        # Rarity factor: Multiply by log of rank to amplify rare words
        return t1_val * math.log(rank + 1)

    # 4. Process Streams (Simplified for this run)
    master_word_stream = []
    sentences = nltk.sent_tokenize(text)
    for sent in sentences:
        words = [w for w in nltk.word_tokenize(sent) if w.isalpha()]
        for word in words:
            t1 = get_word_track1(word)
            t2 = get_word_track2(word, t1)
            master_word_stream.append({'Word': word, 'T1_Raw': t1, 'T2_Raw': t2})
    
    # 5. Save Master Word CSV
    base_name = os.path.basename(text_filepath)
    csv_path = f"corrected_waveform_{base_name}.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Word', 'T1_Raw', 'T2_Raw'])
        writer.writeheader()
        writer.writerows(master_word_stream)
    
    print(f"Correctly processed {text_filepath}, output to {csv_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python comprehensive_author_fingerprint.py <text_file> <lang_file>")
        sys.exit(1)
    
    analyze_text_forensically(sys.argv[1], sys.argv[2])