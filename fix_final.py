import re

with open('app/src/main/java/com/tvlaoto/data/repository/ChannelRepository.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('import java.io.InputStream\nimport java.io.InputStream', 'import java.io.InputStream')

with open('app/src/main/java/com/tvlaoto/data/repository/ChannelRepository.kt', 'w', encoding='utf-8') as f:
    f.write(content)

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('GtaShapes.MediumCardShape', 'GtaShapes.LargeCardShape')
if 'import androidx.compose.foundation.layout.heightIn' not in content:
    content = content.replace('import androidx.compose.foundation.layout.height', 'import androidx.compose.foundation.layout.height\nimport androidx.compose.foundation.layout.heightIn')

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
