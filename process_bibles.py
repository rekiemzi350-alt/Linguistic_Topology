import os
import re

BOOKS_66 = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
    "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians",
    "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians",
    "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
]

def process_nkjv(input_path, output_dir):
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    book_data = {i+1: [] for i in range(66)}
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split('\t')
            if len(parts) >= 4:
                try:
                    book_id = int(parts[0])
                    text = parts[3].strip()
                    if book_id in book_data:
                        book_data[book_id].append(text)
                except ValueError:
                    continue
                    
    for b_id, lines in book_data.items():
        if lines:
            book_name = BOOKS_66[b_id-1].replace(" ", "_")
            # Put double newline between verses to act as paragraph markers for analysis
            with open(f"{output_dir}/{b_id:02d}_{book_name}.txt", 'w', encoding='utf-8') as out:
                out.write("\n\n".join(lines))

def split_gutenberg(input_path, output_dir, book_list):
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Improved regex for Bible book titles
    book_content = {name: [] for name in book_list}
    current_book = None
    
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        upper_stripped = stripped.upper()
        
        found = False
        for name in book_list:
            # Check for various title formats
            titles = [
                name.upper(),
                f"THE BOOK OF {name.upper()}",
                f"THE FIRST BOOK OF {name.upper()}",
                f"THE SECOND BOOK OF {name.upper()}",
                f"THE HOLY GOSPEL OF JESUS CHRIST ACCORDING TO SAINT {name.upper()}",
                f"THE HOLY GOSPEL OF JESUS CHRIST ACCORDING TO ST. {name.upper()}"
            ]
            if upper_stripped in titles:
                current_book = name
                found = True
                break
        
        if current_book and not found:
            book_content[current_book].append(line)
            
    for i, name in enumerate(book_list):
        lines = book_content[name]
        if lines:
            safe_name = name.replace(" ", "_")
            with open(f"{output_dir}/{i+1:02d}_{safe_name}.txt", 'w', encoding='utf-8') as out:
                out.write("\n\n".join(lines))

if __name__ == "__main__":
    process_nkjv("test_documents/bible_nkjv.txt", "test_documents/NKJV")
    split_gutenberg("test_documents/bible_kjv.txt", "test_documents/KJV", BOOKS_66)
    split_gutenberg("test_documents/bible_douay.txt", "test_documents/DOUAY", BOOKS_66)