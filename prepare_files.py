import zipfile
import re
import os

epub_path = 'exhaustiveconcor1890stro.epub'
trimmed_epub_path = 'exhaustiveconcor1890stro_trimmed.epub'
trimmed_html_path = 'trimmed_content.html'

# Pages to keep for the trimmed version
keep_pages_range = range(1, 1619) # 1 to 1618

def read_file_from_zip(z, name):
    try:
        return z.read(name).decode('utf-8')
    except:
        return ""

def create_trimmed_epub():
    print("Creating trimmed EPUB...")
    with zipfile.ZipFile(epub_path, 'r') as zin:
        with zipfile.ZipFile(trimmed_epub_path, 'w') as zout:
            # Copy all files except the ones we want to remove from the spine/manifest effectively
            # Actually, simpler: copy everything, but modify content.opf
            
            # Find content.opf
            opf_name = 'EPUB/content.opf'
            if opf_name not in zin.namelist():
                # Try to find it via META-INF/container.xml usually, but hardcoding based on previous ls is faster
                # If not found, search
                for n in zin.namelist():
                    if n.endswith('.opf'):
                        opf_name = n
                        break
            
            print(f"Found OPF: {opf_name}")
            
            opf_content = read_file_from_zip(zin, opf_name)
            
            # Regex to find spine items
            # <itemref idref="page_1619" /> ...
            # We want to remove references to page_1619 to page_1832
            
            new_opf_content = opf_content
            
            # Remove itemrefs from spine
            # We assume IDs are like 'page_N' or similar that map to the filenames
            # Looking at previous ls: EPUB/page_1.html.
            # Usually manifest has: <item id="page_1" href="page_1.html" ... />
            # Spine has: <itemref idref="page_1" />
            
            # Let's just iterate over the range and remove the itemrefs
            for i in range(1619, 1833):
                # Try to find the idref. It might not be exactly 'page_N'.
                # But based on filenames 'page_N.html', it is likely 'page_N'.
                # We can also check the manifest for href="page_N.html" to get the ID.
                
                # Simple approach: remove by filename in manifest? No, must remove from spine.
                # Let's find the ID for the filename.
                fname = f"page_{i}.html"
                # Regex to find id for this href
                # <item ... href="page_1619.html" ... id="ID" ... >
                match = re.search(r'<item[^>]*href=["\'].*?'+fname+r'["\'][^>]*id=["\'](.*?)["\']', opf_content)
                if match:
                    id_val = match.group(1)
                    # Remove from spine: <itemref idref="ID" ... />
                    # Handle self-closing and non-self-closing
                    new_opf_content = re.sub(r'<itemref[^>]*idref=["\']'+id_val+r'["\'][^>]*/>', '', new_opf_content)
                    new_opf_content = re.sub(r'<itemref[^>]*idref=["\']'+id_val+r'["\'][^>]*>.*?</itemref>', '', new_opf_content)
            
            for item in zin.infolist():
                if item.filename == opf_name:
                    zout.writestr(opf_name, new_opf_content)
                elif 'page_' in item.filename and item.filename.endswith('.html'):
                    # Check if it is in the excluded range
                    m = re.search(r'page_(\d+)', item.filename)
                    if m:
                        pg_num = int(m.group(1))
                        if pg_num < 1619:
                            zout.writestr(item, zin.read(item.filename))
                        # Else skip
                    else:
                        zout.writestr(item, zin.read(item.filename))
                else:
                    zout.writestr(item, zin.read(item.filename))

    print(f"Created {trimmed_epub_path}")

def extract_trimmed_content():
    print("Extracting trimmed content for PDF...")
    content_accum = []
    content_accum.append('<html><body>')
    
    with zipfile.ZipFile(epub_path, 'r') as z:
        for i in keep_pages_range:
            page_path = f'EPUB/page_{i}.html'
            try:
                page_content = z.read(page_path).decode('utf-8', errors='ignore')
                # Extract body
                m = re.search(r'<body[^>]*>(.*?)</body>', page_content, re.DOTALL | re.IGNORECASE)
                if m:
                    content_accum.append(m.group(1))
                    content_accum.append('<br/>') # Page break marker essentially
            except KeyError:
                pass
            except Exception as e:
                print(f"Error reading {page_path}: {e}")
                
    content_accum.append('</body></html>')
    
    with open(trimmed_html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_accum))
    print(f"Created {trimmed_html_path}")

create_trimmed_epub()
extract_trimmed_content()
