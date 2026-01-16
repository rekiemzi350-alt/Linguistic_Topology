import os
import sys
import glob
from io import StringIO

# Add current directory to path to find the app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app logic
try:
    from linguistic_topology_app import parse_lang_file, analyze_language
except ImportError:
    print("Error: Could not import linguistic_topology_app.py. Make sure it is in the same directory.")
    sys.exit(1)

def capture_analysis(lang_file, output_dir):
    try:
        lang_data = parse_lang_file(lang_file)
        
        # Capture stdout
        old_stdout = sys.stdout
        result_buffer = StringIO()
        sys.stdout = result_buffer
        
        analyze_language(lang_data)
        
        sys.stdout = old_stdout
        result_text = result_buffer.getvalue()
        
        # Write to file
        base_name = os.path.basename(lang_file)
        result_file = os.path.join(output_dir, base_name.replace(".lang", "_results.txt"))
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(result_text)
            
        return True, base_name
    except Exception as e:
        sys.stdout = sys.__stdout__ # Restore just in case
        return False, f"{os.path.basename(lang_file)}: {e}"

def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    languages_dir = os.path.join(repo_dir, "languages")
    baseline_dir = os.path.join(repo_dir, "baseline_results")
    
    if not os.path.exists(baseline_dir):
        os.makedirs(baseline_dir)
        print(f"Created directory: {baseline_dir}")
        
    lang_files = glob.glob(os.path.join(languages_dir, "*.lang"))
    
    # Filter out TECH files
    lang_files = [f for f in lang_files if "TECH.lang" not in f]
    
    print(f"Found {len(lang_files)} native languages. Starting analysis...")
    
    success_count = 0
    errors = []
    
    for lang_file in lang_files:
        success, msg = capture_analysis(lang_file, baseline_dir)
        if success:
            # print(f"Analyzed: {msg}") 
            # Keep output minimal as requested
            sys.stdout.write(".")
            sys.stdout.flush()
            success_count += 1
        else:
            print(f"\nFailed: {msg}")
            errors.append(msg)
            
    print(f"\n\nCompleted. {success_count} languages analyzed.")
    print(f"Results saved to: {baseline_dir}")
    if errors:
        print("\nErrors encountered:")
        for err in errors:
            print(err)

if __name__ == "__main__":
    main()
