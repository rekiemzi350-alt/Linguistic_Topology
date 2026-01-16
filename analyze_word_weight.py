import sys
import re

def get_word_weight(word):
    weight = 0
    for char in word.lower():
        if 'a' <= char <= 'z':
            # ord('a') is 97, so ord(c) - 96 gives a=1, b=2...
            weight += ord(char) - 96
    return weight

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        return

    # Split into words (remove punctuation)
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    
    if not words:
        print("No words found.")
        return

    weights = [get_word_weight(w) for w in words]
    
    # Calculate Stats
    avg_weight = sum(weights) / len(weights)
    max_weight = max(weights)
    heaviest_word = words[weights.index(max_weight)]
    
    print(f"\n--- WEIGHT ANALYSIS: {filepath} ---")
    print(f"Total Words Scanned: {len(words)}")
    print(f"Average Word Weight: {avg_weight:.2f}")
    print(f"Heaviest Word:       '{heaviest_word}' (Score: {max_weight})")
    
    print("\n--- THE WORD-WEIGHT WAVEFORM (First 50 Words) ---")
    print("Height = Sum of Letter Values (A=1...Z=26)\n")
    
    # Simple ASCII Graph for first 50 words
    limit = 50
    graph_height = 15
    sample = weights[:limit]
    max_sample = max(sample) if sample else 1
    
    # Normalize to graph height
    grid = [[' ' for _ in range(limit)] for _ in range(graph_height)]
    
    for x, w in enumerate(sample):
        # Scale weight to grid height
        h = int((w / max_sample) * (graph_height - 1))
        for y in range(h + 1):
            char = "█" if y == h else "│"
            grid[graph_height - 1 - y][x] = char

    for row in grid:
        print("".join(row))
        
    print("-" * limit)
    print("Word Position ->")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_word_weight.py <file1> <file2> ...")
    else:
        for f in sys.argv[1:]:
            analyze_file(f)
