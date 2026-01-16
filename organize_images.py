import os
import shutil
import math
from PIL import Image

# Configuration
SOURCE_DIRS = [
    "/sdcard/Books",
    "/sdcard/DCIM",
    "/sdcard/Documents",
    "/sdcard/Download",
    "/sdcard/Download2",
    "/sdcard/Pictures",
    "/sdcard/Pictures Ii"
]
DEST_ROOT = "/sdcard/Pics"
IGNORE_DIR_NAME = ".thumbnails"

# Supported extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.tiff', '.tif'}

def get_aspect_ratio_str(width, height):
    if height == 0: return "0•0"
    gcd = math.gcd(width, height)
    x = width // gcd
    y = height // gcd
    return f"{x}•{y}"

def get_unique_filename(directory, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

def process_file(file_path):
    try:
        # Check extension first
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in IMAGE_EXTENSIONS:
            return

        # Open image to get dimensions
        # We verify it's an image by opening it.
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                ratio_str = get_aspect_ratio_str(width, height)
        except Exception:
            # Not a valid image or cannot be opened
            return

        # Determine destination folder
        dest_dir = os.path.join(DEST_ROOT, f"Pics - {ratio_str}")
        
        # Ensure destination exists
        os.makedirs(dest_dir, exist_ok=True)
        
        # Determine destination filename
        filename = os.path.basename(file_path)
        new_filename = get_unique_filename(dest_dir, filename)
        dest_path = os.path.join(dest_dir, new_filename)
        
        # Avoid moving if it's the same file (in case of overlap, though unlikely given paths)
        if os.path.abspath(file_path) == os.path.abspath(dest_path):
            return

        # Move file
        print(f"Moving {file_path} -> {dest_path}")
        shutil.move(file_path, dest_path)
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    print("Starting image organization...")
    
    # Create root dest if not exists
    if not os.path.exists(DEST_ROOT):
        try:
            os.makedirs(DEST_ROOT)
        except PermissionError:
            print(f"Permission denied creating {DEST_ROOT}. Please ensure Termux has storage permissions.")
            return

    for source_dir in SOURCE_DIRS:
        if not os.path.exists(source_dir):
            print(f"Source directory not found, skipping: {source_dir}")
            continue

        print(f"Scanning {source_dir}...")
        for root, dirs, files in os.walk(source_dir):
            # Modify dirs in-place to skip ignored directories
            if IGNORE_DIR_NAME in dirs:
                dirs.remove(IGNORE_DIR_NAME)
            
            for file in files:
                file_path = os.path.join(root, file)
                process_file(file_path)

    print("Organization complete.")

if __name__ == "__main__":
    main()
