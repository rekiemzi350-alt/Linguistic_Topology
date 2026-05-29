import os
import re
import json
import numpy as np
import pandas as pd
from language_math import HebrewGematriaProcessor

class DeepForensicAnalyzer:
    def __init__(self):
        self.hp = HebrewGematriaProcessor("DeepForensic")
        self.geez_map = {
            'ሀ': 1, 'ለ': 2, 'ሐ': 3, 'መ': 4, 'ሠ': 5, 'ረ': 6, 'ሰ': 7, 'ቀ': 8, 'በ': 9, 'ተ': 10,
            'ኀ': 20, 'ነ': 30, 'አ': 40, 'ከ': 50, 'ወ': 60, 'ዐ': 70, 'ዘ': 80, 'የ': 90, 'ደ': 100
        }
        self.ghost_patterns = {
            "hebraism": [r"\bAnd it came to pass\b", r"\bBehold\b", r"\bsons of\b", r"\bface of the\b"],
            "hellenism": [r"\bthe\b \bof the\b", r"\bverily\b", r"\bunto\b"],
            "geez_marker": [r"\bspirits\b", r"\brighteous\b", r"\blord\b \bof\b \bspirits\b"]
        }

    def detect_ghosts(self, text):
        results = {}
        for lang, patterns in self.ghost_patterns.items():
            count = 0
            for p in patterns:
                count += len(re.findall(p, text, re.IGNORECASE))
            results[lang] = count
        return results

    def get_greek_isopsephy(self, text):
        greek_map = {
            'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5, 'ζ': 7, 'η': 8, 'θ': 9, 'ι': 10,
            'κ': 20, 'λ': 30, 'μ': 40, 'ν': 50, 'ξ': 60, 'ο': 70, 'π': 80, 'ρ': 100,
            'σ': 200, 'τ': 300, 'υ': 400, 'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800, 'ς': 200
        }
        return sum(greek_map.get(c, 0) for c in text.lower())

    def get_geez_weight(self, text):
        return sum(self.geez_map.get(c, 0) for c in text)

    def analyze_file(self, filepath):
        print(f"Deep Analysis (Integrated): {os.path.basename(filepath)}...")
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        ghost_metrics = self.detect_ghosts(text)
        
        # Sentence Segmentation
        sentences = re.split(r'(?<=[.!?])\s+|\n', text)
        sentences = [s.strip() for s in sentences if len(s) > 10]
        
        sentence_data = []
        for i, sent in enumerate(sentences):
            # 1. Linguistic Weight
            heb = re.findall(r'[\u0590-\u05FF]+', sent)
            grk = re.findall(r'[\u0370-\u03FF]+', sent)
            gez = re.findall(r'[\u1200-\u137F]+', sent)
            eng = re.findall(r'\b[a-zA-Z]+\b', sent)

            heb_wt = sum(self.hp.get_gematria(w) for w in heb)
            grk_wt = sum(self.get_greek_isopsephy(w) for w in grk)
            gez_wt = sum(self.get_geez_weight(w) for w in gez)
            eng_wt = sum(sum(ord(c)-96 for c in w.lower() if 'a'<=c<='z') for w in eng)
            
            total_wt = heb_wt + grk_wt + gez_wt + eng_wt
            
            word_count = len(re.findall(r'\b\w+\b', sent))
            if word_count == 0: continue

            sentence_data.append({
                "weight": total_wt,
                "word_count": word_count,
                "is_conversation": 1 if ('"' in sent or '“' in sent) else 0
            })

        df = pd.DataFrame(sentence_data)
        if df.empty: return None

        stats = {
            "title": os.path.basename(filepath),
            "total_sentences": len(df),
            "avg_sentence_len": df['word_count'].mean(),
            "avg_weight": df['weight'].mean(),
            "weight_variance": df['weight'].var(),
            "hebraisms": ghost_metrics["hebraism"],
            "hellenisms": ghost_metrics["hellenism"],
            "geez_markers": ghost_metrics["geez_marker"],
            "conversation_pct": df['is_conversation'].mean() * 100,
            "rebels": len(df[np.abs(df.weight - df.weight.mean()) > (3 * df.weight.std())])
        }
        return stats
        
        # Save sentence-level detail
        df.to_csv(filepath + "_deep_map.csv", index=False)
        return stats

if __name__ == "__main__":
    analyzer = DeepForensicAnalyzer()
    target_dir = "test_documents"
    files = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith(".txt")]
    
    master_stats = []
    for f in files:
        res = analyzer.analyze_file(f)
        if res: master_stats.append(res)
    
    # Final Report
    master_df = pd.DataFrame(master_stats)
    master_df.to_csv("deep_forensic_master_stats.csv", index=False)
    
    with open("deep_forensic_final_report.txt", "w") as f:
        f.write("=== DEEPEST FORENSIC & TOPOLOGICAL BREAKDOWN ===\n\n")
        for s in master_stats:
            f.write(f"WORK: {s['title']}\n")
            f.write(f"  - Total Sentences: {s['total_sentences']}\n")
            f.write(f"  - Avg Sentence Length: {s['avg_sentence_len']:.2f} words\n")
            f.write(f"  - Topological Density (Avg Wt): {s['avg_weight']:.2f}\n")
            f.write(f"  - Style Fracture (Weight Var): {s['weight_variance']:.2f}\n")
            f.write(f"  - Conversation Ratio: {s['conversation_pct']:.2f}%\n")
            f.write(f"  - REBEL Verses (Interpolation Risk): {s['rebels']}\n")
            f.write("-" * 40 + "\n")
