import re
with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''        // Tap Gestures Layer
        Box(
            modifier = Modifier
                .fillMaxSize()
                .pointerInput(Unit) {
                    detectTapGestures(
                        onDoubleTap = { onToggleFullscreen() },
                        onTap = { onTogglePlayPause() }
                    )
                }
        )'''

replacement = '''        // Tap Gestures Layer
        if (!isCatchup) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .pointerInput(Unit) {
                        detectTapGestures(
                            onDoubleTap = { onToggleFullscreen() },
                            onTap = { onTogglePlayPause() }
                        )
                    }
            )
        }'''

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated VideoPlayerPanel gestures")
else:
    print("Target not found in VideoPlayerPanel")
