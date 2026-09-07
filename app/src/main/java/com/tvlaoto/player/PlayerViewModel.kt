package com.tvlaoto.player

import android.app.Application
import androidx.annotation.OptIn
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import androidx.media3.common.PlaybackException
import androidx.media3.common.Player
import androidx.media3.common.VideoSize
import androidx.media3.common.util.UnstableApi
import androidx.media3.exoplayer.ExoPlayer
import com.tvlaoto.data.model.IptvChannel
import com.tvlaoto.data.model.EpgProgram
import com.tvlaoto.data.repository.ChannelRepository
import com.tvlaoto.network.StreamSniffer
import androidx.media3.datasource.HttpDataSource
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

@OptIn(UnstableApi::class)
class PlayerViewModel(
    application: Application,
    private val repository: ChannelRepository
) : AndroidViewModel(application), Player.Listener {

    val player: ExoPlayer = TvPlayerFactory.createPlayer(application).apply {
        addListener(this@PlayerViewModel)
    }

    private val _currentChannel = MutableStateFlow<IptvChannel?>(null)
    val currentChannel: StateFlow<IptvChannel?> = _currentChannel.asStateFlow()

    private val _isPlaying = MutableStateFlow(false)
    val isPlaying: StateFlow<Boolean> = _isPlaying.asStateFlow()

    private val _isDecryptingLink = MutableStateFlow(false)
    val isDecryptingLink: StateFlow<Boolean> = _isDecryptingLink.asStateFlow()

    private val sniffer by lazy { StreamSniffer(application) }

    private val _isBuffering = MutableStateFlow(true)
    val isBuffering: StateFlow<Boolean> = _isBuffering.asStateFlow()

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage: StateFlow<String?> = _errorMessage.asStateFlow()

    fun clearError() {
        _errorMessage.value = null
    }

    private val _showOverlay = MutableStateFlow(true)
    val showOverlay: StateFlow<Boolean> = _showOverlay.asStateFlow()

    private val _isEpgPanelVisible = MutableStateFlow(false)
    val isEpgPanelVisible: StateFlow<Boolean> = _isEpgPanelVisible.asStateFlow()

    private val _epgList = MutableStateFlow<List<EpgProgram>>(emptyList())
    val epgList: StateFlow<List<EpgProgram>> = _epgList.asStateFlow()

    private val _isEpgLoading = MutableStateFlow(false)
    val isEpgLoading: StateFlow<Boolean> = _isEpgLoading.asStateFlow()

    private val _videoResolution = MutableStateFlow("HD 1080p")
    val videoResolution: StateFlow<String> = _videoResolution.asStateFlow()

    private var overlayHideJob: Job? = null
    private var allChannels: List<IptvChannel> = emptyList()
    private val tokenCache = mutableMapOf<String, String>()
    private val catchupTokenCache = mutableMapOf<String, String>()
    private val epgCache = mutableMapOf<String, List<EpgProgram>>()

    private val _currentCatchupProgram = MutableStateFlow<EpgProgram?>(null)
    val currentCatchupProgram: StateFlow<EpgProgram?> = _currentCatchupProgram.asStateFlow()

    init {
        viewModelScope.launch {
                        repository.playlist.collect { playlist ->
                allChannels = playlist?.categories?.flatMap { it.channels } ?: emptyList()
                val current = _currentChannel.value
                if (current != null) {
                    val updated = allChannels.find { it.id == current.id }
                    if (updated != null && updated.isFavorite != current.isFavorite) {
                        _currentChannel.value = updated
                    }
                }
            }
        }
    }

    fun playChannel(channel: IptvChannel) {
        _currentCatchupProgram.value = null
        _currentChannel.value = channel
        _errorMessage.value = null
        _isBuffering.value = true
        _epgList.value = emptyList()
        showOverlayTemporarily()

        com.tvlaoto.util.AppLogger.i("Player", "Playing: ${channel.name} (${channel.id}) isSup=${channel.isSup}")
        com.tvlaoto.util.AppLogger.d("Player", "Stream URL: ${channel.streamUrl}")

        repository.saveLastPlayedChannel(channel.id)
        
        if (channel.isSup) {
            fetchEpg()
        }

        if (channel.isSup) {
            // Priority 1: Pre-resolved URL from server-side resolver
            val resolvedUrl = channel.resolvedUrl
            val resolvedAge = if (channel.resolvedAt > 0) System.currentTimeMillis() / 1000 - channel.resolvedAt else Long.MAX_VALUE

            if (resolvedUrl != null && resolvedAge < 3600) {
                // Resolved URL still fresh (< 1 hour old)
                com.tvlaoto.util.AppLogger.d("Player", "Using pre-resolved URL (age=${resolvedAge}s)")
                try {
                    val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = resolvedUrl))
                    player.setMediaSource(mediaSource)
                    player.prepare()
                    player.playWhenReady = true
                } catch (e: Exception) {
                    com.tvlaoto.util.AppLogger.e("Player", "Resolved play error, falling back to sniff", e)
                    sniffAndPlay(channel)
                }
            } else {
                // Priority 2: Cached token from previous sniff
                val cachedUrl = tokenCache[channel.streamUrl]
                if (cachedUrl != null) {
                    com.tvlaoto.util.AppLogger.d("Player", "Using cached token URL")
                    try {
                        val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = cachedUrl))
                        player.setMediaSource(mediaSource)
                        player.prepare()
                        player.playWhenReady = true
                    } catch (e: Exception) {
                        com.tvlaoto.util.AppLogger.e("Player", "Cached play error", e)
                        _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng"
                        _isBuffering.value = false
                    }
                } else {
                    // Priority 3: Sniff via WebView (fallback)
                    sniffAndPlay(channel)
                }
            }
        } else {
            try {
                val mediaSource = TvPlayerFactory.createMediaSource(channel)
                player.setMediaSource(mediaSource)
                player.prepare()
                player.playWhenReady = true
            } catch (e: Exception) {
                com.tvlaoto.util.AppLogger.e("Player", "Direct play error", e)
                _errorMessage.value = e.localizedMessage ?: "Failed to play stream"
                _isBuffering.value = false
            }
        }
    }

    private fun sniffAndPlay(channel: IptvChannel) {
        viewModelScope.launch {
            _isDecryptingLink.value = true
            player.stop()
            com.tvlaoto.util.AppLogger.i("Player", "Sniffing stream for: ${channel.name}")
            val realUrl = sniffer.sniff(channel.streamUrl)
            _isDecryptingLink.value = false
            
            if (realUrl != null) {
                com.tvlaoto.util.AppLogger.i("Player", "Sniff OK: ${realUrl.take(80)}...")
                tokenCache[channel.streamUrl] = realUrl
                try {
                    val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = realUrl))
                    player.setMediaSource(mediaSource)
                    player.prepare()
                    player.playWhenReady = true
                } catch (e: Exception) {
                    com.tvlaoto.util.AppLogger.e("Player", "Play after sniff error", e)
                    _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng bị khóa"
                    _isBuffering.value = false
                }
            } else {
                com.tvlaoto.util.AppLogger.e("Player", "Sniff FAILED for: ${channel.name}")
                _errorMessage.value = "Không thể bẻ khóa liên kết."
                _isBuffering.value = false
            }
        }
    }

    fun playChannelById(channelId: String) {
        if (_currentChannel.value?.id == channelId && _errorMessage.value == null) {
            return // Đã đang phát kênh này (live hoặc catchup) và không bị lỗi, không cần reset
        }
        val channel = repository.findChannelById(channelId) ?: allChannels.find { it.id == channelId }
        if (channel != null) {
            playChannel(channel)
        }
    }

    fun playNextChannel() {
        if (allChannels.isEmpty()) return
        val current = _currentChannel.value ?: return
        val currentIndex = allChannels.indexOfFirst { it.id == current.id }
        val nextIndex = if (currentIndex != -1 && currentIndex < allChannels.size - 1) {
            currentIndex + 1
        } else {
            0
        }
        playChannel(allChannels[nextIndex])
    }

    fun playPreviousChannel() {
        if (allChannels.isEmpty()) return
        val current = _currentChannel.value ?: return
        val currentIndex = allChannels.indexOfFirst { it.id == current.id }
        val prevIndex = if (currentIndex > 0) {
            currentIndex - 1
        } else {
            allChannels.size - 1
        }
        playChannel(allChannels[prevIndex])
    }

    fun toggleOverlay() {
        if (_showOverlay.value) {
            _showOverlay.value = false
            overlayHideJob?.cancel()
        } else {
            showOverlayTemporarily()
        }
    }

    fun showOverlayTemporarily(durationMs: Long = 4000) {
        _showOverlay.value = true
        overlayHideJob?.cancel()
        overlayHideJob = viewModelScope.launch {
            delay(durationMs)
            _showOverlay.value = false
        }
    }

    fun retryCurrentChannel() {
        val current = _currentChannel.value ?: return
        playChannel(current)
    }

    override fun onPlaybackStateChanged(playbackState: Int) {
        val stateName = when(playbackState) {
            Player.STATE_BUFFERING -> "BUFFERING"
            Player.STATE_READY -> "READY"
            Player.STATE_ENDED -> "ENDED"
            Player.STATE_IDLE -> "IDLE"
            else -> "UNKNOWN($playbackState)"
        }
        com.tvlaoto.util.AppLogger.d("Player", "State: $stateName (channel=${_currentChannel.value?.name})")
        
        when (playbackState) {
            Player.STATE_BUFFERING -> {
                _isBuffering.value = true
                _errorMessage.value = null
            }
            Player.STATE_READY -> {
                _isBuffering.value = false
                _errorMessage.value = null
            }
            Player.STATE_ENDED -> {
                _isBuffering.value = false
            }
            Player.STATE_IDLE -> {}
        }
    }

    override fun onIsPlayingChanged(isPlaying: Boolean) {
        _isPlaying.value = isPlaying
        com.tvlaoto.util.AppLogger.d("Player", "isPlaying=$isPlaying")
    }

    override fun onPlayerError(error: PlaybackException) {
        com.tvlaoto.util.AppLogger.e("Player", "Player error: code=${error.errorCode} msg=${error.message}", error)
        val currentCh = _currentChannel.value
        val isHttpError = error.errorCode == PlaybackException.ERROR_CODE_IO_BAD_HTTP_STATUS || error.cause is HttpDataSource.HttpDataSourceException
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
        }
        
        _isBuffering.value = false
        _errorMessage.value = error.message ?: "Playback error: code ${error.errorCode}"
    }

    override fun onVideoSizeChanged(videoSize: VideoSize) {
        if (videoSize.width > 0 && videoSize.height > 0) {
            val quality = when {
                videoSize.height >= 2160 -> "4K UHD (${videoSize.width}x${videoSize.height})"
                videoSize.height >= 1080 -> "FULL HD (${videoSize.width}x${videoSize.height})"
                videoSize.height >= 720 -> "HD (${videoSize.width}x${videoSize.height})"
                else -> "SD (${videoSize.width}x${videoSize.height})"
            }
            _videoResolution.value = quality
        }
    }

    fun showEpgPanel() {
        _isEpgPanelVisible.value = true
        fetchEpg()
    }

    fun hideEpgPanel() {
        _isEpgPanelVisible.value = false
    }

    private fun fetchEpg() {
        val channel = _currentChannel.value ?: return
        if (!channel.isSup) return
        
        if (epgCache.containsKey(channel.id)) {
            _epgList.value = epgCache[channel.id]!!
            return
        }
        
        viewModelScope.launch {
            _isEpgLoading.value = true
            val list = sniffer.scrapeEpg(channel.streamUrl)
            if (list.isNotEmpty()) {
                epgCache[channel.id] = list
            }
            _epgList.value = list
            _isEpgLoading.value = false
        }
    }

    fun playCatchup(program: EpgProgram) {
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
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        player.removeListener(this)
        player.release()
        sniffer.destroyCachedWebView()
    }
}

