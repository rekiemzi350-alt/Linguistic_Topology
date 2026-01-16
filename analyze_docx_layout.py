import zipfile
import xml.etree.ElementTree as ET
import sys
import os

file_path = "12-11-2025 Conversation with Gemini on AI and Computer Games.docx.bak"

def analyze_docx(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    try:
        with zipfile.ZipFile(path, 'r') as docx:
            # Analyze Styles (for defaults)
            styles_xml = docx.read('word/styles.xml')
            styles_root = ET.fromstring(styles_xml)
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            print("--- Styles Analysis ---")
            
            # Check DocDefaults
            docDefaults = styles_root.find('.//w:docDefaults', namespaces)
            if docDefaults:
                rPrDefault = docDefaults.find('.//w:rPrDefault/w:rPr', namespaces)
                if rPrDefault:
                     fonts = rPrDefault.find('w:rFonts', namespaces)
                     if fonts is not None:
                        print(f"Default Font (Theme): {fonts.get(f'{{{namespaces['w']}}}asciiTheme')}")
                        print(f"Default Font (Ascii): {fonts.get(f'{{{namespaces['w']}}}ascii')}")
                     sz = rPrDefault.find('w:sz', namespaces)
                     if sz is not None:
                        val = sz.get(f'{{{namespaces["w"]}}}val')
                        if val:
                            print(f"Default Size: {int(val)/2} pt")

            # Look for 'Normal' style
            for style in styles_root.findall('.//w:style', namespaces):
                style_id = style.get(f'{{{namespaces['w']}}}styleId')
                if style_id == 'Normal':
                    rPr = style.find('w:rPr', namespaces)
                    if rPr is not None:
                        fonts = rPr.find('w:rFonts', namespaces)
                        if fonts is not None:
                            print(f"Normal Style Font: {fonts.get(f'{{{namespaces['w']}}}ascii')}")
                        sz = rPr.find('w:sz', namespaces)
                        if sz is not None:
                             val = sz.get(f'{{{namespaces["w"]}}}val')
                             if val:
                                print(f"Normal Style Size: {int(val)/2} pt")
                    pPr = style.find('w:pPr', namespaces)
                    if pPr is not None:
                        spacing = pPr.find('w:spacing', namespaces)
                        if spacing is not None:
                             line = spacing.get(f'{{{namespaces['w']}}}line')
                             print(f"Normal Style Line Spacing: {line}")


            # Analyze Document (for sections and direct formatting)
            doc_xml = docx.read('word/document.xml')
            doc_root = ET.fromstring(doc_xml)
            
            print("\n--- Document Layout Analysis ---")
            
            # Margins from Section Properties
            # sectPr can be a child of body, or inside p/pPr
            sectPrs = doc_root.findall('.//w:sectPr', namespaces)
            if not sectPrs:
                # Sometimes sectPr is only at the end of body
                sectPrs = doc_root.findall('.//w:body/w:sectPr', namespaces)

            for i, sectPr in enumerate(sectPrs):
                pgMar = sectPr.find('w:pgMar', namespaces)
                if pgMar is not None:
                    top = int(pgMar.get(f'{{{namespaces['w']}}}top', 0)) / 1440
                    bottom = int(pgMar.get(f'{{{namespaces['w']}}}bottom', 0)) / 1440
                    left = int(pgMar.get(f'{{{namespaces['w']}}}left', 0)) / 1440
                    right = int(pgMar.get(f'{{{namespaces['w']}}}right', 0)) / 1440
                    print(f"Section {i+1} Margins (inches): Top={top:.2f}, Bottom={bottom:.2f}, Left={left:.2f}, Right={right:.2f}")
            
            # Paragraph Analysis (sampling)
            paragraphs = doc_root.findall('.//w:body/w:p', namespaces)
            print(f"\nTotal Paragraphs: {len(paragraphs)}")
            
            # Check a few paragraphs for spacing and fonts
            for i, p in enumerate(paragraphs[:10]): 
                print(f"\nParagraph {i+1}:")
                pPr = p.find('w:pPr', namespaces)
                if pPr is not None:
                    spacing = pPr.find('w:spacing', namespaces)
                    if spacing is not None:
                        line = spacing.get(f'{{{namespaces['w']}}}line')
                        lineRule = spacing.get(f'{{{namespaces['w']}}}lineRule')
                        before = spacing.get(f'{{{namespaces['w']}}}before')
                        after = spacing.get(f'{{{namespaces['w']}}}after')
                        print(f"  Spacing: Line={line}, Rule={lineRule}, Before={before}, After={after}")
                    
                    ind = pPr.find('w:ind', namespaces)
                    if ind is not None:
                         left_ind = ind.get(f'{{{namespaces['w']}}}left')
                         first_line = ind.get(f'{{{namespaces['w']}}}firstLine')
                         print(f"  Indentation: Left={left_ind}, FirstLine={first_line}")
                    
                    jc = pPr.find('w:jc', namespaces)
                    if jc is not None:
                        print(f"  Alignment: {jc.get(f'{{{namespaces['w']}}}val')}")

                # Check runs for direct font/size
                runs = p.findall('w:r', namespaces)
                for r in runs:
                    rPr = r.find('w:rPr', namespaces)
                    if rPr is not None:
                        rFonts = rPr.find('w:rFonts', namespaces)
                        if rFonts is not None:
                            print(f"  Run Font: {rFonts.get(f'{{{namespaces['w']}}}ascii')}")
                        sz = rPr.find('w:sz', namespaces)
                        if sz is not None:
                             val = sz.get(f'{{{namespaces["w"]}}}val')
                             if val:
                                print(f"  Run Size: {int(val)/2} pt")
                    t = r.find('w:t', namespaces)
                    if t is not None and t.text:
                         print(f"  Text snippet: {t.text[:20]}...")
                         break # Just show the first run's text

    except Exception as e:
        print(f"Error analyzing docx: {e}")

analyze_docx(file_path)
