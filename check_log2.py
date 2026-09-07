import re
with open('log.txt', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
for line in lines:
    if 'com.tvlaoto' in line or 'ExoPlayer' in line or 'PlayerViewModel' in line or 'chromium' in line:
        print(line.rstrip())
