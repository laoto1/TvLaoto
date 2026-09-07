import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
try:
    r = requests.get("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html", headers=headers)
    print("Status:", r.status_code)
    
    html = r.text
    
    # search for token or ajax
    import re
    matches = re.findall(r"ajax.*?url\s*:\s*['\"]([^'\"]+)['\"]", html, re.IGNORECASE)
    print("Ajax URLs:", matches)
    
    # Check if there is settoken
    if "setToken" in html or "token" in html:
        print("Contains token related code")
        
except Exception as e:
    print(e)
