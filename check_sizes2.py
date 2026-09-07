import os

def get_size(start_path):
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except:
        pass
    return total_size

paths = [
    r"C:\Users",
    r"C:\Windows\Temp",
    r"C:\ProgramData",
]

for p in paths:
    size = get_size(p)
    print(f"{p}: {size / (1024*1024*1024):.2f} GB")
