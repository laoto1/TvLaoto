from playwright.sync_api import sync_playwright
import time
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    api_calls = []
    
    def handle_response(res):
        url = res.url
        if "vtvdigital.vn" in url and ("api" in url or "timeshift" in url or "catchup" in url or "m3u8" in url):
            try:
                body = res.text()
                api_calls.append({
                    "url": url,
                    "status": res.status,
                    "method": res.request.method,
                    "post_data": res.request.post_data,
                    "headers": dict(res.request.headers),
                    "body_snippet": body[:500] if body else ""
                })
            except:
                api_calls.append({"url": url, "status": res.status, "error": "could not read body"})
    
    page.on("response", handle_response)
    
    # Load VTV1
    page.goto("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html")
    time.sleep(5)
    
    print("=== INITIAL API CALLS ===")
    for call in api_calls:
        print(json.dumps(call, indent=2, ensure_ascii=False))
    
    # Now click on the first program item (catchup)
    print("\n=== CLICKING FIRST CATCHUP PROGRAM ===")
    api_calls.clear()
    
    try:
        items = page.query_selector_all('.app-program-item')
        print(f"Found {len(items)} program items")
        if items:
            items[0].click()
            time.sleep(5)
            
            print(f"\n=== API CALLS AFTER CLICK ({len(api_calls)}) ===")
            for call in api_calls:
                print(json.dumps(call, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
    
    browser.close()

