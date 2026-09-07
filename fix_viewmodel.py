with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Imports
if "import com.tvlaoto.network.StreamSniffer" not in content:
    content = content.replace(
        "import com.tvlaoto.data.repository.ChannelRepository",
        "import com.tvlaoto.data.repository.ChannelRepository\nimport com.tvlaoto.network.StreamSniffer\nimport androidx.media3.datasource.HttpDataSource"
    )

# Adding sniffer and isDecryptingLink state
if "val isDecryptingLink: StateFlow<Boolean>" not in content:
    content = content.replace(
        "private val _isBuffering = MutableStateFlow(true)",
        "private val _isDecryptingLink = MutableStateFlow(false)\n    val isDecryptingLink: StateFlow<Boolean> = _isDecryptingLink.asStateFlow()\n\n    private val sniffer by lazy { StreamSniffer(application) }\n\n    private val _isBuffering = MutableStateFlow(true)"
    )

# Update playChannel
new_play_channel = """    fun playChannel(channel: IptvChannel) {
        _currentChannel.value = channel
        _errorMessage.value = null
        _isBuffering.value = true
        showOverlayTemporarily()

        repository.saveLastPlayedChannel(channel.id)

        if (channel.isSup) {
            viewModelScope.launch {
                _isDecryptingLink.value = true
                player.stop() // Dừng player chờ giải mã
                val realUrl = sniffer.sniff(channel.streamUrl)
                _isDecryptingLink.value = false
                
                if (realUrl != null) {
                    try {
                        val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = realUrl))
                        player.setMediaSource(mediaSource)
                        player.prepare()
                        player.playWhenReady = true
                    } catch (e: Exception) {
                        _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng bị bẻ khóa"
                        _isBuffering.value = false
                    }
                } else {
                    _errorMessage.value = "Không thể bẻ khóa liên kết."
                    _isBuffering.value = false
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

import re
content = re.sub(r'    fun playChannel\(channel: IptvChannel\) \{.*?\n    \}', new_play_channel, content, flags=re.DOTALL)

# Update onPlayerError for Auto-Refresh
new_on_error = """    override fun onPlayerError(error: PlaybackException) {
        val currentCh = _currentChannel.value
        if (currentCh?.isSup == true && error.cause is HttpDataSource.HttpDataSourceException) {
            // Lỗi 403 hoặc mạng liên quan tới Token -> Auto refresh
            _errorMessage.value = "Token hết hạn. Đang lấy lại luồng mới..."
            playChannel(currentCh) // Sniff lại
            return
        }
        
        _isBuffering.value = false
        _errorMessage.value = error.message ?: "Playback error: code ${error.errorCode}"
    }"""

content = re.sub(r'    override fun onPlayerError\(error: PlaybackException\) \{.*?\n    \}', new_on_error, content, flags=re.DOTALL)

with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated PlayerViewModel successfully")
