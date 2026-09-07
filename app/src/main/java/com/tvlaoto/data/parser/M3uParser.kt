package com.tvlaoto.data.parser

import com.tvlaoto.data.model.IptvCategory
import com.tvlaoto.data.model.IptvChannel
import com.tvlaoto.data.model.IptvPlaylist
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.BufferedReader
import java.io.InputStream
import java.io.InputStreamReader

/**
 * Ultra-fast, robust streaming M3U parser.
 * Generates deterministic channel IDs based on channel names and groups so favorites persist.
 */
object M3uParser {

    suspend fun parse(inputStream: InputStream): IptvPlaylist = withContext(Dispatchers.IO) {
        val reader = BufferedReader(InputStreamReader(inputStream, Charsets.UTF_8), 32 * 1024)
        val categoryMap = LinkedHashMap<String, MutableList<IptvChannel>>()

        var currentTvgId: String? = null
        var currentTvgName: String? = null
        var currentLogo: String? = null
        var currentGroup = "Tổng Hợp"
        var currentChannelName = "Unknown Channel"
        var currentUserAgent: String? = null
        var currentReferrer: String? = null
        var currentResolvedAt: Long = 0
        var channelCounter = 1

        reader.useLines { lines ->
            for (rawLine in lines) {
                val line = rawLine.trim()
                if (line.isEmpty()) continue

                if (line.startsWith("#EXTINF:", ignoreCase = true)) {
                    // Extract attributes
                    currentTvgId = extractAttribute(line, "tvg-id")
                    currentTvgName = extractAttribute(line, "tvg-name")
                    currentLogo = extractAttribute(line, "tvg-logo")
                    
                    val parsedGroup = extractAttribute(line, "group-title")?.trim()
                    currentGroup = if (!parsedGroup.isNullOrBlank()) parsedGroup else "Tổng Hợp"
                    
                    currentResolvedAt = extractAttribute(line, "resolved-at")?.toLongOrNull() ?: 0

                    // Extract channel name after the last comma
                    val commaIndex = line.lastIndexOf(',')
                    if (commaIndex != -1 && commaIndex < line.length - 1) {
                        currentChannelName = line.substring(commaIndex + 1).trim()
                    } else {
                        currentChannelName = currentTvgName ?: "Kênh $channelCounter"
                    }
                } else if (line.startsWith("#EXTVLCOPT:", ignoreCase = true) ||
                    line.startsWith("#EXTHTTP:", ignoreCase = true)
                ) {
                    if (line.contains("http-user-agent=", ignoreCase = true)) {
                        currentUserAgent = line.substringAfter("http-user-agent=").trim()
                    }
                    if (line.contains("http-referrer=", ignoreCase = true)) {
                        currentReferrer = line.substringAfter("http-referrer=").trim()
                    }
                } else if (!line.startsWith("#")) {
                    // Generate deterministic ID based on channel name and group
                    val uniqueId = "ch_${currentChannelName.hashCode()}_${currentGroup.hashCode()}"

                    // If URL is already a resolved m3u8 (from server-side resolver)
                    val isResolved = currentResolvedAt > 0 && line.contains(".m3u8")

                    val channel = IptvChannel(
                        id = uniqueId,
                        channelNumber = channelCounter++,
                        name = currentChannelName,
                        streamUrl = line,
                        logoUrl = currentLogo?.takeIf { it.isNotBlank() },
                        groupTitle = currentGroup,
                        tvgId = currentTvgId,
                        tvgName = currentTvgName,
                        userAgent = currentUserAgent,
                        httpReferrer = currentReferrer,
                        resolvedUrl = if (isResolved) line else null,
                        resolvedAt = currentResolvedAt
                    )

                    categoryMap.getOrPut(currentGroup) { ArrayList() }.add(channel)

                    // Reset transient per-channel state
                    currentTvgId = null
                    currentTvgName = null
                    currentLogo = null
                    currentGroup = "Tổng Hợp"
                    currentChannelName = "Unknown Channel"
                    currentUserAgent = null
                    currentReferrer = null
                    currentResolvedAt = 0
                }
            }
        }

        val categories = categoryMap.map { (group, channels) ->
            IptvCategory(title = group, channels = channels)
        }

        IptvPlaylist(
            title = "TvLaoto Playlist",
            categories = categories,
            totalChannels = channelCounter - 1
        )
    }

    private fun extractAttribute(line: String, key: String): String? {
        val searchDouble = "$key=\""
        val startDouble = line.indexOf(searchDouble, ignoreCase = true)
        if (startDouble != -1) {
            val valueStart = startDouble + searchDouble.length
            val endDouble = line.indexOf('"', valueStart)
            if (endDouble != -1) {
                return line.substring(valueStart, endDouble)
            }
        }

        val searchSingle = "$key='"
        val startSingle = line.indexOf(searchSingle, ignoreCase = true)
        if (startSingle != -1) {
            val valueStart = startSingle + searchSingle.length
            val endSingle = line.indexOf('\'', valueStart)
            if (endSingle != -1) {
                return line.substring(valueStart, endSingle)
            }
        }

        val searchUnquoted = "$key="
        val startUnquoted = line.indexOf(searchUnquoted, ignoreCase = true)
        if (startUnquoted != -1) {
            val valueStart = startUnquoted + searchUnquoted.length
            var endUnquoted = line.indexOf(' ', valueStart)
            val commaPos = line.indexOf(',', valueStart)
            if (commaPos != -1 && (endUnquoted == -1 || commaPos < endUnquoted)) {
                endUnquoted = commaPos
            }
            if (endUnquoted == -1) {
                endUnquoted = line.length
            }
            return line.substring(valueStart, endUnquoted).trim()
        }

        return null
    }
}
