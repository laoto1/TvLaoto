with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('text = "• LIVE"', 'text = "LIVE"')
content = content.replace('text = "? LIVE"', 'text = "LIVE"')

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
