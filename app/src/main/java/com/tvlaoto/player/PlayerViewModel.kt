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
    private val epgCache = mutableMapOf<String, List<EpgProgram>>()

    private val _currentCatchupProgram = MutableStateFlow<EpgProgram?>(null)
    val currentCatchupProgram: StateFlow<EpgProgram?> = _currentCatchupProgram.asStateFlow()

    private var tokenRetryCount = 0

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
        tokenRetryCount = 0
        _isBuffering.value = true
        _epgList.value = emptyList()
        showOverlayTemporarily()

        com.tvlaoto.util.AppLogger.i("Player", "Playing: ${channel.name} (${channel.id})")
        com.tvlaoto.util.AppLogger.d("Player", "Stream URL: ${channel.streamUrl}")

        repository.saveLastPlayedChannel(channel.id)
        
        // Fetch EPG for channel
        fetchEpg()

        // For TV360 channels: fetch stream URL on-demand from TV360 API
        val tv360Key = when {
            channel.streamUrl.contains("tv360.vn") -> {
                val chIdMatch = Regex("""[?&]ch=(\d+)""").find(channel.streamUrl)
                if (chIdMatch != null) {
                    chIdMatch.groupValues[1]
                } else {
                    val match = Regex("""thvl(\d)""", RegexOption.IGNORE_CASE).find(channel.name)
                    match?.let { "thvl${it.groupValues[1]}" }
                }
            }
            else -> null
        }
        if (tv360Key != null) {
            viewModelScope.launch {
                try {
                    com.tvlaoto.util.AppLogger.i("Player", "Fetching TV360 URL for $tv360Key (${channel.name})...")
                    val tv360Url = repository.fetchTv360Url(tv360Key)
                    if (tv360Url != null) {
                        com.tvlaoto.util.AppLogger.i("Player", "TV360 resolved: ${tv360Url.take(80)}...")
                        val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = tv360Url))
                        player.setMediaSource(mediaSource)
                        player.prepare()
                        player.playWhenReady = true
                    } else {
                        if (channel.resolvedUrl != null) {
                            com.tvlaoto.util.AppLogger.i("Player", "TV360 API failed, using pre-resolved URL: ${channel.resolvedUrl.take(60)}...")
                            val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = channel.resolvedUrl))
                            player.setMediaSource(mediaSource)
                            player.prepare()
                            player.playWhenReady = true
                        } else {
                            com.tvlaoto.util.AppLogger.w("Player", "TV360 URL resolution failed for $tv360Key (${channel.name})")
                            _errorMessage.value = "Kênh này yêu cầu tài khoản TV360 hoặc tạm ngừng phát"
                            _isBuffering.value = false
                        }
                    }
                } catch (e: Exception) {
                    com.tvlaoto.util.AppLogger.e("Player", "TV360 play error", e)
                    _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng TV360"
                    _isBuffering.value = false
                }
            }
            return
        }

        // For VTVGo channels without pre-resolved URL: fetch stream via API
        if (channel.streamUrl.contains("vtvgo.vn") && channel.resolvedUrl == null) {
            viewModelScope.launch {
                try {
                    // Extract channel ID from URL: antv-1,89.html -> 89, vtv1-1.html -> 1
                    val channelId = Regex("""(?:-(\d+)\.html|,(\d+)\.html)""").find(channel.streamUrl)?.let {
                        it.groupValues[1].ifEmpty { it.groupValues[2] }
                    }
                    if (channelId == null) {
                        com.tvlaoto.util.AppLogger.w("Player", "Cannot extract channel ID from: ${channel.streamUrl}")
                        _errorMessage.value = "Không thể xác định kênh."
                        _isBuffering.value = false
                        return@launch
                    }
                    com.tvlaoto.util.AppLogger.i("Player", "Fetching VTVGo live URL for channel $channelId (${channel.name})...")
                    val liveUrls = repository.fetchVtvgoLiveUrls(channelId)
                    if (liveUrls.isEmpty()) {
                        com.tvlaoto.util.AppLogger.w("Player", "VTVGo API returned no stream for channel $channelId")
                        _errorMessage.value = "Không thể tải luồng phát sóng."
                        _isBuffering.value = false
                        return@launch
                    }

                    // Probe URLs to find one that actually works (some CDNs return 404)
                    var workingUrl: String? = null
                    for (url in liveUrls) {
                        try {
                            val probeReq = okhttp3.Request.Builder()
                                .url(url)
                                .head()
                                .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                                .build()
                            val probeResp = repository.probeUrl(probeReq)
                            com.tvlaoto.util.AppLogger.d("Player", "Probe ${url.take(60)}: ${probeResp}")
                            if (probeResp in 200..299) {
                                workingUrl = url
                                break
                            }
                        } catch (e: Exception) {
                            com.tvlaoto.util.AppLogger.d("Player", "Probe failed ${url.take(60)}: ${e.message}")
                        }
                    }
                    // Fallback to first URL if all probes fail (some CDNs block HEAD but allow GET)
                    val liveUrl = workingUrl ?: liveUrls.first()

                    com.tvlaoto.util.AppLogger.i("Player", "VTVGo resolved: ${liveUrl.take(80)}...")
                    val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = liveUrl))
                    player.setMediaSource(mediaSource)
                    player.prepare()
                    player.playWhenReady = true
                } catch (e: Exception) {
                    com.tvlaoto.util.AppLogger.e("Player", "VTVGo play error", e)
                    _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng VTVGo"
                    _isBuffering.value = false
                }
            }
            return
        }

        // Determine the actual URL to play (pre-resolved channels)
        val playUrl = channel.resolvedUrl ?: channel.streamUrl

        com.tvlaoto.util.AppLogger.d("Player", "Play URL: ${playUrl.take(80)}...")

        try {
            val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = playUrl))
            player.setMediaSource(mediaSource)
            player.prepare()
            player.playWhenReady = true
        } catch (e: Exception) {
            com.tvlaoto.util.AppLogger.e("Player", "Play error", e)
            _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng"
            _isBuffering.value = false
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
        if (currentCh?.resolvedUrl != null && isHttpError) {
            val catchupProg = _currentCatchupProgram.value
            if (catchupProg != null) {
                _errorMessage.value = "Token xem lại hết hạn."
                _currentCatchupProgram.value = null
                _isBuffering.value = false
                return
            } else if (tokenRetryCount < 1) {
                // Re-fetch resolved playlist for fresh tokens (max 1 retry)
                tokenRetryCount++
                _errorMessage.value = "Token hết hạn. Đang tải lại..."
                viewModelScope.launch {
                    repository.refreshResolvedUrls()
                    val freshChannel = repository.getChannelById(currentCh.id)
                    if (freshChannel != null && freshChannel.resolvedUrl != currentCh.resolvedUrl) {
                        playChannel(freshChannel)
                    } else {
                        // Token unchanged — stop retrying
                        _isBuffering.value = false
                        _errorMessage.value = "Không thể phát kênh này. Token hết hạn."
                    }
                }
                return
            } else {
                _isBuffering.value = false
                _errorMessage.value = "Không thể phát kênh này. Token hết hạn."
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
        
        if (epgCache.containsKey(channel.id)) {
            _epgList.value = epgCache[channel.id]!!
            return
        }
        
        viewModelScope.launch {
            _isEpgLoading.value = true
            // For VTV channels: fetch live EPG with slotId directly from VTVGo API v21
            var list: List<EpgProgram> = emptyList()
            if (channel.streamUrl.contains("vtvgo.vn")) {
                list = repository.fetchEpgFromApi(channel.streamUrl)
            } else if (channel.streamUrl.contains("tv360.vn")) {
                // TV360 channels: fetch live EPG directly from TV360 API
                val chIdMatch = Regex("""[?&]ch=(\d+)""").find(channel.streamUrl)
                val tv360Key = if (chIdMatch != null) {
                    chIdMatch.groupValues[1]
                } else {
                    val match = Regex("""thvl(\d)""", RegexOption.IGNORE_CASE).find(channel.name)
                    match?.let { "thvl${it.groupValues[1]}" }
                }
                if (tv360Key != null) {
                    list = repository.fetchTv360Epg(tv360Key)
                }
            }
            if (list.isEmpty()) {
                com.tvlaoto.util.AppLogger.d("Player", "Direct EPG empty, trying server EPG for ${channel.name}...")
                list = repository.fetchServerEpg(channel.name)
            }
            if (list.isNotEmpty()) {
                epgCache[channel.id] = list
            }
            _epgList.value = list
            _isEpgLoading.value = false
        }
    }

    fun playCatchup(program: EpgProgram) {
        val channel = _currentChannel.value ?: return
        
        hideEpgPanel()
        _currentCatchupProgram.value = program
        _isBuffering.value = true

        viewModelScope.launch {
            // If program already has catchupUrl pre-resolved, use it
            var catchupUrl = program.catchupUrl

            // 1. TV360 channel
            if (catchupUrl == null && channel.streamUrl.contains("tv360.vn")) {
                val chIdMatch = Regex("""[?&]ch=(\d+)""").find(channel.streamUrl)
                val tv360Key = if (chIdMatch != null) {
                    chIdMatch.groupValues[1]
                } else {
                    val match = Regex("""thvl(\d)""", RegexOption.IGNORE_CASE).find(channel.name)
                    match?.let { "thvl${it.groupValues[1]}" }
                }
                if (tv360Key != null) {
                    com.tvlaoto.util.AppLogger.i("Player", "Fetching TV360 catchup for $tv360Key: ${program.title}")
                    catchupUrl = repository.fetchTv360CatchupUrl(tv360Key, program)
                }
            }
            // 2. VTV channel from VTVGo
            else if (catchupUrl == null && channel.streamUrl.contains("vtvgo.vn")) {
                // Extract VTVGo channel ID from stream URL
                val channelId = Regex("""(?:-(\d+)\.html|,(\d+)\.html)""").find(channel.streamUrl)?.let {
                    it.groupValues[1].ifEmpty { it.groupValues[2] }
                }

                if (channelId == null || program.slotId == null || !ChannelRepository.VTV_CATCHUP_CHANNEL_IDS.contains(channelId)) {
                    _errorMessage.value = "Kênh này chưa hỗ trợ xem lại."
                    _isBuffering.value = false
                    _currentCatchupProgram.value = null
                    return@launch
                }

                com.tvlaoto.util.AppLogger.i("Player", "Fetching catchup: ${program.title} (slotId=${program.slotId})")

                // Fetch catchup URL on-demand from VTVGo API
                catchupUrl = repository.fetchCatchupUrl(channelId, program)
            }

            if (catchupUrl != null) {
                com.tvlaoto.util.AppLogger.i("Player", "Playing catchup: ${catchupUrl.take(80)}...")
                try {
                    val mediaSource = TvPlayerFactory.createMediaSource(channel.copy(streamUrl = catchupUrl))
                    player.setMediaSource(mediaSource)
                    player.prepare()
                    player.playWhenReady = true
                } catch (e: Exception) {
                    com.tvlaoto.util.AppLogger.e("Player", "Catchup play error", e)
                    _errorMessage.value = e.localizedMessage ?: "Lỗi phát luồng xem lại"
                    _isBuffering.value = false
                }
            } else {
                _errorMessage.value = "Không thể tải link xem lại."
                _isBuffering.value = false
                _currentCatchupProgram.value = null
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        player.removeListener(this)
        player.release()
    }
}

