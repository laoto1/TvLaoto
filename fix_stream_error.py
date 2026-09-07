with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('text = "STREAM ERROR"', 'text = stringResource(R.string.stream_error)')

with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
