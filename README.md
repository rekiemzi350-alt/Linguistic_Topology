# Linguistic Topology: Mapping the Erik Convergence

**Developed by Erik Mize**

## Overview
Linguistic Topology is a computational framework for analyzing the structural "friction" and convergence properties within human language number systems. This project provides the tools to map **Erik Convergence**—the process by which integers, when iterated through a linguistic length-addition map, coalesce into primary attractor basins or "Rivers."

## The Main Trunk (OEIS A391196)
At the heart of this research is **OEIS Sequence A391196**, which identifies the primary trajectory of the English language under the iterative map:

$$a_{n+1} = a_n + \text{Length}(\text{EnglishName}(a_n))$$

### Key Topological Findings:
*   **The Main Trunk:** A robust attractor basin that captures ~96% of all integers in the range [0, 100].
*   **The Rebel Stream:** A distinct anomalous trajectory starting at seeds {83, 84, 93, 94} that remains independent for thousands of steps before merging with the Main Trunk at 2827.
*   **Structural Identity:** A methodology for comparing "Convergence Velocity" across different languages (e.g., English, Sumerian, Ancient Greek) to identify shared linguistic roots or forensic identities.

## Project Structure
*   `linguistic_topology_app.py`: The core analysis engine and simulation tool.
*   `languages/`: A library of `.lang` files defining the naming rules and scripts for various ancient and modern languages.

## Usage
To analyze a language's topology:
```bash
python linguistic_topology_app.py languages/english.lang
```

To perform a forensic comparison between two languages:
```bash
python linguistic_topology_app.py languages/english.lang languages/german.lang
```

## Citation & Priority
The patterns and methodologies contained herein were first identified by the author in 2003 and formally codified in 2025.
Official OEIS Entry: [A391196](https://oeis.org/A391196)

## License
This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license. This means you are free to use and share the research for non-commercial purposes, provided you credit Erik Mize. Commercial use requires explicit permission.

---
*Initial analysis and verification assisted by Gemini CLI.*
