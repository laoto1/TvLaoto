package com.tvlaoto.data.model

import androidx.compose.runtime.Immutable

@Immutable
data class EpgProgram(
    val index: Int,
    val time: String,
    val title: String,
    val isReplayable: Boolean,
    val startEpoch: Long = 0L,
    val endEpoch: Long = 0L,
    val catchupUrl: String? = null,
    val slotId: String? = null,       // VTVGo programId for catchup API
    val startTimeIso: String? = null,  // ISO 8601 for catchup API
    val endTimeIso: String? = null     // ISO 8601 for catchup API
)
