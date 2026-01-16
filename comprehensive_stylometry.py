import sys
import os
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')

# Standard English frequency order (excluding Y for now)
CONSONANTS_BASE = "tnshrdlcmwfgpbvkjxzq" 
VOWELS_BASE = "eaoiu"

def is_y_vowel(word):
    word = word.lower()
    if 'y' not in word:
        return False
    if word.endswith('y'):
        return True
    y_indices = [i for i, char in enumerate(word) if char == 'y']
    for idx in y_indices:
        if 0 < idx < len(word) - 1:
            if word[idx-1] not in "aeiou" and word[idx+1] not in "aeiou":
                return True
    if not any(v in word for v in "aeiou"):
        return True
    return False

def get_letter_values(word):
    y_vowel = is_y_vowel(word)
    word = word.lower()
    
    if y_vowel:
        v_order = "eaoiuy"
        c_order = "tnshrdlcmwfgpbvkjxzq"
    else:
        v_order = "eaoiu"
        c_order = "tnshrdlcmwfgypbvkjxzq"

    v_map = {char: i + 1 for i, char in enumerate(v_order)}
    c_map = {char: i + 1 for i, char in enumerate(c_order)}
    
    values = []
    for char in word:
        if char in v_map:
            values.append(v_map[char])
        elif char in c_map:
            values.append(c_map[char])
    return values

def get_word_value(word):
    return sum(get_letter_values(word))

def simplify_tag(tag):
    if tag.startswith('NN'): return 'NOUN'
    if tag.startswith('VB'): return 'VERB'
    if tag.startswith('PRP'): return 'PRONOUN'
    if tag.startswith('JJ'): return 'ADJ'
    if tag.startswith('RB'): return 'ADV'
    return 'OTHER'

def analyze_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split into chapters (look for Chapter X or Part X at start of line)
    chapters = re.split(r'(?i)\n(?:Chapter|TABLET|Tablet|Part|Section)\s+(?:[IVXLCDM]+|\d+)\b', text)
    if len(chapters) <= 1:
        # Try splitting by single character Roman numerals if no "Chapter" prefix
        chapters = re.split(r'\n[IVXLCDM]+\.\n', text)
    
    if len(chapters) == 1:
        chapters = [text]
    else:
        # Filter out very short segments that might be metadata/TOC
        chapters = [c for c in chapters if len(c.strip()) > 500]

    chapter_data = []
    total_word_count = 0
    
    for c_idx, chapter_text in enumerate(chapters):
        if not chapter_text.strip():
            continue
        
        paragraphs = [p.strip() for p in chapter_text.split('\n\n') if p.strip()]
        chap_stats = {
            'paragraphs': len(paragraphs),
            'conv_paragraphs': 0,
            'sentences': 0,
            'conv_sentences': 0,
            'words': 0,
            'pos_counts': Counter(),
            'pos_values': Counter(),
            'sentences_per_para': [],
            'words_per_para': []
        }

        # Match any kind of double or single quote (straight, curly, or mangled UTF-8)
        conv_pattern = r'["\'\u201c\u201d\u2018\u2019\u00ab\u00bb]|â€[œ\x9d]|â€™'

        for para in paragraphs:
            has_conversation = bool(re.search(conv_pattern, para))
            if has_conversation:
                chap_stats['conv_paragraphs'] += 1
            
            sentences = sent_tokenize(para)
            chap_stats['sentences'] += len(sentences)
            chap_stats['sentences_per_para'].append(len(sentences))
            
            para_word_count = 0
            for sent in sentences:
                sent_has_conv = bool(re.search(conv_pattern, sent))
                if sent_has_conv:
                    chap_stats['conv_sentences'] += 1
                
                words = [w for w in word_tokenize(sent) if w.isalpha()]
                para_word_count += len(words)
                chap_stats['words'] += len(words)
                
                pos_tags = nltk.pos_tag(words)
                for word, tag in pos_tags:
                    cat = simplify_tag(tag)
                    val = get_word_value(word)
                    chap_stats['pos_counts'][cat] += 1
                    chap_stats['pos_values'][cat] += val
            
            chap_stats['words_per_para'].append(para_word_count)

        total_word_count += chap_stats['words']
        chapter_data.append(chap_stats)

    # PAGE APPROXIMATION (500 words per page)
    words_per_page = 500
    total_pages = max(1, total_word_count // words_per_page)

    print(f"--- Global Analysis Results for {os.path.basename(file_path)} ---")
    print(f"Total Chapters: {len(chapter_data)}")
    print(f"Total Word Count: {total_word_count}")
    print(f"Approximate Page Count: {total_pages}")
    
    total_conv_p = sum(c['conv_paragraphs'] for c in chapter_data)
    total_p = sum(c['paragraphs'] for c in chapter_data)
    print(f"\nParagraph Stats:")
    print(f"  Total Paragraphs: {total_p}")
    print(f"  Conversation Paragraphs: {total_conv_p} ({(total_conv_p/total_p*100):.1f}%)")
    print(f"  Non-Conversation Paragraphs: {total_p - total_conv_p} ({((total_p - total_conv_p)/total_p*100):.1f}%)")
    
    total_conv_s = sum(c['conv_sentences'] for c in chapter_data)
    total_s = sum(c['sentences'] for c in chapter_data)
    print(f"\nSentence Stats:")
    print(f"  Total Sentences: {total_s}")
    print(f"  Conversation Sentences: {total_conv_s} (Ratio: {total_conv_s/total_s:.2f})")
    print(f"  Non-Conversation Sentences: {total_s - total_conv_s} (Ratio: {(total_s - total_conv_s)/total_s:.2f})")

    print(f"\nPer Chapter Averages:")
    print(f"{ 'Chap':<5} | {'Words/Para':<12} | {'Sents/Para':<12} | {'Conv%':<8}")
    for i, c in enumerate(chapter_data):
        avg_w = sum(c['words_per_para'])/len(c['words_per_para']) if c['words_per_para'] else 0
        avg_s = sum(c['sentences_per_para'])/len(c['sentences_per_para']) if c['sentences_per_para'] else 0
        conv_pct = (c['conv_paragraphs']/c['paragraphs']*100) if c['paragraphs'] else 0
        print(f"{i+1:<5} | {avg_w:<12.1f} | {avg_s:<12.1f} | {conv_pct:<8.1f}%")

    print(f"\nGrammar Category Values (Total / Average per Word):")
    all_pos_counts = Counter()
    all_pos_values = Counter()
    for c in chapter_data:
        all_pos_counts += c['pos_counts']
        all_pos_values += c['pos_values']
    
    for cat in sorted(all_pos_counts.keys()):
        count = all_pos_counts[cat]
        val = all_pos_values[cat]
        avg = val/count if count else 0
        print(f"  {cat:<8}: Count={count:<6} TotalValue={val:<10} AvgValue={avg:.2f}")

    print(f"\nPage Averages (approx {words_per_page} words):")
    print(f"  Sentences/Page: {total_s/total_pages:.1f}")
    print(f"  Paragraphs/Page: {total_p/total_pages:.1f}")
    for cat in sorted(all_pos_counts.keys()):
        print(f"  {cat}/Page: {all_pos_counts[cat]/total_pages:.1f}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python comprehensive_stylometry.py <file_path>")
    else:
        analyze_text(sys.argv[1])
