import re

with open('app/src/main/java/com/tvlaoto/data/model/IptvChannel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('val currentProgram: String = "Chương trình trực tiếp"', 'val currentProgram: String = "Trực tiếp"')
content = content.replace('val programTime: String = "19:00 - 19:45"', 'val programTime: String = "Đang phát sóng"')
content = content.replace('val programDescription: String = "Bản tin thời sự cập nhật những tin tức mới nhất trong ngày."', 'val programDescription: String = ""')

with open('app/src/main/java/com/tvlaoto/data/model/IptvChannel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated IptvChannel defaults")
