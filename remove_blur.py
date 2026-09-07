with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'\.blur\(radiusX = 35\.dp, radiusY = 35\.dp[^)]+\)', '', content)
content = re.sub(r'import androidx\.compose\.ui\.draw\.blur\n', '', content)

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed .blur from HomeScreen.kt")
