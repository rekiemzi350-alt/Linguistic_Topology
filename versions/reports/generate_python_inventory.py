import os
import ast
import sys

# Configuration
SOURCE_DIR = "/data/data/com.termux/files/home/coffee"
OUTPUT_FILE = "python_scripts.txt"

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Parse AST to get docstring and imports
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree)
        
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)

        # Heuristic Description
        description = ""
        if docstring:
            # Take the first non-empty line of the docstring
            lines = [l.strip() for l in docstring.split('\n') if l.strip()]
            if lines:
                description = lines[0]
        
        if not description:
            # Fallback: Describe based on imports or content
            if "django" in imports or "flask" in imports or "fastapi" in imports:
                description = "Web application/API server."
            elif "matplotlib" in imports or "seaborn" in imports or "plotly" in imports:
                description = "Data visualization and plotting."
            elif "pandas" in imports or "numpy" in imports:
                description = "Data analysis or scientific computing."
            elif "torch" in imports or "tensorflow" in imports:
                description = "Machine learning or deep learning model."
            elif "requests" in imports or "urllib" in imports or "selenium" in imports:
                description = "Web scraping or network requests."
            elif "unittest" in imports or "pytest" in imports:
                description = "Unit testing script."
            elif "subprocess" in imports or "shutil" in imports:
                description = "System automation or file management."
            else:
                description = "General utility or calculation script."

        # Heuristic Language Recommendation
        recommendation = "Python is likely suitable."
        
        # Performance critical indicators
        has_heavy_loops = "for" in content and "range" in content and ("1000" in content or "len" in content)
        is_math_heavy = "math" in imports and not ("numpy" in imports or "pandas" in imports)
        is_threading = "threading" in imports or "multiprocessing" in imports
        
        if "numpy" in imports or "pandas" in imports or "torch" in imports:
            recommendation = "Python (Optimal). Leverages optimized C libraries for data/ML."
        elif is_math_heavy or has_heavy_loops:
            recommendation = "C++ or Rust. Computationally intensive loops/math might benefit from compiled languages."
        elif is_threading:
            recommendation = "Go or Elixir. Concurrency might be handled more efficiently/simply."
        elif "selenium" in imports:
            recommendation = "Node.js (Puppeteer/Playwright). Often has better native integration for browser automation."
        elif "subprocess" in imports and len(content.split('\n')) < 50:
            recommendation = "Bash/Shell. Simple system commands might be cleaner in a shell script."
        
        return description, recommendation

    except Exception as e:
        return f"Error analyzing file: {str(e)}", "N/A"

def main():
    results = []
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Skip hidden/system dirs
        if any(part.startswith('.') for part in root.split(os.sep)):
            continue
            
        for file in files:
            if file.endswith(".py") and file != os.path.basename(__file__):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, SOURCE_DIR)
                
                desc, rec = analyze_file(path)
                
                results.append(f"File: {rel_path}\nDescription: {desc}\nRecommendation: {rec}\n" + "-"*40)

    # Sort for tidiness
    results.sort()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("PYTHON SCRIPT INVENTORY & ANALYSIS\n")
        f.write("==================================\n\n")
        f.write("\n".join(results))
    
    print(f"Analysis complete. Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
