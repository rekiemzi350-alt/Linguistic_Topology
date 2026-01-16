import os
import shutil
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

TARGET_DIR = "/storage/emulated/0/Books/AI_Conversations/"

def apply_standard(file_path):
    print(f"Processing: {os.path.basename(file_path)}")
    
    # Create backup
    backup_path = file_path + ".bak"
    shutil.copy2(file_path, backup_path)
    
    try:
        doc = Document(file_path)
        
        # 1. Set Margins (1 inch)
        for section in doc.sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
            
        # 2. Iterate Paragraphs
        for i, paragraph in enumerate(doc.paragraphs):
            # Clear existing formatting where possible (naive approach)
            # We rely on setting specific attributes to override
            
            # Logic for Header vs Body
            if i == 0:
                # Title
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                font_size = Pt(18)
            elif i == 1 or i == 2:
                # Date / Topic
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                font_size = Pt(16)
            else:
                # Body
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                font_size = Pt(12)
            
            # Apply Paragraph Spacing (Single)
            paragraph_format = paragraph.paragraph_format
            paragraph_format.line_spacing = 1.0
            paragraph_format.space_before = Pt(0)
            paragraph_format.space_after = Pt(0)

            # Apply Font and Size to all Runs
            # Note: This overrides manual formatting within the paragraph
            for run in paragraph.runs:
                run.font.name = 'Georgia'
                run.font.size = font_size
                
        doc.save(file_path)
        print(f"  -> Updated: {os.path.basename(file_path)}")

    except Exception as e:
        print(f"  -> Failed: {e}")
        # Restore backup on failure
        shutil.copy2(backup_path, file_path)

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"Directory not found: {TARGET_DIR}")
        return

    files = [f for f in os.listdir(TARGET_DIR) if f.lower().endswith(".docx") and not f.lower().endswith(".bak")]
    
    print(f"Found {len(files)} .docx files in {TARGET_DIR}")
    
    for f in files:
        apply_standard(os.path.join(TARGET_DIR, f))

if __name__ == "__main__":
    main()
