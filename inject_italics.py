
import sys
import re
import statistics
import nltk
import html

# --- Dependency Check ---
try:
    import nltk
except ImportError:
    print("Error: The 'nltk' library is not installed.", file=sys.stderr)
    print("Please install it by running: pip install nltk", file=sys.stderr)
    sys.exit(1)

# --- Hoax Scanner Core Logic ---
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

def get_suspicious_sentences(plain_text):
    """Analyzes plain text and returns a set of suspicious sentences."""
    print("Analyzing text to identify suspicious sentences...")
    suspicious_sentences = set()
    
    # Ensure NLTK data is available
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("First-time setup: Downloading 'punkt' tokenizer...", file=sys.stderr)
        nltk.download('punkt', quiet=True)

    sentences = nltk.sent_tokenize(plain_text)
    for sentence in sentences:
        # The text inside the HTML is often just the words and spaces.
        # We'll normalize whitespace to improve matching chances.
        cleaned_sentence = ' '.join(sentence.split())
        if not cleaned_sentence:
            continue

        cv_score = get_bit_velocity_cv(cleaned_sentence)
        if cv_score >= MODERN_THRESHOLD:
            # We need to escape HTML entities in the sentence text itself
            # to match how it appears in the pdftohtml output.
            escaped_text = html.escape(cleaned_sentence)
            suspicious_sentences.add(escaped_text)
            
    print(f"Found {len(suspicious_sentences)} unique suspicious sentence patterns.")
    return suspicious_sentences

def inject_italics_into_html(html_path, plain_text_path, output_path):
    """
    Identifies suspicious sentences from plain_text and wraps them
    in <i> tags within the complex HTML file.
    This is a best-effort, direct string replacement.
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        with open(plain_text_path, 'r', encoding='utf-8') as f:
            plain_text = f.read()
    except FileNotFoundError as e:
        print(f"Error: Could not read input file - {e}", file=sys.stderr)
        sys.exit(1)

    suspicious_phrases = get_suspicious_sentences(plain_text)

    # Sort by length descending to replace longer sentences before shorter ones
    # that might be substrings of the longer ones.
    sorted_phrases = sorted(list(suspicious_phrases), key=len, reverse=True)

    count = 0
    print("Injecting italics into HTML (this may take a moment)...")
    for phrase in sorted_phrases:
        # This is a very brittle replacement. It assumes the exact phrase exists
        # within the HTML content as a contiguous string.
        # We need to be careful not to re-replace text.
        # The `(?!<)` is a negative lookahead to not match if we've already inserted a tag.
        
        # Create a regex that is flexible with whitespace between words
        # and not too greedy. This is slightly more robust than plain replacement.
        words = phrase.split()
        # Escape special regex characters in the words themselves
        escaped_words = [re.escape(w) for w in words]
        # Create a pattern that allows for variable whitespace and tags between words
        pattern = r'\s*'.join(escaped_words)
        
        # This is still not perfect, but it's a more robust attempt.
        # We find the text but wrap it with our tags.
        # Unfortunately, re.sub can't easily wrap a complex pattern that includes tags.
        # We will stick to a simpler, more direct replacement for this attempt.
        
        # We look for the phrase but ensure it's not already inside an <i> tag.
        # This is difficult with regex. Simple string replacement is the only feasible approach here.
        # To avoid re-italicizing, we can replace `phrase` with `<i>phrase</i>`
        # and subsequent searches for substrings won't find a clean match.
        
        if phrase in html_content:
            html_content = html_content.replace(phrase, f"<i>{phrase}</i>")
            count += 1
            
    print(f"Made {count} replacements.")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"\nSUCCESS: Final HTML file saved as '{output_path}'")
    except IOError as e:
        print(f"Error writing to output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Hardcoded paths for this specific task
    html_input = "html_output/newtestament.html"
    text_input = "newtestament_full.txt"
    html_output = "newtestament_final_with_italics.html"
    
    inject_italics_into_html(html_input, text_input, html_output)
