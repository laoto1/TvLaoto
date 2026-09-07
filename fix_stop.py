with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("viewModel.player.stop()", "// viewModel.player.stop() // Removed to allow seamless transition back to HomeScreen")

with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed player.stop() from PlayerScreen")
