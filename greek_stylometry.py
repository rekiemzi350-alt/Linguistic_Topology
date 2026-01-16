import sys
import os
import re
from collections import Counter

# Ancient Greek frequency order (Approximate based on Perseus/TLG data)
# Vowels: ε α ο ι η υ ω
# Consonants: σ ν τ ρ π λ μ δ κ γ θ χ ζ ψ φ ξ
GREEK_ORDER = "εαοισντρῃπλυδκγθχζψφξω" # Order of commonality

def get_letter_values(word):
    word = word.lower()
    # Basic mapping for Greek characters
    v_order = "εαοίιηυωῃ" 
    c_order = "σντρπλυδκγθχζψφξ" # Note: υ can be ambiguous but treated as vowel usually
    
    # We will use the GREEK_ORDER for a general topological weight
    v_map = {char: i + 1 for i, char in enumerate(GREEK_ORDER)}
    
    values = []
    for char in word:
        if char in v_map:
            values.append(v_map[char])
        else:
            # Handle accented characters by normalization (simplified)
            norm_char = char.replace('ά','α').replace('έ','ε').replace('ή','η').replace('ί','ι').replace('ό','ο').replace('ύ','υ').replace('ώ','ω')
            if norm_char in v_map:
                values.append(v_map[norm_char])
    return values

def get_word_value(word):
    return sum(get_letter_values(word))

def analyze_greek_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Clean text: keep only Greek characters
    greek_only = re.findall(r'[\u0370-\u03FF\u1F00-\u1FFF]+', text)
    
    # Basic structural units
    words = [w for w in greek_only if len(w) > 1]
    
    # In Greek, sentences usually end with . ; (which is ?) or ·
    sentences = re.split(r'[.;·]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

    total_value = sum(get_word_value(w) for w in words)
    avg_word_val = total_value / len(words) if words else 0
    
    # Calculate word lengths and weights
    weights = [get_word_value(w) for w in words]
    
    print(f"--- Greek Topological Analysis: {os.path.basename(file_path)} ---")
    print(f"Total Greek Words: {len(words)}")
    print(f"Total Sentences: {len(sentences)}")
    print(f"Mean Word Weight (Topological): {avg_word_val:.2f}")
    
    # Variance in weight (Complexity check)
    if weights:
        mean = sum(weights) / len(weights)
        variance = sum((w - mean) ** 2 for w in weights) / len(weights)
        print(f"Weight Variance (Style Skewness): {variance:.2f}")

    # Pacing
    print(f"Words per Sentence: {len(words)/len(sentences):.1f}" if sentences else "N/A")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python greek_stylometry.py <file_path>")
    else:
        analyze_greek_text(sys.argv[1])
