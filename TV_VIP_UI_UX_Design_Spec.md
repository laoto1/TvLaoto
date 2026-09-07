# TV VIP --- UI/UX Design Specification

## 1. Mục tiêu

Thiết kế giao diện ứng dụng xem truyền hình trực tuyến cao cấp, hiện
đại, mượt và dễ sử dụng.

Phong cách tổng thể: - Premium / Luxury - Neon futuristic -
Glassmorphism - Gradient + Glow - Lấy cảm hứng từ không khí neon Miami /
cyberpunk / game AAA hiện đại - Có cảm giác tương tự các giao diện game
thế hệ mới, nhưng **không sao chép trực tiếp giao diện, logo hoặc tài
sản thương hiệu của GTA** - Ưu tiên trải nghiệm xem TV, không biến giao
diện thành một game UI quá nặng

Mục tiêu kỹ thuật: - Animation mượt nhưng nhẹ - Tối ưu cho máy yếu -
Không sử dụng hiệu ứng blur/glow quá nặng - Không tạo quá nhiều layer
hoặc particle - Ưu tiên GPU-friendly CSS/animation - Giao diện phải rõ
ràng khi dùng trên màn hình Full HD và 4K

------------------------------------------------------------------------

# 2. Layout tổng thể

Tỷ lệ thiết kế tham khảo: - Desktop: 16:9 - Canvas tham khảo: 1536 ×
1024 hoặc 1920 × 1080 - Responsive cho laptop, desktop và TV

Cấu trúc:

``` text
┌─────────────────────────────────────────────────────────────┐
│ LOGO       NAVIGATION                         SEARCH SETTING│
├───────────────────┬─────────────────────────────────────────┤
│                   │                                         │
│  DANH SÁCH KÊNH  │              VIDEO PLAYER               │
│                   │                                         │
│  Filter           │                                         │
│  Channel 01       │                                         │
│  Channel 02       │                                         │
│  Channel 03       │                                         │
│  Channel 04       │                                         │
│  Channel 05       │                                         │
│  Channel 06       │                                         │
│  Channel 07       │                                         │
│  Channel 08       │                                         │
│                   │─────────────────────────────────────────│
│                   │ Program information + Actions           │
├───────────────────┴─────────────────────────────────────────┤
│ TIME / DATE       │ BROADCAST NOTICE           │ NOW PLAYING │
└─────────────────────────────────────────────────────────────┘
```

**Không có khu vực "KÊNH NỔI BẬT".**

Khu vực video player và thông tin chương trình phải chiếm phần lớn không
gian màn hình.

------------------------------------------------------------------------

# 3. Header

Header nằm phía trên cùng.

### Logo

Logo dạng chữ:

``` text
TV VIP
PREMIUM
```

Phong cách: - Chữ TV lớn - Gradient cyan → blue → violet - VIP màu pink
/ magenta - Có thể có crown nhỏ phía trên VIP - Glow rất nhẹ

Không sử dụng glow mạnh làm mất độ sắc nét.

### Navigation

Các mục:

``` text
Truyền hình
Phim bộ
Thể thao
Thiếu nhi
Tin tức
Radio
```

Mỗi mục có icon đơn giản.

Tab đang chọn: - Background gradient nhẹ - Border sáng - Glow nhẹ - Text
sáng hơn

Ví dụ:

``` text
[ TV icon  Truyền hình ]
```

Active state có thể dùng gradient:

``` text
purple → pink
```

### Header actions

Bên phải:

``` text
[ Search ] [ Settings ] [ Avatar ] [ VIP ]
```

Button dạng circular glass.

------------------------------------------------------------------------

# 4. Channel Sidebar

Sidebar bên trái là thành phần quan trọng.

Tiêu đề:

``` text
DANH SÁCH KÊNH
```

Font: - Bold - Modern sans-serif - Có thể dùng gradient text rất nhẹ

### Filter

Các filter:

``` text
[Tất cả] [Yêu thích] [VTV] [VTVCab] [Filter]
```

Active filter: - Pink/purple gradient - Glow nhỏ - Border sáng

Inactive: - Dark glass - Border mảnh - Text xám sáng

------------------------------------------------------------------------

# 5. Channel Card

Mỗi kênh là một card ngang.

Ví dụ:

``` text
01    [VTV1]    VTV1 HD
                 Thời sự 19h                         ♡
```

Thông tin: - Số thứ tự - Logo kênh - Tên kênh - Chương trình hiện tại -
Favorite button

### Channel card bình thường

Background: - Dark navy - Slight transparency - Border mỏng - Border
radius khoảng 12--16px

### Channel đang chọn

Card active phải nổi bật:

