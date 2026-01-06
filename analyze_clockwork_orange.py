import os
import pandas as pd
import re

def get_word_value(word):
    # Strip non-alphanumeric for length calculation
    clean_word = re.sub(r'[^a-zA-Z0-9]', '', word)
    length = len(clean_word)
    if length == 0:
        return 0, 0
    # Parity: Even (+), Odd (-)
    # Note: The user's system often uses Even as Peak (+), Odd as Valley (-)
    # or sometimes reversed. I'll stick to: Even=Positive, Odd=Negative.
    val = length if length % 2 == 0 else -length
    return length, val

def process_text(file_path, output_csv):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return None

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Tokenize words
    words = text.split()
    
    data = []
    for i, word in enumerate(words):
        length, val = get_word_value(word)
        if length > 0:
            data.append({
                'Sequence': i,
                'Word': word,
                'T1_Raw': length,
                'T1_Plot': val,
                'T2_Raw': length * 1.5, # Placeholder for weighted track
                'T2_Plot': val * 1.5
            })
    
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Saved waveform to {output_csv}")
    return df

def run_analysis():
    print("Analyzing 'A Clockwork Orange'...")
    co_df = process_text('test_documents/a_clockwork_orange.txt', 'waveforms/waveform_clockwork_orange.csv')
    
    print("Analyzing 'Modern English' baseline...")
    me_df = process_text('modern_english.txt', 'waveforms/waveform_modern_english.csv')

    if co_df is not None and me_df is not None:
        # Calculate some variance metrics
        co_avg_len = co_df['T1_Raw'].mean()
        me_avg_len = me_df['T1_Raw'].mean()
        
        co_parity_bias = (co_df['T1_Plot'] > 0).mean() # Percentage of Even words
        me_parity_bias = (me_df['T1_Plot'] > 0).mean()
        
        print("\n--- COMPARATIVE METRICS ---")
        print(f"A Clockwork Orange: Avg Word Len={co_avg_len:.2f}, Even Parity={co_parity_bias:.2%}")
        print(f"Modern English:     Avg Word Len={me_avg_len:.2f}, Even Parity={me_parity_bias:.2%}")
        
        # Check for Nadsat influence (unique word patterns)
        # Nadsat often uses Russian loanwords which might have different length distributions. 
        
        print("\nTop 10 Longest Words in Clockwork Orange:")
        print(co_df.sort_values(by='T1_Raw', ascending=False)['Word'].head(10).tolist())

if __name__ == "__main__":
    run_analysis()
