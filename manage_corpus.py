import os
import sys
import xml.etree.ElementTree as ET
import re
import segment_text

def clean_text_content(text):
    """Normalize text: remove extra whitespace."""
    return re.sub(r'\s+', ' ', text).strip()

def parse_abbyy_xml(xml_file, output_file):
    print(f"Parsing {xml_file}...")
    
    current_line_chars = []
    all_lines = []
    
    # Use iterparse to handle large files
    try:
        context = ET.iterparse(xml_file, events=("start", "end"))
        context = iter(context)
        event, root = next(context)

        for event, elem in context:
            tag_name = elem.tag.split('}')[-1]
            
            if event == "end" and tag_name == "charParams":
                if elem.text:
                    current_line_chars.append(elem.text)
                else:
                    current_line_chars.append(" ")
                elem.clear()
                
            elif event == "end" and tag_name == "line":
                line_text = "".join(current_line_chars).strip()
                if line_text:
                    all_lines.append(line_text)
                current_line_chars = []
                elem.clear()
                
            elif event == "end" and tag_name == "page":
                elem.clear()
                
        # Basic cleaning of common OCR headers
        cleaned_lines = []
        header_patterns = [
            r'^\d+$', 
            r'^Digitized by', 
            r'^University of Toronto', 
            r'^\^5\d+$'
        ]
        
        for line in all_lines:
            is_header = False
            for pat in header_patterns:
                if re.search(pat, line, re.IGNORECASE):
                    is_header = True
                    break
            if not is_header:
                cleaned_lines.append(line)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(cleaned_lines))
            
        print(f"Success! Saved {len(cleaned_lines)} lines to {output_file}")
        
    except Exception as e:
        print(f"Error parsing XML: {e}")

def list_corpus():
    corpus_dir = "test_documents"
    print(f"Scanning {corpus_dir}...")
    count = 0
    if os.path.exists(corpus_dir):
        for root, dirs, files in os.walk(corpus_dir):
            for file in files:
                if file.endswith(".txt"):
                    print(f" - {file}")
                    count += 1
    print(f"Total: {count} text files found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_corpus.py list")
        print("  python manage_corpus.py import_abbyy <xml_file> <output_txt>")
        print("  python manage_corpus.py segment <file_path>")
        sys.exit(1)
        
    cmd = sys.argv[1]
    
    if cmd == "list":
        list_corpus()
    elif cmd == "import_abbyy":
        if len(sys.argv) != 4:
            print("Usage: python manage_corpus.py import_abbyy <xml_file> <output_txt>")
        else:
            parse_abbyy_xml(sys.argv[2], sys.argv[3])
    elif cmd == "segment":
        if len(sys.argv) != 3:
            print("Usage: python manage_corpus.py segment <file_path>")
        else:
            segment_text.segment_file(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
