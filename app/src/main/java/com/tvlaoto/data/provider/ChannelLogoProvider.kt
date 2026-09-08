package com.tvlaoto.data.provider

import com.tvlaoto.R
import com.tvlaoto.data.model.IptvChannel

object ChannelLogoProvider {

    private const val GITHUB_LOGO_BASE =
        "https://raw.githubusercontent.com/AqFad2811/epg-iptv-logos/main/logos/vn"

    fun getDrawableFallback(channel: IptvChannel): Int? {
        val norm = channel.name.lowercase().trim()
        val normTvg = (channel.tvgName ?: channel.tvgId ?: "").lowercase().trim()

        return when {
            // VTV5 variants MUST come before generic VTV5
            norm.contains("tây nam") || norm.contains("taynambo") || norm.contains("tnb") ||
            normTvg.contains("tây nam") || normTvg.contains("taynambo") -> R.drawable.logo_vtv5taynambo
            norm.contains("tây nguyên") || norm.contains("taynguyen") || 
            normTvg.contains("tây nguyên") || normTvg.contains("taynguyen") -> R.drawable.logo_vtv5taynguyen

            // VTV channels
            norm.contains("vtv1") || norm.contains("vtvt1") || normTvg.contains("vtv1") -> R.drawable.logo_vtv1
            norm.contains("vtv2") || normTvg.contains("vtv2") -> R.drawable.logo_vtv2
            norm.contains("vtv3") || normTvg.contains("vtv3") -> R.drawable.logo_vtv3
            norm.contains("vtv4") || normTvg.contains("vtv4") -> R.drawable.logo_vtv4
            norm.contains("vtv5") || normTvg.contains("vtv5") -> R.drawable.logo_vtv5
            norm.contains("vtv6") || normTvg.contains("vtv6") -> R.drawable.logo_vtv6
            norm.contains("vtv7") || normTvg.contains("vtv7") -> R.drawable.logo_vtv7
            norm.contains("vtv8") || normTvg.contains("vtv8") -> R.drawable.logo_vtv8
            norm.contains("vtv9") || normTvg.contains("vtv9") -> R.drawable.logo_vtv9
            norm.contains("vtv10") || normTvg.contains("vtv10") -> R.drawable.logo_vtv10

            // THVL channels
            norm.contains("thvl1") || norm.contains("vĩnh long 1") || normTvg.contains("thvl1") -> R.drawable.logo_thvl1
            norm.contains("thvl2") || norm.contains("vĩnh long 2") || normTvg.contains("thvl2") -> R.drawable.logo_thvl2
            norm.contains("thvl3") || norm.contains("vĩnh long 3") || normTvg.contains("thvl3") -> R.drawable.logo_thvl3
            norm.contains("thvl4") || norm.contains("vĩnh long 4") || normTvg.contains("thvl4") -> R.drawable.logo_thvl4
            norm.contains("thvl5") || norm.contains("vĩnh long 5") || normTvg.contains("thvl5") -> R.drawable.logo_thvl5

            // Trung ương
            norm.contains("antv") || norm.contains("công an") -> R.drawable.logo_antv
            norm.contains("qpvn") || norm.contains("quốc phòng") -> R.drawable.logo_qpvn

            // Địa phương - specific variants first (e.g. "Quảng Ninh 3" before "Quảng Ninh 1")
            norm.contains("quảng ninh 3") || norm == "quảng ninh 3" -> R.drawable.logo_quangninh3
            norm.contains("quảng ninh 1") || norm == "quảng ninh 1" -> R.drawable.logo_quangninh1
            norm.contains("đồng nai 2") -> R.drawable.logo_dongnai2
            norm.contains("đồng nai 1") || norm == "đồng nai 1" -> R.drawable.logo_dongnai1
            norm.contains("đồng tháp") -> R.drawable.logo_dongthap1
            norm.contains("tây ninh 2") -> R.drawable.logo_tayninh2
            norm.contains("tây ninh 1") || norm == "tây ninh 1" -> R.drawable.logo_tayninh1
            norm.contains("quảng trị 2") -> R.drawable.logo_quangtri2
            norm.contains("cần thơ 2") -> R.drawable.logo_cantho2
            norm.contains("cần thơ 1") || norm == "cần thơ 1" -> R.drawable.logo_cantho1
            norm.contains("bắc ninh 1") -> R.drawable.logo_bacninh1
            norm.contains("bình dương") -> R.drawable.logo_binhduong1
            norm.contains("đà nẵng") -> R.drawable.logo_danang1
            norm.contains("hà nội 1") -> R.drawable.logo_hanoi1
            norm.contains("hà nội 2") -> R.drawable.logo_hanoi2

            // Địa phương - single province names
            norm.contains("hưng yên") -> R.drawable.logo_hungyen
            norm.contains("thanh hóa") -> R.drawable.logo_thanhhoa
            norm.contains("nghệ an") -> R.drawable.logo_nghean
            norm.contains("phú thọ") -> R.drawable.logo_phutho
            norm.contains("an giang") -> R.drawable.logo_angiang
            norm.contains("ninh bình") -> R.drawable.logo_ninhbinh
            norm.contains("quảng nam") -> R.drawable.logo_quangnam
            norm.contains("khánh hòa") -> R.drawable.logo_khanhhoa
            norm.contains("lai châu") -> R.drawable.logo_laichau
            norm.contains("thái nguyên") -> R.drawable.logo_thainguyen
            norm.contains("huế") || norm.contains("tt huế") -> R.drawable.logo_hue
            norm.contains("cà mau") -> R.drawable.logo_camau
            norm.contains("đắk lắk") || norm.contains("đắc lắc") -> R.drawable.logo_daklak
            norm.contains("hải phòng") -> R.drawable.logo_haiphong
            norm.contains("điện biên") -> R.drawable.logo_dienbien
            norm.contains("bắc ninh") -> R.drawable.logo_bacninh
            norm.contains("vũng tàu") || norm.contains("br vũng tàu") -> R.drawable.logo_bariavungtau
            norm.contains("sơn la") -> R.drawable.logo_sonla
            norm.contains("tuyên quang") -> R.drawable.logo_tuyenquang
            norm.contains("gia lai") -> R.drawable.logo_gialai
            norm.contains("quảng trị") -> R.drawable.logo_quangtri
            norm.contains("lào cai") -> R.drawable.logo_laocai
            norm.contains("thái bình") -> R.drawable.logo_thaibinh
            norm.contains("phú yên") -> R.drawable.logo_phuyen
            norm.contains("bạc liêu") -> R.drawable.logo_baclieu
            norm.contains("lâm đồng") -> R.drawable.logo_lamdong
            norm.contains("hòa bình") -> R.drawable.logo_hoabinh
            norm.contains("hà giang") -> R.drawable.logo_hagiang
            norm.contains("bến tre") -> R.drawable.logo_bentre
            norm.contains("trà vinh") -> R.drawable.logo_travinh
            norm.contains("bình định") -> R.drawable.logo_binhdinh
            norm.contains("kon tum") -> R.drawable.logo_kontum
            norm.contains("sóc trăng") -> R.drawable.logo_soctrang
            norm.contains("bắc kạn") || norm.contains("bắc cạn") -> R.drawable.logo_backan
            norm.contains("bình thuận") -> R.drawable.logo_binhthuan
            norm.contains("kiên giang") -> R.drawable.logo_kiengiang
            norm.contains("đắk nông") || norm.contains("đăk nông") -> R.drawable.logo_daknong
            norm.contains("ninh thuận") -> R.drawable.logo_ninhthuan
            norm.contains("hậu giang") -> R.drawable.logo_haugiang
            norm.contains("tiền giang") -> R.drawable.logo_tiengiang
            norm.contains("vĩnh phúc") -> R.drawable.logo_vinhphuc
            norm.contains("quảng ninh") -> R.drawable.logo_quangninh1
            norm.contains("quảng ngãi") -> R.drawable.logo_quangngai
            norm.contains("nam định") -> R.drawable.logo_namdinh
            norm.contains("lạng sơn") -> R.drawable.logo_langson
            norm.contains("cao bằng") -> R.drawable.logo_caobang
            norm.contains("hà tĩnh") -> R.drawable.logo_hatinh
            else -> null
        }
    }

