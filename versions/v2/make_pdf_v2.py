import zipfile
import os
from fpdf import FPDF
import re
import sys

# Extract images
print("Extracting images...")
with zipfile.ZipFile('exhaustiveconcor1890stro.epub', 'r') as z:
    for f in z.namelist():
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Extract to current dir, flattening path (EPUB/image.jpg -> image.jpg)
            # because HTML likely refs them relatively or we need to fix paths.
            # The HTML refs are likely relative.
            # However, stripped HTML often loses path context.
            # If HTML says <img src="image_0001.jpg">, fpdf looks in cwd.
            filename = os.path.basename(f)
            with open(filename, 'wb') as img_out:
                img_out.write(z.read(f))

# Updated PDF Generation
ROBOTO_PATH = '/system/fonts/Roboto-Regular.ttf'
NOTO_HEBREW_PATH = '/system/fonts/NotoSansHebrew-Regular.ttf'
NOTO_ARAMAIC_PATH = '/system/fonts/NotoSansImperialAramaic-Regular.ttf'

def create_pdf(html_path, output_path, title):
    print(f"Processing {html_path} -> {output_path}...")
    pdf = FPDF()
    pdf.add_page()
    
    # Register Fonts - MAPPING EVERYTHING TO REGULAR TO AVOID CRASHES
    pdf.add_font("Roboto", style="", fname=ROBOTO_PATH)
    pdf.add_font("Roboto", style="B", fname=ROBOTO_PATH)
    pdf.add_font("Roboto", style="I", fname=ROBOTO_PATH)
    pdf.add_font("Roboto", style="BI", fname=ROBOTO_PATH)
    
    pdf.add_font("NotoHebrew", style="", fname=NOTO_HEBREW_PATH)
    pdf.add_font("NotoHebrew", style="B", fname=NOTO_HEBREW_PATH) # Fake
    
    # Try Aramaic
    try:
        pdf.add_font("NotoAramaic", fname=NOTO_ARAMAIC_PATH)
        has_aramaic = True
    except:
        has_aramaic = False

    pdf.set_font("Roboto", size=12)
    
    # Fallbacks
    fallbacks = ["NotoHebrew"]
    if has_aramaic:
        fallbacks.append("NotoAramaic")
    pdf.set_fallback_fonts(fallbacks)

    # Title
    pdf.set_font("Roboto", size=24)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    pdf.set_font("Roboto", size=10)

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Pre-process HTML to fix image paths if necessary
        # If HTML has <img src="EPUB/image.jpg"> and we extracted to ., we need to remove EPUB/ prefix
        # or just hope basename matches.
        # Actually, extracting to basename is safest if HTML uses basename.
        # Let's clean the HTML text slightly.
        # Remove <head>...</head> to avoid meta tag errors
        text = re.sub(r'<head>.*?</head>', '', text, flags=re.DOTALL)
        
        # Split chunks
        chunks = re.split(r'(<div.*?</div>|<p.*?</p>|<br\s*/>)', text, flags=re.DOTALL)
        
        count = 0
        buffer = ""
        for chunk in chunks:
            if not chunk.strip():
                continue
            
            # Check for image tags in chunk and ensure they point to existing files
            # <img src="EPUB/image.jpg"/> -> <img src="image.jpg"/>
            chunk = re.sub(r'src=["\'].*?/([^/]+\.(jpg|jpeg|png|gif))["\']', r'src="\1"', chunk, flags=re.IGNORECASE)

            buffer += chunk
            # Smaller buffer for safety
            if len(buffer) > 20000: 
                try:
                    pdf.write_html(buffer)
                except Exception as e:
                    print(f"Error writing chunk: {e}")
                    # Fallback: strip tags
                    clean_text = re.sub('<[^<]+?>', '', buffer)
                    try:
                        pdf.multi_cell(0, 5, clean_text)
                    except:
                        pass
                buffer = ""
                count += 1
                if count % 100 == 0:
                    print(f"Processed {count} chunks...")
        
        if buffer:
            try:
                pdf.write_html(buffer)
            except:
                 clean_text = re.sub('<[^<]+?>', '', buffer)
                 pdf.multi_cell(0, 5, clean_text)

        pdf.output(output_path)
        print(f"Successfully created {output_path}")

    except Exception as e:
        print(f"Failed to create PDF {output_path}: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("title")
    args = parser.parse_args()
    
    create_pdf(args.input, args.output, args.title)
