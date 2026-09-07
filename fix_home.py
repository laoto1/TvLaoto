with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

if "val isDecryptingLink by playerViewModel.isDecryptingLink.collectAsState()" not in content:
    content = content.replace(
        "val isBuffering by playerViewModel.isBuffering.collectAsState()",
        "val isBuffering by playerViewModel.isBuffering.collectAsState()\n    val isDecryptingLink by playerViewModel.isDecryptingLink.collectAsState()"
    )

if "isDecryptingLink = isDecryptingLink" not in content:
    content = content.replace(
        "isBuffering = isBuffering,",
        "isBuffering = isBuffering,\n                                isDecryptingLink = isDecryptingLink,"
    )

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated HomeScreen.kt")
