import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

side_panel = """        EpgSidePanel(
            visible = isEpgPanelVisible,
            epgList = epgList,
            isLoading = isEpgLoading,
            onClose = { playerViewModel.hideEpgPanel() },
            onPlayCatchup = { program -> playerViewModel.playCatchup(program) }
        )"""
        
# Remove the wrongfully placed side_panel
content = content.replace(side_panel, "")

# The root Box of HomeScreen ends where?
# HomeScreen function signature:
# @Composable
# fun HomeScreen(
# ...
# ) {
# ...
#    Box(...) {
#        ...
#    } // <- This is the closing brace of root Box
# } // <- This is the closing brace of HomeScreen function

# CategoryChip is the last function in the file.
# We need to insert EpgSidePanel inside the root Box of HomeScreen.
# Let's find: "                SettingsDialog("
# which is inside the root Box.

# In HomeScreen.kt, SettingsDialog and SearchOverlayDialog are usually at the end of the root Box.
# Let's find "        }" right after "            }" of SearchOverlayDialog.

content = content.replace("SettingsDialog(", side_panel + "\n\n        SettingsDialog(")

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed HomeScreen.kt")
