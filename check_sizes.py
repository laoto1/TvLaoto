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
    r"C:\Users\Administrator\.gradle\caches",
    r"C:\Users\Administrator\.gradle\daemon",
    r"C:\Users\Administrator\.gradle\wrapper",
    r"C:\Users\Administrator\AppData\Local\Temp",
    r"C:\Users\Administrator\.android",
    r"C:\Users\Administrator\source\repos\TvLaoto\app\build",
    r"C:\Users\Administrator\.gemini\antigravity"
]

for p in paths:
    size = get_size(p)
    print(f"{p}: {size / (1024*1024*1024):.2f} GB")