-   Border gradient pink/purple
-   Background sáng hơn
-   Glow rất nhẹ
-   Có indicator nhỏ cho biết đang phát
-   Logo rõ hơn
-   Favorite icon sáng

Không dùng animation rung/lắc.

------------------------------------------------------------------------

# 6. Video Player

Video player là vùng lớn nhất bên phải.

Tỷ lệ đề xuất:

``` text
16:9
```

Border radius: - 16--24px

Container: - Dark glass - Border gradient - Shadow mềm

### Overlay

Góc trên:

``` text
● LIVE
```

LIVE badge: - Pink/red gradient - Chữ trắng - Có dot nhỏ

### Player controls

Ở cạnh dưới video:

``` text
[ Pause ] [ LIVE ] ────────────────●──── [ Volume ] [ Settings ] [ Fullscreen ]
```

Controls: - Tối giản - Icon trắng - Hover glow - Không quá nhiều nút

Progress bar: - Track màu dark - Active progress màu pink - Thumb màu
trắng

------------------------------------------------------------------------

# 7. Program Information

Ngay dưới video player.

Ví dụ:

``` text
Thời sự 19h     LIVE

19:00 - 19:45

Bản tin thời sự cập nhật những thông tin mới nhất trong ngày.
```

Bên phải:

``` text
[ ↻ Xem lại ] [ ♥ Yêu thích ] [ ↗ Chia sẻ ]
```

### Button style

Primary: - Pink / violet gradient - White text - Soft glow

Secondary: - Dark glass - Thin border

Hover: - Brighten - Translate Y khoảng -1px - Glow nhẹ

Không sử dụng animation quá lớn.

------------------------------------------------------------------------

# 8. Bottom Status Bar

Thanh trạng thái cố định ở cuối màn hình.

Chia thành 3 khu vực:

### Time

``` text
19:30
Thứ Sáu, 30/05/2025
```

### Broadcast notice

``` text
🔊 Thông báo:
Lịch phát sóng có thể thay đổi tùy theo nhà đài.
```

### Current channel

``` text
Wi-Fi icon
Đang phát: VTV1 HD
Signal icon
```

Background: - Dark glass - Border nhẹ - Radius lớn - Opacity vừa phải

------------------------------------------------------------------------

# 9. Color System

## Background

Primary:

``` text
#050816
```

Secondary:

``` text
#0B1024
```

Panel:

``` text
rgba(15, 20, 45, 0.80)
```

## Gradient

Primary gradient:

``` text
#7C3AED → #EC4899
```

Alternative:

``` text
#22D3EE → #8B5CF6 → #EC4899
```

## Text

Primary:

``` text
#FFFFFF
```

Secondary:

``` text
#B8BDD3
```

Muted:

``` text
#6F7694
```

## Accent

Pink:

``` text
#FF4FA3
```

Purple:

``` text
#8B5CF6
```

Cyan:

``` text
#22D3EE
```

------------------------------------------------------------------------

# 10. Glow System

Glow phải tiết chế.

### Small glow

Dùng cho: - Active button - Active channel - LIVE badge - Icons

Ví dụ concept:

``` css
box-shadow:
0 0 18px rgba(236, 72, 153, 0.20);
```

### Large glow

Chỉ dùng cho: - Logo - Hero player border - Active navigation

Không phủ glow lên toàn bộ UI.

------------------------------------------------------------------------

# 11. Glassmorphism

Panel nên có:

``` text
background:
rgba(10, 15, 35, 0.75)

border:
1px solid rgba(255,255,255,0.10)

backdrop-filter:
blur(10px)
```

Tuy nhiên phải có fallback cho máy yếu.

Máy yếu: - Giảm blur - Giảm shadow - Tắt decorative glow - Không ảnh
hưởng đến khả năng xem video

------------------------------------------------------------------------

# 12. Typography

Phong cách chữ: - Modern - Clean - Premium - Dễ đọc tiếng Việt

Ưu tiên:

``` text
Inter
Roboto
Be Vietnam Pro
SF Pro Display
```

Heading: - 600--700

Body: - 400--500

Không dùng font quá futuristic khiến tiếng Việt khó đọc.

------------------------------------------------------------------------

# 13. Icon Style

Icon phải đồng nhất.

Phong cách: - Outline - Rounded - Minimal

Các icon cần có: - TV - Movie - Sport - Kids - News - Radio - Search -
Settings - Heart - Share - Volume - Fullscreen - Filter - Wi-Fi -
Signal - Replay - Pause - Play

Không sử dụng icon 3D phức tạp.

------------------------------------------------------------------------

# 14. Animation

Animation phải mượt và nhẹ.

## Navigation

Hover:

