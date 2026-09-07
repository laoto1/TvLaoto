from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    def handle_request(req):
        if ".m3u8" in req.url:
            print("Found m3u8:", req.url)
            
    page.on("request", handle_request)
    
    page.goto("https://vtvgo.vn/channel/vtv1-1,1.html")
    time.sleep(5)
    browser.close()
