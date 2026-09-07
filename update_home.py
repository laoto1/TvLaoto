import re
with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# find the place where we compute liveProgram
content = content.replace('''    val epgList by playerViewModel.epgList.collectAsState()''',
'''    val epgList by playerViewModel.epgList.collectAsState()
    val currentCatchupProgram by playerViewModel.currentCatchupProgram.collectAsState()
    
    val liveProgram = remember(epgList) {
        if (epgList.isEmpty()) null
        else {
            val currentTime = java.util.Calendar.getInstance()
            val currentHour = currentTime.get(java.util.Calendar.HOUR_OF_DAY)
            val currentMinute = currentTime.get(java.util.Calendar.MINUTE)
            val currentTotalMinutes = currentHour * 60 + currentMinute
            var live: com.tvlaoto.data.model.EpgProgram? = null
            for (p in epgList) {
                val timeParts = p.time.split(":")
                if (timeParts.size == 2) {
                    val h = timeParts[0].toIntOrNull() ?: 0
                    val m = timeParts[1].toIntOrNull() ?: 0
                    val totalMins = h * 60 + m
                    if (totalMins <= currentTotalMinutes) {
                        live = p
                    } else break
                }
            }
            live
        }
    }''')

content = content.replace('''                        ProgramInfoPanel(
                              channel = currentPlayingChannel,
                              onReplayClick = {
                                  playerViewModel.showEpgPanel()
                              },
                              onFavoriteClick = { currentPlayingChannel?.let { repository.toggleFavorite(it.id) } },

                        )''',
'''                        ProgramInfoPanel(
                              channel = currentPlayingChannel,
                              currentCatchupProgram = currentCatchupProgram,
                              liveProgram = liveProgram,
                              onReplayClick = {
                                  playerViewModel.showEpgPanel()
                              },
                              onFavoriteClick = { currentPlayingChannel?.let { repository.toggleFavorite(it.id) } },
                        )''')

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HomeScreen.kt")
