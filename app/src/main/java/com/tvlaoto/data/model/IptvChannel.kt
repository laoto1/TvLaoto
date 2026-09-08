package com.tvlaoto.data.model

import androidx.compose.runtime.Immutable

@Immutable
data class IptvChannel(
    val id: String,
    val channelNumber: Int,
    val name: String,
    val streamUrl: String,
    val logoUrl: String? = null,
    val groupTitle: String = "Tổng Hợp",
    val tvgId: String? = null,
    val tvgName: String? = null,
    val userAgent: String? = null,
    val httpReferrer: String? = null,
    val currentProgram: String = "Trực tiếp",
    val programTime: String = "Đang phát sóng",
    val programDescription: String = "",
    val isFavorite: Boolean = false,
    val resolvedUrl: String? = null,   // Pre-resolved m3u8 URL with token
    val resolvedAt: Long = 0           // Unix timestamp when resolved
)

fun IptvChannel.supportsCatchup(): Boolean {
    if (resolvedUrl != null) return true
    if (streamUrl.contains("tv360.vn") || name.contains("THVL", ignoreCase = true) || groupTitle.equals("THVL", ignoreCase = true)) return true
    if (streamUrl.contains("vtvgo.vn")) {
        val channelId = Regex("""(?:-(\d+)\.html|,(\d+)\.html)""").find(streamUrl)?.let {
            it.groupValues[1].ifEmpty { it.groupValues[2] }
        }
        return channelId in com.tvlaoto.data.repository.ChannelRepository.VTV_CATCHUP_CHANNEL_IDS ||
                name.startsWith("VTV", ignoreCase = true) || groupTitle.equals("VTV", ignoreCase = true)
    }
    return false
}

