import os
import shutil
import sys

def move_with_space_management(src_root, dst_root):
    if not os.path.exists(src_root):
        print(f"Source {src_root} does not exist.")
        return

    for root, dirs, files in os.walk(src_root):
        # Determine relative path
        rel_path = os.path.relpath(root, src_root)
        if rel_path == ".":
            target_dir = dst_root
        else:
            target_dir = os.path.join(dst_root, rel_path)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)

            try:
                # Copy and then remove to ensure space is managed
                shutil.copy2(src_file, dst_file)
                os.remove(src_file)
                print(f"Moved: {src_file}")
            except Exception as e:
                print(f"Error moving {src_file}: {e}")

if __name__ == "__main__":
    # Source paths
    src1 = "/sdcard/Pics"
    src2 = "/sdcard/Pictures Ii"
    
    # Destination is current directory
    dst1 = os.path.join(os.getcwd(), "Pics")
    dst2 = os.path.join(os.getcwd(), "Pictures Ii")

    print("Starting move of Pics...")
    move_with_space_management(src1, dst1)
    
    print("\nStarting move of Pictures Ii...")
    move_with_space_management(src2, dst2)
    
    # Cleanup empty source directories
    try:
        shutil.rmtree(src1)
        shutil.rmtree(src2)
    except:
        pass

    print("\nMove complete.")
