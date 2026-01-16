import os
import re

def check_files():
    for filename in os.listdir('.'):
        if filename.endswith(('.txt', '.html', '.md')):
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    hebrew = re.findall(r'[\u0590-\u05FF]', content)
                    if len(hebrew) > 100: # Threshold for a good sample
                        print(f"FOUND: {filename} ({len(hebrew)} Hebrew characters)")
            except Exception:
                pass

if __name__ == "__main__":
    check_files()
