import os
import glob
from linguistic_topology_app import parse_lang_file, analyze_language

def generate_report():
    lang_files = glob.glob("*.lang")
    if not lang_files:
        print("No .lang files found in the current directory.")
        return

    print("=" * 60)
    print("GLOBAL LINGUISTIC TOPOLOGY REPORT")
    print("=" * 60)
    print(f"Found {len(lang_files)} language definitions.")

    # We'll use a slightly modified version of analyze_language to return data
    results = []

    for lang_file in sorted(lang_files):
        try:
            lang_data = parse_lang_file(lang_file)
            # Run simulation
            paths = {}
            for start_num in range(101):
                path = []
                curr = start_num
                while curr < 800 and len(path) < 100:
                    path.append(curr)
                    length = lang_data["get_len_func"](curr, lang_data["rules"])
                    if length == 0: break
                    curr += length
                paths[start_num] = path

            unique_rivers = []
            groups = {}
            for start_num in range(101):
                my_path = paths.get(start_num, [])
                if len(my_path) < 5: continue
                my_tail = tuple(my_path[-5:])
                found_river = False
                for river_id, river_tail in enumerate(unique_rivers):
                    if my_tail == river_tail:
                        groups[river_id].append(start_num)
                        found_river = True
                        break
                if not found_river:
                    new_id = len(unique_rivers)
                    unique_rivers.append(my_tail)
                    groups[new_id] = [start_num]

            sorted_groups = sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
            
            # Dominant River %
            max_unity = 0
            if sorted_groups:
                max_unity = len(sorted_groups[0][1])

            results.append({
                "name": lang_data["name"],
                "rivers": len(unique_rivers),
                "unity": max_unity,
                "file": lang_file
            })

        except Exception as e:
            print(f"Error processing {lang_file}: {e}")

    # Display Summary Table
    print("\n{:<25} | {:<8} | {:<8} | {:<15}".format("Language", "Rivers", "Unity %", "File"))
    print("-" * 65)
    
    # Sort results by unity descending
    results.sort(key=lambda x: x["unity"], reverse=True)

    for r in results:
        print("{:<25} | {:<8} | {:<8}% | {:<15}".format(
            r["name"], r["rivers"], r["unity"], r["file"]
        ))
    
    print("\n" + "=" * 60)
    print("Interpretation:")
    print(" - High Unity (90%+) indicates an 'Integrative' mindset (Modern).")
    print(" - Low Unity (<50%) indicates a 'Fractured' or 'Categorical' mindset (Ancient).")
    print("=" * 60)

if __name__ == "__main__":
    generate_report()
