with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(90, 150):
    if i < len(lines): print(lines[i].rstrip())
