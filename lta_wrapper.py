
import subprocess
import json
import sys
import os
import linguistic_topology_app

# Path to the compiled Go binary
GO_BINARY_PATH = "./go_core/lta_core"

def run_go_analysis(file_path):
    """Executes the Go binary and returns the parsed JSON result."""
    if not os.path.exists(GO_BINARY_PATH):
        return None

    try:
        # Run the Go binary
        result = subprocess.run(
            [GO_BINARY_PATH, "-file", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Warning: Go accelerator failed ({e}). Falling back to Python.")
        return None

def print_results(data):
    """Formats and prints the analysis results (matches original app style)."""
    print(f"\n--- Analysis for: {data['language_name']} ---")
    print(f"Structure: {data['distinct_rivers']} Distinct River(s) found for integers 0-100.")
    print("-" * 40)
    
    # Sort just in case JSON order varied (Go handles sorting, but good to be safe)
    rivers = sorted(data['rivers'], key=lambda x: x['count'], reverse=True)
    
    for i, river in enumerate(rivers):
        tail = river['tail_preview']
        # Extract just the numbers for the preview if needed, or use as is
        # The Go app returns "...1 2 3", Python app expects "...(1, 2, 3)"
        # We'll format it to look similar
        
        print(f"  River #{i+1}: {river['percentage']}% of numbers converge here.")
        print(f"     -> Ends in pattern: {tail}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lta_wrapper.py <lang_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    # 1. Try Go Accelerator
    go_result = run_go_analysis(file_path)
    
    if go_result:
        print("(Using High-Performance Go Engine)")
        print_results(go_result)
    else:
        # 2. Fallback to Python
        print("(Using Standard Python Engine)")
        lang_data = linguistic_topology_app.parse_lang_file(file_path)
        linguistic_topology_app.analyze_language(lang_data)
