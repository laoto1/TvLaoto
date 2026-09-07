import re

with open('app/src/main/java/com/tvlaoto/ui/components/EpgSidePanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the main Panel shape and border
target_panel = """            // Glass Panel
            Column(
                modifier = Modifier
                    .fillMaxHeight()
                    .width(420.dp)
                    .background(Brush.horizontalGradient(listOf(Color(0xE60A0A14), Color(0xF212121C)))) // Glass effect
                    .border(1.dp, Color(0x33FFFFFF))
                    .padding(vertical = 16.dp, horizontal = 20.dp)
            ) {"""

replacement_panel = """            // Glass Panel
            Column(
                modifier = Modifier
                    .fillMaxHeight()
                    .padding(vertical = 24.dp, horizontal = 16.dp)
                    .width(420.dp)
                    .clip(RoundedCornerShape(24.dp))
                    .background(Brush.horizontalGradient(listOf(Color(0xE60A0A14), Color(0xF212121C))))
                    .neonBorder(
                        brush = Brush.linearGradient(listOf(Color(0x66FFFFFF), Color(0x1AFFFFFF))),
                        cornerRadius = 24.dp,
                        borderWidth = 1.dp,
                        glowRadius = 12.dp
                    )
                    .padding(vertical = 20.dp, horizontal = 24.dp)
            ) {"""
content = content.replace(target_panel, replacement_panel)

# Fix the EpgProgramItem styles
target_item = """    val backgroundBrush = when {
        isFocused || isPlayingThis -> Brush.horizontalGradient(
            colors = listOf(Color(0x4DE91E63), Color(0x339C27B0))
        )
        else -> Brush.linearGradient(
            colors = listOf(Color(0x1AFFFFFF), Color(0x1AFFFFFF))
        )
    }

    val borderBrush = when {
        isFocused || isPlayingThis -> Brush.horizontalGradient(
            colors = listOf(Color(0x99E91E63), Color(0x669C27B0))
        )
        else -> SolidColor(Color(0x11FFFFFF))
    }"""

replacement_item = """    val backgroundBrush = when {
        isFocused || isPlayingThis -> Brush.horizontalGradient(
            colors = listOf(Color(0x66E91E63), Color(0x669C27B0))
        )
        else -> Brush.linearGradient(
            colors = listOf(Color(0x1AFFFFFF), Color(0x1AFFFFFF))
        )
    }

    val borderBrush = when {
        isFocused || isPlayingThis -> Brush.horizontalGradient(
            colors = listOf(Color(0xFFE91E63), Color(0xFF9C27B0))
        )
        else -> SolidColor(Color.Transparent)
    }"""
content = content.replace(target_item, replacement_item)

# Remove LIVE / PLAYING padding so it matches the image (just the tag, no extra spacer if possible, wait the code is fine)

with open('app/src/main/java/com/tvlaoto/ui/components/EpgSidePanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated EpgSidePanel UI")
