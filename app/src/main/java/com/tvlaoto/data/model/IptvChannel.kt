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
