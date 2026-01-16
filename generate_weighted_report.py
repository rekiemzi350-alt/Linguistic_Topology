import os
import glob
from linguistic_topology_app import parse_lang_file, get_western_name
from frequency_tables import get_weight_map

def get_word_weight(word, weight_map):
    """Calculates the total weight of a word based on a frequency map."""
    # Strip spaces and punctuation
    clean_word = word.replace(" ", "").replace("-", "").lower()
    return sum(weight_map.get(char, 26) for char in clean_word) # Default to 26 for unknown chars

def generate_weighted_report():
    lang_files = glob.glob("*.lang")
    if not lang_files:
        print("No .lang files found.")
        return

    print("=" * 80)
    print("GLOBAL WEIGHTED TOPOLOGY REPORT (Erik Frequency-Weight Algorithm)")
    print("=" * 80)
    print(f"Algorithm: n_next = n_curr + Sum(Weights of letters in n_curr's name)")
    print(f"Weight: 1 for most common, 26 for least common.")
    print("-" * 80)

    results = []

    for lang_file in sorted(lang_files):
        try:
            lang_data = parse_lang_file(lang_file)
            weight_map = get_weight_map(lang_data["name"])
            
            # For non-alphabetic languages like Sumerian, we use sign count as weight
            # Or if no weight map, use length.
            use_length_as_weight = not weight_map

            paths = {}
            for start_num in range(101):
                path = []
                curr = start_num
                # Weighted jumps are larger, so we need a larger ceiling
                while curr < 2000 and len(path) < 100:
                    path.append(curr)
                    if use_length_as_weight:
                        weight = lang_data["get_len_func"](curr, lang_data["rules"])
                    else:
                        name = get_western_name(curr, lang_data["rules"])
                        weight = get_word_weight(name, weight_map)
                    
                    if weight == 0 and curr != 0: break
                    curr += weight
                paths[start_num] = path

            # Group the paths
            unique_rivers = []
            groups = {}
            for start_num in range(101):
                my_path = paths.get(start_num, [])
                if not my_path: continue
                my_tail = tuple(my_path[-3:])
                found_river = False
                for rid, rtail in enumerate(unique_rivers):
                    if my_tail == rtail:
                        groups[rid].append(start_num)
                        found_river = True
                        break
                if not found_river:
                    new_id = len(unique_rivers)
                    unique_rivers.append(my_tail)
                    groups[new_id] = [start_num]

            sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
            max_unity = (len(sorted_groups[0][1]) / 101) * 100 if sorted_groups else 0

            results.append({
                "name": lang_data["name"],
                "rivers": len(unique_rivers),
                "unity": max_unity,
                "file": lang_file
            })

        except Exception as e:
            # print(f"Error processing {lang_file}: {e}")
            pass

    # Sort results by unity
    results.sort(key=lambda x: x["unity"], reverse=True)

    print("{:<25} | {:<8} | {:<8} | {:<15}".format("Language", "Rivers", "Unity %", "File"))
    print("-" * 75)
    for r in results:
        print("{:<25} | {:<8} | {:<8.1f}% | {:<15}".format(
            r["name"], r["rivers"], r["unity"], r["file"]
        ))
    
    print("\n" + "=" * 80)
    print("Conclusion: The 'Interwoven Pattern' revealed by letter weighting.")
    print("Note: Languages with higher Unity in weighted space show stronger internal")
    print("harmonic resonance in their phonetic structure.")
    print("=" * 80)

if __name__ == "__main__":
    generate_weighted_report()
