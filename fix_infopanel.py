import re

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Hide description if empty
desc_old = """            Spacer(modifier = Modifier.height(5.dp))

            Text(
                text = channel.programDescription,
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = FontWeight.Normal,
                    fontSize = 11.5.sp,
                    color = Color(0xFF64748B)
                ),
                maxLines = 2
            )"""
desc_new = """            if (channel.programDescription.isNotEmpty()) {
                Spacer(modifier = Modifier.height(5.dp))

                Text(
                    text = channel.programDescription,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Normal,
                        fontSize = 11.5.sp,
                        color = Color(0xFF64748B)
                    ),
                    maxLines = 2
                )
            }"""
content = content.replace(desc_old, desc_new)

# Replay button conditionally
replay_old = """            // 1. Replay
            EpgActionButton(
                title = stringResource(R.string.replay),
                icon = Icons.Default.Replay,
                backgroundBrush = Brush.horizontalGradient(
                    colors = listOf(Color(0xFF6366F1), Color(0xFF8B5CF6))
                ),
                borderColor = Color.Transparent,
                onClick = onReplayClick
            )"""
replay_new = """            // 1. Replay
            if (channel.isSup) {
                EpgActionButton(
                    title = stringResource(R.string.replay),
                    icon = Icons.Default.Replay,
                    backgroundBrush = Brush.horizontalGradient(
                        colors = listOf(Color(0xFF6366F1), Color(0xFF8B5CF6))
                    ),
                    borderColor = Color.Transparent,
                    onClick = onReplayClick
                )
            }"""
content = content.replace(replay_old, replay_new)

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated ProgramInfoPanel")
