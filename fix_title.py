import re
with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'r', encoding='utf-8') as f:
    content = f.read()

target = "if(split[j].trim() != time && split[j].trim().length > 2) {"
replacement = "if(split[j].trim() != time && split[j].trim().length > 2 && split[j].trim().toUpperCase() !== 'LIVE' && split[j].trim().toUpperCase() !== '• LIVE') {"

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed title extraction in StreamSniffer")
else:
    print("Target not found!")
