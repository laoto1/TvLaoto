from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    requests = []
    
    page.on("request", lambda request: requests.append(request.url) if "vtvdigital.vn" in request.url or "m3u8" in request.url else None)
    
    page.goto("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html")
    time.sleep(5)
    
    print("Requests after load:")
    for req in requests:
        if "programs" not in req and "cdn" not in req:
            print(req)
            
    print("Clicking a catchup program...")
    requests.clear()
    
    # Click the first .app-program-item
    page.evaluate("document.querySelector('.app-program-item').click()")
    time.sleep(3)
    
    print("Requests after click:")
    for req in requests:
        print(req)
        
    browser.close()
