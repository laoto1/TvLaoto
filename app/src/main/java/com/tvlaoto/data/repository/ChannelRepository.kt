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
import java.util.concurrent.TimeUnit
import com.tvlaoto.data.db.AppStateDao
import com.tvlaoto.data.db.AppState

class ChannelRepository(
    private val context: Context,
    private val appStateDao: AppStateDao
) {

    companion object {
        // URL to the resolved playlist with pre-extracted m3u8 tokens
        // This is updated every 30 minutes by GitHub Actions
        const val RESOLVED_PLAYLIST_URL = "https://raw.githubusercontent.com/laoto1/TvLaoto/main/resolved_playlist.m3u"
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
     * This replaces streamUrl with tokenized URLs for isSup channels.
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
}




