import os
import shutil

# Configuration
SOURCE_DIR = os.getcwd()
DEST_DIR = "/sdcard/Documents/Lazylist"

print(f"Starting backup from {SOURCE_DIR} to {DEST_DIR}...")

count = 0
for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.endswith(".py"):
            # Calculate relative path
            rel_path = os.path.relpath(root, SOURCE_DIR)
            
            # Construct destination path
            dest_folder = os.path.join(DEST_DIR, rel_path)
            
            # Ensure destination folder exists
            os.makedirs(dest_folder, exist_ok=True)
            
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_folder, file)
            
            try:
                shutil.copy2(src_file, dest_file)
                print(f"Copied: {file}")
                count += 1
            except Exception as e:
                print(f"Failed to copy {file}: {e}")

print(f"\nBackup complete. {count} Python files copied.")
