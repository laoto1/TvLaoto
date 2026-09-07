package com.tvlaoto.data.model

import androidx.compose.runtime.Immutable

@Immutable
data class IptvCategory(
    val title: String,
    val channels: List<IptvChannel>
)

@Immutable
data class IptvPlaylist(
    val title: String = "TvLaoto Playlist",
    val categories: List<IptvCategory>,
    val totalChannels: Int
)

