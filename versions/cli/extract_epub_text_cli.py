import zipfile
import os
import sys
from lxml import etree

def extract_epub_text(epub_path):
    output_path = epub_path.replace(".epub", ".txt")
    with zipfile.ZipFile(epub_path, 'r') as epub:
        items = [n for n in epub.namelist() if n.endswith(('.html', '.xhtml'))]
        items.sort()
        
        full_text = []
        for item in items:
            with epub.open(item) as f:
                content = f.read()
                parser = etree.HTMLParser()
                tree = etree.fromstring(content, parser)
                paragraphs = tree.xpath('//p')
                for p in paragraphs:
                    text = "".join(p.itertext()).strip()
                    if text:
                        full_text.append(text)
        
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write("\n\n".join(full_text))
    print(f"Extracted text to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_epub_text(sys.argv[1])
