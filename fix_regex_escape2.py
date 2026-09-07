import re
with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'Regex\(".*?"\)\.find\(url\)', r'Regex("-(\\\\w+)\\\\.html").find(url)', content)

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed regex strictly")
