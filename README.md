# Gemini Linguistic Toolkit (GLT)

An analytical suite for exploring "Linguistic Topology," "Waveform Structures," and the "Erik Convergence" algorithm across ancient and modern languages.

## Overview
This toolkit provides a set of Python-based scripts designed to analyze how different languages converge into "Main Trunks" of logic or diverge into "Rebel Streams." It measures the "Convergence Velocity" of a language by calculating trajectories based on the native sign count (e.g., Sumerian Cuneiform) or letter count (e.g., English).

The project has evolved to include tools for linguistic forensics and a comprehensive documentation of the theory's progression.

## Core Concepts
- **Convergence Velocity:** A metric for how quickly a language's number system unifies disparate starting points into a single trajectory. English has a high velocity (97% unity), while languages like Navajo are hyper-fractured (37% unity).
- **Linguistic Forensics:** The application of stylometric analysis to identify the statistical "fingerprint" of a text, which can help determine authorship or detect translation artifacts.
- **The "River" Model:** A metaphor for the flow of numbers under the `n -> n + L(n)` map, consisting of a Main Trunk, Tributaries, and Rebel Streams.

## How to Run
In a Termux or Linux environment:
1. Ensure Python 3 is installed.
2. Run the master menu:
   ```bash
   ./run_app.sh
   ```
3. From the main menu, press 'H' to open the detailed help guide.

## Toolkit Features
The main menu provides access to several modules:

1.  **Linguistic Topology Analysis:**
    *   **NEW:** "Turbo Mode" Analysis (10x-100x faster) using the Go Core.
    *   Analyze the convergence properties of languages using `.lang` files.
    *   Run simulations for hardcoded languages (English, French, etc.).
    *   Perform extended (1,000,000 step) traces on ancient languages to test for ultimate convergence.
    *   Verify Convergence for Seeds 0-13: Explicitly demonstrates how early integers merge into the Main Trunk.

2.  **Linguistic Forensics (Hoax ID):**
    *   **Quick Fingerprint:** Generates a single statistical "fingerprint" for an entire text file.
    *   **Advanced Bias Detector:** A more sophisticated tool that attempts to separate a translator's introduction from the main text. It generates two fingerprints to measure the "stylistic distance" between the translator and the original author's translated work, helping to detect bias.
    *   **Topological Stylometry Analyzer:** A multi-vector forensic tool that partitions text by grammar and calculates the "Topological Weight" of part-of-speech categories. It detects author signatures by measuring the unconscious mathematical structure of their prose.
    *   **Code Breaker Simulation:** A proof-of-concept demonstrating how topological analysis can be used to identify the source language of a number-based cipher.

3.  **Theory & Documentation:**
    *   View the core documents that explain the theory and its evolution, including the formal mathematical definition, the algorithm's step-by-step logic, and the final OEIS submission draft.

## New Hybrid Architecture (v2.0)
The toolkit now employs a hybrid Python/Go architecture for maximum performance.

*   **lta_wrapper.py**: The main entry point. Automatically detects if the Go binary is compiled and uses it for heavy number-crunching. Falls back to Python if missing.
    ```bash
    python lta_wrapper.py <lang_file>
    ```
*   **go_core/**: Contains the source code for the high-performance Go engine.
    *   Compile with: `cd go_core && go build -o lta_core lta_core.go`
*   **manage_languages.py**: A unified utility for maintaining the language library.
    *   `list`: Show all available languages.
    *   `validate`: Check for syntax/script errors.
    *   `set_math`: Update the math system (e.g., western, sumerian, hebrew).
*   **manage_corpus.py**: Utilities for managing the text corpus.
    *   `list`: List all text files in `test_documents/`.
    *   `import_abbyy`: Convert Abbyy XML (from Archive.org) to clean text.
    *   `segment`: Splits a text file into segments (Front Matter, Introduction, Chapters) to isolate translator bias from the original author's text.

---
*Developed by Erik Mize, with assistance from the Gemini CLI, for research into the mathematical properties of language and its impact on civilizational stability.*