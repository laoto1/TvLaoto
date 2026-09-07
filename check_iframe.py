with open('vtv.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
iframes = re.findall(r'<iframe.*?src=["\'](.*?)["\']', content, re.IGNORECASE)
print("IFRAMES:", iframes)
