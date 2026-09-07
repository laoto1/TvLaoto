with open('app/build.gradle.kts', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'implementation\("org\.mozilla\.geckoview:geckoview-omni[^"]+"\)', '', content)

with open('app/build.gradle.kts', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed geckoview from build.gradle.kts")
