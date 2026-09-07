import os

def analyze_dir(path):
    try:
        items = []
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                items.append((entry.name, entry.stat(follow_symlinks=False).st_size))
            elif entry.is_dir(follow_symlinks=False):
                # shallow size for dirs or full? Let's just do full for direct children
                def get_size(start_path):
                    total = 0
                    for dirpath, _, filenames in os.walk(start_path):
                        for f in filenames:
                            fp = os.path.join(dirpath, f)
                            if not os.path.islink(fp):
                                total += os.path.getsize(fp)
                    return total
                items.append((entry.name + " (DIR)", get_size(entry.path)))
        
        items.sort(key=lambda x: x[1], reverse=True)
        for name, size in items[:15]:
            print(f"{name}: {size / (1024**3):.2f} GB")
    except:
        pass

print("Desktop:")
analyze_dir("C:\\Users\\Administrator\\Desktop")
print("Downloads:")
analyze_dir("C:\\Users\\Administrator\\Downloads")
print("Documents:")
analyze_dir("C:\\Users\\Administrator\\Documents")
