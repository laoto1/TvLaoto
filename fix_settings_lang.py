with open('app/src/main/java/com/tvlaoto/ui/components/SettingsDialog.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('text = "Ti?ng Vi?t"', 'text = stringResource(R.string.vietnamese)')
content = content.replace('text = "English"', 'text = stringResource(R.string.english)')

with open('app/src/main/java/com/tvlaoto/ui/components/SettingsDialog.kt', 'w', encoding='utf-8') as f:
    f.write(content)
