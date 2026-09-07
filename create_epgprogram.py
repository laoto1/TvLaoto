content = """package com.tvlaoto.data.model

import androidx.compose.runtime.Immutable

@Immutable
data class EpgProgram(
    val index: Int,
    val time: String,
    val title: String,
    val isReplayable: Boolean
)
"""
with open('app/src/main/java/com/tvlaoto/data/model/EpgProgram.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Created EpgProgram.kt")
