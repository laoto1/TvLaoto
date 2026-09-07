with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

target = """            if (replayUrl != null) {
                catchupTokenCache[cacheKey] = replayUrl
                try {
                    val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = replayUrl))
                    player.setMediaSource(mediaSource)
                    player.prepare()
                    player.playWhenReady = true
                } catch (e: Exception) {
                    _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng xem lại"
                    _isBuffering.value = false
                }
            } else {
                _errorMessage.value = "Chương trình này hiện không khả dụng hoặc không tồn tại để xem lại!"
                _isBuffering.value = false
            }"""

replacement = """            if (replayUrl != null) {
                catchupTokenCache[cacheKey] = replayUrl
                try {
                    val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = replayUrl))
                    player.setMediaSource(mediaSource)
                    player.prepare()
                    player.playWhenReady = true
                } catch (e: Exception) {
                    _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng xem lại"
                    _isBuffering.value = false
                }
            } else {
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
                }
                _errorMessage.value = "Chương trình này hiện không khả dụng hoặc không tồn tại để xem lại!"
                _isBuffering.value = false
            }"""

if "Chương trình này hiện không khả dụng hoặc không tồn tại để xem lại!" in content:
    import re
    # We can just replace the else block using regex or string replace.
    # But wait, the exact indentation might differ.
    pass

