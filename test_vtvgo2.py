import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
try:
    r = requests.get("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html", headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    scripts = soup.find_all("script")
    
    for s in scripts:
        if s.string and ("ajax" in s.string.lower() or "token" in s.string.lower() or "m3u8" in s.string.lower() or "stream" in s.string.lower()):
            print("--- SCRIPT FOUND ---")
            lines = s.string.split("\n")
            for line in lines:
                if "url" in line.lower() or "ajax" in line.lower() or "token" in line.lower() or "type" in line.lower():
                    print(line.strip())
            
except Exception as e:
    print(e)
