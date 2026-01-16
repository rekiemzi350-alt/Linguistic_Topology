import re
import sys
import os

def identify_header(line):
    """
    Identifies if a line is a header for a section that needs segregation.
    Handles OCR typos and loose constraints for older texts.
    """
    clean_line = line.strip()
    if not clean_line or len(clean_line) > 100: 
        return False
    
    # Normalize for comparison
    upper_line = clean_line.upper()

    # 1. Strong Keywords (Standalone is usually enough for these)
    # The user asked for "Editor... in conjunction with...", but in practice
    # "PREFACE" in a translated work is *always* the translator/editor.
    # We will be aggressive to ensure we catch them.
    standalone_types = [
        "FOREWORD", "PREFACE", "PROLOGUE", "PRELUDE", 
        "PROLEGOMENON", "PREAMBLE", "CHRONOLOGY", "ABBREVIATIONS"
    ]
    
    for t in standalone_types:
        if t in upper_line:
            # Check if it's likely a header (short line, or contains 'THE')
            if len(upper_line) < 30 or "THE" in upper_line:
                return True

    # 2. "Introduction" with OCR Typo Tolerance
    # Pattern: I N T [any char] O D U C T I O N
    # Laurence text has "INTEODUCTION"
    intro_pattern = r"INT[A-Z]ODUCTION"
    if re.search(intro_pattern, upper_line):
        return True
        
    if "INTRODUCTION" in upper_line:
        return True

    # 3. Specific phrases requested
    if "TO THE READER" in upper_line: return True
    if "AUTHOR'S NOTE" in upper_line: return True
    if "NOTE TO THE READER" in upper_line: return True

    return False

def segment_file(file_path):
    print(f"Analyzing {file_path} for bias sections...")
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    dir_name = os.path.dirname(file_path)
    output_dir = os.path.join(dir_name, f"{base_name}_Segments")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    segments = []
    current_segment_name = "Front_Matter_Start" # Often title pages are just front matter
    current_lines = []
    
    # We want to identify the "Real" book start too. 
    # Usually "CHAPTER 1" or "CHAP. I" marks the end of bias sections.
    book_start_pattern = r"^(CHAPTER|CHAP\.|BOOK)\s+[IVX0-9]+"

    found_segments = 0

    for line in lines:
        is_header = identify_header(line)
        is_book_start = re.match(book_start_pattern, line.strip(), re.IGNORECASE)
        
        if is_book_start:
            # Everything from here on is definitely the book
            if current_lines:
                segments.append((current_segment_name, current_lines))
            current_segment_name = "The_Book_of_Enoch"
            current_lines = [line]
            found_segments += 1
            print(f" -> Found Book Start: {line.strip()}")
            # Determine if we just dump the rest? 
            # Actually, the loop continues, so if another "PREFACE" appears inside the book, 
            # we might split it. But usually headers don't appear mid-text.
            # We'll continue matching to be safe.
            
        elif is_header:
            # Save previous
            if current_lines:
                segments.append((current_segment_name, current_lines))
            
            # Start new
            # Sanitize filename
            clean_header = "".join(x for x in line.strip() if x.isalnum() or x in " _-")
            if len(clean_header) > 30: clean_header = clean_header[:30]
            current_segment_name = clean_header.replace(" ", "_")
            current_lines = [line]
            found_segments += 1
            print(f" -> Found Section: {line.strip()}")
            
        else:
            current_lines.append(line)

    # Final append
    if current_lines:
        segments.append((current_segment_name, current_lines))

    # Write
    count = 0
    created_files = []
    for name, seg_lines in segments:
        if len(seg_lines) < 2: continue
        
        # Dedupe names
        out_path = os.path.join(output_dir, f"{name}.txt")
        i = 1
        while os.path.exists(out_path):
            out_path = os.path.join(output_dir, f"{name}_{i}.txt")
            i += 1
            
        with open(out_path, 'w', encoding='utf-8') as f:
            f.writelines(seg_lines)
        created_files.append(out_path)
        count += 1

    print(f"Segmentation complete. Created {count} files in {output_dir}")
    return created_files

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python segment_text.py <file_path>")
        sys.exit(1)
    
    segment_file(sys.argv[1])