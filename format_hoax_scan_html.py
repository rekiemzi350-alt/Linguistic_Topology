
import re
import statistics
import sys
import nltk
import html

# --- NLTK Data Check ---
# Ensure necessary NLTK tokenizers are downloaded
for resource in ['punkt', 'punkt_tab']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        print(f"Downloading '{resource}' tokenizer...")
        nltk.download(resource, quiet=True)

# --- Core Logic from previous scripts ---
BIT_MAP = {
    'a': '0', 's': '1', 'd': '10', 'f': '11', 'g': '100', 'h': '101', 'j': '110', 'k': '111', 'l': '00',
    'q': '000', 'w': '001', 'e': '010', 'r': '011', 't': '1000', 'y': '1001', 'u': '1010', 'i': '1011', 'o': '1100', 'p': '1101',
    'z': '1110', 'x': '1111', 'c': '0000', 'v': '0001', 'b': '0010', 'n': '0011', 'm': '0100'
}
MODERN_THRESHOLD = 0.55

def get_word_weight(word):
    clean_word = re.sub(r'[^a-z]', '', word.lower())
    bit_string = ''.join(BIT_MAP.get(char, '') for char in clean_word)
    return len(bit_string)

def get_bit_velocity_cv(text_segment):
    words = text_segment.split()
    if len(words) < 5: return 0.0
    weights = [get_word_weight(word) for word in words if get_word_weight(word) > 0]
    if len(weights) < 3: return 0.0
    try:
        mean = statistics.mean(weights)
        stdev = statistics.stdev(weights)
        return stdev / mean if mean > 0 else 0.0
    except statistics.StatisticsError:
        return 0.0

# --- HTML Generation ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hoax Scan Report</title>
    <style>
        body {{
                    background-color: #000000;
                    color: #FFFFFF;
                    font-family: monospace;
                    font-size: 14px;
                }}
                .suspicious {{
                    font-style: italic;
                }}
                pre {{
                    white-space: pre-wrap; /* Allows text to wrap */
                    word-wrap: break-word; /* Breaks long words if necessary */
                }}
    </style>
</head>
<body>
    <pre>
{content}
    </pre>
</body>
</html>
"""

def format_text_as_html(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    
    processed_content = ""
    for sentence in sentences:
        cv_score = get_bit_velocity_cv(sentence)
        
        # We must escape the sentence to prevent HTML injection issues
        # e.g., if the text contains '<' or '>'
        escaped_sentence = html.escape(sentence)

        if cv_score >= MODERN_THRESHOLD:
            # Wrap in a red span
            processed_content += f'<span class="suspicious">{escaped_sentence}</span>'
        else:
            processed_content += escaped_sentence

    final_html = HTML_TEMPLATE.format(content=processed_content)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Processing complete. HTML output saved to {output_path}")
    except IOError as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python format_hoax_scan_html.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    format_text_as_html(input_file, output_file)
