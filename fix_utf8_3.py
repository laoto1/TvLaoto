import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Truy?n hnh', 'Truyền hình')
content = content.replace('T?t c?', 'Tất cả')
content = content.replace('Yu thch', 'Yêu thích')
content = content.replace('Khng tm th?y knh', 'Không tìm thấy kênh')
content = content.replace('B? l?c nng cao', 'Bộ lọc nâng cao')
content = content.replace('B? L?C NANG CAO', 'BỘ LỌC NÂNG CAO')
content = content.replace('DANH SACH KENH', 'DANH SÁCH KÊNH')
content = content.replace('Fade m? d?n d?ng b? v?i n?n', 'Fade mờ dần đồng bộ với nền')
content = content.replace('Trong su?t ? gi?a', 'Trong suốt ở giữa')
content = content.replace('H?ng neon', 'Hồng neon')
content = content.replace('Da xo Knh n?i b?t', 'Đã xoá Kênh nổi bật')
content = content.replace('Phng to t?i da', 'Phóng to tối đa')
content = content.replace('N?n h?ng m? d?u m?t', 'Nền hồng mờ dịu mắt')
content = content.replace('N?n xm m? trong su?t', 'Nền xám mờ trong suốt')
content = content.replace('Vi?n h?ng gradient', 'Viền hồng gradient')
content = content.replace('Vi?n tr?ng m?', 'Viền trắng mờ')
content = content.replace('L?p c?c quang nh sng (tu? ch?n thm d? gi?ng ?nh 1)', 'Lớp cực quang ánh sáng (tuỳ chọn thêm để giống ảnh 1)')

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced exact strings')
