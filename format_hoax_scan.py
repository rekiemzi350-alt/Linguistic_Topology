
import re
import statistics
import sys
import nltk

# Download the 'punkt' tokenizer if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading 'punkt' tokenizer for sentence splitting...")
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading 'punkt_tab' tokenizer for sentence splitting...")
    nltk.download('punkt_tab', quiet=True)

# --- Core Logic from hoax_scanner.py ---

# VARIABLE BIT-VELOCITY ENCODING (Based on QWERTY layout)
# Home row is fastest (shortest codes), then top, then bottom.
BIT_MAP = {
    'a': '0', 's': '1', 'd': '10', 'f': '11', 'g': '100', 'h': '101', 'j': '110', 'k': '111', 'l': '00',
    'q': '000', 'w': '001', 'e': '010', 'r': '011', 't': '1000', 'y': '1001', 'u': '1010', 'i': '1011', 'o': '1100', 'p': '1101',
    'z': '1110', 'x': '1111', 'c': '0000', 'v': '0001', 'b': '0010', 'n': '0011', 'm': '0100'
}

# --- Thresholds from hoax_scanner.py ---
ANCIENT_THRESHOLD = 0.45  # CV below this is likely ancient/literal
MODERN_THRESHOLD = 0.55   # CV above this is likely modern/paraphrased

def get_word_weight(word):
    """Calculates the 'bit-velocity weight' of a word based on the BIT_MAP."""
    # Sanitize word to lowercase letters only
    clean_word = re.sub(r'[^a-z]', '', word.lower())
    bit_string = ''.join(BIT_MAP.get(char, '') for char in clean_word)
    return len(bit_string)

def get_bit_velocity_cv(text_segment):
    """
    Calculates the Coefficient of Variation (CV) of word weights for a segment.
    Returns CV, or 0.0 if not enough data.
    """
    words = text_segment.split()
    if len(words) < 5:  # Need at least a few words to get meaningful variance
        return 0.0

    weights = [get_word_weight(word) for word in words]
    
    # Filter out zero-weight words (e.g., numbers, symbols)
    weights = [w for w in weights if w > 0]

    if len(weights) < 3: # Need at least a few valid words
        return 0.0

    try:
        mean = statistics.mean(weights)
        stdev = statistics.stdev(weights)
        return stdev / mean if mean > 0 else 0.0
    except statistics.StatisticsError:
        return 0.0

def format_text(input_path, output_path):
    """
    Reads text, analyzes each sentence, and writes a formatted version.
    - Sentences classified as MODERN are wrapped in italics (*).
    - Sentences classified as ANCIENT are left as is.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    # Use NLTK to split the text into sentences
    sentences = nltk.sent_tokenize(text)
    
    formatted_lines = []
    
    for sentence in sentences:
        # Clean up sentence for processing, but keep original for output
        sentence_for_analysis = sentence.replace('\n', ' ')
        cv_score = get_bit_velocity_cv(sentence_for_analysis)
        
        # Preserve original sentence and its formatting (like newlines)
        original_sentence = sentence

        if cv_score >= MODERN_THRESHOLD:
            # Wrap in italics for "Modern/Suspicious"
            formatted_lines.append(f"*{original_sentence.strip()}*")
        # Sentences below the MODERN_THRESHOLD (Ancient or Mixed) are left as-is
        else:
            formatted_lines.append(original_sentence.strip())

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(formatted_lines))
        print(f"Processing complete. Output saved to {output_path}")
    except IOError as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python format_hoax_scan.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    format_text(input_file, output_file)
