import collections
import sys
import re

def analyze_patterns(file_path, num_chars=1000):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    # 1. Clean and Filter
    # We focus on letters only for the frequency analysis
    clean_text = re.sub(r'[^a-zA-Z]', '', text).lower()
    
    if not clean_text:
        print("No letters found in text.")
        return

    # 2. Determine Frequency in THIS text
    counter = collections.Counter(clean_text)
    
    # Sort by frequency (most common first)
    # If tie, sort alphabetically to be deterministic
    sorted_letters = sorted(counter.keys(), key=lambda x: (-counter[x], x))
    
    # 3. Build the Map (1 to 26)
    # If there are fewer than 26 letters used, we just go up to N.
    # If there are 26, the last one is 26.
    
    letter_map = {}
    print(f"--- Frequency Mapping for {file_path} ---")
    print("Rank | Letter | Count | Value")
    print("-" * 35)
    for i, letter in enumerate(sorted_letters):
        val = i + 1
        letter_map[letter] = val
        if i < 5 or i >= len(sorted_letters) - 5: # Show top 5 and bottom 5
             print(f"{i+1:4} |   {letter.upper()}    | {counter[letter]:5} | {val}")
        if i == 5:
            print(" ... ")

    # 4. Convert a sample of the text to the numeric stream
    print("\n--- Interwoven Numeric Pattern (First 500 chars) ---")
    
    # We process the original text to keep some structure, or just the clean stream?
    # "interwoven patterns created by the numeric value of the individual letters"
    # Usually implies the continuous stream.
    
    sample_stream = clean_text[:500]
    numeric_stream = [letter_map[char] for char in sample_stream]
    
    # Visualizing the "Weave"
    # We can print rows of numbers.
    
    row_width = 20
    for i in range(0, len(numeric_stream), row_width):
        row = numeric_stream[i:i+row_width]
        # Format as 2-digit numbers
        row_str = " ".join(f"{x:02}" for x in row)
        print(row_str)

    # 5. Simple Pattern Analysis
    # Sum of the stream vs expected average
    total_sum = sum(numeric_stream)
    avg_val = total_sum / len(numeric_stream)
    print(f"\nStream Length: {len(numeric_stream)}")
    print(f"Total Sum: {total_sum}")
    print(f"Average Value: {avg_val:.2f} (Expected for random 1-26 is ~13.5, weighted is usually lower)")

    # check for 'parity' or alternating patterns (high-low-high-low)
    shifts = 0
    for j in range(len(numeric_stream) - 1):
        if numeric_stream[j] < 13 and numeric_stream[j+1] >= 13:
            shifts += 1
        elif numeric_stream[j] >= 13 and numeric_stream[j+1] < 13:
            shifts += 1
            
    print(f"High/Low Frequency Shifts: {shifts} (Rough measure of 'texture')")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        analyze_patterns(target_file)
    else:
        print("Please provide a file path.")
