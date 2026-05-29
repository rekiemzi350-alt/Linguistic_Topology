from fpdf import FPDF
import sys
import re

# Font paths
ROBOTO_PATH = '/system/fonts/Roboto-Regular.ttf'
NOTO_HEBREW_PATH = '/system/fonts/NotoSansHebrew-Regular.ttf'
# Check if Aramaic exists, if not use Hebrew
NOTO_ARAMAIC_PATH = '/system/fonts/NotoSansImperialAramaic-Regular.ttf'

def create_pdf(html_path, output_path, title):
    print(f"Processing {html_path} -> {output_path}...")
    
    pdf = FPDF()
    pdf.add_page()
    
    # Add fonts
    pdf.add_font("Roboto", fname=ROBOTO_PATH)
    pdf.add_font("NotoHebrew", fname=NOTO_HEBREW_PATH)
    try:
        pdf.add_font("NotoAramaic", fname=NOTO_ARAMAIC_PATH)
        has_aramaic = True
    except:
        has_aramaic = False
        
    pdf.set_font("Roboto", size=12)
    
    # Set fallbacks
    fallbacks = ["NotoHebrew"]
    if has_aramaic:
        fallbacks.append("NotoAramaic")
    
    try:
        pdf.set_fallback_fonts(fallbacks)
    except Exception as e:
        print(f"Warning: set_fallback_fonts failed: {e}")

    # Read HTML content
    # Since write_html is memory intensive and might fail on huge files, 
    # and the HTML is simple (just text mostly), we might need to chunk it.
    # However, for simplicity, let's try reading it.
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        # Basic cleanup: remove html/body tags, just keep the content
        # write_html expects HTML. 
        # For the huge file, we might want to split by <br/> or <div> to avoid one massive block
        
        # Insert title
        pdf.set_font("Roboto", size=24)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(10)
        pdf.set_font("Roboto", size=10)
        
        # Split text into chunks to avoid passing one massive string to write_html?
        # fpdf2 write_html handles parsing.
        # But let's check length.
        print(f"Text length: {len(text)} chars")
        
        # If text is > 1MB, maybe chunk it?
        # The trimmed content is likely > 5MB.
        # chunking by <div> or <p> is safer.
        
        # Simple chunker
        chunks = re.split(r'(<div.*?</div>|<p.*?</p>|<br\s*/>)', text, flags=re.DOTALL)
        
        # Only process non-empty chunks
        count = 0
        buffer = ""
        for chunk in chunks:
            if not chunk.strip():
                continue
            
            buffer += chunk
            if len(buffer) > 50000: # 50k chars batch
                try:
                    pdf.write_html(buffer)
                except Exception as e:
                    print(f"Error writing chunk: {e}")
                    # Fallback: write as text stripping tags
                    clean_text = re.sub('<[^<]+?>', '', buffer)
                    pdf.multi_cell(0, 5, clean_text)
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
