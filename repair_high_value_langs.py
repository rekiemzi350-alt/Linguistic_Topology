import os

LANG_DIR = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"

# High-Precision Data for Ancient/Classical Languages
data_fixes = {
    "ancient_greek": {
        16: "ἑκκαίδεκα", 17: "ἑπτακαίδεκα", 18: "ὀκτωκαίδεκα", 19: "ἐννεακαίδεκα",
        100: "ἑκατόν"
    },
    "biblical_hebrew": {
        11: "אחד עשר", 12: "שנים עשר", 13: "שלשה עשר", 14: "ארבעה עשר", 
        15: "חמשה עשר", 16: "ששה עשר", 17: "שבעה עשר", 18: "שמונה עשר", 19: "תשעה עשר",
        100: "מאה"
    },
    "sanskrit": {
        11: "एकादश", 12: "द्वादश", 13: "त्रयोदश", 14: "चतुर्दश", 
        15: "पञ्चदश", 16: "षोडश", 17: "सप्तदश", 18: "अष्टादश", 19: "नवदश",
        100: "शतम्"
    },
    "old_norse": {
        11: "ellifu", 12: "tólf", 13: "þrettán", 14: "fjórtán", 
        15: "fimmtán", 16: "sextán", 17: "sjaután", 18: "atján", 19: "nítján",
        100: "hundrað"
    },
    "latin": {
        11: "undecim", 12: "duodecim", 13: "tredecim", 14: "quattuordecim", 
        15: "quindecim", 16: "sedecim", 17: "septendecim", 18: "duodeviginti", 19: "undeviginti",
        100: "centum"
    }
}

def apply_fix(name, fixes):
    path = os.path.join(LANG_DIR, name + ".lang")
    if not os.path.exists(path): return
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Check what's already there to avoid duplicates
    existing_keys = []
    for line in lines:
        parts = line.split(":", 1)
        if len(parts) == 2 and parts[0].strip().isdigit():
            existing_keys.append(int(parts[0].strip()))
            
    new_lines = []
    for k, v in sorted(fixes.items()):
        if k not in existing_keys:
            new_lines.append(f"{k}: {v}\n")
            
    if new_lines:
        # Append to the end or after the last number
        lines.extend(new_lines)
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True
    return False

for name, fixes in data_fixes.items():
    if apply_fix(name, fixes):
        print(f"Fixed {name}")
