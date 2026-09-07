import re

with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Add tokenCache
if "private val tokenCache = mutableMapOf<String, String>()" not in content:
    content = content.replace("private var allChannels: List<IptvChannel> = emptyList()", "private var allChannels: List<IptvChannel> = emptyList()\n    private val tokenCache = mutableMapOf<String, String>()")

# Replace playChannel
new_playChannel = """    fun playChannel(channel: IptvChannel) {
        _currentChannel.value = channel
        _errorMessage.value = null
        _isBuffering.value = true
        showOverlayTemporarily()

        repository.saveLastPlayedChannel(channel.id)

        if (channel.isSup) {
            val cachedUrl = tokenCache[channel.streamUrl]
            if (cachedUrl != null) {
                try {
                    val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = cachedUrl))
                    player.setMediaSource(mediaSource)
                    player.prepare()
                    player.playWhenReady = true
                } catch (e: Exception) {
                    _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng"
                    _isBuffering.value = false
                }
            } else {
                viewModelScope.launch {
                    _isDecryptingLink.value = true
                    player.stop() // Dừng player chờ giải mã
                    val realUrl = sniffer.sniff(channel.streamUrl)
                    _isDecryptingLink.value = false
                    
                    if (realUrl != null) {
                        tokenCache[channel.streamUrl] = realUrl // Lưu vào cache
                        try {
                            val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = realUrl))
                            player.setMediaSource(mediaSource)
                            player.prepare()
                            player.playWhenReady = true
                        } catch (e: Exception) {
                            _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng bị khóa"
                            _isBuffering.value = false
                        }
                    } else {
                        _errorMessage.value = "Không thể bẻ khóa liên kết."
                        _isBuffering.value = false
                    }
                }
            }
        } else {
            try {
                val mediaSource = TvPlayerFactory.createMediaSource(channel)
                player.setMediaSource(mediaSource)
                player.prepare()
                player.playWhenReady = true
            } catch (e: Exception) {
                _errorMessage.value = e.localizedMessage ?: "Failed to play stream"
                _isBuffering.value = false
            }
        }
    }"""

content = re.sub(r'    fun playChannel\(channel: IptvChannel\) \{.*?\n    \}', new_playChannel, content, flags=re.DOTALL)

# Replace onPlayerError
new_onPlayerError = """    override fun onPlayerError(error: PlaybackException) {
        val currentCh = _currentChannel.value
        val isHttpError = error.errorCode == PlaybackException.ERROR_CODE_IO_BAD_HTTP_STATUS || error.cause is HttpDataSource.HttpDataSourceException
        if (currentCh?.isSup == true && isHttpError) {
            tokenCache.remove(currentCh.streamUrl)
            _errorMessage.value = "Token hết hạn. Đang lấy lại luồng mới..."
            playChannel(currentCh) // Sniff lại
            return
        }
        
        _isBuffering.value = false
        _errorMessage.value = error.message ?: "Playback error: code ${error.errorCode}"
    }"""

content = re.sub(r'    override fun onPlayerError\(error: PlaybackException\) \{.*?\n    \}', new_onPlayerError, content, flags=re.DOTALL)

with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated PlayerViewModel.kt with cache")
