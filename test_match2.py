import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'Truy.*?nh', content)
with open('debug_regex.txt', 'w', encoding='utf-8') as f:
    f.write('Truy: ' + str(matches) + '\n')
    f.write('Tất cả: ' + str(re.findall(r'T.*?t c.*?', content)))
