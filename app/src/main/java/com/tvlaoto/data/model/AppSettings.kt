package com.tvlaoto.data.model

import androidx.compose.runtime.Immutable

@Immutable
data class AppSettings(
    val customM3uUrl: String = "",
    val languageCode: String = "vi", // "vi" or "en"
    val lastPlayedChannelId: String? = null
)

