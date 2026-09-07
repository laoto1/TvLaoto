import urllib.request

req_mobile = urllib.request.Request("https://vtvgo.vn/channel/vtv1-1,1.html", headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'})
try:
    resp = urllib.request.urlopen(req_mobile)
    html = resp.read().decode('utf-8')
    if "tải ứng dụng" in html.lower() or "download app" in html.lower() or "chuyển sang app" in html.lower() or "app-banner" in html.lower():
        print("Mobile version contains App Banner!")
    else:
        print("Mobile version seems clean.")
except Exception as e:
    print("Mobile error:", e)

req_desktop = urllib.request.Request("https://vtvgo.vn/channel/vtv1-1,1.html", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
try:
    resp = urllib.request.urlopen(req_desktop)
    html = resp.read().decode('utf-8')
    if "tải ứng dụng" in html.lower() or "download app" in html.lower() or "app-banner" in html.lower():
        print("Desktop version contains App Banner!")
    else:
        print("Desktop version seems clean.")
except Exception as e:
    print("Desktop error:", e)
