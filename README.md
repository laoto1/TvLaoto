# 🌴 TvLaoto — Ứng Dụng Xem Kênh Truyền Hình Android TV Box (Phong Cách GTA VI)

Ứng dụng xem truyền hình trực tuyến (IPTV / M3U) chuyên biệt cho **Android TV Box**, **Smart TV** và **Android TV Emulator**. Giao diện lấy cảm hứng từ phong cách **GTA VI Vice City** với tông màu neon rực rỡ, hiệu ứng phát sáng (glow), chuyển cảnh mượt mà 60fps và được tối ưu đặc biệt cho các dòng **TV Box cấu hình yếu** (1GB - 2GB RAM, chip Amlogic / Rockchip / Allwinner).

---

## ✨ Điểm Nổi Bật & Tính Năng

- 🎮 **Thiết Kế GTA VI Vice City:**
  - Tông màu nền đen sâu kết hợp dải màu Neon Hot Pink (`#FF1493`), Electric Cyan (`#00E5FF`), Vice Purple (`#8B5CF6`) và Gold Highlight (`#FFD700`).
  - Thẻ kênh phóng to 1.08x và tỏa ánh sáng neon cyan khi di chuyển con trỏ (D-pad focus).
  - HUD trong suốt hiển thị thông tin kênh, thời gian thực, độ phân giải và danh mục khi chuyển kênh.
  - Màn hình Splash động mang đậm phong cách giới thiệu trailer GTA VI.

- ⚡ **Tối Ưu Hiệu Năng Cho TV Box Cấu Hình Yếu (60 FPS):**
  - **GPU-Only Transforms (`graphicsLayer`):** Mọi chuyển động phóng to, nảy spring, xoay và mờ dần được xử lý trực tiếp trên GPU RenderNode, **không kích hoạt tính toán layout hay recomposition**.
  - **Radial Glow Pre-baked:** Thay vì sử dụng Gaussian Blur thời gian thực gây nghẽn GPU Mali, ứng dụng sử dụng kỹ thuật vẽ Radial Gradient tối ưu bộ nhớ.
  - **Ảo Hóa Danh Sách (`TvLazyRow` / `LazyColumn`):** Chỉ hiển thị và cấp phát bộ nhớ cho các thẻ kênh xuất hiện trên màn hình.

- 📺 **Trình Phát Media3 (ExoPlayer) Chuyên Nghiệp:**
  - **SurfaceView:** Render video trực tiếp trên Hardware Overlay Layer, bỏ qua GPU Compositor giúp chống giật lag tuyệt đối.
  - **Instant Zapping (Chuyển kênh tức thì):** Tinh chỉnh bộ đệm khởi đầu 1.0s giúp kênh phát ngay lập tức khi bấm chuyển.
  - **Hỗ trợ đầy đủ luồng HLS (`.m3u8`) & MP4:** Tự động nhận diện User-Agent, Referrer và xử lý lỗi luồng phát.

- 📋 **Hỗ Trợ M3U Toàn Diện & Đa Ngôn Ngữ:**
  - Tích hợp sẵn danh sách kênh truyền hình Việt Nam (VTV, HTV, THVL, Hà Nội) & Quốc Tế (France 24, DW, Al Jazeera, Red Bull TV, NASA TV).
  - Hỗ trợ người dùng nhập đường dẫn M3U tùy chỉnh qua hộp thoại Cài Đặt.
  - Bộ phân tích M3U đơn luồng tốc độ cao, xử lý mượt mà file playlist dung lượng lớn (15.000+ kênh) mà không gây tràn bộ nhớ (OOM).
  - Hỗ trợ song ngữ **Tiếng Việt** và **Tiếng Anh**.

---

## 🎮 Hướng Dẫn Điều Khiển Bằng Remote TV (D-Pad)

| Phím Remote | Chức năng trong Màn hình chính (Home) | Chức năng trong Trình phát (Player) |
|---|---|---|
| **Lên (▲)** | Di chuyển con trỏ lên hàng danh mục trên | Chuyển đến kênh kế tiếp (Next Channel) |
| **Xuống (▼)** | Di chuyển con trỏ xuống hàng danh mục dưới | Chuyển về kênh trước đó (Previous Channel) |
| **Trái (◄) / Phải (►)** | Cuộn xem các kênh trong hàng | — |
| **OK / Enter** | Mở kênh đang chọn để xem toàn màn hình | Bật / Tắt thanh thông tin HUD kênh |
| **Back / Quay lại** | Thoát ứng dụng | Quay về màn hình danh sách kênh |

