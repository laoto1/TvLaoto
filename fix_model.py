content = """package com.tvlaoto.data.model

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
    val currentProgram: String = "Chương trình trực tiếp",
    val programTime: String = "19:00 - 19:45",
    val programDescription: String = "Bản tin thời sự cập nhật những tin tức mới nhất trong ngày.",
    val isFavorite: Boolean = false,
    val isSup: Boolean = false
)
"""
with open('app/src/main/java/com/tvlaoto/data/model/IptvChannel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
