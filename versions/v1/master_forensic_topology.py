import os
import re
import json
import numpy as np
from language_math import HebrewGematriaProcessor

class ForensicReporter:
    def __init__(self):
        self.hp = HebrewGematriaProcessor("Forensic")
        self.results = {}
        # Ge'ez mapping for Enoch texts (simplified for topology)
        self.geez_map = {
            'ሀ': 1, 'ለ': 2, 'ሐ': 3, 'መ': 4, 'ሠ': 5, 'ረ': 6, 'ሰ': 7, 'ቀ': 8, 'በ': 9, 'ተ': 10,
            'ኀ': 20, 'ነ': 30, 'አ': 40, 'ከ': 50, 'ወ': 60, 'ዐ': 70, 'ዘ': 80, 'የ': 90, 'ደ': 100
        }

    def get_greek_isopsephy(self, text):
        greek_map = {
            'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5, 'ζ': 7, 'η': 8, 'θ': 9, 'ι': 10,
            'κ': 20, 'λ': 30, 'μ': 40, 'ν': 50, 'ξ': 60, 'ο': 70, 'π': 80, 'ρ': 100,
            'σ': 200, 'τ': 300, 'υ': 400, 'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800, 'ς': 200
        }
        return sum(greek_map.get(c, 0) for c in text.lower())

    def get_geez_weight(self, text):
        return sum(self.geez_map.get(c, 0) for c in text)

    def analyze_text(self, filepath):
        if "Modern_Fiction" in filepath: return
        print(f"Analyzing (Native Script): {os.path.basename(filepath)}...")
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return

        chapters = re.split(r'\n\s*\n\s*\n|\bChapter\b|\bBOOK\b', text)
        chapter_metrics = []

        for i, chap in enumerate(chapters):
            if len(chap) < 100: continue
            
            # Extract Native Script segments
            heb = re.findall(r'[\u0590-\u05FF]+', chap)
            grk = re.findall(r'[\u0370-\u03FF]+', chap)
            gez = re.findall(r'[\u1200-\u137F]+', chap)
            eng = re.findall(r'\b[a-zA-Z]+\b', chap)

            # Native weights
            heb_wt = [self.hp.get_gematria(w) for w in heb]
            grk_wt = [self.get_greek_isopsephy(w) for w in grk]
            gez_wt = [self.get_geez_weight(w) for w in gez]
            eng_wt = [sum(ord(c)-96 for c in w.lower() if 'a'<=c<='z') for w in eng]

            # Combined Topology for the segment
            all_wt = heb_wt + grk_wt + gez_wt + eng_wt
            if not all_wt: continue

            chapter_metrics.append({
                "chapter": i,
                "avg_weight": float(np.mean(all_wt)),
                "variance": float(np.std(all_wt)),
                "lang_mix": {
                    "hebrew": len(heb),
                    "greek": len(grk),
                    "geez": len(gez),
                    "english": len(eng)
                }
            })

        if chapter_metrics:
            self.results[filepath] = {
                "total_words": len(re.findall(r'\b\w+\b', text)),
                "chapters": chapter_metrics,
                "overall_avg_weight": float(np.mean([c["avg_weight"] for c in chapter_metrics]))
            }

    def generate_report(self):
        report_path = "forensic_master_report.txt"
        with open(report_path, "w") as f:
            f.write("=== MASTER LINGUISTIC TOPOLOGY & FORENSIC REPORT ===\n")
            f.write(f"Date: 2026-01-09\n\n")
            
            f.write(f"{ 'Work Title':<60} | { 'Words':<10} | { 'Avg Wt':<8} | {'Heb/Grk/Gez Density'}\n")
            f.write("-" * 110 + "\n")
            
            sorted_works = sorted(self.results.items(), key=lambda x: x[1]['overall_avg_weight'], reverse=True)
            
            for path, data in sorted_works:
                title = os.path.basename(path)[:55]
                mix = sum(c['lang_mix']['hebrew'] + c['lang_mix']['greek'] + c['lang_mix']['geez'] for c in data['chapters'])
                f.write(f"{title:<60} | {data['total_words']:<10} | {data['overall_avg_weight']:<8.2f} | {mix}\n")

            f.write("\n=== ANOMALY DETECTION (HOAX SCAN) ===\n")
            for path, data in self.results.items():
                weights = [c["avg_weight"] for c in data["chapters"]]
                if len(weights) < 3: continue
                mean = np.mean(weights)
                std = np.std(weights)
                
                for c in data["chapters"]:
                    if std > 0 and abs(c["avg_weight"] - mean) > 2 * std:
                        f.write(f"ALERT: {os.path.basename(path)} - Chapter {c['chapter']} deviates by {abs(c['avg_weight']-mean)/std:.2f} sigma.\n")
                        f.write(f"      Possible Style Shift / Interpolation detected.\n")

        return report_path

if __name__ == "__main__":
    fr = ForensicReporter()
    target_dir = "test_documents"
    if os.path.exists(target_dir):
        files = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith(".txt")]
        for f in files:
            fr.analyze_text(f)
        print(f"\nReport generated: {fr.generate_report()}")
    else:
        print(f"Error: Directory {target_dir} not found.")