with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "fun scrapeEpg" in line:
        for j in range(i, i+50):
            print(lines[j].rstrip())
        break