    fun getLogoUrl(channel: IptvChannel): String {
        // Local drawable is always preferred (handled by getDrawableFallback)
        // Only return URL as fallback when no local drawable exists
        if (getDrawableFallback(channel) != null) {
            return "" // Empty = will use local drawable instead
        }
        // Fallback to URL from playlist if available
        return channel.logoUrl ?: ""
    }

    fun getProgramMock(channelName: String): Triple<String, String, String> {
        val norm = channelName.lowercase()
        return when {
            norm.contains("vtv1") -> Triple(
                "Thời sự 19h",
                "19:00 - 19:45",
                "Bản tin thời sự cập nhật những tin tức mới nhất trong ngày."
            )
            norm.contains("vtv2") -> Triple(
                "Khoa học & Đời sống",
                "19:30 - 20:15",
                "Khám phá thế giới tự nhiên và các ứng dụng công nghệ hiện đại."
            )
            norm.contains("vtv3") -> Triple(
                "Anh trai vượt ngàn chông gai",
                "20:00 - 22:30",
                "Chương trình truyền hình thực tế âm nhạc đỉnh cao quy tụ dàn nghệ sĩ hàng đầu."
            )
            norm.contains("vtv4") -> Triple(
                "Bản tin tiếng Việt",
                "18:30 - 19:15",
                "Nhịp cầu kết nối kiều bào Việt Nam trên khắp thế giới với quê hương."
            )
            norm.contains("vtv5") -> Triple(
                "Sắc màu văn hóa các dân tộc",
                "19:15 - 20:00",
                "Tôn vinh và giới thiệu nét đẹp truyền thống của 54 dân tộc anh em."
            )
            norm.contains("vtv6") || norm.contains("cần thơ") -> Triple(
                "Khám phá thế giới",
                "19:30 - 20:30",
                "Hành trình khám phá những vùng đất kỳ vĩ và văn hóa độc đáo."
            )
            norm.contains("vtv7") -> Triple(
                "Trường học không khoảng cách",
                "19:00 - 20:00",
                "Bài giảng kiến thức bổ ích dành cho học sinh mọi lứa tuổi."
            )
            norm.contains("vtv8") -> Triple(
                "Thời sự Miền Trung - Tây Nguyên",
                "19:45 - 20:15",
                "Thông tin thời sự kinh tế xã hội nổi bật khu vực Miền Trung."
            )
            norm.contains("vtv9") -> Triple(
                "Phim truyện",
                "20:00 - 21:00",
                "Phim truyền hình hấp dẫn phát sóng khung giờ vàng."
            )
            norm.contains("htv7") -> Triple(
                "Nhanh như chớp",
                "21:00 - 22:30",
                "Gameshow giải trí vui nhộn với những câu đố mẹo thú vị."
            )
            norm.contains("thvl1") || norm.contains("vĩnh long 1") -> Triple(
                "Phim truyện Việt Nam",
                "20:00 - 21:30",
                "Đón xem những bộ phim truyền hình đặc sắc miền Tây sông nước."
            )
            else -> Triple(
                "Chương trình giải trí",
                "Đang phát sóng",
                "Chương trình giải trí tổng hợp hấp dẫn dành cho mọi gia đình."
            )
        }
    }
}
