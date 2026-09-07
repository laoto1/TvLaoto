import re
with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''        // SurfaceView Video Layer
        AndroidView(
            factory = { ctx ->
                PlayerView(ctx).apply {
                    this.player = player
                    useController = isCatchup
                    resizeMode = AspectRatioFrameLayout.RESIZE_MODE_ZOOM
                    layoutParams = FrameLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT
                    )
                }
            },
            modifier = Modifier.fillMaxSize()
        )'''

replacement = '''        // SurfaceView Video Layer
        AndroidView(
            factory = { ctx ->
                PlayerView(ctx).apply {
                    this.player = player
                    useController = isCatchup
                    resizeMode = AspectRatioFrameLayout.RESIZE_MODE_ZOOM
                    layoutParams = FrameLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT
                    )
                    isFocusable = true
                }
            },
            update = { playerView ->
                playerView.useController = isCatchup
                if (isCatchup) {
                    playerView.requestFocus()
                }
            },
            modifier = Modifier.fillMaxSize().focusable(isCatchup)
        )'''

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated VideoPlayerPanel")
else:
    print("Target not found in VideoPlayerPanel")

