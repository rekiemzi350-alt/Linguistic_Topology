import pandas as pd
import numpy as np
import sys
import os

def analyze_forensics(vol_num):
    # Load the Sentence Level Data (Level 4)
    # It contains "Mode" (Narrative vs Conversation/Quote implied context)
    # Note: Our current tagger marked "Conversation" based on quotes (" "), 
    # which in a non-fiction book like SD usually implies a Quote or citation.
    
    file_path = f"waveform_level4_sentences_Secret_Doctrine_Vol{vol_num}.txt.csv"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)
    
    # Split into "Blavatsky Voice" (Narrative) vs "External Voice" (Quotes/Conversation)
    # In SD, "Conversation" mode (sentences with quotes) acts as a proxy for citations/quotes.
    blavatsky = df[df['Mode'] == 'Narrative']
    external = df[df['Mode'] == 'Conversation']
    
    print(f"\n--- VOLUME {vol_num} FORENSIC ANALYSIS ---")
    print(f"Narrative Sentences: {len(blavatsky)}")
    print(f"Quote/Citation Sentences: {len(external)}")
    
    if len(external) < 10:
        print("Not enough quote data for reliable forensic comparison.")
        return

    # 1. Structural Comparison (Complexity)
    # Do the quotes use simpler or more complex sentence structures than HPB?
    b_complex = blavatsky['Complexity'].value_counts(normalize=True).get('Compound/Complex', 0)
    e_complex = external['Complexity'].value_counts(normalize=True).get('Compound/Complex', 0)
    
    print(f"Structural Complexity (HPB): {b_complex:.2%}")
    print(f"Structural Complexity (Quotes): {e_complex:.2%}")
    
    # 2. Waveform Variance (The "Mental Fingerprint")
    # We use Track 2 (Weighted Sum) as it captures vocabulary rarity.
    # Calculate the Standard Deviation (Volatility) of the waveform.
    b_std = blavatsky['T2_Raw'].std()
    e_std = external['T2_Raw'].std()
    
    print(f"Vocabulary Volatility (HPB): {b_std:.2f}")
    print(f"Vocabulary Volatility (Quotes): {e_std:.2f}")
    
    # 3. Forensic Distance (Z-Score approximation)
    # How distinct are the two voices?
    # Difference in Means / Avg Standard Deviation
    b_mean = blavatsky['T2_Raw'].mean()
    e_mean = external['T2_Raw'].mean()
    
    diff = abs(b_mean - e_mean)
    avg_std = (b_std + e_std) / 2
    z_score = diff / avg_std
    
    print(f"Forensic Distance (Z-Score): {z_score:.4f}")
    
    if z_score < 0.1:
        print(">> RESULT: HIGH PROBABILITY OF SINGLE AUTHOR. (Quotes match Narrative style almost perfectly)")
    elif z_score < 0.3:
        print(">> RESULT: AMBIGUOUS. (Quotes are stylistically very similar to HPB)")
    else:
        print(">> RESULT: DISTINCT VOICES. (Quotes show statistically significant difference from HPB)")

    return z_score

print("=== THE SECRET DOCTRINE: PLAGIARISM & HOAX DETECTOR ===")
print("Methodology: Comparing 'Track 2' (Weighted Atomic/Molecular Signature) of Narrative vs. Quotes.")

z_scores = []
for i in range(1, 5):
    z = analyze_forensics(i)
    if z: z_scores.append(z)

avg_z = sum(z_scores) / len(z_scores) if z_scores else 0
print("\n=== FINAL VERDICT ===")
print(f"Average Forensic Distance across all volumes: {avg_z:.4f}")

if avg_z > 0.3:
    print("CONCLUSION: The 'Quotes' in The Secret Doctrine possess a distinctly different")
    print("topological fingerprint than H.P. Blavatsky's narrative voice.")
    print("This SUPPORTS the claim that she was citing external sources (or distinct entities)")
    print("rather than fabricating them herself.")
else:
    print("CONCLUSION: The 'Quotes' and Narrative are stylistically indistinguishable.")
    print("This SUPPORTS the claim of single-authorship (fabrication or high-degree rewriting).")
