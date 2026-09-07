import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace corrupted Vietnamese strings in UI
# We'll use a more generic wildcard to catch the replacement character
replacements = [
    (r'Truy\w*n h\w*nh', 'Truyền hình'),
    (r'T\w*t c\w*', 'Tất cả'),
    (r'Y\w*u th\w*ch', 'Yêu thích'),
    (r'Kh\w*ng t\w*m th\w*y k\w*nh', 'Không tìm thấy kênh'),
    (r'B\w* l\w*c', 'Bộ lọc nâng cao'),
    (r'B\w* L\w*C NANG CAO', 'BỘ LỌC NÂNG CAO'),
    (r'DANH SACH KENH', 'DANH SÁCH KÊNH'),
    (r'Fade m\w* d\w*n d\w*ng b\w* v\w*i n\w*n', 'Fade mờ dần đồng bộ với nền'),
    (r'Trong su\w*t \w* gi\w*a', 'Trong suốt ở giữa'),
    (r'H\w*ng neon', 'Hồng neon'),
    (r'Da xo\w* K\w*nh n\w*i b\w*t', 'Đã xoá Kênh nổi bật'),
    (r'Ph\w*ng to t\w*i da', 'Phóng to tối đa'),
    (r'N\w*n h\w*ng m\w* d\w*u m\w*t', 'Nền hồng mờ dịu mắt'),
    (r'N\w*n x\w*m m\w* trong su\w*t', 'Nền xám mờ trong suốt'),
    (r'Vi\w*n h\w*ng gradient', 'Viền hồng gradient'),
    (r'Vi\w*n tr\w*ng m\w*', 'Viền trắng mờ'),
    (r'L\w*p c\w*c quang \w*nh s\w*ng \(tu\w* ch\w*n th\w*m d\w* gi\w*ng \w*nh 1\)', 'Lớp cực quang ánh sáng (tuỳ chọn thêm để giống ảnh 1)')
]

for pattern, replacement in replacements:
    content = re.sub(pattern.replace(r'\w*', r'[^\x00-\x7F]*'), replacement, content)

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced')
