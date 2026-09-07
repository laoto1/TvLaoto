import requests
import re
from bs4 import BeautifulSoup
import urllib.parse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
try:
    url = "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html"
    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    
    scripts = soup.find_all("script")
    
    # 1. Look for ajax calls in inline scripts
    for s in scripts:
        if s.string:
            if "ajax" in s.string.lower() or "post" in s.string.lower():
                matches = re.findall(r"url\s*:\s*['\"]([^'\"]+)['\"]", s.string)
                if matches:
                    print("Inline AJAX URLs:", matches)
                
    # 2. Extract external script URLs
    for s in scripts:
        if s.has_attr("src"):
            src = s["src"]
            if not src.startswith("http"):
                src = urllib.parse.urljoin(url, src)
            print("External JS:", src)
            
except Exception as e:
    print(e)
