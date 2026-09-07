with open('app/src/main/java/com/tvlaoto/ui/components/SearchOverlayDialog.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('.com.tvlaoto.ui.theme.neonBorder', '.neonBorder')

with open('app/src/main/java/com/tvlaoto/ui/components/SearchOverlayDialog.kt', 'w', encoding='utf-8') as f:
    f.write(content)
