import os

# Dictionary of missing numbers for key languages
# Format: "filename_part": {num: "word"}
updates = {
    "albanian": {
        11: "njëmbëdhjetë", 12: "dymbëdhjetë", 13: "trembëdhjetë", 14: "katërmbëdhjetë",
        15: "pesëmbëdhjetë", 16: "gjashtëmbëdhjetë", 17: "shtatëmbëdhjetë", 18: "tetëmbëdhjetë", 19: "nëntëmbëdhjetë"
    },
    "anglo_saxon": {
        11: "endleofan", 12: "twelf", 13: "threotine", 14: "feowertine",
        15: "fiftine", 16: "sixtine", 17: "seofontine", 18: "eahtatine", 19: "nigontine"
    },
    "armenian_western": {
        11: "տասնմէկ", 12: "տասներկու", 13: "տասներեք", 14: "տասնչորս",
        15: "տասնհինգ", 16: "տասնվեց", 17: "տասնեօթը", 18: "տասնութ", 19: "տասնինը"
    },
    "azerbaijani": {
        11: "on bir", 12: "on iki", 13: "on üç", 14: "on dörd",
        15: "on beş", 16: "on altı", 17: "on yeddi", 18: "on səkkiz", 19: "on doqquz"
    },
    "belorussian": {
        11: "адзiнаццаць", 12: "дванаццаць", 13: "трынаццаць", 14: "чатырнаццаць",
        15: "пятнаццаць", 16: "шаснаццаць", 17: "сiмнаццаць", 18: "васемнаццаць", 19: "дзевятнаццаць"
    },
    "bengali": {
        11: "এগারো", 12: "বারো", 13: "তেরো", 14: "চৌদ্দ",
        15: "পনেরো", 16: "ষোল", 17: "সতেরো", 18: "আঠারো", 19: "ঊনিশ"
    },
    "bulgarian": {
        11: "единадесет", 12: "дванадесет", 13: "тринадесет", 14: "четиринадесет",
        15: "петнадесет", 16: "шестнадесет", 17: "седемнадесет", 18: "осемнадесет", 19: "деветнадесет"
    }
}

def update_file(filepath, data):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Check if 11 is already there
        for line in lines:
            if line.strip().startswith("11:"):
                return False
                
        # Find insertion point (after 10:)
        insert_idx = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("10:"):
                insert_idx = i + 1
                break
        
        if insert_idx == -1:
            # Append if no 10 found (unlikely but safe)
            insert_idx = len(lines)
            
        new_lines = []
        for n in range(11, 20):
            if n in data:
                new_lines.append(f"{n}: {data[n]}\n")
                
        lines[insert_idx:insert_idx] = new_lines
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    base_dir = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"
    count = 0
    
    for filename in os.listdir(base_dir):
        if not filename.endswith(".lang") or "TECH" in filename:
            continue
            
        # Match filename to updates
        # Simple string matching
        matched_key = None
        for key in updates:
            if filename == f"{key}.lang":
                matched_key = key
                break
        
        if matched_key:
            if update_file(os.path.join(base_dir, filename), updates[matched_key]):
                print(f"Updated {filename}")
                count += 1
                
    print(f"Batch update complete. Fixed {count} files.")

if __name__ == "__main__":
    main()
