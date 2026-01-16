import os

src_dir = "/sdcard/Documents/Test_Files"
dst_dir = "test_documents"

src_files = os.listdir(src_dir)
dst_files = os.listdir(dst_dir)

# Normalize names for comparison (remove extensions)
dst_names = {os.path.splitext(f)[0] for f in dst_files}

missing = []
for f in src_files:
    name, ext = os.path.splitext(f)
    if name not in dst_names:
        missing.append(f)

print("Missing files:")
for m in missing:
    print(m)