---

## 🏗️ Cấu Trúc Mã Nguồn

```
TvLaoto/
├── app/
│   ├── src/main/
│   │   ├── AndroidManifest.xml                  # Khai báo Leanback TV launcher & quyền
│   │   ├── java/com/tvlaoto/
│   │   │   ├── MainActivity.kt                  # Activity chính (toàn màn hình TV)
│   │   │   ├── TvLaotoApp.kt                    # Application class quản lý cài đặt toàn cục
│   │   │   ├── data/
│   │   │   │   ├── model/
│   │   │   │   │   ├── IptvChannel.kt           # Model kênh truyền hình
│   │   │   │   │   ├── IptvCategory.kt          # Model danh mục kênh
│   │   │   │   │   └── AppSettings.kt           # Model cài đặt người dùng
│   │   │   │   ├── parser/
│   │   │   │   │   └── M3uParser.kt             # Bộ phân tích M3U streaming chống OOM
│   │   │   │   └── repository/
│   │   │   │       └── ChannelRepository.kt     # Quản lý nguồn kênh (nội bộ & URL)
│   │   │   ├── player/
│   │   │   │   ├── TvPlayerFactory.kt           # Khởi tạo Media3 ExoPlayer tối ưu TV Box
│   │   │   │   └── PlayerViewModel.kt           # ViewModel quản lý phát & chuyển kênh
│   │   │   └── ui/
│   │   │       ├── theme/
│   │   │       │   ├── GtaColors.kt             # Bảng màu Neon GTA 6 Vice City
│   │   │       │   ├── GtaShapes.kt             # Bo tròn góc giao diện
│   │   │       │   └── GtaTheme.kt              # Theme Material3 TV
│   │   │       ├── components/
│   │   │       │   ├── ChannelCard.kt           # Thẻ kênh hiệu ứng phát sáng neon
│   │   │       │   ├── CategoryRow.kt           # Hàng danh mục cuộn ngang ảo hóa
│   │   │       │   ├── GradientHeader.kt        # Tiêu đề chữ gradient neon
│   │   │       │   ├── NeonDivider.kt           # Đường phân cách phát sáng
│   │   │       │   ├── LoadingIndicator.kt      # Vòng xoay neon nhấp nháy
│   │   │       │   ├── PlayerOverlay.kt         # HUD thông tin kênh trong suốt
│   │   │       │   └── SettingsDialog.kt        # Hộp thoại cài đặt URL M3U & ngôn ngữ
│   │   │       ├── screens/
│   │   │       │   ├── SplashScreen.kt          # Màn hình chào động GTA 6
│   │   │       │   ├── HomeScreen.kt            # Màn hình chính duyệt danh mục
│   │   │       │   └── PlayerScreen.kt          # Màn hình phát video toàn màn hình
│   │   │       └── navigation/
│   │   │           └── AppNavigation.kt         # Đồ thị điều hướng màn hình
│   │   └── res/
│   │       ├── values/strings.xml               # Ngôn ngữ mặc định (English)
│   │       ├── values-vi/strings.xml            # Ngôn ngữ Tiếng Việt
│   │       ├── values/colors.xml & themes.xml   # Resource màu và theme tối
│   │       ├── drawable/banner.xml              # TV Banner cho màn hình chủ Leanback
│   │       └── raw/demo_playlist.m3u            # Danh sách kênh demo chất lượng cao
```

---

## 🚀 Hướng Dẫn Biên Dịch & Cài Đặt (Build & Run)

1. **Mở dự án trong Android Studio:**
   - Chọn `File` -> `Open` -> Trỏ đến thư mục `TvLaoto`.
   - Android Studio sẽ tự động đồng bộ Gradle và tải các dependency.

2. **Biên dịch file APK:**
   - **Debug APK:** Chạy lệnh `./gradlew assembleDebug` hoặc chọn `Build` -> `Build Bundle(s) / APK(s)` -> `Build APK(s)`.
   - File APK xuất ra tại: `app/build/outputs/apk/debug/app-debug.apk`.

3. **Cài đặt lên Android TV Box:**
   - Bật **Tùy chọn cho nhà phát triển (Developer Options)** và **Gỡ lỗi USB / Mạng (ADB Debugging)** trên TV Box.
   - Kết nối qua ADB:
     ```bash
     adb connect <ĐỊA_CHỈ_IP_TV_BOX>:5555
     adb install -r app/build/outputs/apk/debug/app-debug.apk
     ```

