import re
with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'val channelIdMatch = Regex\(.*?\)\.find\(url\)', r'val channelIdMatch = Regex("-(\\\\d+)(?:,|\\\\.html)").find(url)', content)

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated regex to support commas!")
