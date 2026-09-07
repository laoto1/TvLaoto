with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Add catchupTokenCache
content = content.replace(
'''    private val tokenCache = mutableMapOf<String, String>()
    private val epgCache = mutableMapOf<String, List<EpgProgram>>()''',
'''    private val tokenCache = mutableMapOf<String, String>()
    private val catchupTokenCache = mutableMapOf<String, String>()
    private val epgCache = mutableMapOf<String, List<EpgProgram>>()''')

# In playChannel, clear currentCatchupProgram
# We don't need to clear the cache, just keep it.

# In playCatchup
target_playcatchup = '''    fun playCatchup(program: EpgProgram) {
        val channel = _currentChannel.value ?: return
        if (!channel.isSup) return
        
        hideEpgPanel()
        _currentCatchupProgram.value = program
        
        viewModelScope.launch {
            _isDecryptingLink.value = true
            player.stop()
            val replayUrl = sniffer.sniffCatchup(channel.streamUrl, program.index)
            _isDecryptingLink.value = false
            
            if (replayUrl != null) {
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
                _errorMessage.value = "Không thể lấy liên kết xem lại."
                _isBuffering.value = false
            }
        }
    }'''

replacement_playcatchup = '''    fun playCatchup(program: EpgProgram) {
        val channel = _currentChannel.value ?: return
        if (!channel.isSup) return
        
        hideEpgPanel()
        _currentCatchupProgram.value = program
        
        val cacheKey = "${channel.id}_${program.index}_${program.time}"
        val cachedUrl = catchupTokenCache[cacheKey]
        
        if (cachedUrl != null) {
            _isBuffering.value = true
            try {
                val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = cachedUrl))
                player.setMediaSource(mediaSource)
                player.prepare()
                player.playWhenReady = true
            } catch (e: Exception) {
                _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng xem lại"
                _isBuffering.value = false
            }
            return
        }
        
        viewModelScope.launch {
            _isDecryptingLink.value = true
            player.stop()
            val replayUrl = sniffer.sniffCatchup(channel.streamUrl, program.index)
            _isDecryptingLink.value = false
            
            if (replayUrl != null) {
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
                _errorMessage.value = "Không thể lấy liên kết xem lại."
                _isBuffering.value = false
            }
        }
    }'''

content = content.replace(target_playcatchup, replacement_playcatchup)

# Also handle ExoPlayer error to invalidate cache
target_error = '''        val isHttpError = error.errorCode == PlaybackException.ERROR_CODE_IO_BAD_HTTP_STATUS || error.cause is HttpDataSource.HttpDataSourceException
        if (currentCh?.isSup == true && isHttpError) {
            tokenCache.remove(currentCh.streamUrl)
            _errorMessage.value = "Token hết hạn. Đang lấy lại luồng mới..."
            playChannel(currentCh) // Sniff lại
            return
        }'''

replacement_error = '''        val isHttpError = error.errorCode == PlaybackException.ERROR_CODE_IO_BAD_HTTP_STATUS || error.cause is HttpDataSource.HttpDataSourceException
        if (currentCh?.isSup == true && isHttpError) {
            val catchupProg = _currentCatchupProgram.value
            if (catchupProg != null) {
                val cacheKey = "${currentCh.id}_${catchupProg.index}_${catchupProg.time}"
                catchupTokenCache.remove(cacheKey)
                _errorMessage.value = "Token xem lại hết hạn. Đang tải lại..."
                playCatchup(catchupProg)
                return
            } else {
                tokenCache.remove(currentCh.streamUrl)
                _errorMessage.value = "Token hết hạn. Đang lấy lại luồng mới..."
                playChannel(currentCh) // Sniff lại
                return
            }
        }'''

content = content.replace(target_error, replacement_error)

with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated PlayerViewModel caching")
