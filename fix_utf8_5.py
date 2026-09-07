import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    (r'Truy[^\x00-\x7F\w]*n h[^\x00-\x7F\w]*nh', 'Truyền hình'),
    (r'T[^\x00-\x7F\w]*t c[^\x00-\x7F\w]*', 'Tất cả'),
    (r'Y[^\x00-\x7F\w]*u th[^\x00-\x7F\w]*ch', 'Yêu thích'),
    (r'Kh[^\x00-\x7F\w]*ng t[^\x00-\x7F\w]*m th[^\x00-\x7F\w]*y k[^\x00-\x7F\w]*nh', 'Không tìm thấy kênh'),
    (r'B[^\x00-\x7F\w]* l[^\x00-\x7F\w]*c n[^\x00-\x7F\w]*ng cao', 'Bộ lọc nâng cao'),
    (r'B[^\x00-\x7F\w]* l[^\x00-\x7F\w]*c', 'Bộ lọc nâng cao'),
    (r'B[^\x00-\x7F\w]* L[^\x00-\x7F\w]*C NANG CAO', 'BỘ LỌC NÂNG CAO'),
    (r'DANH SACH KENH', 'DANH SÁCH KÊNH'),
    (r'Fade m[^\x00-\x7F\w]* d[^\x00-\x7F\w]*n d[^\x00-\x7F\w]*ng b[^\x00-\x7F\w]* v[^\x00-\x7F\w]*i n[^\x00-\x7F\w]*n', 'Fade mờ dần đồng bộ với nền'),
    (r'Trong su[^\x00-\x7F\w]*t [^\x00-\x7F\w]* gi[^\x00-\x7F\w]*a', 'Trong suốt ở giữa'),
    (r'H[^\x00-\x7F\w]*ng neon', 'Hồng neon'),
    (r'Da xo[^\x00-\x7F\w]* K[^\x00-\x7F\w]*nh n[^\x00-\x7F\w]*i b[^\x00-\x7F\w]*t', 'Đã xoá Kênh nổi bật'),
    (r'Ph[^\x00-\x7F\w]*ng to t[^\x00-\x7F\w]*i da', 'Phóng to tối đa'),
    (r'N[^\x00-\x7F\w]*n h[^\x00-\x7F\w]*ng m[^\x00-\x7F\w]* d[^\x00-\x7F\w]*u m[^\x00-\x7F\w]*t', 'Nền hồng mờ dịu mắt'),
    (r'N[^\x00-\x7F\w]*n x[^\x00-\x7F\w]*m m[^\x00-\x7F\w]* trong su[^\x00-\x7F\w]*t', 'Nền xám mờ trong suốt'),
    (r'Vi[^\x00-\x7F\w]*n h[^\x00-\x7F\w]*ng gradient', 'Viền hồng gradient'),
    (r'Vi[^\x00-\x7F\w]*n tr[^\x00-\x7F\w]*ng m[^\x00-\x7F\w]*', 'Viền trắng mờ'),
    (r'L[^\x00-\x7F\w]*p c[^\x00-\x7F\w]*c quang [^\x00-\x7F\w]*nh s[^\x00-\x7F\w]*ng \(tu[^\x00-\x7F\w]* ch[^\x00-\x7F\w]*n th[^\x00-\x7F\w]*m d[^\x00-\x7F\w]* gi[^\x00-\x7F\w]*ng [^\x00-\x7F\w]*nh 1\)', 'Lớp cực quang ánh sáng (tuỳ chọn thêm để giống ảnh 1)')
]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print('Replaced exact strings with charset wildcard')
