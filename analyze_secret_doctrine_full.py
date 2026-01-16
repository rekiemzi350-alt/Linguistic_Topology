import re
import sys

# Configuration
INPUT_FILE = "/data/data/com.termux/files/home/coffee/test_documents/Secret_Doctrine_Vol1.txt"
OUTPUT_REPORT = "/data/data/com.termux/files/home/coffee/test_results/Secret_Doctrine_Vol1_Analysis.txt"

# Topology Rebel Seeds
REBEL_SEEDS = {83, 84, 93, 94}

def clean_text(text):
    # Remove Gutenberg Header/Footer
    start_marker = "*** START OF THIS PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THIS PROJECT GUTENBERG EBOOK"
    
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    
    if start_idx != -1:
        text = text[start_idx:]
    if end_idx != -1:
        text = text[:end_idx]
        
    return text

def analyze_full_volume():
    print(f"Reading {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
    except FileNotFoundError:
        print("File not found! Make sure curl finished.")
        return

    clean_content = clean_text(raw_text)
    
    # Split sentences (simple heuristic)
    # 1. Replace newlines with spaces
    # 2. Split by . ? !
    content = clean_content.replace('\n', ' ')
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10] # Filter short noise
    
    print(f"Analyzing {len(sentences)} sentences...")
    
    rebel_sentences = []
    
    for i, sent in enumerate(sentences):
        # Calculate Seed (Letter Count)
        # Filter strictly for letters a-z
        letters_only = re.sub(r'[^a-zA-Z]', '', sent)
        seed = len(letters_only)
        
        # Check if Rebel
        if seed in REBEL_SEEDS:
            rebel_sentences.append({
                "index": i,
                "seed": seed,
                "text": sent
            })

    # Generate Report
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write("=== SECRET DOCTRINE VOL 1: FORENSIC TOPOLOGY REPORT ===\n")
        f.write(f"Total Sentences Analyzed: {len(sentences)}\n")
        f.write(f"Rebel Sentences Found:    {len(rebel_sentences)}\n")
        f.write(f"Rebel Saturation:         {(len(rebel_sentences)/len(sentences))*100:.2f}%")
        f.write("\n" + "-" * 60 + "\n\n")
        
        for item in rebel_sentences:
            f.write(f"[Seed {item['seed']}] (Sent #{item['index']})\n")
            f.write(f'"{item["text"]}"\n')
            f.write("-" * 30 + "\n")
            
    print(f"Analysis Complete. Found {len(rebel_sentences)} anomalies.")
    print(f"Report saved to {OUTPUT_REPORT}")

if __name__ == "__main__":
    analyze_full_volume()