``` text
transform: translateY(-1px)
opacity: 1
```

Transition:

``` text
150–200ms
ease-out
```

## Channel selection

Khi chọn: - Border fade-in - Background fade-in - Glow fade-in

Duration:

``` text
180–250ms
```

## Button

Hover: - Brightness tăng nhẹ - Glow tăng nhẹ - TranslateY -1px

Active: - Scale khoảng 0.98

Không dùng: - Bounce - Shake - Heavy spring - Particle explosion

------------------------------------------------------------------------

# 15. Performance / Low-End Mode

Đây là yêu cầu quan trọng.

UI phải hoạt động tốt trên máy yếu.

## Không nên dùng

``` text
❌ Nhiều particle
❌ Animated background liên tục
❌ Video background toàn màn hình
❌ Blur quá mạnh
❌ Box-shadow hàng trăm layer
❌ Canvas animation phức tạp
❌ SVG filter nặng
❌ 3D WebGL nếu không cần
```

## Nên dùng

``` text
✓ CSS transform
✓ CSS opacity
✓ CSS gradient
✓ Static background
✓ Một số glow nhẹ
✓ Lazy loading
✓ GPU-friendly animation
✓ will-change chỉ khi thực sự cần
```

Animation nên tập trung vào:

``` text
transform
opacity
```

Hạn chế animation trực tiếp:

``` text
width
height
top
left
box-shadow
filter
```

------------------------------------------------------------------------

# 16. Low Performance Mode

Nên có setting:

``` text
Hiệu năng

○ Cao
○ Cân bằng
● Tiết kiệm
```

### Cao

-   Blur
-   Glow
-   Gradient animation nhẹ
-   Shadow

### Cân bằng

-   Giảm blur
-   Giảm shadow
-   Tắt background animation

### Tiết kiệm

-   Không blur
-   Không animated gradient
-   Không decorative glow
-   Static UI
-   Chỉ giữ animation thiết yếu

Video playback vẫn phải hoạt động bình thường.

------------------------------------------------------------------------

# 17. Responsive

## Desktop

Sidebar:

``` text
360–420px
```

Player:

``` text
flex: 1
```

## Laptop

Sidebar:

``` text
300–340px
```

## Màn hình nhỏ

Sidebar có thể chuyển thành drawer:

``` text
[☰ Danh sách kênh]
```

Player đưa lên trên.

------------------------------------------------------------------------

# 18. UX Principles

Ưu tiên thứ tự:

``` text
1. Xem video
2. Chọn kênh
3. Biết chương trình đang phát
4. Điều khiển player
5. Tìm kiếm
6. Yêu thích
7. Cài đặt
```

Không để decorative elements cạnh tranh với video.

Người dùng phải có thể chọn kênh trong tối đa 1--2 thao tác.

------------------------------------------------------------------------

# 19. Visual Direction

Hình ảnh tổng thể nên có cảm giác:

``` text
Premium TV App
+
Miami Neon
+
Cyberpunk
+
AAA Game UI
+
Glassmorphism
```

Nhưng phải giữ:

``` text
Clean
Elegant
Fast
Readable
Functional
```

Không biến thành: - Gaming dashboard quá rối - Cyberpunk quá nhiều
neon - UI có quá nhiều panel - UI nhiều animation gây lag

------------------------------------------------------------------------

# 20. Background

Background có thể sử dụng hình ảnh thành phố neon / sunset / palm trees
/ futuristic urban environment.

Phong cách:

``` text
Miami sunset
Purple sky
Pink neon
Blue neon
Dark navy foreground
```

Background phải tối hơn UI để đảm bảo readability.

Có thể phủ một lớp:

``` text
rgba(3, 5, 18, 0.55)
```

để giảm độ tương phản của background.

Tránh background quá sáng phía sau text.

------------------------------------------------------------------------

# 21. Accessibility

Đảm bảo: - Text đủ tương phản - Button có vùng click tối thiểu khoảng
40--44px - Không chỉ dùng màu để thể hiện trạng thái - LIVE phải có
text + indicator - Focus state rõ ràng - Keyboard navigation hoạt động -
Font không quá nhỏ

------------------------------------------------------------------------

# 22. Component Structure

Nên chia component:

``` text
App
├── Header
│   ├── Logo
│   ├── Navigation
│   └── UserActions
│
├── MainLayout
│   ├── ChannelSidebar
│   │   ├── ChannelFilter
│   │   └── ChannelList
│   │       └── ChannelCard
│   │
│   └── Content
│       ├── VideoPlayer
│       └── ProgramInfo
│
└── StatusBar
    ├── Clock
    ├── BroadcastNotice
    └── CurrentChannel
```

