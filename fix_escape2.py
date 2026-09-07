import io

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the bad line
bad_line = "                   var title = titleEl.innerText.replace(/\\u2022\\s*LIVE/g, '').replace('LIVE', '').trim();"
good_line = "                   var title = titleEl.innerText.replace(/•\\\\s*LIVE/g, '').replace('LIVE', '').trim();"

content = content.replace(bad_line, good_line)

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed regex escape sequence properly")
