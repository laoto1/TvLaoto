import re

# Update PlayerScreen.kt
with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'r', encoding='utf-8') as f:
    ps_content = f.read()

if "val isDecryptingLink by viewModel.isDecryptingLink.collectAsState()" not in ps_content:
    ps_content = ps_content.replace(
        "val isBuffering by viewModel.isBuffering.collectAsState()",
        "val isBuffering by viewModel.isBuffering.collectAsState()\n    val isDecryptingLink by viewModel.isDecryptingLink.collectAsState()"
    )

new_buffering_ps = """        // Buffering Indicator
        if (isDecryptingLink) {
            Box(
                modifier = Modifier.fillMaxSize().background(Color(0x99000000)),
                contentAlignment = Alignment.Center
            ) {
                NeonLoadingIndicator(text = "Đang bẻ khóa liên kết...")
            }
        } else if (isBuffering && errorMessage == null) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                NeonLoadingIndicator(text = currentChannel?.name ?: stringResource(R.string.loading_channels))
            }
        }"""

ps_content = re.sub(r'        // Buffering Indicator\n        if \(isBuffering && errorMessage == null\) \{.*?        \}', new_buffering_ps, ps_content, flags=re.DOTALL)

with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'w', encoding='utf-8') as f:
    f.write(ps_content)


# Update VideoPlayerPanel.kt
with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    vp_content = f.read()

if "isDecryptingLink: Boolean," not in vp_content:
    vp_content = vp_content.replace(
        "isBuffering: Boolean,",
        "isBuffering: Boolean,\n    isDecryptingLink: Boolean = false,"
    )

new_buffering_vp = """        // Loading Spinner while buffering
        if (isDecryptingLink) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color(0x99000000)),
                contentAlignment = Alignment.Center
            ) {
                NeonLoadingIndicator(text = "Đang bẻ khóa liên kết...")
            }
        } else if (isBuffering) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color(0x66000000)),
                contentAlignment = Alignment.Center
            ) {
                NeonLoadingIndicator(text = channel?.name)
            }
        }"""

vp_content = re.sub(r'        // Loading Spinner while buffering\n        if \(isBuffering\) \{.*?        \}', new_buffering_vp, vp_content, flags=re.DOTALL)

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
    f.write(vp_content)

print("Updated UI files")
