import codecs

content = '''package com.tvlaoto.data.provider

import com.tvlaoto.R
import com.tvlaoto.data.model.IptvChannel

object ChannelLogoProvider {

    private const val GITHUB_LOGO_BASE =
        "https://raw.githubusercontent.com/AqFad2811/epg-iptv-logos/main/logos/vn"

    fun getDrawableFallback(channel: IptvChannel): Int? {
        val norm = channel.name.lowercase().trim()
        val normTvg = (channel.tvgName ?: channel.tvgId ?: "").lowercase().trim()

        return when {
            norm.contains("vtv1") || norm.contains("vtv 1") || normTvg.contains("vtv1") -> R.drawable.ic_logo_vtv1
            norm.contains("vtv3") || norm.contains("vtv 3") || normTvg.contains("vtv3") -> R.drawable.ic_logo_vtv3
            norm.contains("vtv6") || norm.contains("vtv 6") || normTvg.contains("vtv6") || norm.contains("c\u1ea7n th\u01a1") -> R.drawable.ic_logo_vtv6
            norm.contains("vtv9") || norm.contains("vtv 9") || normTvg.contains("vtv9") -> R.drawable.ic_logo_vtv9
            norm.contains("htv7") || norm.contains("htv 7") || normTvg.contains("htv7") -> R.drawable.ic_logo_htv7
            norm.contains("thvl1") || norm.contains("thvl 1") || norm.contains("v\u0129nh long 1") || normTvg.contains("thvl1") -> R.drawable.ic_logo_thvl1
            norm.contains("antv") || normTvg.contains("antv") -> R.drawable.ic_logo_antv
            norm.contains("vtc1") || norm.contains("vtc 1") || normTvg.contains("vtc1") -> R.drawable.ic_logo_vtc1
            else -> null
        }
    }

    fun getLogoUrl(channel: IptvChannel): String {
        if (!channel.logoUrl.isNullOrBlank()) {
            return channel.logoUrl
        }
        val normName = channel.name.lowercase().trim()
        val normTvg = (channel.tvgName ?: channel.tvgId ?: "").lowercase().trim()
        return when {
            normName.contains("vtv1") || normTvg.contains("vtv1") -> "GITHUB_LOGO_BASE/vtv1.png"
            normName.contains("vtv2") || normTvg.contains("vtv2") -> "GITHUB_LOGO_BASE/vtv2.png"
            normName.contains("vtv3") || normTvg.contains("vtv3") -> "GITHUB_LOGO_BASE/vtv3.png"
            normName.contains("vtv4") || normTvg.contains("vtv4") -> "GITHUB_LOGO_BASE/vtv4.png"
            normName.contains("vtv5") || normTvg.contains("vtv5") -> "GITHUB_LOGO_BASE/vtv5.png"
            normName.contains("vtv6") || normTvg.contains("vtv6") -> "GITHUB_LOGO_BASE/vtv6.png"
            normName.contains("vtv7") || normTvg.contains("vtv7") -> "GITHUB_LOGO_BASE/vtv7.png"
            normName.contains("vtv8") || normTvg.contains("vtv8") -> "GITHUB_LOGO_BASE/vtv8.png"
            normName.contains("vtv9") || normTvg.contains("vtv9") -> "GITHUB_LOGO_BASE/vtv9.png"
            else -> ""
        }
    }

    fun getProgramMock(channelName: String): Triple<String, String, String> {
        val norm = channelName.lowercase()
        return when {
            norm.contains("vtv1") -> Triple(
                "Th\u1eddi s\u1ef1 19h",
                "19:00 - 19:45",
                "B\u1ea3n tin th\u1eddi s\u1ef1 c\u1eadp nh\u1eadt nh\u1eefng tin t\u1ee9c m\u1edbi nh\u1ea5t trong ng\u00e0y."
            )
            norm.contains("vtv2") -> Triple(
                "Khoa h\u1ecdc & \u0110\u1eddi s\u1ed1ng",
                "19:30 - 20:15",
                "Kh\u00e1m ph\u00e1 th\u1ebf gi\u1edbi t\u1ef1 nhi\u00ean v\u00e0 c\u00e1c \u1ee9ng d\u1ee5ng c\u00f4ng ngh\u1ec7 hi\u1ec7n \u0111\u1ea1i."
            )
            norm.contains("vtv3") -> Triple(
                "Anh trai v\u01b0\u1ee3t ng\u00e0n ch\u00f4ng gai",
                "20:00 - 22:30",
                "Ch\u01b0\u01a1ng tr\u00ecnh truy\u1ec1n h\u00ecnh th\u1ef1c t\u1ebf \u00e2m nh\u1ea1c \u0111\u1ec9nh cao quy t\u1ee5 d\u00e0n ngh\u1ec7 s\u0129 h\u00e0ng \u0111\u1ea7u."
            )
            norm.contains("vtv4") -> Triple(
                "B\u1ea3n tin ti\u1ebfng Vi\u1ec7t",
                "18:30 - 19:15",
                "Nh\u1ecbp c\u1ea7u k\u1ebft n\u1ed1i ki\u1ec1u b\u00e0o Vi\u1ec7t Nam tr\u00ean kh\u1eafp th\u1ebf gi\u1edbi v\u1edbi qu\u00ea h\u01b0\u01a1ng."
            )
            norm.contains("vtv5") -> Triple(
                "S\u1eafc m\u00e0u v\u0103n h\u00f3a c\u00e1c d\u00e2n t\u1ed9c",
                "19:15 - 20:00",
                "T\u00f4n vinh v\u00e0 gi\u1edbi thi\u1ec7u n\u00e9t \u0111\u1eb9p truy\u1ec1n th\u1ed1ng c\u1ee7a 54 d\u00e2n t\u1ed9c anh em."
            )
            norm.contains("vtv6") || norm.contains("c\u1ea7n th\u01a1") -> Triple(
                "Kh\u00e1m ph\u00e1 th\u1ebf gi\u1edbi",
                "19:30 - 20:30",
                "H\u00e0nh tr\u00ecnh kh\u00e1m ph\u00e1 nh\u1eefng v\u00f9ng \u0111\u1ea5t k\u1ef3 v\u0129 v\u00e0 v\u0103n h\u00f3a \u0111\u1ed9c \u0111\u00e1o."
            )
            norm.contains("vtv7") -> Triple(
                "Tr\u01b0\u1eddng h\u1ecdc kh\u00f4ng kho\u1ea3ng c\u00e1ch",
                "19:00 - 20:00",
                "B\u00e0i gi\u1ea3ng ki\u1ebfn th\u1ee9c b\u1ed5 \u00edch d\u00e0nh cho h\u1ecdc sinh m\u1ecdi l\u1ee9a tu\u1ed5i."
            )
            norm.contains("vtv8") -> Triple(
                "Th\u1eddi s\u1ef1 Mi\u1ec1n Trung - T\u00e2y Nguy\u00ean",
                "19:45 - 20:15",
                "Th\u00f4ng tin th\u1eddi s\u1ef1 kinh t\u1ebf x\u00e3 h\u1ed9i n\u1ed5i b\u1eadt khu v\u1ef1c Mi\u1ec1n Trung."
            )
            norm.contains("vtv9") -> Triple(
                "Phim truy\u1ec7n",
                "20:00 - 21:00",
                "Phim truy\u1ec1n h\u00ecnh h\u1ea5p d\u1eabn ph\u00e1t s\u00f3ng khung gi\u1edd v\u00e0ng."
            )
            norm.contains("htv7") -> Triple(
                "Nhanh nh\u01b0 ch\u1edbp",
                "21:00 - 22:30",
                "Gameshow gi\u1ea3i tr\u00ed vui nh\u1ed9n v\u1edbi nh\u1eefng c\u00e2u \u0111\u1ed1 m\u1eb9o th\u00fa v\u1ecb."
            )
            norm.contains("thvl1") || norm.contains("v\u0129nh long 1") -> Triple(
                "Phim truy\u1ec7n Vi\u1ec7t Nam",
                "20:00 - 21:30",
                "\u0110\u00f3n xem nh\u1eefng b\u1ed9 phim truy\u1ec1n h\u00ecnh \u0111\u1eb7c s\u1eafc mi\u1ec1n T\u00e2y s\u00f4ng n\u01b0\u1edbc."
            )
            else -> Triple(
                "Ch\u01b0\u01a1ng tr\u00ecnh gi\u1ea3i tr\u00ed",
                "\u0110ang ph\u00e1t s\u00f3ng",
                "Ch\u01b0\u01a1ng tr\u00ecnh gi\u1ea3i tr\u00ed t\u1ed5ng h\u1ee3p h\u1ea5p d\u1eabn d\u00e0nh cho m\u1ecdi gia \u0111\u00ecnh."
            )
        }
    }
}
'''
with codecs.open('app/src/main/java/com/tvlaoto/data/provider/ChannelLogoProvider.kt', 'w', 'utf-8') as f:
    f.write(content)

print("ChannelLogoProvider written successfully")
