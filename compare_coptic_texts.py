import sys
import os
import math
import subprocess
import pandas as pd

GREEK_LOANS = {
    "ⲇⲉ", "ⲅⲁⲣ", "ⲁⲗⲗⲁ", "ⲙⲉⲛ", "ⲟⲩⲛ", "ϩⲱⲥⲧⲉ", "ⲧⲟⲧⲉ",
    "ⲕⲟⲥⲙⲟⲥ", "ⲯⲩⲭⲏ", "ⲡⲛⲉⲩⲙⲁ", "ⲁⲅⲁⲑⲟⲛ", "ⲭⲁⲣⲓⲥ", "ⲥⲱⲙⲁ", "ⲉⲝⲟⲩⲥⲓⲁ"
}

def get_stats_for_text(text_filepath, lang_filepath, name):
    print(f"--- Analyzing: {name} ---")
    # 1. Run the CORRECTED forensic engine
    subprocess.run([
        "python", 
        "comprehensive_author_fingerprint.py", 
        text_filepath, 
        lang_filepath
    ], stdout=subprocess.DEVNULL)
    
    # 2. Load the CORRECTED data
    csv_path = f"corrected_waveform_{os.path.basename(text_filepath)}.csv"
    if not os.path.exists(csv_path):
        print(f"FATAL: Corrected analysis failed to generate CSV for {name}.")
        return None
        
    df = pd.read_csv(csv_path)

    # 3. Recalculate stats on valid data
    total_words = len(df)
    if total_words == 0: return None

    df['is_greek'] = df['Word'].apply(lambda w: 1 if w in GREEK_LOANS else 0)
    greek_ratio = (df['is_greek'].sum() / total_words) * 100
    
    volatility = df['T2_Raw'].std()
    mean_weight = df['T2_Raw'].mean()
    
    # Check for NaN or zero volatility which indicates a problem
    if pd.isna(volatility) or volatility == 0:
        print(f"FATAL: Analysis of {name} resulted in zero volatility. Check language file and text content.")
        return None

    print(f"  > Total Words: {total_words}")
    print(f"  > Greek Loan Density: {greek_ratio:.2f}%")
    print(f"  > Topological Volatility: {volatility:.2f}")
    
    return {
        "name": name,
        "greek_density": greek_ratio,
        "volatility": volatility,
        "mean_weight": mean_weight
    }

def compare(stats1, stats2):
    print("\n=== CORRECTED FORENSIC COMPARISON ===")
    print(f"Baseline: {stats1['name']}")
    print(f"Target:   {stats2['name']}")
    print("-" * 40)
    
    g_diff = stats2['greek_density'] - stats1['greek_density']
    print(f"Greek Loan-Word Delta: {g_diff:+.2f}%")
    if g_diff > 2.0:
        print("  >> ALERT: Target has significantly HIGHER Greek residue. Likely a rougher/more literal translation from Greek.")
    else:
        print("  >> RESULT: Greek usage is consistent with the time period.")

    diff = abs(stats1['mean_weight'] - stats2['mean_weight'])
    z_score = diff / stats1['volatility']
    
    print(f"Topological Distance (Z-Score): {z_score:.4f}")
    if z_score < 0.5:
        print("  >> VERDICT: HIGH SYNTACTIC MATCH. The text fits the Coptic profile of the era.")
    else:
        print("  >> VERDICT: ANOMALY. The text's structure does not fit the baseline control group.")

if __name__ == "__main__":
    lang_file = "linguistic_topology_repo/languages/coptic.lang"
    
    ref_stats = get_stats_for_text("coptic_thomas_sample.txt", lang_file, "Gospel of Thomas (Control)")
    target_stats = get_stats_for_text("mary_original_coptic.txt", lang_file, "Gospel of Mary (Target)")
    
    if ref_stats and target_stats:
        compare(ref_stats, target_stats)