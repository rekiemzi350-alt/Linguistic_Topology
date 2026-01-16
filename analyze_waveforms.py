import os
import sys
import glob

# Ensure we can import the app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from linguistic_topology_app import parse_lang_file
except ImportError:
    print("Error: Could not import linguistic_topology_app.py")
    sys.exit(1)

def get_main_trunk(lang_data, limit_val=5000, max_steps=500):
    """
    Finds the 'Main Trunk' of the language by simulating paths from 1-100
    and picking the path that collects the most merges.
    Returns the path as a list of integers.
    """
    paths = {}
    
    # Simulate all tributaries from 1-100
    for start_num in range(1, 101):
        path = []
        curr = start_num
        step = 0
        while curr < limit_val and step < max_steps:
            path.append(curr)
            try:
                length = lang_data["get_len_func"](curr, lang_data["rules"])
                if length == 0: break
                curr += length
                step += 1
            except Exception:
                break
        paths[start_num] = path

    # Find the dominant tail (Trunk)
    # We look at the last number in each path.
    tails = {}
    for start_num, path in paths.items():
        if not path: continue
        # use the last 5 numbers as a signature
        signature = tuple(path[-5:]) if len(path) >= 5 else tuple(path)
        if signature not in tails:
            tails[signature] = []
        tails[signature].append(start_num)

    # Sort by number of tributaries converging to this tail
    sorted_tails = sorted(tails.items(), key=lambda item: len(item[1]), reverse=True)
    
    if not sorted_tails:
        return []

    # Pick the representative start number from the largest group
    dominant_signature, members = sorted_tails[0]
    best_start = members[0]
    
    return paths[best_start]

def to_waveform(path):
    """Converts a path [n0, n1, n2...] into peaks/valleys [n0, -n1, n2, -n3...]"""
    wave = []
    for i, val in enumerate(path):
        if i % 2 == 0:
            wave.append(val)  # Peak
        else:
            wave.append(-val) # Valley
    return wave

def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    languages_dir = os.path.join(repo_dir, "languages")
    output_dir = os.path.join(repo_dir, "baseline_results")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    lang_files = glob.glob(os.path.join(languages_dir, "*.lang"))
    lang_files = [f for f in lang_files if "TECH.lang" not in f]
    
    print(f"Analyzing waveforms for {len(lang_files)} languages...")

    # Store results: name -> trunk_path
    trunks = {}
    
    for lang_file in lang_files:
        try:
            lang_data = parse_lang_file(lang_file)
            name = lang_data['name']
            
            trunk = get_main_trunk(lang_data)
            if trunk:
                trunks[name] = trunk
            
            # Save individual waveform data
            base_name = os.path.basename(lang_file).replace(".lang", "")
            wave_file = os.path.join(output_dir, f"{base_name}_waveform.csv")
            
            wave = to_waveform(trunk)
            with open(wave_file, "w", encoding="utf-8") as f:
                f.write("Step,Value,WaveformValue\n")
                for i, (val, wave_val) in enumerate(zip(trunk, wave)):
                    f.write(f"{i},{val},{wave_val}\n")
                    
        except Exception as e:
            print(f"Skipping {os.path.basename(lang_file)} due to error: {e}")

    # Cross-Language Synchronization Check
    print("\nChecking for synchronization...")
    
    # We compare the last 10 steps of the trunks
    # Key: Tail tuple, Value: List of language names
    synced_groups = {}
    
    for name, trunk in trunks.items():
        if len(trunk) < 10:
            tail = tuple(trunk)
        else:
            tail = tuple(trunk[-10:])
        
        if tail not in synced_groups:
            synced_groups[tail] = []
        synced_groups[tail].append(name)
        
    report_file = os.path.join(output_dir, "waveform_sync_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("=== WAVEFORM SYNCHRONIZATION REPORT ===\n")
        f.write("Checking if languages converge to the exact same integer sequence (sync up).\n\n")
        
        sync_found = False
        for tail, names in synced_groups.items():
            if len(names) > 1:
                sync_found = True
                f.write(f"SYNC GROUP FOUND ({len(names)} languages):\n")
                f.write(f"  Converged Sequence (Tail): {tail}\n")
                f.write(f"  Languages: {', '.join(sorted(names))}\n")
                f.write("-" * 40 + "\n")
        
        if not sync_found:
            f.write("No distinct languages synced up to the same integer sequence.\n")
            f.write("Each language maintained a unique river path based on its orthography.\n")

    print(f"Analysis complete. Report saved to: {report_file}")
    
    # Print summary to CLI
    with open(report_file, "r") as f:
        print(f.read())

if __name__ == "__main__":
    main()
