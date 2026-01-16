import zipfile
import os
import re
from lxml import etree

def extract_epub_text(epub_path, output_path):
    with zipfile.ZipFile(epub_path, 'r') as epub:
        # Get all HTML/XHTML files
        items = [n for n in epub.namelist() if n.endswith(('.html', '.xhtml'))]
        # Usually they are ordered in content.opf, but we'll just sort them for a rough order
        items.sort()
        
        full_text = []
        for item in items:
            with epub.open(item) as f:
                content = f.read()
                parser = etree.HTMLParser()
                tree = etree.fromstring(content, parser)
                # Extract text from paragraphs
                paragraphs = tree.xpath('//p')
                for p in paragraphs:
                    text = "".join(p.itertext()).strip()
                    if text:
                        full_text.append(text)
                # Also capture headers
                headers = tree.xpath('//h1|//h2|//h3')
                for h in headers:
                    text = "".join(h.itertext()).strip()
                    if text:
                        full_text.append(text)
        
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write("\n\n".join(full_text))

if __name__ == "__main__":
    test_dir = "test_documents"
    for filename in os.listdir(test_dir):
        if filename.endswith(".epub"):
            epub_path = os.path.join(test_dir, filename)
            text_path = os.path.join(test_dir, filename.replace(".epub", ".txt"))
            print(f"Extracting {filename}...")
            extract_epub_text(epub_path, text_path)
