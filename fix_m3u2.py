import re

with open('app/src/main/java/com/tvlaoto/data/parser/M3uParser.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'K.nh \$channelCounter', 'Kênh $channelCounter', content)

with open('app/src/main/java/com/tvlaoto/data/parser/M3uParser.kt', 'w', encoding='utf-8') as f:
    f.write(content)
