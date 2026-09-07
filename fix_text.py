with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will use re.sub for robust replacements.

content = content.replace('Truy?n hnh', 'Truyền hình')
content = content.replace('T?t c?', 'Tất cả')
content = content.replace('Yu thch', 'Yêu thích')
content = content.replace('Khng tm th?y knh', 'Không tìm thấy kênh')
content = content.replace('B? L?C NANG CAO', 'BỘ LỌC NÂNG CAO')

content = content.replace('// N?n h?ng m? d?u m?t', '// Nền hồng mờ dịu mắt')
content = content.replace('// N?n xm m? trong su?t', '// Nền xám mờ trong suốt')
content = content.replace('// Vi?n h?ng gradient', '// Viền hồng gradient')
content = content.replace('// Vi?n tr?ng m?', '// Viền trắng mờ')
content = content.replace('// L?p c?c quang nh sng (tu? ch?n thm d? gi?ng ?nh 1)', '// Lớp cực quang ánh sáng (tuỳ chọn thêm để giống ảnh 1)')

content = content.replace('// LEFT COLUMN: DANH SACH KENH (Neon Glowing Frame)', '// LEFT COLUMN: DANH SÁCH KÊNH (Neon Glowing Frame)')
content = content.replace('// Fade mo dan dong bo voi nen', '// Fade mờ dần đồng bộ với nền')

# Also replace any other broken "T?t c?" like "T?t c" etc if missed, though exact match should work.

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
