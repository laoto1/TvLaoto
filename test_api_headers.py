from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    def handle_request(req):
        if "s-channels/source" in req.url:
            print("API URL:", req.url)
            print("Headers:", req.headers)
            print("Post Data:", req.post_data)
            
    page.on("request", handle_request)
    
    page.goto("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html")
    time.sleep(5)
    browser.close()
