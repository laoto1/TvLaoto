import re

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

new_func = """@Composable
fun PlayerControlIcon(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    val neonGradient = remember {
        Brush.linearGradient(
            colors = listOf(GtaColors.ElectricCyan, GtaColors.HotPink)
        )
    }
    
    val glassGradient = remember {
        Brush.linearGradient(
            colors = listOf(Color(0xE6FFFFFF), Color(0x80FFFFFF))
        )
    }

    Box(
        modifier = modifier
            .clip(CircleShape) // for click ripple bounded to circle
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() },
        contentAlignment = Alignment.Center
    ) {
        // Glow layer underneath (only visible when focused)
        if (isFocused) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                modifier = Modifier
                    .fillMaxSize()
                    .blur(radius = 8.dp),
                tint = GtaColors.HotPink
            )
        }

        // Foreground Icon Layer with Gradient
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier
                .fillMaxSize()
                .graphicsLayer(alpha = 0.99f)
                .drawWithCache {
                    onDrawWithContent {
                        drawContent()
                        drawRect(
                            brush = if (isFocused) neonGradient else glassGradient,
                            blendMode = androidx.compose.ui.graphics.BlendMode.SrcAtop
                        )
                    }
                },
            tint = Color.White // overridden by SrcAtop
        )
    }
}
"""

content = re.sub(r'@Composable\nfun PlayerControlIcon.*?^}', new_func, content, flags=re.DOTALL | re.MULTILINE)

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated PlayerControlIcon in VideoPlayerPanel')
