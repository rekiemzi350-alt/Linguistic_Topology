import os
import subprocess
import zipfile
import re

# Source files from the list generated
INPUT_LIST = "files_to_convert.txt"
OUTPUT_DIR = "/data/data/com.termux/files/home/coffee/test_documents/converted_library/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_epub(path, out_path):
    try:
        with zipfile.ZipFile(path, 'r') as z:
            html_files = [n for n in z.namelist() if n.endswith(('.html', '.xhtml', '.htm'))]
            html_files.sort()
            text_content = []
            for h in html_files:
                with z.open(h) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    text = re.sub(r'<[^>]+>', ' ', content)
                    text = re.sub(r'\s+', ' ', text).strip()
                    if text: text_content.append(text)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(text_content))
        return True
    except: return False

def main():
    with open(INPUT_LIST, 'r') as f:
        files = [line.strip() for line in f.readlines()]

    print(f"Starting mass conversion of {len(files)} files...")
    
    for path in files:
        base = os.path.basename(path)
        name, ext = os.path.splitext(base)
        ext = ext.lower()
        out_path = os.path.join(OUTPUT_DIR, name + ".txt")
        
        if os.path.exists(out_path): continue

        if ext == ".epub":
            extract_epub(path, out_path)
        elif ext == ".pdf":
            subprocess.run(["pdftotext", path, out_path], capture_output=True)
        elif ext in [".docx", ".doc"]:
            # Basic fallback: strings extraction or simple zip parse if docx
            if ext == ".docx":
                try:
                    with zipfile.ZipFile(path, 'r') as z:
                        content = z.read('word/document.xml').decode('utf-8')
                        text = re.sub(r'<[^>]+>', ' ', content)
                        with open(out_path, 'w', encoding='utf-8') as f:
                            f.write(text)
                except: pass
            else:
                subprocess.run(["strings", path, ">", out_path], shell=True)

    print("Conversion complete.")

if __name__ == "__main__":
    main()
