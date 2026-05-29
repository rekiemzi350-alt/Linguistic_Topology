import os
import subprocess
import sys
import numpy as np
import re
import pandas as pd # For DataFrame to display results
import mido # Already installed or attempted

# --- Manual Pearson Correlation (using numpy) ---
def pearsonr(x, y):
    """
    Calculates Pearson correlation coefficient between two arrays.
    Equivalent to scipy.stats.pearsonr for 1D arrays.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    
    # Handle cases where std is zero to avoid division by zero
    if np.std(x) == 0 or np.std(y) == 0:
        return 0.0, 1.0 # Correlation is undefined, p-value is 1.0 (no significance)
    
    corr = np.corrcoef(x, y)[0, 1]
    # P-value calculation for Pearson correlation is complex. For this context,
    # we'll return a dummy p-value, as the primary request is correlation.
    return corr, None 

# --- Analysis Configuration ---
COMPOSERS_AND_MUSIC = {
    "Beethoven": {"midi": ["beethoven_symphony_5_1.mid", "beethoven_symphony_5_2.mid", "beethoven_symphony_5_3-4.mid"], "lang_code": "german"},
    "Mozart": {"midi": "mozart_symphony_40.mid", "lang_code": "german"},
    "Chopin": {"midi": "chopin_minute_waltz.mid", "lang_code": "polish"},
    "Debussy": {"midi": "debussy_clair_de_lune.mid", "lang_code": "french"},
}

ALL_LANGUAGES_TO_TEST = {
    "german": {"filepath": "german.lang", "name": "German"},
    "polish": {"filepath": "polish.lang", "name": "Polish"},
    "french": {"filepath": "french.lang", "name": "French"},
    "italian": {"filepath": "italian.lang", "name": "Italian"},
    "russian": {"filepath": "russian.lang", "name": "Russian"},
    "czech": {"filepath": "czech.lang", "name": "Czech"},
    "finnish": {"filepath": "finnish.lang", "name": "Finnish"},
    "hungarian": {"filepath": "hungarian.lang", "name": "Hungarian"},
    "english_us": {"filepath": "english_us.lang", "name": "American English"},
    "english_uk": {"filepath": "english_uk.lang", "name": "UK English"},
    "dutch_hist": {"filepath": "dutch_hist.lang", "name": "Historical Dutch"}, # From previous stock market analysis
}

# --- Linguistic Waveform Generation ---

def get_number_name(n, lang_rules):
    if n in lang_rules.get("direct", {}):
        return lang_rules["direct"][n]
    
    # Simple, additive rules for larger numbers.
    # This part should ideally be defined more comprehensively per language
    # but serves as a reasonable approximation for extending the sequence.
    name = ""
    if n >= 1000000 and "million" in lang_rules:
        name_part = get_number_name(n // 1000000, lang_rules)
        if name_part: name += name_part + " "
        name += lang_rules["million"]
        n %= 1000000
        if n > 0: name += " "
    
    if n >= 1000 and "thousand" in lang_rules:
        name_part = get_number_name(n // 1000, lang_rules)
        if name_part: name += name_part + " "
        name += lang_rules["thousand"]
        n %= 1000
        if n > 0: name += " "
    
    if n >= 100 and "hundred" in lang_rules:
        name_part = get_number_name(n // 100, lang_rules)
        if name_part: name += name_part + " "
        name += lang_rules["hundred"]
        n %= 100
        if n > 0: name += " "

    if n > 0: # handle remaining < 100
        if n in lang_rules.get("direct", {}):
            name += lang_rules["direct"][n]
        else:
            tens = n // 10 * 10
            ones = n % 10
            if tens in lang_rules.get("direct", {}):
                name += lang_rules["direct"][tens]
                if ones > 0:
                    name += lang_rules.get("ten_sep", "") + lang_rules["direct"].get(ones, "")
            elif ones > 0: # If only ones digit exists after hundreds/thousands
                 name += lang_rules["direct"].get(ones, "")

    return name.strip()


def load_lang_rules(lang_code):
    filepath = ALL_LANGUAGES_TO_TEST[lang_code]["filepath"]
    if not os.path.exists(filepath):
        # Fallback for built-in languages if not in current dir
        repo_path = os.path.join("linguistic_topology_repo", "languages", filepath)
        if os.path.exists(repo_path):
            filepath = repo_path
        else:
            print(f"Warning: Language file not found for {lang_code} at {filepath} or {repo_path}")
            return None

    rules = {"direct": {}}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip() # Remove leading/trailing whitespace
            if not line or line.startswith('#'): continue # Skip empty lines and comments
            
            if ":" not in line: # Skip lines that don't contain a colon
                print(f"Warning: Malformed line in {filepath} skipped: {line}")
                continue

            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if key.isdigit():
                rules["direct"][int(key)] = val
            else:
                rules[key] = val.replace('"', '')
    return rules

def generate_linguistic_waveform(lang_code, num_steps):
    rules = load_lang_rules(lang_code)
    if not rules: return []
    
    # Ensure 'thousand' and 'million' are present for large numbers
    # Simplified addition if missing, as exact forms vary
    if 'thousand' not in rules: rules['thousand'] = 'thousand'
    if 'million' not in rules: rules['million'] = 'million'
    
    waveform = []
    current_value = 0
    for _ in range(num_steps):
        name = get_number_name(current_value, rules)
        if not name: # Handle cases where get_number_name might return empty string for 0, etc.
             length = 0
        else:
            length = len(re.sub(r'[^a-zA-Z]', '', name))
        
        # Ensure length is not zero for progression
        if length == 0 and current_value != 0:
            length = 1 # Avoid infinite loop for a zero-length name
        
        current_value += length
        waveform.append(length) # Use the change (length) as the value
    return waveform

# --- Musical Waveform Generation ---

def generate_musical_waveform(midi_paths):
    if not isinstance(midi_paths, list):
        midi_paths = [midi_paths] # Ensure it's always a list for consistent processing
        
    all_notes = []
    for midi_path in midi_paths:
        if not os.path.exists(midi_path):
            print(f"Warning: MIDI file not found: {midi_path}")
            return [] # Return empty if any part is missing
            
        try:
            mid = mido.MidiFile(midi_path)
            notes_from_part = []
            for msg in mid:
                if msg.type == 'note_on' and msg.velocity > 0 and msg.note is not None:
                    notes_from_part.append(msg.note)
            all_notes.extend(notes_from_part)
        except Exception as e:
            print(f"Error processing MIDI {midi_path}: {e}")
            return [] # Return empty if any part causes an error
            
    # Debugging: Check length of notes
    # print(f"  -> Extracted {len(all_notes)} notes from {midi_paths}")

    if len(all_notes) < 2:
        # print(f"  -> Not enough notes ({len(all_notes)}) for intervals in {midi_paths}")
        return []
    
    intervals = np.diff(all_notes).tolist()
    # print(f"  -> Generated {len(intervals)} intervals from {midi_paths}")
    return intervals

# --- Main Analysis ---

def analyze_cross_correlation():
    print("--- Phase 2: Analyzing Music & Language Cross-Correlation ---")
    
    # 1. Pre-generate all musical waveforms
    musical_waveforms = {}
    for composer, data in COMPOSERS_AND_MUSIC.items():
        print(f"Generating musical waveform for {composer}'s {data['midi']}...")
        wave = generate_musical_waveform(data["midi"])
        if not wave:
            print(f"  -> Skipping {composer} due to empty or invalid musical waveform.")
            continue # Skip adding to musical_waveforms if empty
        musical_waveforms[composer] = wave
        # Debug: Print length of generated musical wave
        print(f"  -> {composer} musical wave length: {len(wave)}")

    if not musical_waveforms:
        print("\nNo valid musical waveforms were generated. Cannot proceed with correlation.")
        return

    # 2. Pre-generate all linguistic waveforms (up to a max length needed)
    # Determine max length needed among all *valid* musical waveforms
    max_musical_len = max(len(w) for w in musical_waveforms.values()) if musical_waveforms else 1000
    print(f"\nGenerating linguistic waveforms (up to {max_musical_len} steps)...")
    
    linguistic_waveforms = {}
    for lang_code, lang_info in ALL_LANGUAGES_TO_TEST.items():
        print(f"  -> Generating for {lang_info['name']} ({lang_code})...")
        linguistic_waveforms[lang_code] = generate_linguistic_waveform(lang_code, max_musical_len)
        if not linguistic_waveforms[lang_code]:
             print(f"  -> Skipping {lang_info['name']} due to empty linguistic waveform (likely no rules).")
        # Debug: Print length of generated linguistic wave
        print(f"  -> {lang_info['name']} linguistic wave length: {len(linguistic_waveforms[lang_code])}")


    # 3. Perform cross-correlation
    results_matrix = {} # {composer: {lang: correlation}}
    for composer, music_wave in musical_waveforms.items():
        if not music_wave: continue
        results_matrix[composer] = {}
        
        # Calculate volatility for music (once per piece)
        music_volatility = pd.Series(music_wave).rolling(window=3).std().dropna()
        # Debug: Print length of musical volatility
        print(f"  -> {composer} musical volatility length: {len(music_volatility)}")

        if len(music_volatility) < 2: # Need at least 2 points for pearsonr
            print(f"  -> Not enough musical volatility data for {composer}. Skipping correlations for this piece.")
            continue

        for lang_code, lang_wave in linguistic_waveforms.items():
            if not lang_wave: continue
            
            # Use linguistic wave up to the length of music wave
            lang_wave_trimmed = lang_wave[:len(music_wave)]
            if len(lang_wave_trimmed) < 2:
                results_matrix[composer][lang_code] = np.nan
                continue

            # Calculate volatility for language
            linguistic_volatility = pd.Series(lang_wave_trimmed).rolling(window=3).std().dropna()
            # Debug: Print length of linguistic volatility
            # print(f"  -> {ALL_LANGUAGES_TO_TEST[lang_code]['name']} linguistic volatility length: {len(linguistic_volatility)}")
            
            # Align volatility series for correlation
            min_vol_len = min(len(music_volatility), len(linguistic_volatility))
            if min_vol_len < 2: # Need at least 2 points for pearsonr
                results_matrix[composer][lang_code] = np.nan
                continue

            corr, _ = pearsonr(music_volatility[:min_vol_len], linguistic_volatility[:min_vol_len])
            results_matrix[composer][lang_code] = corr

    print("\n--- Cross-Correlation Matrix (Volatility) ---")
    results_df = pd.DataFrame(results_matrix)
    print(results_df.to_string())

    # Find closest language for each composer
    print("\n--- Strongest Correlations (Composer's Music vs. All Languages) ---")
    best_matches = []
    for composer_name, row in results_df.iterrows():
        # Only add to best_matches if there are non-NaN correlations in the row
        if not row.isnull().all(): 
            # Find the best correlated language for this composer
            best_corr = row.max()
            best_lang_code = row.idxmax()

            # Ensure best_corr is not NaN before adding to results
            if not pd.isna(best_corr):
                if composer_name in COMPOSERS_AND_MUSIC:
                    musical_language_code = COMPOSERS_AND_MUSIC[composer_name]["lang_code"]
                    
                    best_matches.append({
                        "Composer": composer_name,
                        "Musical Language": musical_language_code,
                        "Strongest Correlated Language": ALL_LANGUAGES_TO_TEST[best_lang_code]["name"],
                        "Correlation": best_corr
                    })
    best_matches_df = pd.DataFrame(best_matches)
    if not best_matches_df.empty:
        best_matches_df = best_matches_df.sort_values(by="Correlation", ascending=False)
        print(best_matches_df.to_string(index=False))
    else:
        print("No meaningful correlations calculated (insufficient valid data or all correlations are NaN).")

    print("\n--- Conclusion ---")
    print("This analysis measures the correlation between the rhythmic volatility of a musical piece")
    print("and the rhythmic volatility of various linguistic number systems.")
    print("A higher correlation suggests a structural similarity in the 'rhythm' of change.")
    print("\nNOTE: This is a theoretical exploration of structural similarities, not a predictive model.")

    if not musical_waveforms:
        print("\n**WARNING**: No valid musical waveforms could be generated from the provided MIDI files.")
        print("Please ensure the MIDI files are valid and not corrupted. You can place them in the 'coffee' directory.")
        print("Expected MIDI filenames (and their composers):")
        for composer, data in COMPOSERS_AND_MUSIC.items():
            if composer not in musical_waveforms: # Check if it wasn't successfully processed
                if isinstance(data['midi'], list): # Handle multiple midi files for one composer
                    for filename in data['midi']:
                        print(f" - {composer}: {filename}")
                else:
                    print(f" - {composer}: data['midi']")


if __name__ == "__main__":
    # Ensure all required lang files exist (create placeholders if necessary)
    all_needed_lang_codes = set(COMPOSERS_AND_MUSIC[c]["lang_code"] for c in COMPOSERS_AND_MUSIC)
    all_needed_lang_codes.update(ALL_LANGUAGES_TO_TEST.keys())

    for lang_code in all_needed_lang_codes:
        if lang_code in ALL_LANGUAGES_TO_TEST:
            filepath = ALL_LANGUAGES_TO_TEST[lang_code]["filepath"]
            if not os.path.exists(filepath):
                repo_path = os.path.join("linguistic_topology_repo", "languages", filepath)
                if not os.path.exists(repo_path):
                    print(f"Creating placeholder for missing language: {filepath}")
                    with open(filepath, "w") as f:
                        f.write(f"name: {ALL_LANGUAGES_TO_TEST[lang_code]['name']}\n")
                        f.write("hundred: hundred\n")
                        f.write("thousand: thousand\n")
                        f.write("million: million\n")
                        f.write("ten_sep: -\n")
                        f.write("hundred_sep:  and \n")
                        f.write("0: zero\n1: one\n") # Basic entries
        else:
            print(f"Warning: Language code '{lang_code}' in COMPOSERS_AND_MUSIC but not in ALL_LANGUAGES_TO_TEST. Skipping.")


    analyze_cross_correlation()
