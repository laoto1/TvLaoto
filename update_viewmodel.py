import re

with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

imports = """import com.tvlaoto.data.model.EpgProgram"""
content = content.replace("import com.tvlaoto.data.model.IptvChannel", "import com.tvlaoto.data.model.IptvChannel\n" + imports)

states = """    private val _showOverlay = MutableStateFlow(true)
    val showOverlay: StateFlow<Boolean> = _showOverlay.asStateFlow()

    private val _isEpgPanelVisible = MutableStateFlow(false)
    val isEpgPanelVisible: StateFlow<Boolean> = _isEpgPanelVisible.asStateFlow()

    private val _epgList = MutableStateFlow<List<EpgProgram>>(emptyList())
    val epgList: StateFlow<List<EpgProgram>> = _epgList.asStateFlow()

    private val _isEpgLoading = MutableStateFlow(false)
    val isEpgLoading: StateFlow<Boolean> = _isEpgLoading.asStateFlow()"""
content = content.replace("    private val _showOverlay = MutableStateFlow(true)\n    val showOverlay: StateFlow<Boolean> = _showOverlay.asStateFlow()", states)

funcs = """    fun showEpgPanel() {
        _isEpgPanelVisible.value = true
        fetchEpg()
    }

    fun hideEpgPanel() {
        _isEpgPanelVisible.value = false
    }

    private fun fetchEpg() {
        val channel = _currentChannel.value ?: return
        if (!channel.isSup) return
        
        viewModelScope.launch {
            _isEpgLoading.value = true
            val list = sniffer.scrapeEpg(channel.streamUrl)
            _epgList.value = list
            _isEpgLoading.value = false
        }
    }

    fun playCatchup(program: EpgProgram) {
        val channel = _currentChannel.value ?: return
        if (!channel.isSup) return
        
        hideEpgPanel()
        
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
    }
"""

# Insert funcs before onCleared
parts = content.rsplit('    override fun onCleared() {', 1)
content = parts[0] + funcs + "\n    override fun onCleared() {" + parts[1]

with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated PlayerViewModel.kt")
