package com.tvlaoto.data.model

import androidx.compose.runtime.Immutable

@Immutable
data class EpgProgram(
    val index: Int,
    val time: String,
    val title: String,
    val isReplayable: Boolean,
    val startEpoch: Long = 0L,
    val endEpoch: Long = 0L
)
