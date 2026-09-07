import re
with open('log.txt', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
for line in lines[-200:]:
    if 'tvlaoto' in line or 'ExoPlayer' in line or 'Exception' in line or 'Error' in line:
        print(line.rstrip())