**Không tạo component `FeaturedChannels` hoặc khu vực `Kênh nổi bật`.**

------------------------------------------------------------------------

# 23. Suggested Interaction

### Chọn kênh

``` text
Click ChannelCard
↓
Active channel thay đổi
↓
Player chuyển sang stream mới
↓
ProgramInfo cập nhật
↓
CurrentChannel cập nhật
```

Transition phải nhanh và không chặn thao tác.

### Favorite

``` text
Click Heart
↓
Icon chuyển trạng thái
↓
Animation nhỏ
↓
Lưu trạng thái
```

### Search

Search có thể lọc: - Tên kênh - Tên chương trình

Ví dụ:

``` text
Tìm kiếm "VTV"
→ VTV1
→ VTV3
→ VTV6
→ VTV9
```

------------------------------------------------------------------------

# 24. Sample Channel Data

``` json
[
  {
    "number": "01",
    "name": "VTV1 HD",
    "program": "Thời sự 19h",
    "category": "VTV",
    "live": true,
    "favorite": true
  },
  {
    "number": "02",
    "name": "VTV3 HD",
    "program": "Anh trai vượt ngàn chông gai",
    "category": "VTV",
    "live": true,
    "favorite": false
  },
  {
    "number": "03",
    "name": "VTV6 HD",
    "program": "Khám phá thế giới",
    "category": "VTV",
    "live": true,
    "favorite": false
  },
  {
    "number": "04",
    "name": "VTV9 HD",
    "program": "Phim truyện",
    "category": "VTV",
    "live": true,
    "favorite": false
  },
  {
    "number": "05",
    "name": "HTV7 HD",
    "program": "Phim trên HTV7",
    "category": "Khác",
    "live": true,
    "favorite": false
  },
  {
    "number": "06",
    "name": "THVL1 HD",
    "program": "Phim Việt Nam",
    "category": "Khác",
    "live": true,
    "favorite": false
  },
  {
    "number": "07",
    "name": "ANTV HD",
    "program": "An ninh toàn cảnh",
    "category": "Khác",
    "live": true,
    "favorite": false
  },
  {
    "number": "08",
    "name": "VTC1 HD",
    "program": "Tin tức 24h",
    "category": "Khác",
    "live": true,
    "favorite": false
  }
]
```

------------------------------------------------------------------------

# 25. Design Keywords

Nếu dùng AI để tạo UI/UX, có thể đưa các keyword sau:

``` text
premium TV streaming app
dark luxury interface
neon Miami aesthetic
purple pink cyan gradient
subtle glow
glassmorphism
AAA game-inspired UI
modern futuristic dashboard
clean TV channel selector
large live video player
dark navy background
high-end streaming service
smooth micro-interactions
low-performance friendly
minimal animation
responsive desktop UI
```

------------------------------------------------------------------------

# 26. Prompt mẫu cho AI UI Generator

``` text
Design a premium desktop TV streaming application UI.

Create a dark navy luxury interface inspired by modern AAA game dashboards and neon Miami aesthetics, using subtle purple, pink and cyan gradients.

The interface must contain:
- Premium TV VIP logo
- Top navigation for Television, Movies, Sports, Kids, News and Radio
- Search, Settings and User Profile buttons
- A left sidebar titled "DANH SÁCH KÊNH"
- Channel filters: Tất cả, Yêu thích, VTV, VTVCab
- A vertical list of TV channels
- A large 16:9 live video player on the right
- LIVE indicator
- Minimal video playback controls
- Program title and schedule below the player
- Replay, Favorite and Share buttons
- Bottom status bar with clock, broadcast notice and currently playing channel

Do NOT include a "KÊNH NỔI BẬT" / Featured Channels section.

Visual style:
- dark navy
- glassmorphism
- subtle neon glow
- elegant rounded cards
- thin luminous borders
- pink/purple/cyan gradients
- premium typography
- clean spacing
- polished AAA-game quality

Performance requirements:
- lightweight UI
- minimal blur
- minimal shadows
- no particle effects
- no heavy animated backgrounds
- animations should primarily use transform and opacity
- suitable for low-end computers

The final result should feel expensive, futuristic and polished while remaining practical as a real TV streaming application.
```

------------------------------------------------------------------------

# 27. Final Design Rule

**Công thức tổng thể:**

``` text
70% Functional TV UI
20% Premium Visual Design
10% Neon / Game-inspired Effects
```

Không đảo ngược tỷ lệ này.

Mục tiêu cuối cùng:

> Một ứng dụng xem truyền hình có cảm giác cao cấp như một sản phẩm giải
> trí AAA, nhưng vẫn nhẹ, nhanh, rõ ràng và thực dụng.
