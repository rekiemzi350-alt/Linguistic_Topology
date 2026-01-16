import os
import re
import numpy as np
from language_math import HebrewGematriaProcessor

class ReverseTranslator:
    def __init__(self):
        self.hp = HebrewGematriaProcessor("Reverse")
        self.results = []

    def detect_ghost_syntax(self, text, source_lang):
        """
        Detects artifacts of 'source_lang' in English text.
        For Hebrew: Look for 'And it came to pass', heavy 'and' (vav) usage, 
        and Verb-Subject-Object structures.
        """
        patterns = {
            "hebrew": [r"\bAnd it came to pass\b", r"\band\b", r"\bBehold\b", r"\bsons of\b"],
            "greek": [r"\bthe\b \bof the\b", r"\bfor\b \bit\b \bis\b"],
            "sumerian": [r"\bking\b \bof\b \bkings\b", r"\bgreat\b \bcity\b"]
        }
        
        matches = 0
        for p in patterns.get(source_lang, []):
            matches += len(re.findall(p, text, re.IGNORECASE))
        return matches

    def analyze_deviation(self, eng_text, original_fragment=None):
        """
        Calculates the 'Stress Point' where English grammar 
        fails to accommodate the original language's topology.
        """
        eng_words = re.findall(r"\b\w+\b", eng_text)
        # Measure local convergence velocity (variance of word weights)
        weights = [sum(ord(c)-96 for c in w.lower() if 'a'<=c<='z') for w in eng_words]
        
        # High variance in English often indicates a 'forced' translation of 
        # a high-density original concept.
        local_variance = np.var(weights) if weights else 0
        return local_variance

    def trace_enoch(self):
        print("Tracing 1 Enoch: English -> Ge'ez -> Aramaic...")
        files = {
            "Charles": "test_documents/Book_of_Enoch_Charles.txt",
            "Laurence": "test_documents/Book_of_Enoch_Laurence.txt",
            "Geez": "test_documents/Book_of_Enoch_Geez_Full_OCR.txt"
        }
        
        for name, path in files.items():
            if not os.path.exists(path): continue
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()[:5000] # Sample first 5000 chars
            
            ghosts = self.detect_ghost_syntax(content, "hebrew")
            stress = self.analyze_deviation(content)
            
            self.results.append({
                "work": f"1 Enoch ({name})",
                "ghost_markers": ghosts,
                "topological_stress": stress,
                "evidence": "High" if ghosts > 50 else "Low"
            })

    def trace_secret_doctrine(self):
        print("Tracing The Secret Doctrine: English -> Stanzas of Dzyan...")
        path = "test_documents/Secret_Doctrine_Vol1.txt"
        if not os.path.exists(path): return

        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find the Stanzas (usually marked by Roman Numerals and specific headers)
        stanzas = re.findall(r"STANZA [IVXLC]+.*? (?=STANZA|\Z)", content, re.DOTALL)
        
        for i, stanza in enumerate(stanzas[:10]):
            ghosts = self.detect_ghost_syntax(stanza, "greek") + self.detect_ghost_syntax(stanza, "hebrew")
            stress = self.analyze_deviation(stanza)
            
            self.results.append({
                "work": f"SD Stanza {i+1}",
                "ghost_markers": ghosts,
                "topological_stress": stress,
                "evidence": "Evidence of Pre-Sanskrit/Semitic structure" if stress > 45 else "Modern Synthetic"
            })

    def report(self):
        print("\n=== REVERSE TRANSLATION & SOURCE ORIGIN REPORT ===\n")
        for res in self.results:
            print(f"Target: {res['work']}")
            print(f"  - Ghost Markers Found: {res['ghost_markers']}")
            print(f"  - Topological Stress (Fracture): {res['topological_stress']:.2f}")
            print(f"  - Origin Evidence: {res['evidence']}")
            print("-" * 30)

if __name__ == "__main__":
    rt = ReverseTranslator()
    rt.trace_enoch()
    rt.trace_secret_doctrine()
    rt.report()
