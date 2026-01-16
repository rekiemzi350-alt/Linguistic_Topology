import os
import sys
import re

# Add repo to path
sys.path.append('/data/data/com.termux/files/home/coffee/linguistic_topology_repo')
from linguistic_topology_app import parse_lang_file

LANG_DIR = "/data/data/com.termux/files/home/coffee/linguistic_topology_repo/languages/"

def find_stall_point(path):
    try:
        lang_data = parse_lang_file(path)
        curr = 1
        for i in range(1, 1000):
            l = lang_data['get_len_func'](curr, lang_data['rules'])
            if l == 0:
                return curr
            curr += l
        return 1000 # Success
    except:
        return -1

def main():
    files = sorted([f for f in os.listdir(LANG_DIR) if f.endswith('.lang') and "TECH" not in f])
    print(f"{'Language':<25} | {'Stall Point'}")
    print("-" * 40)
    for f in files:
        stall = find_stall_point(os.path.join(LANG_DIR, f))
        if stall < 1000:
            print(f"{f:<25} | {stall}")

if __name__ == "__main__":
    main()
