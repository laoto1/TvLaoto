from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    def handle_response(res):
        if "vtvdigital.vn" in res.url and "api" in res.url:
            print("--- URL:", res.url)
            try:
                body = res.text()
                if ".m3u8" in body:
                    print("Contains m3u8! Body snippet:", body[:200])
                    print("Request Headers:", res.request.headers)
                    print("Request Data:", res.request.post_data)
            except:
                pass
                
    page.on("response", handle_response)
    
    page.goto("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html")
    time.sleep(5)
    browser.close()
