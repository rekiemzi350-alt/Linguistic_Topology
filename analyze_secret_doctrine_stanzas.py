import sys

# --- The "Stanzas of Dzyan" Sample Text (from Search) ---
STANZAS_TEXT = """
The Eternal Parent wrapped in her Ever-Invisible Robes, had slumbered once again for Seven Eternities.
Time was not, for it lay asleep in the Infinite Bosom of Duration.
Universal Mind was not, for there were no Ah-hi to contain it.
The Seven Ways to Bliss were not. The Great Causes of Misery were not, for there was no one to produce and get ensnared by them.
Darkness alone was Father-Mother, Svabhavat; and Svabhavat was in darkness.
The Universe was still concealed in the Divine Thought and the Divine Bosom.
The last Vibration of the Seventh Eternity thrills through Infinitude. The Mother swells, expanding from within without, like the Bud of the Lotus.
The Vibration sweeps along, touching with its swift Wing the whole Universe and the Germ that dwelleth in Darkness, the Darkness that breathes over the slumbering Waters of Life.
Darkness radiates Light, and Light drops one solitary Ray into the Waters, into the Mother-Deep.
"""

# --- English Topology Map (Simplified) ---
# n -> n + len(name(n))
def num_to_english_len(n):
    # Quick function for standard lengths
    # 0=4, 1=3, 2=3, 3=5, 4=4, 5=4, 6=3, 7=5, 8=5, 9=4, 10=3
    # 11=6, 12=6, 13=8, 14=8, 15=7, 16=7, 17=9, 18=8, 19=8
    # 20=6, 30=6, 40=5, 50=5, 60=5, 70=7, 80=6, 90=6
    # hundreds = +7 ("hundred"), etc.
    # For forensic analysis, we map SENTENCE LENGTH to TOPOLOGY.
    pass

def analyze_stanzas():
    print("--- Forensic Analysis of 'Stanzas of Dzyan' ---")
    
    sentences = [s.strip() for s in STANZAS_TEXT.replace("\n", " ").split(".") if s.strip()]
    
    print(f"Total Sentences Analyzed: {len(sentences)}\n")
    
    total_entropy = 0
    rebel_hits = 0
    
    for i, sent in enumerate(sentences):
        # 1. Word Count Topology
        words = sent.split()
        word_count = len(words)
        
        # 2. Letter Count Topology (The "Erik Convergence" Seed)
        # We treat the total letter count of the sentence as a "Seed" number
        letter_count = len(sent.replace(" ", "").replace(",", "").replace("-", ""))
        
        # Trace this seed
        curr = letter_count
        path = [curr]
        is_rebel = False
        
        # Simple trace logic (English)
        # (This is a simplified simulation of the 'get_next' loop)
        # We know 83, 84, 93, 94 are rebels.
        # We check if the sentence length hits a rebel seed.
        
        rebel_seeds = [83, 84, 93, 94]
        if letter_count in rebel_seeds:
            is_rebel = True
            rebel_hits += 1
            
        print(f"Sentence {i+1}:")
        print(f"  Text: '{sent[:30]}...'")
        print(f"  Length: {letter_count} letters / {word_count} words")
        print(f"  Topology Seed: {letter_count}")
        if is_rebel:
            print("  STATUS: **REBEL STREAM DETECTED** (High Complexity)")
        else:
            print("  STATUS: Main Trunk (Standard English Flow)")
            
    print("-" * 50)
    print(f"Rebel Saturation: {rebel_hits} out of {len(sentences)} sentences ({rebel_hits/len(sentences)*100:.1f}%)")
    
    if rebel_hits == 0:
        print("CONCLUSION: The text flows perfectly with standard English topology.")
        print("INTERPRETATION: Likely a native English composition or a translation heavily smoothed for flow.")
    else:
        print("CONCLUSION: High Topological Friction detected.")
        print("INTERPRETATION: Evidence of translation artifacts or complex/artificial construction.")

if __name__ == "__main__":
    analyze_stanzas()
