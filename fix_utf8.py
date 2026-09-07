import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace corrupted Vietnamese strings in UI
replacements = {
    r'Truy\?n hnh': 'Truyền hình',
    r'T\?t c\?': 'Tất cả',
    r'Yu thch': 'Yêu thích',
    r'Khng tm th\?y knh': 'Không tìm thấy kênh',
    r'B\? l\?c': 'Bộ lọc nâng cao',
    r'B\? L\?C NANG CAO': 'BỘ LỌC NÂNG CAO',
    r'DANH SACH KENH': 'DANH SÁCH KÊNH',
    r'Fade m\? d\?n d\?ng b\? v\?i n\?n': 'Fade mờ dần đồng bộ với nền',
    r'Trong su\?t \? gi\?a': 'Trong suốt ở giữa',
    r'H\?ng neon': 'Hồng neon',
    r'Da xo Knh n\?i b\?t': 'Đã xoá Kênh nổi bật',
    r'Phng to t\?i da': 'Phóng to tối đa',
    r'N\?n h\?ng m\? d\?u m\?t': 'Nền hồng mờ dịu mắt',
    r'N\?n xm m\? trong su\?t': 'Nền xám mờ trong suốt',
    r'Vi\?n h\?ng gradient': 'Viền hồng gradient',
    r'Vi\?n tr\?ng m\?': 'Viền trắng mờ',
    r'L\?p c\?c quang nh sng \(tu\? ch\?n thm d\? gi\?ng \?nh 1\)': 'Lớp cực quang ánh sáng (tuỳ chọn thêm để giống ảnh 1)'
}

for pattern, replacement in replacements.items():
    content = re.sub(pattern, replacement, content)

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced')
