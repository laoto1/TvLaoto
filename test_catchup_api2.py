from playwright.sync_api import sync_playwright
import time
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    api_calls = []
    m3u8_urls = []
    
    def handle_request(req):
        url = req.url
        if ".m3u8" in url or "timeshift" in url or "catchup" in url:
            m3u8_urls.append({"url": url, "method": req.method, "headers": dict(req.headers)})
    
    def handle_response(res):
        url = res.url
        if "vtvdigital.vn" in url:
            try:
                body = res.text()
                if ".m3u8" in body or "timeshift" in body or "catchup" in body or "source" in url:
                    api_calls.append({
                        "url": url,
                        "status": res.status,
                        "method": res.request.method,
                        "post_data": res.request.post_data,
                        "body_snippet": body[:1000] if body else ""
                    })
            except:
                pass
    
    page.on("request", handle_request)
    page.on("response", handle_response)
    
    # Load VTV1 and wait longer for React to render
    page.goto("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html")
    time.sleep(8)
    
    print("=== API CALLS WITH m3u8/timeshift/catchup/source ===")
    for call in api_calls:
        print(json.dumps(call, indent=2, ensure_ascii=False))
    
    print(f"\n=== M3U8 REQUESTS ({len(m3u8_urls)}) ===")
    for req in m3u8_urls:
        print(json.dumps(req, indent=2, ensure_ascii=False))
    
    # Try to find EPG items with different selectors
    print("\n=== DOM INSPECTION ===")
    selectors = ['.app-program-item', '.program-item', '[class*="program"]', '[class*="Program"]', '[class*="catchup"]', '[class*="replay"]']
    for sel in selectors:
        count = page.evaluate(f'document.querySelectorAll("{sel}").length')
        print(f"  {sel}: {count} elements")
    
    # Check what the page actually has
    print("\n=== PAGE INNER HTML (schedule area) ===")
    try:
        html = page.evaluate('document.querySelector("#schedule-container, #epg-container, .schedule, .epg, [class*=schedule], [class*=program-list]")?.innerHTML?.substring(0, 500) || "NOT FOUND"')
        print(html)
    except Exception as e:
        print(f"Error: {e}")
    
    # Try clicking the first program via different methods
    print("\n=== TRYING TO CLICK CATCHUP VIA /ts/ URL ===")
    api_calls.clear()
    m3u8_urls.clear()
    
    # Navigate to the /ts/ (timeshift) page directly
    page.goto("https://vtvgo.vn/channel/vtv1-1,1.html")
    time.sleep(8)
    
    print(f"Current URL after /ts/ nav: {page.url}")
    print(f"\n=== API CALLS AFTER /ts/ ({len(api_calls)}) ===")
    for call in api_calls:
        print(json.dumps(call, indent=2, ensure_ascii=False))
    
    print(f"\n=== M3U8 REQUESTS AFTER /ts/ ({len(m3u8_urls)}) ===")
    for req in m3u8_urls:
        print(json.dumps(req, indent=2, ensure_ascii=False))
    
    browser.close()

