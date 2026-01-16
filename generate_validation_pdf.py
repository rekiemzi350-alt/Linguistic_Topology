import csv
import os
import shutil
from fpdf import FPDF

CSV_FILE = "test_results/language_validation_report.csv"
PDF_FILE = "test_results/validation_report.pdf"
DEST_DIR = "/sdcard/Download/"
TITLE = "Linguistic Topology App - Comprehensive Validation Report"

# Font paths (Termux standard)
ROBOTO_PATH = '/system/fonts/Roboto-Regular.ttf'

class ReportPDF(FPDF):
    def header(self):
        self.set_font("Roboto", size=16)
        self.cell(0, 10, TITLE, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Roboto", size=8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_report():
    print(f"Reading {CSV_FILE}...")
    
    data = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    if not data:
        print("No data found.")
        return

    pdf = ReportPDF()
    pdf.add_font("Roboto", fname=ROBOTO_PATH)
    pdf.set_font("Roboto", size=10)
    pdf.add_page()

    # Column Widths
    # Language, Load, Teen, G42, G123, Scr, Topo, Status, Notes
    # We will summarize: Lang, Status, Notes
    
    header = data[0]
    rows = data[1:]
    
    # Stats
    total = len(rows)
    passed = sum(1 for r in rows if r[7] == "PASS")
    failed = total - passed
    
    pdf.set_font("Roboto", size=12)
    pdf.cell(0, 10, f"Summary: Total Languages: {total} | PASSED: {passed} | FAILED: {failed}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font("Roboto", size=8)
    
    # Table Header
    col_widths = [50, 20, 120] # Language, Status, Notes
    headers = ["Language", "Status", "Notes"]
    
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, border=1, align='C')
    pdf.ln()
    
    # Table Rows
    for row in rows:
        lang_name = row[0]
        status = row[7]
        notes = row[8]
        
        # Color coding
        if status == "PASS":
            pdf.set_text_color(0, 128, 0)
        else:
            pdf.set_text_color(255, 0, 0)
            
        # Cell method doesn't support text wrap well, use MultiCell for Notes if needed?
        # Simpler: Just truncate notes if too long or use multi_cell layout.
        # For simplicity in FPDF1/2 mixed envs, let's keep it simple.
        
        # Save X, Y
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        
        # Language
        pdf.cell(col_widths[0], 6, lang_name, border=1)
        
        # Status
        pdf.cell(col_widths[1], 6, status, border=1, align='C')
        
        # Notes (Reset color for notes? No keep it)
        # Check if notes fits?
        # Clean notes
        notes = notes.replace("Topology Stalled at step", "Stall@")
        notes = notes.replace("Missing Teens:", "NoTeens:")
        
        pdf.cell(col_widths[2], 6, notes[:65], border=1) # Truncate to fit line
        
        pdf.ln()
        pdf.set_text_color(0, 0, 0) # Reset
        
    print(f"Saving PDF to {PDF_FILE}...")
    pdf.output(PDF_FILE)
    
    # Move to Download
    final_dest = os.path.join(DEST_DIR, "LTA_Validation_Report.pdf")
    print(f"Moving to {final_dest}...")
    try:
        shutil.copy(PDF_FILE, final_dest)
        print("Success.")
    except Exception as e:
        print(f"Failed to copy to Download: {e}")

if __name__ == "__main__":
    generate_report()
