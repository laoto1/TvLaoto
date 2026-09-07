import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'Truy.*?nh', content)
print('Truy:', matches)
matches = re.findall(r'T.*?t c.*?', content)
print('Tất cả:', matches)
