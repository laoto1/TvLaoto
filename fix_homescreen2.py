import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove the wrongly placed EpgSidePanel block exactly as it is now
bad_block = """                    EpgSidePanel(
            visible = isEpgPanelVisible,
            epgList = epgList,
            isLoading = isEpgLoading,
            onClose = { playerViewModel.hideEpgPanel() },
            onPlayCatchup = { program -> playerViewModel.playCatchup(program) }
        )"""
content = content.replace(bad_block, "")

# We also know we added an extra "}" at the end of the file that broke it. 
# We need to remove the trailing "}" if there is one extra. Let's just strip trailing whitespace and remove the last '}'
content = content.rstrip()
if content.endswith('}'):
    content = content[:-1].rstrip()

# Now the brace count should be Open: 83, Close: 81 (because we removed the last one, and before it was 83/83).
# Wait, let's just insert EpgSidePanel correctly.
# The correct place is right before the end of the HomeScreen function.
# How to find the end of the HomeScreen function?
# It ends right before "@Composable\nfun ChannelFilterPill"
good_block = """        EpgSidePanel(
            visible = isEpgPanelVisible,
            epgList = epgList,
            isLoading = isEpgLoading,
            onClose = { playerViewModel.hideEpgPanel() },
            onPlayCatchup = { program -> playerViewModel.playCatchup(program) }
        )
    }
}"""
content = content.replace("    }\n}\n\n@Composable\nfun ChannelFilterPill", good_block + "\n\n@Composable\nfun ChannelFilterPill")

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed HomeScreen layout and braces")
