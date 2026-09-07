with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

import re

target_regex = r"\} else \{\s*_errorMessage\.value = \"Chương trình này hiện không khả dụng hoặc không tồn tại để xem lại\!\"\s*_isBuffering\.value = false\s*\}"

replacement = """} else {
                // Restore Live playback
                _currentCatchupProgram.value = null
                val cachedUrl = tokenCache[channel.streamUrl]
                if (cachedUrl != null) {
                    try {
                        val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = cachedUrl))
                        player.setMediaSource(mediaSource)
                        player.prepare()
                        player.playWhenReady = true
                    } catch (e: Exception) {
                        // ignore
                    }
                } else {
                    // Fallback to re-sniffing if not in cache
                    viewModelScope.launch {
                        val realUrl = sniffer.sniff(channel.streamUrl)
                        if (realUrl != null) {
                            tokenCache[channel.streamUrl] = realUrl
                            val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = realUrl))
                            player.setMediaSource(mediaSource)
                            player.prepare()
                            player.playWhenReady = true
                        }
                    }
                }
                
                _errorMessage.value = "Chương trình này hiện không khả dụng hoặc không tồn tại để xem lại!"
                _isBuffering.value = false
            }"""

if re.search(target_regex, content):
    content = re.sub(target_regex, replacement, content)
    with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced the else block!")
else:
    print("Regex not found!")
