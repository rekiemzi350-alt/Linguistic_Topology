import os
import re
import sys

# Configuration
DOCS_DIR = "/data/data/com.termux/files/home/coffee/test_documents/"
OUTPUT_CSV = "/data/data/com.termux/files/home/coffee/test_results/SD_Comprehensive_Quote_Analysis.csv"
REBEL_SEEDS = {83, 84, 93, 94}

def clean_gutenberg(text):
    # Remove header/footer
    start = text.find("*** START OF")
    end = text.find("*** END OF")
    if start != -1: text = text[start:]
    if end != -1: text = text[:end]
    return text

def detect_segment_type(line, in_quote_block):
    # Heuristics for Gutenberg text
    stripped = line.strip()
    
    # 1. Footnotes
    if stripped.startswith("[") or stripped.startswith("*"):
        return "FOOTNOTE", False
        
    # 2. Quotes (Indented blocks or " marks)
    # Gutenberg usually indents block quotes by 2-4 spaces
    # But main paragraphs might be indented too.
    # We rely on " marks for sure quotes, and deep indentation for block quotes.
    if line.startswith("    ") and not line.strip() == "":
        # Potential block quote
        return "QUOTE", True
        
    if '"' in line or "“" in line:
        return "QUOTE_INLINE", False
        
    if in_quote_block and line.strip() != "":
        # Continuation of block
        return "QUOTE", True
        
    # Default
    return "MAIN_TEXT", False

def analyze_sentence(sent):
    letters = re.sub(r'[^a-zA-Z]', '', sent)
    seed = len(letters)
    is_rebel = seed in REBEL_SEEDS
    words = len(sent.split())
    
    # Simple Stylometry: Avg Word Length
    avg_word_len = 0
    if words > 0:
        avg_word_len = seed / words
        
    return seed, is_rebel, words, avg_word_len

def process_volume(vol_num, filename):
    print(f"Processing Volume {vol_num}...")
    path = os.path.join(DOCS_DIR, filename)
    
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
    except:
        print(f"Failed to read {filename}")
        return []

    text = clean_gutenberg(raw_text)
    lines = text.split('\n')
    
    results = []
    current_segment = "MAIN_TEXT"
    in_quote = False
    buffer_sent = ""
    
    # Line-by-line parsing to handle segmentation
    for line in lines:
        if not line.strip(): continue
        
        seg_type, in_quote = detect_segment_type(line, in_quote)
        
        # Sentence Accumulation
        # We append line to buffer, then split by .!?
        # This is tricky because a sentence might span segments.
        # We will attribute the sentence to the segment where it *ends* or mostly resides.
        
        buffer_sent += " " + line.strip()
        
        # Check for sentence end
        if re.search(r'[.!?]["”]?\s*$', line):
            # Split buffer into sentences (handle multiple per line)
            sents = re.split(r'(?<=[.!?]["”])\s+', buffer_sent)
            
            for s in sents:
                s = s.strip()
                if len(s) < 10: continue # Skip noise
                
                seed, rebel, words, avg_w = analyze_sentence(s)
                
                # Truncate text for CSV
                snippet = s[:50].replace(",", " ").replace('"', "'")
                
                results.append(f"{vol_num},{seg_type},{seed},{rebel},{words},{avg_w:.2f},\"{snippet}...\"")
            
            buffer_sent = ""
            
    return results

def main():
    volumes = [
        (1, "Secret_Doctrine_Vol1.txt"),
        (2, "Secret_Doctrine_Vol2.txt"),
        (3, "Secret_Doctrine_Vol3.txt"),
        (4, "Secret_Doctrine_Vol4.txt")
    ]
    
    all_data = []
    
    for vol, file in volumes:
        data = process_volume(vol, file)
        all_data.extend(data)
        
    # Write Master CSV
    print(f"Writing Report to {OUTPUT_CSV}...")
    with open(OUTPUT_CSV, 'w', encoding='utf-8') as f:
        f.write("Volume,Type,Seed,Is_Rebel,Word_Count,Avg_Word_Len,Text_Snippet\n")
        for line in all_data:
            f.write(line + "\n")
            
    # Calculate Statistics
    print("\n--- SUMMARY STATISTICS ---")
    
    total = len(all_data)
    rebels = sum(1 for line in all_data if ",True," in line)
    quotes = sum(1 for line in all_data if "QUOTE" in line)
    rebel_quotes = sum(1 for line in all_data if "QUOTE" in line and ",True," in line)
    
    print(f"Total Sentences: {total}")
    print(f"Total Rebels:    {rebels} ({rebels/total*100:.2f}%)")
    print(f"Total Quotes:    {quotes}")
    print(f"Rebels in Quotes: {rebel_quotes} ({rebel_quotes/quotes*100:.2f}% of quotes)")
    
    if (rebel_quotes/quotes) > (rebels/total):
        print("SIGNIFICANCE: Quotes have HIGHER topological friction than main text. (Possible Translation Artifact)")
    else:
        print("SIGNIFICANCE: Quotes have LOWER/EQUAL topological friction. (Possible Homogenization/Hoax)")

if __name__ == "__main__":
    main()
