import zipfile
import re
import os

epub_path = 'exhaustiveconcor1890stro.epub'
hebrew_range = (1619, 1744)
greek_range = (1745, 1832)

def extract_pages(z, start, end, output_filename, title):
    content_accum = []
    # Header
    content_accum.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
body {{ font-family: serif; line-height: 1.5; padding: 20px; }}
.page-break {{ page-break-before: always; border-top: 1px solid #ccc; margin-top: 20px; padding-top: 20px; }}
</style>
</head>
<body>
<h1>{title}</h1>
''')
    
    for i in range(start, end + 1):
        page_path = f'EPUB/page_{i}.html'
        try:
            page_content = z.read(page_path).decode('utf-8', errors='ignore')
            # Extract body content roughly
            # Regex to find <body ...> ... </body>
            # Or just content between <body> and </body>
            m = re.search(r'<body[^>]*>(.*?)</body>', page_content, re.DOTALL | re.IGNORECASE)
            if m:
                body_inner = m.group(1)
                content_accum.append(f'<div class="page-container" id="page_{i}">')
                content_accum.append(body_inner)
                content_accum.append('</div>')
            else:
                print(f"Warning: No body found in {page_path}")
        except KeyError:
            print(f"Warning: {page_path} not found in archive")
        except Exception as e:
            print(f"Error reading {page_path}: {e}")

    content_accum.append('</body></html>')
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_accum))
    print(f"Created {output_filename}")

try:
    with zipfile.ZipFile(epub_path) as z:
        extract_pages(z, hebrew_range[0], hebrew_range[1], 'hebrew_aramaic_dictionary.html', 'Hebrew and Aramaic Dictionary')
        extract_pages(z, greek_range[0], greek_range[1], 'greek_dictionary.html', 'Greek Dictionary')
except Exception as e:
    print(f"Failed to process epub: {e}")
