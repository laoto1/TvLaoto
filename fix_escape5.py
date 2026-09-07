import io
import re

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Just replace the whole line!
content = re.sub(r'var title = titleEl.innerText.replace\(.*?trim\(\);', r"var title = titleEl.innerText.replace(/\\\\u2022\\\\s*LIVE/g, '').replace('LIVE', '').trim();", content)

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Replaced whole regex line")
