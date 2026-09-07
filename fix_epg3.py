import re

with open('app/src/main/java/com/tvlaoto/data/provider/ChannelLogoProvider.kt', 'r', encoding='utf-8') as f:
    content = f.read()

new_func = '''fun getDrawableFallback(channel: IptvChannel): Int? {
        val norm = channel.name.lowercase().trim()
        val normTvg = (channel.tvgName ?: channel.tvgId ?: "").lowercase().trim()

        return when {
            norm.contains("vtv1") || norm.contains("vtv 1") || normTvg.contains("vtv1") -> R.drawable.ic_logo_vtv1
            norm.contains("vtv3") || norm.contains("vtv 3") || normTvg.contains("vtv3") -> R.drawable.ic_logo_vtv3
            norm.contains("vtv6") || norm.contains("vtv 6") || normTvg.contains("vtv6") || norm.contains("cần thơ") -> R.drawable.ic_logo_vtv6
            norm.contains("vtv9") || norm.contains("vtv 9") || normTvg.contains("vtv9") -> R.drawable.ic_logo_vtv9
            norm.contains("htv7") || norm.contains("htv 7") || normTvg.contains("htv7") -> R.drawable.ic_logo_htv7
            norm.contains("thvl1") || norm.contains("thvl 1") || norm.contains("vĩnh long 1") || normTvg.contains("thvl1") -> R.drawable.ic_logo_thvl1
            norm.contains("antv") || normTvg.contains("antv") -> R.drawable.ic_logo_antv
            norm.contains("vtc1") || norm.contains("vtc 1") || normTvg.contains("vtc1") -> R.drawable.ic_logo_vtc1
            else -> null
        }
    }'''

content = re.sub(r'fun getDrawableFallback.*?\n    }', new_func, content, flags=re.DOTALL)

with open('app/src/main/java/com/tvlaoto/data/provider/ChannelLogoProvider.kt', 'w', encoding='utf-8') as f:
    f.write(content)
