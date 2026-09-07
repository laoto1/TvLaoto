with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Add imports
content = content.replace('import androidx.compose.ui.text.font.FontWeight',
'''import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import kotlinx.coroutines.delay
import androidx.compose.ui.text.font.FontWeight''')

# Add errorMessage state and effect
content = content.replace('''    val isDecryptingLink by playerViewModel.isDecryptingLink.collectAsState()''',
'''    val isDecryptingLink by playerViewModel.isDecryptingLink.collectAsState()
    val errorMessage by playerViewModel.errorMessage.collectAsState()

    androidx.compose.runtime.LaunchedEffect(errorMessage) {
        if (errorMessage != null) {
            delay(4000)
            playerViewModel.clearError()
        }
    }''')


# Add the Toast Box UI inside the main Box overlay
toast_ui = '''
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
'''

# Find the end of BottomStatusBar
content = content.replace('''            // Bottom Status Bar
            BottomStatusBar(
                currentChannelName = currentPlayingChannel?.name
            )
        }''',
'''            // Bottom Status Bar
            BottomStatusBar(
                currentChannelName = currentPlayingChannel?.name
            )
''' + toast_ui + '''        }''')


with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HomeScreen.kt")
