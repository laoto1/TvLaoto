import re

with open('vtv.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Look for m3u8 or token or stream
matches = re.findall(r'https?://[^"\'\s]+\.m3u8[^"\'\s]*', content)
if matches:
    print("Found direct M3U8 in HTML:")
    for m in set(matches):
        print(m)
else:
    print("No direct m3u8 found.")
    
# Look for ajax endpoints
ajax = re.findall(r'url\s*:\s*["\'](.*?)["\']', content)
print("Ajax URLs:", set(ajax))
