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

def analyze_dir(path, max_depth, current_depth=0):
    if current_depth > max_depth:
        return
    try:
        dirs = []
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                dirs.append(entry.path)
        
        sizes = []
        for d in dirs:
            size = get_size(d)
            if size > 1024 * 1024 * 1024: # > 1GB
                sizes.append((d, size))
        
        sizes.sort(key=lambda x: x[1], reverse=True)
        for d, size in sizes:
            print(f"{d}: {size / (1024**3):.2f} GB")
            analyze_dir(d, max_depth, current_depth + 1)
    except:
        pass

print("Scanning C:\\ for large folders (>1GB)...")
analyze_dir("C:\\", max_depth=2)
