import os
import shutil
import zipfile
import re
import subprocess
import time
import sys

# Configuration
SOURCE_DIR = "/sdcard/Documents/test_files/"
DEST_DIR = "/data/data/com.termux/files/home/coffee/test_documents/"
REPORT_DIR = "/data/data/com.termux/files/home/coffee/test_results/"
REPORT_FILE = os.path.join(REPORT_DIR, "conversion_report.txt")
MAIN_STORAGE_REPORT_DIR = "/sdcard/Documents/test_results/"
MAIN_STORAGE_REPORT_FILE = os.path.join(MAIN_STORAGE_REPORT_DIR, "conversion_report.txt")

# Ensure directories exist
os.makedirs(DEST_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(MAIN_STORAGE_REPORT_DIR, exist_ok=True)

def calculate_accuracy(text):
    if not text:
        return 0.0
    
    total_chars = len(text)
    if total_chars == 0:
        return 0.0

    # Count printable characters and common whitespace
    # We want to penalize "garbage" characters or replacement chars.
    printable_chars = len(re.findall(r'[a-zA-Z0-9\s.,!?;:()\'"-\[\]]', text))
    
    # Check for replacement characters or weird control codes (excluding standard whitespace)
    replacement_chars = text.count('\ufffd')
    
    # Simple heuristic: Ratio of good chars to total.
    accuracy = (printable_chars / total_chars) * 100
    
    # Penalize specific "bad" indicators heavily
    if replacement_chars > 0:
        accuracy -= (replacement_chars / total_chars) * 100 * 2 # Double penalty
    
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
                    # Simple HTML tag stripping
                    text = re.sub(r'<[^>]+>', ' ', content)
                    text = re.sub(r'\s+', ' ', text).strip()
                    if text: text_content.append(text)
        return "\n".join(text_content)
    except Exception as e:
        print(f"Error extracting EPUB {path}: {e}")
        return None

def extract_pdf(path):
    try:
        out_path = path + ".tmp.txt"
        # -layout preserves layout which is often better for structure, but -raw might be cleaner text.
        # Defaulting to standard (no flag) or -layout.
        subprocess.run(["pdftotext", path, out_path], capture_output=True, check=True)
        if os.path.exists(out_path):
            with open(out_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            os.remove(out_path)
            return text
    except Exception as e:
        print(f"Error extracting PDF {path}: {e}")
        pass
    return None

def extract_docx(path):
    try:
        with zipfile.ZipFile(path, 'r') as z:
            content = z.read('word/document.xml').decode('utf-8', errors='ignore')
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
    except Exception as e:
        print(f"Error extracting DOCX {path}: {e}")
        return None

def extract_ocr(path):
    try:
        out_base = path + ".tmp"
        # tesseract adds .txt extension automatically
        subprocess.run(["tesseract", path, out_base], capture_output=True, check=True)
        out_path = out_base + ".txt"
        if os.path.exists(out_path):
            with open(out_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            os.remove(out_path)
            return text
    except Exception as e:
        print(f"Error extracting Image {path}: {e}")
        pass
    return None

def main():
    print("=== STARTING SYNC AND CONVERT PROCESS ===")
    
    log_lines = [
        "=== TEST CORPUS CONVERSION REPORT ===",
        f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "-" * 80,
        f"{ 'Filename':<40} | {'Status':<10} | {'Acc %':<8} | {'Err %':<8} | {'Orig Size'}",
        "-" * 80
    ]
    
    # 1. SYNC
    print(f"Syncing from {SOURCE_DIR}...")
    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory not found: {SOURCE_DIR}")
        return

    source_files = os.listdir(SOURCE_DIR)
    synced_count = 0
    
    for filename in source_files:
        src_path = os.path.join(SOURCE_DIR, filename)
        dest_path = os.path.join(DEST_DIR, filename)
        
        # Skip directories
        if os.path.isdir(src_path):
            continue

        if not os.path.exists(dest_path):
            # Check if we already have a converted .txt version
            base, _ = os.path.splitext(filename)
            txt_dest = os.path.join(DEST_DIR, base + ".txt")
            if not os.path.exists(txt_dest):
                try:
                    shutil.copy2(src_path, dest_path)
                    synced_count += 1
                except Exception as e:
                    print(f"Failed to copy {filename}: {e}")

    print(f"Synced {synced_count} new files.")
    log_lines.append(f"Synced {synced_count} new files from source.")
    log_lines.append("-" * 80)
    
    # 2. CONVERT
    print("Converting files...")
    files_in_dest = sorted(os.listdir(DEST_DIR))
    
    success_count = 0
    fail_count = 0
    skipped_count = 0
    
    for filename in files_in_dest:
        file_path = os.path.join(DEST_DIR, filename)
        if not os.path.isfile(file_path):
            continue
            
        base_name, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # Skip text files and result files
        if ext in ['.txt', '.results', '.csv', '.log', '.mp3', '.py', '.sh', '.bak']:
            continue
            
        print(f"Processing: {filename}")
        
        original_size = os.path.getsize(file_path)
        converted_text = None
        
        if ext == '.epub':
            converted_text = extract_epub(file_path)
        elif ext == '.pdf':
            converted_text = extract_pdf(file_path)
        elif ext == '.docx':
            converted_text = extract_docx(file_path)
        elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            converted_text = extract_ocr(file_path)
        else:
            log_lines.append(f"{filename[:40]:<40} | {'SKIP':<10} | {'-':>8} | {'-':>8} | {original_size}")
            skipped_count += 1
            continue
            
        if converted_text and len(converted_text.strip()) > 0:
            accuracy = calculate_accuracy(converted_text)
            error_pct = 100.0 - accuracy
            
            txt_path = os.path.join(DEST_DIR, base_name + ".txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(converted_text)
            
            status = "SUCCESS"
            if accuracy < 50.0:
                status = "LOW_ACC" # Warning flag
            
            log_lines.append(f"{filename[:40]:<40} | {status:<10} | {accuracy:>8.2f} | {error_pct:>8.2f} | {original_size}")
            success_count += 1
            
            # Clean up original file
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error removing {filename}: {e}")
                
        else:
            log_lines.append(f"{filename[:40]:<40} | {'FAIL':<10} | {0.0:>8.2f} | {100.0:>8.2f} | {original_size}")
            fail_count += 1

    # Summary
    log_lines.append("-" * 80)
    log_lines.append(f"Total Processed: {success_count + fail_count + skipped_count}")
    log_lines.append(f"Successful:      {success_count}")
    log_lines.append(f"Failed:          {fail_count}")
    log_lines.append(f"Skipped:         {skipped_count}")
    
    report_content = "\n".join(log_lines)
    
    # Save reports
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    try:
        with open(MAIN_STORAGE_REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"Reports saved to:\n {REPORT_FILE}\n {MAIN_STORAGE_REPORT_FILE}")
    except Exception as e:
        print(f"Report saved to {REPORT_FILE}, but failed to copy to main storage: {e}")

if __name__ == "__main__":
    main()