import os
import hashlib
import re
import shutil
from collections import Counter

# Configuration
SOURCE_DIR = "."
# Skip these directories to avoid messing up code or system files
SKIP_DIRS = {".git", ".gemini", "__pycache__", "node_modules", "Lazylist", "erik_calc"}
# Heuristics for splitting
SPLIT_PATTERNS = [
    r"(\n\s*Chapter\s+[IVX0-9]+.*?\n)",  # Chapter I...
    r"(\n\s*BOOK\s+[IVX0-9]+.*?\n)",     # BOOK I...
    r"(_{10,})",                         # _________
    r"(={10,})",                         # =========
    r"(\n\s*Topic:.*?\n)",               # Topic: ...
    r"(\n\s*Date: \d{4}-\d{2}-\d{2}.*?\n)" # Date: YYYY-MM-DD...
]

def calculate_md5(filepath):
    """Calculates MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return None

def normalize_text(text):
    """
    Cleans up line breaks and spacing.
    1. Unifies line endings.
    2. Removes excessive blank lines.
    3. Merges paragraph lines (heuristic: line ends with [a-z,], next starts with [a-z]).
    """
    # Standardize endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    
    # Remove excessive blank lines (max 2)
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    # Merge lines that look like broken paragraphs.
    # Look for: char[a-z,] + newline + char[a-z]
    # We replace the newline with a space.
    # Be careful not to merge list items or headers.
    lines = text.split('\n')
    normalized_lines = []
    if not lines: return ""
    
    buffer_line = lines[0]
    
    for i in range(1, len(lines)):
        current_line = lines[i]
        stripped_current = current_line.strip()
        stripped_buffer = buffer_line.strip()
        
        # Heuristic for merging
        should_merge = False
        if stripped_buffer and stripped_current:
            if stripped_buffer[-1] in "abcdefghijklmnopqrstuvwxyz,;" and stripped_current[0] in "abcdefghijklmnopqrstuvwxyz":
                should_merge = True
        
        if should_merge:
            buffer_line += " " + current_line.strip()
        else:
            normalized_lines.append(buffer_line)
            buffer_line = current_line
            
    normalized_lines.append(buffer_line)
    return "\n".join(normalized_lines)

def get_topics(text):
    """
    Simple keyword extraction to guess topic/group.
    """
    text_lower = text.lower()
    
    if "machiavelli" in text_lower or "prince" in text_lower:
        return "Machiavelli"
    if "oeis" in text_lower or "sequence" in text_lower:
        return "OEIS_Sequences"
    if "gemini" in text_lower or "assistant" in text_lower:
        return "Gemini_Conversations"
    if "linguistic" in text_lower or "topology" in text_lower:
        return "Linguistic_Topology"
    if "sumerian" in text_lower or "cuneiform" in text_lower:
        return "Ancient_Languages"
    if "python" in text_lower or "import os" in text_lower:
        return "Code_Snippets"
    
    return "Misc_Text"

def split_and_save(filepath, content):
    """
    Splits content based on regex patterns and saves to new files.
    Returns list of new files created.
    """
    # Determine best split pattern
    best_pattern = None
    max_splits = 1
    
    for pattern in SPLIT_PATTERNS:
        splits = re.split(pattern, content)
        # Filter empty splits
        valid_splits = [s for s in splits if len(s.strip()) > 100]
        if len(valid_splits) > max_splits:
            max_splits = len(valid_splits)
            best_pattern = pattern
    
    # If no significant splitting found, just save cleaned version
    if max_splits < 2:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return []

    # Perform split
    print(f"Splitting {filepath} into {max_splits} parts...")
    parts = re.split(best_pattern, content)
    
    base_dir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    created_files = []
    
    # Re-assemble parts (header + content)
    # re.split with capturing group keeps the delimiters.
    # We iterate and combine delimiters with following content if needed.
    
    # Simple approach: save every substantial chunk
    counter = 1
    for part in parts:
        if len(part.strip()) < 50: continue # Skip noise
        
        new_name = f"{name}_Part{counter}{ext}"
        new_path = os.path.join(base_dir, new_name)
        
        # Try to guess a better name from the first line of the part?
        # For now, keep it simple to avoid errors.
        
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(part)
        created_files.append(new_path)
        counter += 1
        
    # Remove original if splitting was successful
    if created_files:
        os.remove(filepath)
        
    return created_files

def main():
    print("Starting Text Corpus Cleanup...")
    
    # 1. Deduplication
    print("\n--- Deduplication ---")
    seen_hashes = {}
    duplicates_removed = 0
    
    all_txt_files = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Filter dirs
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                h = calculate_md5(path)
                if h in seen_hashes:
                    print(f"Removing duplicate: {path} (matches {seen_hashes[h]})")
                    os.remove(path)
                    duplicates_removed += 1
                else:
                    seen_hashes[h] = path
                    all_txt_files.append(path)
                    
    print(f"Removed {duplicates_removed} duplicates.")
    
    # 2. Cleaning & Splitting
    print("\n--- Cleaning & Splitting ---")
    processed_files = [] # List of final file paths
    
    for path in all_txt_files:
        # Check if file still exists (might be removed if dup)
        if not os.path.exists(path): continue
        
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            cleaned_content = normalize_text(content)
            
            # Save or Split
            new_files = split_and_save(path, cleaned_content)
            if new_files:
                processed_files.extend(new_files)
            else:
                processed_files.append(path)
                
        except Exception as e:
            print(f"Error processing {path}: {e}")

    # 3. Grouping
    print("\n--- Grouping by Topic ---")
    
    # Ensure group dirs exist
    groups = ["Machiavelli", "OEIS_Sequences", "Gemini_Conversations", 
              "Linguistic_Topology", "Ancient_Languages", "Code_Snippets", "Misc_Text"]
    
    for g in groups:
        os.makedirs(os.path.join(SOURCE_DIR, "Corpus_Groups", g), exist_ok=True)
        
    for path in processed_files:
        if not os.path.exists(path): continue
        
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                # Read first 2000 chars for topic guess
                sample = f.read(2000)
                
            topic = get_topics(sample)
            dest_dir = os.path.join(SOURCE_DIR, "Corpus_Groups", topic)
            filename = os.path.basename(path)
            dest_path = os.path.join(dest_dir, filename)
            
            # Handle name collision in destination
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                dest_path = os.path.join(dest_dir, f"{base}_{hashlib.md5(path.encode()).hexdigest()[:4]}{ext}")
            
            shutil.move(path, dest_path)
            
        except Exception as e:
            print(f"Error moving {path}: {e}")
            
    print("\nDone. Files are organized in ./Corpus_Groups/")

if __name__ == "__main__":
    main()
