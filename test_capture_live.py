from playwright.sync_api import sync_playwright
import time
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    live_urls = []
    all_api = []
    
    def handle_request(req):
        url = req.url
        if ".m3u8" in url:
            live_urls.append(url)
    
    def handle_response(res):
        url = res.url
        if "vtvdigital.vn" in url and ("source" in url or "channel" in url or "stream" in url):
            try:
                body = res.text()
                all_api.append({
                    "url": url,
                    "method": res.request.method,
                    "post_data": res.request.post_data,
                    "request_headers": dict(res.request.headers),
                    "status": res.status,
                    "body": body[:2000]
                })
            except:
                all_api.append({"url": url, "error": "cant read"})
    
    page.on("request", handle_request)
    page.on("response", handle_response)
    
    page.goto("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html")
    time.sleep(10)
    
    print("=== LIVE M3U8 URLs ===")
    for url in live_urls:
        print(url)
    
    print(f"\n=== API RESPONSES ({len(all_api)}) ===")
    for api in all_api:
        print(json.dumps(api, indent=2, ensure_ascii=False))
    
    browser.close()

