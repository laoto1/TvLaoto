with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('.fillMaxSize() 12.dp else 4.dp),', '.fillMaxSize(),')

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed syntax error in VideoPlayerPanel.kt")
