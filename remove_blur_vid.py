with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'\s*\.blur\(radius = [^)]+\)', '', content)
content = re.sub(r'import androidx\.compose\.ui\.draw\.blur\n', '', content)

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed .blur from VideoPlayerPanel.kt")
