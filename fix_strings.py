import codecs

vi_strings = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">TvLaoto</string>
    <string name="app_tagline">Truyền Hình Vice City GTA VI</string>
    <string name="all_channels">TẤT CẢ KÊNH</string>
    <string name="categories">DANH MỤC</string>
    <string name="search_hint">Tìm kiếm kênh hoặc số.</string>
    <string name="settings">CÀI ĐẶT</string>
    <string name="custom_m3u_url">Đường Dẫn Danh Sách M3U Tùy Chỉnh</string>
    <string name="enter_m3u_hint">https://example.com/danhsach.m3u</string>
    <string name="load_playlist">TẢI DANH SÁCH</string>
    <string name="reset_default">KHÔI PHỤC MẶC ĐỊNH</string>
    <string name="language">Ngôn Ngữ</string>
    <string name="vietnamese">Tiếng Việt</string>
    <string name="english">English</string>
    <string name="save">LƯU</string>
    <string name="cancel">HỦY</string>
    <string name="loading_channels">ĐANG KHỞI TẠO KÊNH TRUYỀN HÌNH...</string>
    <string name="no_channels_found">Không tìm thấy kênh nào</string>
    <string name="channel_error">Không thể phát luồng này. Vui lòng thử kênh khác.</string>
    <string name="retry">THỬ LẠI</string>
    <string name="now_playing">ĐANG PHÁT</string>
    <string name="press_back_exit">Nhấn BACK lần nữa để thoát</string>
    <string name="dpad_guide">Lên/Xuống: Đổi Kênh     OK: Thông Tin Kênh     BACK: Danh Sách</string>
    <string name="stream_error">LỖI LUỒNG PHÁT</string>
    <string name="favorite">Yêu thích</string>
    <string name="favorited">Đã thích</string>
    <string name="replay">Xem lại</string>
</resources>
"""

en_strings = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">TvLaoto</string>
    <string name="app_tagline">GTA VI Vice City IPTV</string>
    <string name="all_channels">ALL CHANNELS</string>
    <string name="categories">CATEGORIES</string>
    <string name="search_hint">Search channel or number.</string>
    <string name="settings">SETTINGS</string>
    <string name="custom_m3u_url">Custom M3U Playlist URL</string>
    <string name="enter_m3u_hint">https://example.com/playlist.m3u</string>
    <string name="load_playlist">LOAD PLAYLIST</string>
    <string name="reset_default">RESTORE DEMO PLAYLIST</string>
    <string name="language">Language</string>
    <string name="vietnamese">Tiếng Việt</string>
    <string name="english">English</string>
    <string name="save">SAVE</string>
    <string name="cancel">CANCEL</string>
    <string name="loading_channels">INITIALIZING VICE CITY CHANNELS...</string>
    <string name="no_channels_found">No channels found</string>
    <string name="channel_error">Unable to stream this channel. Please try another.</string>
    <string name="retry">RETRY</string>
    <string name="now_playing">NOW PLAYING</string>
    <string name="press_back_exit">Press BACK again to exit</string>
    <string name="dpad_guide">Up/Down: Change Channel     OK: Channel Info     BACK: Return to Grid</string>
    <string name="stream_error">STREAM ERROR</string>
    <string name="favorite">Favorite</string>
    <string name="favorited">Favorited</string>
    <string name="replay">Replay</string>
</resources>
"""

with codecs.open('app/src/main/res/values-vi/strings.xml', 'w', 'utf-8') as f:
    f.write(vi_strings)

with codecs.open('app/src/main/res/values/strings.xml', 'w', 'utf-8') as f:
    f.write(en_strings)

print("Updated strings.xml")
