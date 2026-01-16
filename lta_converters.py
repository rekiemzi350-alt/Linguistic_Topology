import os
import subprocess
from PIL import Image
import docx
import ebooklib
from ebooklib import epub
import bs4

def docx_to_text(path):
    """Extracts text from a .docx file."""
    try:
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"[ERROR] Failed to process DOCX file: {e}"

def epub_to_text(path):
    """Extracts text from an .epub file."""
    try:
        book = epub.read_epub(path)
        text_parts = []
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = bs4.BeautifulSoup(item.get_body_content(), 'html.parser')
            # Get all text, separating paragraphs with newlines
            text = soup.get_text(separator='\n')
            text_parts.append(text)
        return "\n".join(text_parts)
    except Exception as e:
        return f"[ERROR] Failed to process EPUB file: {e}"

def pdf_to_text(path, output_txt_path):
    """Converts a .pdf file to a .txt file using pdftotext."""
    try:
        # Use the pdftotext command-line tool
        subprocess.run(['pdftotext', path, output_txt_path], check=True)
        return f"[SUCCESS] PDF converted to {output_txt_path}"
    except FileNotFoundError:
        return "[ERROR] 'pdftotext' command not found. Please install poppler-utils."
    except subprocess.CalledProcessError as e:
        return f"[ERROR] pdftotext failed: {e}"
    except Exception as e:
        return f"[ERROR] An unexpected error occurred: {e}"

def convert_document_to_text(input_path):
    """
    Main function to convert a document (DOCX, EPUB, PDF) to a text file.
    The output file will have the same name with a .txt extension.
    """
    base, ext = os.path.splitext(input_path)
    output_path = base + ".txt"
    
    print(f"\nConverting {os.path.basename(input_path)} to {os.path.basename(output_path)}...")
    
    ext = ext.lower()
    result_message = ""
    
    if ext == '.docx':
        text = docx_to_text(input_path)
        if text.startswith("[ERROR]"):
            result_message = text
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            result_message = f"[SUCCESS] DOCX converted to {output_path}"
            
    elif ext == '.epub':
        text = epub_to_text(input_path)
        if text.startswith("[ERROR]"):
            result_message = text
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            result_message = f"[SUCCESS] EPUB converted to {output_path}"

    elif ext == '.pdf':
        result_message = pdf_to_text(input_path, output_path)
        
    else:
        result_message = f"[ERROR] Unsupported document type: {ext}"
        
    print(result_message)

def convert_image_format(input_path, output_format):
    """
    Converts an image to a different format.
    e.g., convert_image('image.jpg', 'png') -> creates 'image.png'
    """
    base, ext = os.path.splitext(input_path)
    output_path = base + "." + output_format.lower()
    
    print(f"\nConverting {os.path.basename(input_path)} to {os.path.basename(output_path)}...")
    
    try:
        with Image.open(input_path) as img:
            # Handle formats that might lose transparency (like JPEG)
            if output_format.lower() == 'jpg' or output_format.lower() == 'jpeg':
                if img.mode in ('RGBA', 'LA'):
                    # Create a white background image
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, (0, 0), img.convert('RGBA'))
                    background.save(output_path, 'JPEG')
                else:
                    img.convert('RGB').save(output_path, 'JPEG')
            else:
                img.save(output_path, output_format.upper())
        print(f"[SUCCESS] Image saved as {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to convert image: {e}")
