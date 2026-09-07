import os

def get_size(start_path):
    total_size = 0
    try:
        for entry in os.scandir(start_path):
            if entry.is_file(follow_symlinks=False):
                total_size += entry.stat(follow_symlinks=False).st_size
            elif entry.is_dir(follow_symlinks=False):
                total_size += get_size(entry.path)
    except:
        pass
    return total_size

paths = [
    r"C:\$Recycle.Bin",
    r"C:\System Volume Information",
]

for p in paths:
    size = get_size(p)
    print(f"{p}: {size / (1024**3):.2f} GB")
