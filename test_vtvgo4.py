import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
try:
    url = "https://web-cache-aws.vtvdigital.vn/static/main.b01668db.v2.0.min.js"
    r = requests.get(url, headers=headers)
    js = r.text
    
    urls = set(re.findall(r"['\"](https?://[^'\"]+vtv[^'\"]+)['\"]", js, re.IGNORECASE))
    print("URLs found in JS:")
    for u in urls:
        print(u)
        
    api_paths = set(re.findall(r"['\"](/api/[^'\"]+)['\"]", js, re.IGNORECASE))
    print("\nAPI paths:")
    for p in api_paths:
        print(p)
        
    ajax = re.findall(r"\.post\(['\"]([^'\"]+)['\"]", js)
    print("\nPosts:", ajax)
    
except Exception as e:
    print(e)
