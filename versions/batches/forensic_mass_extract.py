import os
import subprocess
import sys

def extract_text(pdf_path):
    txt_path = pdf_path.replace(".pdf", ".txt")
    print(f"Extracting: {pdf_path} -> {txt_path}")
    # Using pdftotext if available, else a simple python fallback
    try:
        subprocess.run(["pdftotext", pdf_path, txt_path], check=True)
        return txt_path
    except Exception as e:
        print(f"pdftotext failed for {pdf_path}: {e}")
        return None

if __name__ == "__main__":
    target_dir = "test_documents"
    files = [f for f in os.listdir(target_dir) if f.endswith(".pdf")]
    for f in files:
        extract_text(os.path.join(target_dir, f))
