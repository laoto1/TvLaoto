package com.tvlaoto.ui.util

import com.tvlaoto.R

/**
 * Maps channel names to local drawable resource IDs.
 * Returns null if no local logo exists (fallback to URL).
 */
object ChannelLogoMapper {

    private val logoMap = mapOf(
        // VTV channels
        "vtv1" to R.drawable.logo_vtv1,
        "vtv2" to R.drawable.logo_vtv2,
        "vtv3" to R.drawable.logo_vtv3,
        "vtv4" to R.drawable.logo_vtv4,
        "vtv5" to R.drawable.logo_vtv5,
        "vtv5taynambo" to R.drawable.logo_vtv5taynambo,
        "vtv5tnb" to R.drawable.logo_vtv5taynambo,
        "vtv5hdtâynambộ" to R.drawable.logo_vtv5taynambo,
        "vtv5taynguyen" to R.drawable.logo_vtv5taynguyen,
        "vtv5tn" to R.drawable.logo_vtv5taynguyen,
        "vtv5hdtâynguyên" to R.drawable.logo_vtv5taynguyen,
        "vtv6" to R.drawable.logo_vtv6,
        "vtv7" to R.drawable.logo_vtv7,
        "vtv8" to R.drawable.logo_vtv8,
        "vtv9" to R.drawable.logo_vtv9,
        "vtv10" to R.drawable.logo_vtv10,
        // THVL channels
        "thvl1" to R.drawable.logo_thvl1,
        "thvl2" to R.drawable.logo_thvl2,
        "thvl3" to R.drawable.logo_thvl3,
        "thvl4" to R.drawable.logo_thvl4,
        "thvl5" to R.drawable.logo_thvl5,
        // Trung ương
        "antv" to R.drawable.logo_antv,
        "qpvn" to R.drawable.logo_qpvn,
        // Địa phương
        "hànội1" to R.drawable.logo_hanoi1,
        "hànội2" to R.drawable.logo_hanoi2,
        "hưngyên" to R.drawable.logo_hungyen,
        "thanhhóa" to R.drawable.logo_thanhhoa,
        "nghệan" to R.drawable.logo_nghean,
        "phúthọ" to R.drawable.logo_phutho,
        "angiang" to R.drawable.logo_angiang,
        "ninhbình" to R.drawable.logo_ninhbinh,
        "quảngninh1" to R.drawable.logo_quangninh1,
        "đànẵng1" to R.drawable.logo_danang1,
        "quảngnam" to R.drawable.logo_quangnam,
        "đồngnai1" to R.drawable.logo_dongnai1,
        "đồngtháp1" to R.drawable.logo_dongthap1,
        "khánhhòa" to R.drawable.logo_khanhhoa,
        "laichâu" to R.drawable.logo_laichau,
        "tâyninh2" to R.drawable.logo_tayninh2,
        "tâyninh1" to R.drawable.logo_tayninh1,
        "tháinguyên" to R.drawable.logo_thainguyen,
        "tthuế" to R.drawable.logo_hue,
        "càmau" to R.drawable.logo_camau,
        "đắklắk" to R.drawable.logo_daklak,
        "hảiphòng" to R.drawable.logo_haiphong,
        "bìnhdương1" to R.drawable.logo_binhduong1,
        "điệnbiên" to R.drawable.logo_dienbien,
        "bắcninh" to R.drawable.logo_bacninh,
        "brvũngtàu" to R.drawable.logo_bariavungtau,
        "sơnla" to R.drawable.logo_sonla,
        "tuyênquang" to R.drawable.logo_tuyenquang,
        "gialai" to R.drawable.logo_gialai,
        "quảngtrị" to R.drawable.logo_quangtri,
        "làocai" to R.drawable.logo_laocai,
        "tháibình" to R.drawable.logo_thaibinh,
        "phúyên" to R.drawable.logo_phuyen,
        "bạcliêu" to R.drawable.logo_baclieu,
        "lâmđồng" to R.drawable.logo_lamdong,
        "hòabình" to R.drawable.logo_hoabinh,
        "hàgiang" to R.drawable.logo_hagiang,
        "bếntre" to R.drawable.logo_bentre,
        "tràvinh" to R.drawable.logo_travinh,
        "bìnhđịnh" to R.drawable.logo_binhdinh,
        "quảngtrị2" to R.drawable.logo_quangtri2,
        "kontum" to R.drawable.logo_kontum,
        "sóctrăng" to R.drawable.logo_soctrang,
        "bắckạn" to R.drawable.logo_backan,
        "cầnthơ1" to R.drawable.logo_cantho1,
        "cầnthơ2" to R.drawable.logo_cantho2,
        "bìnhthuận" to R.drawable.logo_binhthuan,
        "kiêngiang" to R.drawable.logo_kiengiang,
        "đắknông" to R.drawable.logo_daknong,
        "ninhthuận" to R.drawable.logo_ninhthuan,
        "hậugiang" to R.drawable.logo_haugiang,
        "tiềngiang" to R.drawable.logo_tiengiang,
        "đồngnai2" to R.drawable.logo_dongnai2,
        "vĩnhphúc" to R.drawable.logo_vinhphuc,
        "quảngninh3" to R.drawable.logo_quangninh3,
        "quảngngãi" to R.drawable.logo_quangngai,
        "namđịnh" to R.drawable.logo_namdinh,
        "bắcninh1" to R.drawable.logo_bacninh1,
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

