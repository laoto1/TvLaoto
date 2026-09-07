from playwright.sync_api import sync_playwright
import time
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--autoplay-policy=no-user-gesture-required"])
    page = browser.new_page()
    
    all_m3u8 = []
    all_api = []
    
    def handle_request(req):
        url = req.url
        if ".m3u8" in url or "timeshift" in url or "catchup" in url:
            all_m3u8.append({
                "url": url,
                "method": req.method,
                "headers": {k:v for k,v in req.headers.items() if k.lower() in ['authorization', 'cookie', 'referer', 'origin']}
            })
    
    def handle_response(res):
        url = res.url
        if "vtvdigital.vn" in url:
            ct = res.headers.get("content-type", "")
            if "json" in ct:
                try:
                    body = res.text()
                    if "m3u8" in body or "source" in url or "stream" in url or ".m3u8" in body:
                        all_api.append({
                            "url": url,
                            "method": res.request.method,
                            "post_data": res.request.post_data,
                            "status": res.status,
                            "body": body[:2000]
                        })
                except:
                    pass
    
    page.on("request", handle_request)
    page.on("response", handle_response)
    
    # Load VTV1 channel
    page.goto("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html", wait_until="networkidle")
    print("Page loaded, waiting for video...")
    time.sleep(15)
    
    print(f"=== M3U8 REQUESTS ({len(all_m3u8)}) ===")
    for m in all_m3u8:
        print(json.dumps(m, indent=2, ensure_ascii=False))
    
    print(f"\n=== API RESPONSES with m3u8 ({len(all_api)}) ===")
    for a in all_api:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    
    # Now try clicking the catchup tab or a past program
    print("\n=== TRYING TO INTERACT WITH EPG ===")
    all_m3u8.clear()
    all_api.clear()
    
    # Take screenshot to see what the page looks like
    page.screenshot(path="vtvgo_screenshot.png")
    print("Screenshot saved as vtvgo_screenshot.png")
    
    # Try to find the schedule/EPG section
    page_html = page.content()
    with open("vtvgo_page.html", "w", encoding="utf-8") as f:
        f.write(page_html)
    print("Full page HTML saved as vtvgo_page.html")
    
    # Find all links that look like catchup/replay
    links = page.evaluate("""
        () => {
            const links = [];
            document.querySelectorAll('a[href]').forEach(a => {
                const href = a.getAttribute('href') || '';
                const text = (a.textContent || '').trim().substring(0, 50);
                if (href.includes('channel') || href.includes('ts') || href.includes('replay') || href.includes('catchup') || text.match(/\\d{2}:\\d{2}/)) {
                    links.push({href, text});
                }
            });
            return JSON.stringify(links);
        }
    """)
    print(f"Relevant links: {links}")
    
    browser.close()

