import os
import shutil
import zipfile
import re
import subprocess
import time

# Configuration
DEST_DIR = "/data/data/com.termux/files/home/coffee/test_documents/"
REPORT_DIR = "/data/data/com.termux/files/home/coffee/test_results/"
REPORT_FILE = os.path.join(REPORT_DIR, "conversion_report.txt")
MAIN_STORAGE_REPORT_FILE = "/sdcard/Documents/test_results/conversion_report.txt"

# Ensure report directories exist
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MAIN_STORAGE_REPORT_FILE), exist_ok=True)

def calculate_accuracy(text):
    if not text:
        return 0.0
    
    total_chars = len(text)
    # Count printable characters and common whitespace
    printable_chars = len(re.findall(r'[a-zA-Z0-9\s.,!?;:()\'"-]', text))
    # Check for replacement characters
    replacement_chars = text.count('\ufffd')
    
    accuracy = (printable_chars / total_chars) * 100
    # Penalize replacement characters heavily
    if replacement_chars > 0:
        accuracy -= (replacement_chars / total_chars) * 100
    
    return max(0.0, min(100.0, accuracy))

def extract_epub(path):
    try:
        text_content = []
        with zipfile.ZipFile(path, 'r') as z:
            html_files = [n for n in z.namelist() if n.endswith(('.html', '.xhtml', '.htm'))]
            html_files.sort()
            for h in html_files:
                with z.open(h) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    text = re.sub(r'<[^>]+>', ' ', content)
                    text = re.sub(r'\s+', ' ', text).strip()
                    if text: text_content.append(text)
        return "\n".join(text_content)
    except:
        return None

def extract_pdf(path):
    try:
        out_path = path + ".tmp.txt"
        subprocess.run(["pdftotext", path, out_path], capture_output=True)
        if os.path.exists(out_path):
            with open(out_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            os.remove(out_path)
            return text
    except:
        pass
    return None

def extract_docx(path):
    try:
        with zipfile.ZipFile(path, 'r') as z:
            content = z.read('word/document.xml').decode('utf-8', errors='ignore')
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
    except:
        return None

def extract_ocr(path):
    try:
        out_base = path + ".tmp"
        subprocess.run(["tesseract", path, out_base], capture_output=True)
        out_path = out_base + ".txt"
        if os.path.exists(out_path):
            with open(out_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            os.remove(out_path)
            return text
    except:
        pass
    return None

def main():
    report_lines = [
        "=== LINGUISTIC TOOLKIT CONVERSION REPORT ===",
        f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "-" * 50,
        f"{ 'Filename':<50} | {'Status':<10} | {'Accuracy':<10} | {'Error %':<10}",
        "-" * 50
    ]
    
    files = os.listdir(DEST_DIR)
    total_files = 0
    success_files = 0
    
    for filename in sorted(files):
        file_path = os.path.join(DEST_DIR, filename)
        if not os.path.isfile(file_path):
            continue
            
        base_name, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # Skip already converted or results
        if ext in ['.txt', '.results', '.csv', '.log', '.mp3']:
            continue
            
        total_files += 1
        print(f"Processing: {filename}")
        
        converted_text = None
        if ext == '.epub':
            converted_text = extract_epub(file_path)
        elif ext == '.pdf':
            converted_text = extract_pdf(file_path)
        elif ext == '.docx':
            converted_text = extract_docx(file_path)
        elif ext in ['.jpg', '.jpeg', '.png']:
            converted_text = extract_ocr(file_path)
            
        if converted_text and len(converted_text.strip()) > 10:
            accuracy = calculate_accuracy(converted_text)
            error_pct = 100.0 - accuracy
            
            txt_path = os.path.join(DEST_DIR, base_name + ".txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(converted_text)
            
            report_lines.append(f"{filename[:50]:<50} | {'SUCCESS':<10} | {accuracy:>8.2f}% | {error_pct:>8.2f}%")
            success_files += 1
            
            # Clean up original file as requested
            os.remove(file_path)
        else:
            report_lines.append(f"{filename[:50]:<50} | {'FAILED':<10} | {0.0:>8.2f}% | {100.0:>8.2f}%")

    report_lines.append("-" * 50)
    report_lines.append(f"Total processed: {total_files}")
    report_lines.append(f"Successful conversions: {success_files}")
    if total_files > 0:
        avg_success = (success_files / total_files) * 100
        report_lines.append(f"Overall Success Rate: {avg_success:.2f}%")
    
    report_content = "\n".join(report_lines)
    
    # Save reports
    with open(REPORT_FILE, 'w') as f:
        f.write(report_content)
    with open(MAIN_STORAGE_REPORT_FILE, 'w') as f:
        f.write(report_content)
        
    print(f"\nConversion complete. Report saved to:\n1. {REPORT_FILE}\n2. {MAIN_STORAGE_REPORT_FILE}")

if __name__ == "__main__":
    main()
