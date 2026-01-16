import os
import re
import sys

# --- Text Cleaning & Parsing ---

def clean_text(text):
    """
    Removes XML/HTML tags, headers, and excessive whitespace.
    Tries to isolate the narrative content.
    """
    # Remove XML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove common ebook headers/footers (simplified)
    lines = text.split('\n')
    cleaned_lines = []
    
    start_reading = False
    
    # Heuristic: Skip metadata header until we see a substantial paragraph or Chapter 1
    # For now, just skip empty lines and very short lines at start
    for line in lines:
        s = line.strip()
        if not s: continue
        cleaned_lines.append(s)
        
    return "\n".join(cleaned_lines)

def analyze_structure(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
            
        clean_content = clean_text(raw_text)
        
        # 1. Chapter Analysis
        # Regex for Roman Numerals or "Chapter"
        chapter_matches = re.findall(r'^(?:Chapter|Book|PART)\s+[IVXLCDM\d]+', clean_content, re.MULTILINE | re.IGNORECASE)
        num_chapters = len(chapter_matches)
        if num_chapters == 0:
            # Fallback: Look for just Roman Numerals on a line by themselves
            num_chapters = len(re.findall(r'^[IVXLCDM]+$', clean_content, re.MULTILINE))

        # 2. Sentence Analysis
        # Simple split by punctuation
        sentences = re.split(r'[.!?]+', clean_content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5] # Filter noise
        num_sentences = len(sentences)
        
        avg_sentence_len = 0
        if num_sentences > 0:
            total_words = sum(len(s.split()) for s in sentences)
            avg_sentence_len = total_words / num_sentences

        # 3. Conversation Analysis
        # Count quotes
        quote_matches = re.findall(r'“[^”]+”|"[^ "]+"', clean_content)
        num_quotes = len(quote_matches)
        
        dialogue_ratio = 0
        if num_sentences > 0:
            dialogue_ratio = (num_quotes / num_sentences) * 100

        # Output Report
        print(f"\n--- Analysis: {os.path.basename(filepath)} ---")
        print(f"Total Chapters:   {num_chapters}")
        print(f"Total Sentences:  {num_sentences}")
        print(f"Avg Sentence Len: {avg_sentence_len:.1f} words")
        print(f"Conversations:    {num_quotes} dialogue blocks")
        print(f"Dialogue Ratio:   {dialogue_ratio:.1f}%")
        
        return {
            "file": os.path.basename(filepath),
            "chapters": num_chapters,
            "sentences": num_sentences,
            "avg_len": avg_sentence_len,
            "dialogue": num_quotes
        }
        
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def main():
    target_dir = "/data/data/com.termux/files/home/coffee/test_documents/"
    
    print(f"Scanning directory: {target_dir}\n")
    
    results = []
    
    for filename in os.listdir(target_dir):
        if filename.endswith(".txt") and not filename.endswith(".results"):
            full_path = os.path.join(target_dir, filename)
            res = analyze_structure(full_path)
            if res:
                results.append(res)
    
    # Save Summary CSV
    with open("book_structure_report.csv", "w") as f:
        f.write("File,Chapters,Sentences,Avg_Len,Dialogue_Count\n")
        for r in results:
            f.write(f"{r['file']},{r['chapters']},{r['sentences']},{r['avg_len']:.2f},{r['dialogue']}\n")
            
    print("\nBatch Analysis Complete. Summary saved to 'book_structure_report.csv'.")

if __name__ == "__main__":
    main()
