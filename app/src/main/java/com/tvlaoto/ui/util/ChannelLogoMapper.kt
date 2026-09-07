package com.tvlaoto.ui.util

import com.tvlaoto.R

/**
 * Maps channel names to local drawable resource IDs.
 * Returns null if no local logo exists (fallback to URL).
 */
object ChannelLogoMapper {

    private val logoMap = mapOf(
        "vtv1" to R.drawable.logo_vtv1,
        "vtv2" to R.drawable.logo_vtv2,
        "vtv3" to R.drawable.logo_vtv3,
        "vtv4" to R.drawable.logo_vtv4,
        "vtv5" to R.drawable.logo_vtv5,
        "vtv5taynambo" to R.drawable.logo_vtv5taynambo,
        "vtv5tnb" to R.drawable.logo_vtv5taynambo,
        "vtv5taynguyen" to R.drawable.logo_vtv5taynguyen,
        "vtv5tn" to R.drawable.logo_vtv5taynguyen,
        "vtv6" to R.drawable.logo_vtv6,
        "vtv7" to R.drawable.logo_vtv7,
        "vtv8" to R.drawable.logo_vtv8,
        "vtv9" to R.drawable.logo_vtv9,
        "thvl1" to R.drawable.logo_thvl1,
        "thvl2" to R.drawable.logo_thvl2,
        "thvl3" to R.drawable.logo_thvl3,
        "thvl4" to R.drawable.logo_thvl4,
        "thvl5" to R.drawable.logo_thvl5,
    )

    /**
     * Try to find a local drawable resource ID for the given channel name.
     * Matches by normalizing the channel name (lowercase, remove spaces/hd/special chars).
     */
    fun getLocalLogoResId(channelName: String): Int? {
        val normalized = channelName
            .lowercase()
            .replace(" hd", "")
            .replace(" ", "")
            .replace("tâynam bộ", "taynambo")
            .replace("tây nam bộ", "taynambo")
            .replace("tâynguyên", "taynguyen")
            .replace("tây nguyên", "taynguyen")
            .replace("vtvt", "vtv")  // Handle typo VTVT1 -> VTV1
            .trim()

        // Direct match
        logoMap[normalized]?.let { return it }

        // Fuzzy match: check if any key is contained in the name
        for ((key, resId) in logoMap) {
            if (normalized.contains(key)) {
                return resId
            }
        }

        return null
    }
}

