import re

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'Xem l[^\x00-\x7F\w]*i', 'Xem lại', content)
content = re.sub(r'Y[^\x00-\x7F\w]*u th[^\x00-\x7F\w]*ch', 'Yêu thích', content)

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed ProgramInfoPanel')
