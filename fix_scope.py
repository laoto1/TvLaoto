with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

target = """            // Bottom Status Bar
            BottomStatusBar(
                currentChannelName = currentPlayingChannel?.name
            )

            // Animated Error Toast
            AnimatedVisibility(
                visible = errorMessage != null,
                enter = slideInVertically(initialOffsetY = { -it }) + fadeIn(),
                exit = slideOutVertically(targetOffsetY = { -it }) + fadeOut(),
                modifier = Modifier.align(Alignment.TopCenter).padding(top = 24.dp)
            ) {
                Box(
                    modifier = Modifier
                        .clip(GtaShapes.SmallCardShape)
                        .background(Brush.horizontalGradient(listOf(Color(0xE6FF003C), Color(0xCCFF003C))))
                        .neonBorder(
                            brush = Brush.linearGradient(listOf(Color.White, Color(0x80FFFFFF))),
                            cornerRadius = 8.dp,
                            borderWidth = 1.dp,
                            glowRadius = 8.dp
                        )
                        .padding(horizontal = 24.dp, vertical = 12.dp)
                ) {
                    Text(
                        text = errorMessage ?: "",
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        fontSize = 16.sp
                    )
                }
            }
        }"""

replacement = """            // Bottom Status Bar
            BottomStatusBar(
                currentChannelName = currentPlayingChannel?.name
            )
        }

        // Animated Error Toast
        AnimatedVisibility(
            visible = errorMessage != null,
            enter = slideInVertically(initialOffsetY = { -it }) + fadeIn(),
            exit = slideOutVertically(targetOffsetY = { -it }) + fadeOut(),
            modifier = Modifier.align(Alignment.TopCenter).padding(top = 24.dp)
        ) {
            Box(
                modifier = Modifier
                    .clip(GtaShapes.SmallCardShape)
                    .background(Brush.horizontalGradient(listOf(Color(0xE6FF003C), Color(0xCCFF003C))))
                    .neonBorder(
                        brush = Brush.linearGradient(listOf(Color.White, Color(0x80FFFFFF))),
                        cornerRadius = 8.dp,
                        borderWidth = 1.dp,
                        glowRadius = 8.dp
                    )
                    .padding(horizontal = 24.dp, vertical = 12.dp)
            ) {
                Text(
                    text = errorMessage ?: "",
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp
                )
            }
        }"""

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed AnimatedVisibility scope")
else:
    print("Target not found!")
