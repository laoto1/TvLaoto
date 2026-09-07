with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Replace single backslash w with double backslash
content = content.replace('Regex("-(\\w+)\\.html")', 'Regex("-(\\\\\\\\w+)\\\\\\\\.html")')

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed regex escape")
