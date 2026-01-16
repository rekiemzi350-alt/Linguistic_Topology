import sys
import re
import os
import math
import csv
import nltk
import subprocess
from collections import Counter

# --- 1. CONFIGURATION ---
CONSONANTS = ['t', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'm', 'w', 'f', 'g', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']
VOWELS = ['e', 'a', 'o', 'i', 'u']
LETTER_VALUES = {c: i+1 for i, c in enumerate(CONSONANTS)}
LETTER_VALUES.update({v: i+1 for i, v in enumerate(VOWELS)})
LETTER_VALUES['y'] = 0

COMMON_WORDS_RANK = {
    'the': 1, 'be': 2, 'to': 3, 'of': 4, 'and': 5, 'a': 6, 'in': 7, 'that': 8, 'have': 9, 'i': 10,
    'it': 11, 'for': 12, 'not': 13, 'on': 14, 'with': 15, 'he': 16, 'as': 17, 'you': 18, 'do': 19, 'at': 20
}

def get_word_track1(word):
    return sum(LETTER_VALUES.get(c.lower(), 0) for c in word if c.isalpha())

def get_word_track2(word, t1):
    rank = COMMON_WORDS_RANK.get(word.lower(), 1000)
    return t1 * math.log(rank + 1)

def get_plot_val(val):
    if val == 0: return 0
    return val if int(abs(val)) % 2 != 0 else -val

# --- 2. FORENSIC DECONSTRUCTION ---

class BatteryOptimizedAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.base = os.path.basename(filepath)
        
    def run(self):
        # A. OFF-LOAD LEVEL 1 TO GO (Saves Battery)
        print(f"[*] Calling Go binary for Atomic Analysis (Level 1)...")
        subprocess.run(["./erik_calc", self.filepath])

        # B. PROCESS LINGUISTICS IN PYTHON
        print(f"[*] Starting Linguistic Analysis (Levels 2-4)...")
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        sentences = nltk.sent_tokenize(text)
        
        # Streams
        master_words = []
        cat_streams = {
            'nouns': [], 'verbs': [], 'adjectives': [], 'adverbs': [],
            'pronouns': [], 'prepositions': [], 'conjunctions': []
        }
        sent_stream = []

        word_seq = 0
        for s_seq, raw_s in enumerate(sentences):
            tokens = nltk.word_tokenize(raw_s)
            tagged = nltk.pos_tag(tokens, tagset='universal')
            
            s_t1, s_t2 = 0, 0
            v_count, c_count = 0, 0
            word_count = 0
            
            for word, tag in tagged:
                if not word[0].isalpha(): continue
                
                t1 = get_word_track1(word)
                t2 = get_word_track2(word, t1)
                p1, p2 = get_plot_val(t1), get_plot_val(t2)
                
                row = [word_seq, word, tag, t1, p1, f"{t2:.2f}", f"{p2:.2f}"]
                master_words.append(row)
                
                # Category Mapping
                if tag == 'NOUN': cat_streams['nouns'].append(row)
                elif tag == 'VERB': 
                    cat_streams['verbs'].append(row)
                    v_count += 1
                elif tag == 'ADJ': cat_streams['adjectives'].append(row)
                elif tag == 'ADV': cat_streams['adverbs'].append(row)
                elif tag == 'PRON': cat_streams['pronouns'].append(row)
                elif tag == 'ADP': cat_streams['prepositions'].append(row)
                elif tag == 'CONJ': 
                    cat_streams['conjunctions'].append(row)
                    c_count += 1
                
                s_t1 += t1
                s_t2 += t2
                word_count += 1
                word_seq += 1

            if word_count > 0:
                complexity = "Simple"
                if v_count > 1: complexity = "Compound/Complex" if c_count > 0 else "Complex"
                mode = "Conversation" if '"' in raw_s or '“' in raw_s else "Narrative"
                
                sent_stream.append([
                    s_seq, complexity, mode, word_count,
                    s_t1, get_plot_val(s_t1),
                    f"{s_t2:.2f}", f"{get_plot_val(s_t2):.2f}"
                ])

        # C. WRITE CSVs
        self.write("level2_words_MASTER", ['Sequence','Word','Tag','T1_Raw','T1_Plot','T2_Raw','T2_Plot'], master_words)
        for cat, data in cat_streams.items():
            self.write(f"level3_{cat}", ['Sequence','Word','Tag','T1_Raw','T1_Plot','T2_Raw','T2_Plot'], data)
        self.write("level4_sentences", ['Sequence','Complexity','Mode','Words','T1_Raw','T1_Plot','T2_Raw','T2_Plot'], sent_stream)

    def write(self, suffix, head, data):
        fname = f"waveform_{suffix}_{self.base}.csv"
        with open(fname, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(head)
            writer.writerows(data)
        print(f"  [+] Saved: {fname}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python comprehensive_author_fingerprint.py <file.txt>")
    else:
        BatteryOptimizedAnalyzer(sys.argv[1]).run()
