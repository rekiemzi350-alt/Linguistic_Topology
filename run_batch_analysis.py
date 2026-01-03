import sys
import os
import glob

# Ensure the current directory is in the path to import the app
sys.path.append(os.getcwd())

try:
    from linguistic_topology_app import parse_lang_file, analyze_language
except ImportError:
    # Try importing from the current directory if run from outside
    sys.path.append(os.path.join(os.getcwd(), 'linguistic_topology_repo'))
    from linguistic_topology_app import parse_lang_file, analyze_language

def run_analysis():
    # List of new languages to check
    new_languages = [
        "apiaka_of_tocantins.lang", "arakaju.lang", "old_aramaic.lang", "baenan.lang", 
        "boanari.lang", "cayuse.lang", "corpus.lang", "darkinjung.lang", 
        "kilit_dialect.lang", "leivu_dialect.lang", "manangkari.lang", "matanawi.lang", 
        "morique.lang", "mucuchi_marripu.lang", "ngarla.lang", "paleo_corsican.lang", 
        "palmela.lang", "paravilhana.lang", "pimenteira.lang", "querandi.lang", 
        "samaritan_aramaic.lang", "sapara.lang", "sarghulami.lang", "tehotitachsae.lang", 
        "tiverikoto.lang", "uru.lang", "waikuri.lang", "wajumara.lang", 
        "wakka_wakka.lang", "ware.lang", "yaruma.lang"
    ]

    base_path = "languages"
    # Adjust path if running from root
    if not os.path.exists(base_path):
        base_path = os.path.join("linguistic_topology_repo", "languages")

    print(f"Searching for language files in: {base_path}")
    
    for lang_file in new_languages:
        full_path = os.path.join(base_path, lang_file)
        if os.path.exists(full_path):
            try:
                print(f"\nProcessing {lang_file}...")
                lang_data = parse_lang_file(full_path)
                analyze_language(lang_data)
            except Exception as e:
                print(f"Error processing {lang_file}: {e}")
        else:
            print(f"File not found: {full_path}")

if __name__ == "__main__":
    run_analysis()
