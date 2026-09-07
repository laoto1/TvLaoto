import re
with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Replace any occurrence of the bad regex
content = re.sub(r'Regex\("\^Phim.*?:\\s\*"\)', r'Regex("^Phim truyện:\\\\s*")', content)

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed regex Phim truyen")
