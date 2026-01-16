import os
import sys

# Add the repo to path so we can import the engine
sys.path.append('/data/data/com.termux/files/home/coffee/linguistic_topology_repo')
from linguistic_topology_app import parse_lang_file

def generate_oeis_file(lang_path, output_dir):
    try:
        lang_data = parse_lang_file(lang_path)
        name = lang_data['name']
        filename_clean = name.replace(" ", "_").replace("/", "_")
        
        # Calculate Main Trunk (starting at 1 for safety, as many ancient langs lack 0)
        curr = 1
        sequence = []
        for _ in range(100):
            sequence.append(curr)
            l = lang_data['get_len_func'](curr, lang_data['rules'])
            if l == 0: break # Termination or lack of rule
            curr += l
        
        if len(sequence) < 10: return # Skip if too short
        
        seq_str = ",".join(map(str, sequence))
        
        content = f"""%I A000000 (To be assigned)
%S {seq_str}
%N Trajectory of 1 under the map n -> n + number of signs/letters in {name} name of n.
%C This sequence represents the "Main Trunk" for the {name} linguistic iterative map.
%C 
%C DISCOVERY NOTE: Part of a global mapping of Linguistic Topology first identified by Erik Mize in 2003. 
%C This mapping compares "Convergence Velocity" across human languages to identify shared logical roots.
%C 
%H Erik Mize, Linguistic Topology Research (2003/2025)
%e a(0) = 1.
"""
        with open(f"{output_dir}/OEIS_Submission_{filename_clean}.txt", 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        with open("generation_errors.log", "a") as log:
            log.write(f"{lang_path}: {e}\n")
        return False

def main():
    if os.path.exists("generation_errors.log"):
        os.remove("generation_errors.log")
        
    lang_dir = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"
    output_dir = "/data/data/com.termux/files/home/coffee/oeis_submissions_batch"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    langs = [f for f in os.listdir(lang_dir) if f.endswith('.lang')]
    print(f"Found {len(langs)} languages. Generating submissions...")
    
    success_count = 0
    for lang_file in langs:
        if generate_oeis_file(os.path.join(lang_dir, lang_file), output_dir):
            success_count += 1
            
    print(f"Successfully generated {success_count} submission files in {output_dir}")

if __name__ == "__main__":
    main()
