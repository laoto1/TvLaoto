import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

imports = """import com.tvlaoto.ui.components.EpgSidePanel"""
if "EpgSidePanel" not in content:
    content = content.replace("import com.tvlaoto.ui.components.TopNavigationBar", imports + "\nimport com.tvlaoto.ui.components.TopNavigationBar")

states = """    val isEpgPanelVisible by playerViewModel.isEpgPanelVisible.collectAsState()
    val epgList by playerViewModel.epgList.collectAsState()
    val isEpgLoading by playerViewModel.isEpgLoading.collectAsState()"""
content = content.replace("    val isBuffering by playerViewModel.isBuffering.collectAsState()", states + "\n    val isBuffering by playerViewModel.isBuffering.collectAsState()")

replay = """                        ProgramInfoPanel(
                              channel = currentPlayingChannel,
                              onReplayClick = {
                                  playerViewModel.showEpgPanel()
                              },
                              onFavoriteClick = { currentPlayingChannel?.let { repository.toggleFavorite(it.id) } },"""
content = re.sub(r'                        ProgramInfoPanel\(\s*channel = currentPlayingChannel,\s*onReplayClick = \{.*?\},\s*onFavoriteClick = \{ currentPlayingChannel\?\.let \{ repository\.toggleFavorite\(it\.id\) \} \},', replay, content, flags=re.DOTALL)

side_panel = """        EpgSidePanel(
            visible = isEpgPanelVisible,
            epgList = epgList,
            isLoading = isEpgLoading,
            onClose = { playerViewModel.hideEpgPanel() },
            onPlayCatchup = { program -> playerViewModel.playCatchup(program) }
        )"""

# Insert side panel just before the closing brace of HomeScreen Box
parts = content.rsplit('    }', 1)
content = parts[0] + "\n" + side_panel + "\n    }"

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HomeScreen.kt")
