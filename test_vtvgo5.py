import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
try:
    url = "https://web-cache-aws.vtvdigital.vn/static/main.b01668db.v2.0.min.js"
    r = requests.get(url, headers=headers)
    js = r.text
    
    # find where web-api-vtvgo is used
    matches = re.findall(r".{0,100}web-api-vtvgo\.vtvdigital\.vn.{0,100}", js)
    for m in matches:
        print(m)
        
    print("----------------")
    matches = re.findall(r".{0,100}vtvgo-api-tdtv-v6\.vtvdigital\.vn.{0,100}", js)
    for m in matches:
        print(m)
        
    print("----------------")
    matches = re.findall(r".{0,100}/api/.{0,100}", js)
    for m in matches:
        if "token" in m or "stream" in m or "m3u8" in m:
            print(m)
            
except Exception as e:
    print(e)
