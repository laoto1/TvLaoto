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
            colors = listOf(Color.White, Color(0x99FFFFFF))
        )
    }

    Box(
        modifier = modifier
            .clip(CircleShape)
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() },
        contentAlignment = Alignment.Center
    ) {
        // Glow layer underneath (always visible, stronger when focused)
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier
                .fillMaxSize()
                .blur(radius = if (isFocused) 12.dp else 4.dp),
            tint = if (isFocused) GtaColors.HotPink else Color(0x80FFFFFF)
        )

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
                            blendMode = androidx.compose.ui.graphics.BlendMode.SrcIn
                        )
                    }
                },
            tint = Color.Black
        )
    }
}"""

content = re.sub(r'@Composable\nfun PlayerControlIcon.*?^}', new_func, content, flags=re.DOTALL | re.MULTILINE)

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated PlayerControlIcon in VideoPlayerPanel')
