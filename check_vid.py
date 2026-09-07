with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(30, 60):
    print(lines[i].rstrip())
