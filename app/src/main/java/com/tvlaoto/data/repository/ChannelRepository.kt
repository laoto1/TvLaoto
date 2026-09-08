package com.tvlaoto.data.repository

import android.content.Context
import android.content.SharedPreferences
import com.tvlaoto.R
import com.tvlaoto.data.model.AppSettings
import com.tvlaoto.data.model.IptvCategory
import com.tvlaoto.data.model.IptvChannel
import com.tvlaoto.data.model.IptvPlaylist
import com.tvlaoto.data.parser.M3uParser
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.InputStream
import java.net.URLEncoder
import java.security.MessageDigest
import java.util.concurrent.TimeUnit
import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec
import android.util.Base64
import com.tvlaoto.data.db.AppStateDao
import com.tvlaoto.data.db.AppState

class ChannelRepository(
    private val context: Context,
    private val appStateDao: AppStateDao
) {

    companion object {
        const val RESOLVED_PLAYLIST_URL = "https://raw.githubusercontent.com/laoto1/TvLaoto/main/resolved_playlist.m3u"
        const val RESOLVED_EPG_URL = "https://raw.githubusercontent.com/laoto1/TvLaoto/main/resolved_epg.json"
        const val VTVGO_EPG_API = "https://api.vtvdigital.org/display/v21.0/epg"
        const val VTVGO_PLAYBACK_API = "https://api.vtvdigital.org/live-channel/v21.0/playback/source"
        const val TV360_GET_LINK_API = "https://tv360.vn/public/v1/composite/get-link"
        const val TV360_SCHEDULE_API = "https://tv360.vn/public/v1/live/get-live-schedule"
        const val TV360_AES_SECRET = "eNdtOeNDeNcRyPteDsCREt#2022"
        const val TV360_AUTH_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNjEyNTg1OTkiLCJ1c2VySWQiOjE2MTI1ODU5OSwicHJvZmlsZUlkIjoxNjE0MTA4NDYsImR2aSI6MTAyODE3OTU3NiwiY29udGVudEZpbHRlciI6IjEwMCIsImduYW1lIjoiIiwib3NUeXBlIjoiV0VCIiwiaWF0IjoxNzg4ODgzMzU1LCJleHAiOjE3OTE0NzUzNTV9.4h6ytNsQ43zRCNFhoeJj8K9R5huhugbRkFZ-R5w3yUXoIXR7I6wuf822kjv2-vfxZ6Jd0YuOOC-OTB_nbZCEAw"
        const val TV360_DEVICE_ID = "web_9bb25a58-b0e9-4273-b207-8b818e3f5e9a"
        const val TV360_USER_ID = "161258599"

        // TV360 channel ID mapping: THVL name -> TV360 channel ID
        val TV360_CHANNEL_MAP = mapOf(
            "thvl1" to 25, "thvl2" to 26, "thvl3" to 219,
            "thvl4" to 220, "thvl5" to 91
        )

        // Only VTV channels have catchup/timeshift servers on VTVGo (others return 404 CHANNEL_SOURCE_EMPTY)
        val VTV_CATCHUP_CHANNEL_IDS = setOf("1", "2", "3", "4", "5", "6", "7", "13", "27", "36", "39", "163")
    }

    private val prefs: SharedPreferences =
        context.getSharedPreferences("tvlaoto_prefs", Context.MODE_PRIVATE)

    private val httpClient = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .followRedirects(true)
        .build()

    private val _playlist = MutableStateFlow<IptvPlaylist?>(null)
    val playlist: StateFlow<IptvPlaylist?> = _playlist.asStateFlow()

    private val _settings = MutableStateFlow(loadSettings())
    val settings: StateFlow<AppSettings> = _settings.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _errorMessage = MutableStateFlow<String?>(null)
    val errorMessage: StateFlow<String?> = _errorMessage.asStateFlow()

    var lastTv360Error: String? = null
        private set

    private val tv360SessionId: String = java.util.UUID.randomUUID().toString()

    private fun loadSettings(): AppSettings {
        return AppSettings(
            customM3uUrl = prefs.getString("custom_m3u_url", "") ?: "",
            languageCode = prefs.getString("language_code", "vi") ?: "vi",
            lastPlayedChannelId = prefs.getString("last_channel_id", null)
        )
    }

    suspend fun initialize() {
        val customUrl = _settings.value.customM3uUrl
        if (customUrl.isNotBlank()) {
            loadFromUrl(customUrl)
        } else {
            loadBundledDemoPlaylist()
        }
    }

    suspend fun loadBundledDemoPlaylist() = withContext(Dispatchers.IO) {
        _isLoading.value = true
        _errorMessage.value = null
        try {
            val inputStream: InputStream = context.resources.openRawResource(R.raw.demo_playlist)
            val parsed = M3uParser.parse(inputStream)
            _playlist.value = applyFavorites(parsed)
        } catch (e: Exception) {
            _errorMessage.value = e.localizedMessage ?: "Failed to load demo playlist"
        } finally {
            _isLoading.value = false
        }
    }

    suspend fun loadFromUrl(url: String) = withContext(Dispatchers.IO) {
        if (url.isBlank()) {
            updateCustomUrl("")  // Clear saved URL
            loadBundledDemoPlaylist()
            return@withContext
        }

        _isLoading.value = true
        _errorMessage.value = null
        try {
            val request = Request.Builder()
                .url(url)
                .header("User-Agent", "TvLaoto/1.0 (Android TV)")
                .build()

            val response = httpClient.newCall(request).execute()
            if (!response.isSuccessful) {
                throw Exception("HTTP ${response.code}: ${response.message}")
            }

            val body = response.body ?: throw Exception("Empty response body")
            val parsed = M3uParser.parse(body.byteStream())

            if (parsed.categories.isEmpty()) {
                throw Exception("No valid channels found in M3U file")
            }
            _playlist.value = applyFavorites(parsed)
            updateCustomUrl(url)
        } catch (e: Exception) {
            _errorMessage.value = "Failed to load M3U URL: ${e.localizedMessage}"
            // Fallback to bundled playlist if empty
            if (_playlist.value == null) {
                loadBundledDemoPlaylist()
            }
        } finally {
            _isLoading.value = false
        }
    }

    fun updateCustomUrl(url: String) {
        prefs.edit().putString("custom_m3u_url", url).apply()
        _settings.value = _settings.value.copy(customM3uUrl = url)
    }

    fun updateLanguage(langCode: String) {
        prefs.edit().putString("language_code", langCode).apply()
        _settings.value = _settings.value.copy(languageCode = langCode)
    }

    fun saveLastPlayedChannel(channelId: String) {
        prefs.edit().putString("last_channel_id", channelId).apply()
        _settings.value = _settings.value.copy(lastPlayedChannelId = channelId)
    }

    private fun applyFavorites(playlist: IptvPlaylist): IptvPlaylist {
        val favs = getFavoriteIds()
        return playlist.copy(
            categories = playlist.categories.map { category ->
                category.copy(
                    channels = category.channels.map { channel ->
                        channel.copy(isFavorite = favs.contains(channel.id))
                    }
                )
            }
        )
    }

    fun getFavoriteIds(): Set<String> {
        return prefs.getStringSet("favorite_channels", emptySet()) ?: emptySet()
    }

        suspend fun getLastFilterTab(): String {
        return appStateDao.getAppState()?.lastFilterTab ?: "Tất cả"
    }

    suspend fun saveLastFilterTab(tab: String) {
        appStateDao.saveAppState(AppState(id = 1, lastFilterTab = tab))
    }
    fun toggleFavorite(channelId: String) {
        val currentFavs = getFavoriteIds().toMutableSet()
        if (currentFavs.contains(channelId)) {
            currentFavs.remove(channelId)
        } else {
            currentFavs.add(channelId)
        }
        prefs.edit().putStringSet("favorite_channels", currentFavs).apply()
        
        // Update playlist state to reflect change
        _playlist.value = _playlist.value?.let { currentPlaylist ->
            currentPlaylist.copy(
                categories = currentPlaylist.categories.map { category ->
                    category.copy(
                        channels = category.channels.map { channel ->
                            if (channel.id == channelId) {
                                channel.copy(isFavorite = currentFavs.contains(channelId))
                            } else {
                                channel
                            }
                        }
                    )
                }
            )
        }
    }

    fun findChannelById(id: String): IptvChannel? {
        return _playlist.value?.categories?.flatMap { it.channels }?.find { it.id == id }
    }

    fun getAllChannels(): List<IptvChannel> {
        return _playlist.value?.categories?.flatMap { it.channels } ?: emptyList()
    }

    /**
     * Fetch pre-resolved m3u8 URLs from gist and merge into current playlist.
     * This merges tokenized URLs into the current playlist channels.
     */
    suspend fun fetchResolvedPlaylist() = withContext(Dispatchers.IO) {
        val url = RESOLVED_PLAYLIST_URL
        if (url.isBlank()) return@withContext

        try {
            val request = Request.Builder()
                .url(url)
                .header("User-Agent", "AFlix-TV/1.0")
                .build()

            val response = httpClient.newCall(request).execute()
            if (!response.isSuccessful) return@withContext

            val body = response.body ?: return@withContext
            val resolvedPlaylist = M3uParser.parse(body.byteStream())

            // Build lookup: channel name -> resolved channel
            val resolvedMap = mutableMapOf<String, IptvChannel>()
            resolvedPlaylist.categories.flatMap { it.channels }.forEach { ch ->
                resolvedMap[ch.name] = ch
            }

            // Merge resolved URLs into current playlist
            val currentPlaylist = _playlist.value ?: return@withContext
            _playlist.value = currentPlaylist.copy(
                categories = currentPlaylist.categories.map { category ->
                    category.copy(
                        channels = category.channels.map { channel ->
                            val resolved = resolvedMap[channel.name]
                            if (resolved?.resolvedUrl != null) {
                                channel.copy(
                                    resolvedUrl = resolved.resolvedUrl,
                                    resolvedAt = resolved.resolvedAt
                                )
                            } else {
                                channel
                            }
                        }
                    )
                }
            )
            com.tvlaoto.util.AppLogger.i("ChannelRepo", "Merged ${resolvedMap.size} resolved URLs")
        } catch (e: Exception) {
            com.tvlaoto.util.AppLogger.w("ChannelRepo", "Failed to fetch resolved playlist: ${e.message}")
        }
    }

    /**
     * Force re-fetch resolved URLs from GitHub (called on 403 token expiry).
     */
    suspend fun refreshResolvedUrls() {
        fetchResolvedPlaylist()
    }

    /**
     * Find a channel by its ID in the current playlist.
     */
    fun getChannelById(id: String): IptvChannel? {
        return _playlist.value?.categories?.flatMap { it.channels }?.find { it.id == id }
    }

    // Cache of server EPG data: channel name -> program list
    private var serverEpgCache: Map<String, List<com.tvlaoto.data.model.EpgProgram>> = emptyMap()

    /**
     * Fetch EPG + catchup URLs from resolved_epg.json (GitHub Actions generated).
     * Returns programs for a specific channel name.
     */
    suspend fun fetchServerEpg(channelName: String): List<com.tvlaoto.data.model.EpgProgram> = withContext(Dispatchers.IO) {
        // Return from cache if already loaded
        serverEpgCache[channelName]?.let { return@withContext it }

        val url = RESOLVED_EPG_URL
        if (url.isBlank()) return@withContext emptyList()

        try {
            val request = Request.Builder()
                .url(url)
                .header("User-Agent", "AFlix-TV/1.0")
                .build()

            val response = httpClient.newCall(request).execute()
            if (!response.isSuccessful) return@withContext emptyList()

            val body = response.body?.string() ?: return@withContext emptyList()
            val json = org.json.JSONObject(body)
            val channelsObj = json.optJSONObject("channels") ?: return@withContext emptyList()

            val newCache = mutableMapOf<String, List<com.tvlaoto.data.model.EpgProgram>>()

            val keys = channelsObj.keys()
            while (keys.hasNext()) {
                val chKey = keys.next()
                val chObj = channelsObj.getJSONObject(chKey)
                val name = chObj.optString("name", "")
                val programsArr = chObj.optJSONArray("programs") ?: continue

                val programs = mutableListOf<com.tvlaoto.data.model.EpgProgram>()
                for (i in 0 until programsArr.length()) {
                    val p = programsArr.getJSONObject(i)
                    programs.add(
                        com.tvlaoto.data.model.EpgProgram(
                            index = p.optInt("index", i),
                            time = p.optString("time", ""),
                            title = p.optString("title", ""),
                            isReplayable = p.optBoolean("is_replayable", false),
                            startEpoch = p.optLong("start_epoch", 0),
                            endEpoch = p.optLong("end_epoch", 0),
                            catchupUrl = p.optString("catchup_url", "").ifBlank { null },
                            slotId = p.optString("slot_id", "").ifEmpty { p.optString("slotId", "") }.ifBlank { null },
                            startTimeIso = p.optString("start_time_iso", "").ifEmpty { p.optString("startTime", "") }.ifBlank { null },
                            endTimeIso = p.optString("end_time_iso", "").ifEmpty { p.optString("endTime", "") }.ifBlank { null }
                        )
                    )
                }
                newCache[name] = programs
            }

            serverEpgCache = newCache
            com.tvlaoto.util.AppLogger.i("ChannelRepo", "Loaded EPG for ${newCache.size} channels")

        } catch (e: Exception) {
            com.tvlaoto.util.AppLogger.w("ChannelRepo", "Failed to fetch EPG: ${e.message}")
        }

        serverEpgCache[channelName] ?: emptyList()
    }

    /**
     * Fetch EPG from VTVGo API v21. Returns programs with slotId for catchup.
     */
    suspend fun fetchEpgFromApi(streamUrl: String): List<com.tvlaoto.data.model.EpgProgram> = withContext(Dispatchers.IO) {
        val list = mutableListOf<com.tvlaoto.data.model.EpgProgram>()
        try {
            val channelId = Regex("(?:-(\\d+)\\.html|,(\\d+)\\.html)").find(streamUrl)?.let {
                it.groupValues[1].ifEmpty { it.groupValues[2] }
            } ?: return@withContext emptyList()

            val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US)
            sdf.timeZone = java.util.TimeZone.getTimeZone("Asia/Ho_Chi_Minh")
            val today = sdf.format(java.util.Date())

            val apiUrl = "$VTVGO_EPG_API?channelIDs=$channelId&from=$today&to=$today"

            val request = Request.Builder()
                .url(apiUrl)
                .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                .header("Referer", "https://vtvgo.vn/")
                .header("Origin", "https://vtvgo.vn")
                .build()

            val response = httpClient.newCall(request).execute()
            if (!response.isSuccessful) return@withContext emptyList()

            val body = response.body?.string() ?: return@withContext emptyList()
            val json = org.json.JSONObject(body)
            val dataObj = json.optJSONObject("data") ?: return@withContext emptyList()

            val channelArr = dataObj.optJSONArray(channelId) ?: return@withContext emptyList()
            if (channelArr.length() == 0) return@withContext emptyList()

            // VTVGo API v21 returns array of programs directly: data: { "1": [ { slotId, title, ... }, ... ] }
            val firstItem = channelArr.optJSONObject(0) ?: return@withContext emptyList()
            val programsArr = if (firstItem.has("slotId") || firstItem.has("startTime")) {
                channelArr
            } else {
                firstItem.optJSONArray("programs") ?: channelArr
            }

            val isoSdf = java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", java.util.Locale.US)
            isoSdf.timeZone = java.util.TimeZone.getTimeZone("UTC")
            val localTimeSdf = java.text.SimpleDateFormat("HH:mm", java.util.Locale.US)
            localTimeSdf.timeZone = java.util.TimeZone.getDefault()
            val nowEpoch = System.currentTimeMillis() / 1000

            com.tvlaoto.util.AppLogger.d("ChannelRepo", "EPG v21: ${programsArr.length()} programs for channel $channelId")

            for (i in 0 until programsArr.length()) {
                val item = programsArr.getJSONObject(i)
                val slotId = item.optString("slotId", "")
                val rawTitle = item.optString("title", "").trim()
                val desc = item.optString("description", "").trim()
                val title = if (desc.isNotEmpty()) "$rawTitle: $desc" else rawTitle

                val startIso = item.optString("startTime", "")
                val endIso = item.optString("endTime", "")
                var timeStr = ""
                var startEpoch = 0L
                var endEpoch = 0L

                if (startIso.isNotEmpty()) {
                    try {
                        val date = isoSdf.parse(startIso)
                        timeStr = date?.let { localTimeSdf.format(it) } ?: ""
                        startEpoch = date?.time?.div(1000) ?: 0L
                    } catch (_: Exception) {}
                }
                if (endIso.isNotEmpty()) {
                    try { endEpoch = isoSdf.parse(endIso)?.time?.div(1000) ?: 0L } catch (_: Exception) {}
                }

                val supportsCatchup = VTV_CATCHUP_CHANNEL_IDS.contains(channelId)
                list.add(com.tvlaoto.data.model.EpgProgram(
                    index = i, time = timeStr, title = title,
                    isReplayable = supportsCatchup && endEpoch > 0 && endEpoch < nowEpoch,
                    startEpoch = startEpoch, endEpoch = endEpoch,
                    slotId = slotId, startTimeIso = startIso, endTimeIso = endIso
                ))
            }
        } catch (e: Exception) {
            com.tvlaoto.util.AppLogger.w("ChannelRepo", "EPG v21 error: ${e.message}")
        }
        list
    }

    /**
     * Fetch live stream URLs from VTVGo playback API.
     * Returns ALL available CDN URLs so caller can try fallbacks.
     */
    suspend fun fetchVtvgoLiveUrls(channelId: String): List<String> = withContext(Dispatchers.IO) {
        val urls = mutableListOf<String>()
        try {
            val deviceId = java.util.UUID.randomUUID().toString()
            val jsonBody = org.json.JSONObject().apply {
                put("channelId", channelId)
                put("platform", "webPC")
                put("deviceId", deviceId)
            }

            val requestBody = jsonBody.toString()
                .toByteArray(Charsets.UTF_8)
                .let { okhttp3.RequestBody.create(null, it) }

            val request = Request.Builder()
                .url(VTVGO_PLAYBACK_API)
                .post(requestBody)
                .header("Content-Type", "application/json")
                .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                .header("Referer", "https://vtvgo.vn/")
                .header("Origin", "https://vtvgo.vn")
                .header("Accept", "application/json")
                .build()

            val response = httpClient.newCall(request).execute()
            if (!response.isSuccessful) {
                com.tvlaoto.util.AppLogger.w("ChannelRepo", "VTVGo live API: ${response.code}")
                return@withContext urls
            }

            val body = response.body?.string() ?: return@withContext urls
            val json = org.json.JSONObject(body)
            val data = json.optJSONObject("data") ?: return@withContext urls
            val sourceModes = data.optJSONArray("sourceModes") ?: return@withContext urls

            for (i in 0 until sourceModes.length()) {
                val mode = sourceModes.getJSONObject(i)
                if (mode.optString("id") == "default") {
                    val multiSource = mode.optJSONArray("multiSource") ?: continue
                    for (j in 0 until multiSource.length()) {
                        val sources = multiSource.getJSONObject(j).optJSONArray("sources") ?: continue
                        for (k in 0 until sources.length()) {
                            val url = sources.getJSONObject(k).optString("url", "")
                            if (url.isNotEmpty()) {
                                urls.add(url)
                            }
                        }
                    }
                }
            }
            com.tvlaoto.util.AppLogger.i("ChannelRepo", "VTVGo live: ${urls.size} URLs for ch $channelId")
        } catch (e: Exception) {
            com.tvlaoto.util.AppLogger.w("ChannelRepo", "VTVGo live error: ${e.message}")
        }
        urls
    }

    /**
     * Probe a URL via HEAD request, returns HTTP status code.
     */
    suspend fun probeUrl(request: okhttp3.Request): Int = withContext(Dispatchers.IO) {
        try {
            val response = httpClient.newCall(request).execute()
            val code = response.code
            response.close()
            code
        } catch (e: Exception) {
            -1
        }
    }

    /**
     * Fetch catchup stream URL from VTVGo playback API.
     * Pure HTTP — no WebView needed!
     */
    suspend fun fetchCatchupUrl(channelId: String, program: com.tvlaoto.data.model.EpgProgram): String? = withContext(Dispatchers.IO) {
        try {
            val deviceId = java.util.UUID.randomUUID().toString()
            val jsonBody = org.json.JSONObject().apply {
                put("channelId", channelId)
                put("programId", program.slotId ?: "")
                put("startTime", program.startTimeIso ?: "")
                put("endTime", program.endTimeIso ?: "")
                put("platform", "webPC")
                put("deviceId", deviceId)
            }

            val requestBody = jsonBody.toString()
                .toByteArray(Charsets.UTF_8)
                .let { okhttp3.RequestBody.create(null, it) }

            val request = Request.Builder()
                .url(VTVGO_PLAYBACK_API)
                .post(requestBody)
                .header("Content-Type", "application/json")
                .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                .header("Referer", "https://vtvgo.vn/")
                .header("Origin", "https://vtvgo.vn")
                .header("Accept", "application/json")
                .build()

            val response = httpClient.newCall(request).execute()
            if (!response.isSuccessful) {
                com.tvlaoto.util.AppLogger.w("ChannelRepo", "Catchup API: ${response.code}")
                return@withContext null
            }

            val body = response.body?.string() ?: return@withContext null
            val json = org.json.JSONObject(body)
            val data = json.optJSONObject("data") ?: return@withContext null
            val sourceModes = data.optJSONArray("sourceModes") ?: return@withContext null

            for (i in 0 until sourceModes.length()) {
                val mode = sourceModes.getJSONObject(i)
                if (mode.optString("id") == "default") {
                    val multiSource = mode.optJSONArray("multiSource") ?: continue
                    if (multiSource.length() > 0) {
                        val sources = multiSource.getJSONObject(0).optJSONArray("sources") ?: continue
                        if (sources.length() > 0) {
                            val url = sources.getJSONObject(0).optString("url", "")
                            if (url.isNotEmpty()) {
                                com.tvlaoto.util.AppLogger.i("ChannelRepo", "Catchup: ${url.take(80)}...")
                                return@withContext url
                            }
                        }
                    }
                }
            }
        } catch (e: Exception) {
            com.tvlaoto.util.AppLogger.w("ChannelRepo", "Catchup error: ${e.message}")
        }
        null
    }

    // ---- TV360 API (on-demand for THVL channels) ----

    private fun tv360AesKey(): SecretKeySpec {
        val sha1 = MessageDigest.getInstance("SHA-1").digest(TV360_AES_SECRET.toByteArray())
        val hexStr = sha1.joinToString("") { "%02x".format(it) }
        val keyHex = hexStr.substring(0, 32) // 32 hex chars = 16 bytes = AES-128
        val keyBytes = keyHex.chunked(2).map { it.toInt(16).toByte() }.toByteArray()
        return SecretKeySpec(keyBytes, "AES")
    }

    private fun tv360Encrypt(plaintext: String): String {
        val cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, tv360AesKey())
        return Base64.encodeToString(cipher.doFinal(plaintext.toByteArray()), Base64.NO_WRAP)
    }

    private fun tv360Decrypt(ciphertext: String): String {
        val cipher = Cipher.getInstance("AES/ECB/PKCS5Padding")
        cipher.init(Cipher.DECRYPT_MODE, tv360AesKey())
        return String(cipher.doFinal(Base64.decode(ciphertext, Base64.DEFAULT)))
    }

    /** Last parsed 428 error code for external checking */
    var lastTv360ErrorCode: Int = 0
        private set

    /**
     * Fetch live stream URL from TV360 API.
     * Returns: streaming URL, or null on failure (check lastTv360Error for details).
     * On 428 (device limit): parses active device list and sets descriptive error.
     */
    private fun doFetchTv360(tv360Id: Int, isMovie: Boolean): String? {
        try {
            val timestamp = System.currentTimeMillis() / 1000
            val deviceId = TV360_DEVICE_ID
            val price = if (isMovie) 5000 else 0
            val groupChannel = if (isMovie) 1 else 0
            val params = "id=$tv360Id&type=live&mod=LIVE&t=$timestamp&secured=true&drm=3%2C4&price=$price&subInfo=3&llc=1&groupChannel=$groupChannel"
            val sq = URLEncoder.encode(tv360Encrypt(params), "UTF-8")
            val url = "$TV360_GET_LINK_API?sq=$sq&secured=true"

            val request = Request.Builder()
                .url(url)
                .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                .header("Accept", "application/json, text/plain, */*")
                .header("Content-Type", "application/json")
                .header("Referer", "https://tv360.vn/")
                .header("authorization", "Bearer $TV360_AUTH_TOKEN")
                .header("Cookie", "device-id=$deviceId; shared-device-id=$deviceId; nd13=${TV360_USER_ID}_1; NEXT_LOCALE=vi; session-id=$tv360SessionId")
                .build()

            val response = httpClient.newCall(request).execute()
            val body = response.body?.string() ?: return null

            val json = org.json.JSONObject(body)
            val code = json.optInt("errorCode")
            lastTv360ErrorCode = code
            if (code != 200) {
                val rawMsg = json.optString("message", "")
                com.tvlaoto.util.AppLogger.w("ChannelRepo", "TV360 error ($code) for $tv360Id (isMovie=$isMovie): $rawMsg")

                if (code == 428) {
                    // Parse encrypted device data to get active device list
                    val encData = json.optString("data", "")
                    var deviceCount = 0
                    if (encData.isNotEmpty()) {
                        try {
                            val dec = tv360Decrypt(encData)
                            val devJson = org.json.JSONObject(dec)
                            val devArr = devJson.optJSONArray("device")
                            deviceCount = devArr?.length() ?: 0
                            val devNames = mutableListOf<String>()
                            if (devArr != null) {
                                for (i in 0 until devArr.length()) {
                                    val d = devArr.getJSONObject(i)
                                    val name = d.optString("deviceName", "unknown")
                                    val osType = d.optString("osAppType", "")
                                    devNames.add("$name($osType)")
                                }
                            }
                            com.tvlaoto.util.AppLogger.w("ChannelRepo", "TV360 device limit: $deviceCount active devices: ${devNames.joinToString()}")
                        } catch (e: Exception) {
                            com.tvlaoto.util.AppLogger.w("ChannelRepo", "TV360 428 data parse error: ${e.message}")
                        }
                    }
                    lastTv360Error = "Tài khoản đang xem trên $deviceCount thiết bị khác. " +
                        "Vui lòng tắt luồng xem trên thiết bị khác hoặc đợi vài phút."
                } else {
                    lastTv360Error = when (code) {
                        404 -> "Kênh này hiện tạm ngừng phát sóng trên TV360"
                        401 -> "Kênh này yêu cầu tài khoản hoặc gói cước TV360"
                        else -> rawMsg.ifEmpty { "Không thể tải luồng phát" }
                    }
                }
                return null
            }

            lastTv360ErrorCode = 200
            val encryptedData = json.optString("data", "")
            if (encryptedData.isEmpty()) return null

            val decrypted = tv360Decrypt(encryptedData)
            com.tvlaoto.util.AppLogger.d("ChannelRepo", "TV360 decrypted: ${decrypted.take(150)}...")

            val dataJson = org.json.JSONObject(decrypted)
            val linkPlay = dataJson.optString("urlStreaming", "")
                .ifEmpty { dataJson.optString("url", "") }
                .ifEmpty { dataJson.optString("linkPlay", "") }
                .ifEmpty { dataJson.optString("link_play", "") }

            if (linkPlay.isNotEmpty()) {
                com.tvlaoto.util.AppLogger.i("ChannelRepo", "TV360 URL: ${linkPlay.take(80)}...")
                lastTv360Error = null
                return linkPlay
            }

            val streamRegex = Regex("""https?://[^\s"']+\.(m3u8|mpd)[^\s"']*""")
            val match = streamRegex.find(decrypted)
            if (match != null) {
                com.tvlaoto.util.AppLogger.i("ChannelRepo", "TV360 stream: ${match.value.take(80)}...")
                lastTv360Error = null
                return match.value
            }

            com.tvlaoto.util.AppLogger.w("ChannelRepo", "TV360: no URL in decrypted data")
            return null
        } catch (e: Exception) {
            com.tvlaoto.util.AppLogger.e("ChannelRepo", "TV360 fetch error: ${e.message}", e)
            lastTv360Error = "Lỗi kết nối TV360: ${e.message}"
            return null
        }
    }

    suspend fun fetchTv360Url(channelKey: String): String? = withContext(Dispatchers.IO) {
        val tv360Id = TV360_CHANNEL_MAP[channelKey.lowercase()] ?: channelKey.toIntOrNull() ?: return@withContext null
        val isMovie = tv360Id in setOf(9903, 10009, 10010, 10011, 10012, 10013, 10055) || tv360Id >= 10000
        var url = doFetchTv360(tv360Id, isMovie)

        // Auto-retry on S-006 with alternate parameters
        if (url == null && (lastTv360Error?.contains("không hợp lệ") == true || lastTv360Error?.contains("S-006") == true)) {
            com.tvlaoto.util.AppLogger.i("ChannelRepo", "Retrying TV360 for $tv360Id with alternate parameters...")
            url = doFetchTv360(tv360Id, !isMovie)
        }

        // Auto-retry on 428 (device limit) with delay — sessions may expire between retries
        if (url == null && lastTv360ErrorCode == 428) {
            for (attempt in 1..2) {
                com.tvlaoto.util.AppLogger.i("ChannelRepo", "TV360 device limit retry $attempt/2 for $tv360Id (waiting 5s)...")
                Thread.sleep(5000)
                url = doFetchTv360(tv360Id, isMovie)
                if (url != null || lastTv360ErrorCode != 428) break
            }
        }
        url
    }

    /**
     * Fetch EPG schedule for THVL channel from TV360 API.
     * @param channelKey e.g. "thvl1"
     */
    suspend fun fetchTv360Epg(channelKey: String): List<com.tvlaoto.data.model.EpgProgram> = withContext(Dispatchers.IO) {
        val tv360Id = TV360_CHANNEL_MAP[channelKey.lowercase()] ?: channelKey.toIntOrNull() ?: return@withContext emptyList()
        val list = mutableListOf<com.tvlaoto.data.model.EpgProgram>()
        try {
            val url = "$TV360_SCHEDULE_API?id=$tv360Id"
            val request = Request.Builder()
                .url(url)
                .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                .header("Referer", "https://tv360.vn/")
                .header("authorization", "Bearer $TV360_AUTH_TOKEN")
                .header("Cookie", "device-id=$TV360_DEVICE_ID; shared-device-id=$TV360_DEVICE_ID; nd13=${TV360_USER_ID}_1; NEXT_LOCALE=vi")
                .build()

            val response = httpClient.newCall(request).execute()
            if (!response.isSuccessful) return@withContext emptyList()

            val body = response.body?.string() ?: return@withContext emptyList()
            val json = org.json.JSONObject(body)
            val dataObj = json.optJSONObject("data") ?: return@withContext emptyList()
            val schedulesArr = dataObj.optJSONArray("schedules") ?: return@withContext emptyList()

            val nowEpoch = System.currentTimeMillis() / 1000L

            for (i in 0 until schedulesArr.length()) {
                val item = schedulesArr.getJSONObject(i)
                val id = item.optString("id", "")
                val name = item.optString("name", "").trim()
                val startTime = item.optString("startTime", "")
                val epochSt = item.optLong("epochSt", 0L) / 1000L
                val epochEt = item.optLong("epochEt", 0L) / 1000L

                val isReplayable = (epochEt > 0 && epochEt < nowEpoch) || item.optInt("status", 0) == 1

                list.add(
                    com.tvlaoto.data.model.EpgProgram(
                        index = i,
                        time = startTime,
                        title = name,
                        isReplayable = isReplayable,
                        startEpoch = epochSt,
                        endEpoch = epochEt,
                        slotId = id
                    )
                )
            }
            val replayCount = list.count { it.isReplayable }
            com.tvlaoto.util.AppLogger.i("ChannelRepo", "Loaded TV360 EPG: ${list.size} programs for $channelKey ($replayCount replayable)")
        } catch (e: Exception) {
            com.tvlaoto.util.AppLogger.w("ChannelRepo", "TV360 EPG error for $channelKey: ${e.message}")
        }
        list
    }

    /**
     * Fetch timeshift/catchup stream URL for THVL channel from TV360.
     * Appends timeshift parameter to fresh TV360 stream URL.
     */
    suspend fun fetchTv360CatchupUrl(channelKey: String, program: com.tvlaoto.data.model.EpgProgram): String? = withContext(Dispatchers.IO) {
        val baseStreamUrl = fetchTv360Url(channelKey) ?: return@withContext null
        if (program.startEpoch <= 0) return@withContext baseStreamUrl

        val nowEpoch = System.currentTimeMillis() / 1000L
        val timeshiftSeconds = maxOf(0L, nowEpoch - program.startEpoch)

        val catchupUrl = if (timeshiftSeconds > 0) {
            val delimiter = if (baseStreamUrl.contains("?")) "&" else "?"
            "$baseStreamUrl${delimiter}timeshift=$timeshiftSeconds"
        } else {
            baseStreamUrl
        }

        com.tvlaoto.util.AppLogger.i("ChannelRepo", "TV360 Catchup: timeshift=${timeshiftSeconds}s, url=${catchupUrl.take(80)}...")
        catchupUrl
    }
}




