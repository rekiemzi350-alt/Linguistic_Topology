import os
import time
from datetime import datetime

# --- Constants ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RESULTS_DIR = os.path.join(BASE_DIR, "results")
DEFAULT_DOCS_DIR = os.path.join(BASE_DIR, "test_documents")
DEFAULT_LANGS_DIR = os.path.join(BASE_DIR, "languages")

# --- Session Management ---
_session_id = None
_output_dir = None

def get_session_id():
    global _session_id
    if _session_id is None:
        _session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    return _session_id

def get_output_dir():
    global _output_dir
    if _output_dir is None:
        sid = get_session_id()
        _output_dir = os.path.join(DEFAULT_RESULTS_DIR, sid)
        if not os.path.exists(_output_dir):
            os.makedirs(_output_dir, exist_ok=True)
    return _output_dir

def resolve_path(path):
    """
    Attempts to resolve a path. 
    If it's one of the problematic 'coffee' paths, it converts it to a project-relative path.
    """
    if not path:
        return path
    
    # Handle the problematic hardcoded paths
    coffee_marker = "/data/data/com.termux/files/home/coffee/"
    if coffee_marker in path:
        rel_path = path.split(coffee_marker)[-1]
        
        # Mapping known coffee directories to local ones
        if rel_path.startswith("test_results/"):
            return os.path.join(get_output_dir(), rel_path.replace("test_results/", ""))
        if rel_path.startswith("test_documents/"):
            return os.path.join(DEFAULT_DOCS_DIR, rel_path.replace("test_documents/", ""))
        if rel_path.startswith("linguistic_topology_repo/languages/"):
            return os.path.join(DEFAULT_LANGS_DIR, rel_path.replace("linguistic_topology_repo/languages/", ""))
        
        # Fallback: relative to project root
        return os.path.join(BASE_DIR, rel_path)

    return path

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

# Initialization
if not os.path.exists(DEFAULT_RESULTS_DIR):
    os.makedirs(DEFAULT_RESULTS_DIR, exist_ok=True)
if not os.path.exists(DEFAULT_DOCS_DIR):
    os.makedirs(DEFAULT_DOCS_DIR, exist_ok=True)
