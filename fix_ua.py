import re
with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('connection.requestMethod = "GET"', 'connection.requestMethod = "GET"\n            connection.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")')

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Added User-Agent")
