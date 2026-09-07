from playwright.sync_api import sync_playwright
import time
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    all_requests = []
    all_responses = []
    
    def handle_request(req):
        url = req.url
        if "vtvdigital.vn" in url and ("source" in url or "m3u8" in url or "timeshift" in url or "catchup" in url or "stream" in url or "token" in url or "play" in url):
            all_requests.append({
                "url": url,
                "method": req.method,
                "post_data": req.post_data,
                "headers": {k: v for k, v in req.headers.items() if k in ['authorization', 'cookie', 'content-type', 'origin', 'referer', 'x-requested-with']}
            })
    
    def handle_response(res):
        url = res.url
        if "vtvdigital.vn" in url:
            try:
                ct = res.headers.get("content-type", "")
                if "json" in ct or "source" in url or "token" in url or "play" in url or "stream" in url:
                    body = res.text()
                    all_responses.append({
                        "url": url,
                        "status": res.status,
                        "method": res.request.method,
                        "post_data": res.request.post_data,
                        "body": body[:2000]
                    })
            except:
                pass
    
    page.on("request", handle_request)
    page.on("response", handle_response)
    
    # Load VTV1
    page.goto("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html")
    time.sleep(10)
    
    print("=== PHASE 1: INITIAL LOAD ===")
    print(f"Requests: {len(all_requests)}")
    for req in all_requests:
        print(json.dumps(req, indent=2, ensure_ascii=False))
    print(f"\nResponses: {len(all_responses)}")
    for res in all_responses:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    
    # Now click on a past program item
    print("\n\n=== PHASE 2: CLICK CATCHUP ===")
    all_requests.clear()
    all_responses.clear()
    
    # Try to find and click the first past program
    try:
        # Wait for React to fully render the EPG
        time.sleep(3)
        
        # Click the first program (which should be a past program)
        result = page.evaluate("""
            () => {
                // Find all elements that look like EPG program items
                const allElements = document.querySelectorAll('div, li, span, a, button');
                const programItems = [];
                for (const el of allElements) {
                    const text = el.textContent || '';
                    const cls = el.className || '';
                    if ((cls.includes('program') || cls.includes('Program') || cls.includes('epg') || cls.includes('schedule')) && text.length > 5 && text.length < 200) {
                        programItems.push({tag: el.tagName, cls: cls.substring(0, 100), text: text.substring(0, 80)});
                    }
                }
                return JSON.stringify(programItems.slice(0, 20));
            }
        """)
        print(f"Found program elements: {result}")
        
        # Try specific VTVGo React class names
        count = page.evaluate("document.querySelectorAll('[class*=\"program\"], [class*=\"Program\"], [class*=\"schedule\"], [class*=\"Schedule\"]').length")
        print(f"Elements matching program/schedule: {count}")
        
        # Get the entire page source to search for EPG-related classes
        html_snippet = page.evaluate("""
            () => {
                const body = document.body.innerHTML;
                // Find unique class names containing 'program', 'epg', 'schedule', 'replay'
                const matches = body.match(/class="[^"]*(?:program|epg|schedule|replay|catchup|timeshift)[^"]*"/gi);
                return JSON.stringify(matches ? matches.slice(0, 20) : []);
            }
        """)
        print(f"\nClass names found: {html_snippet}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(3)
    print(f"\nRequests after interaction: {len(all_requests)}")
    for req in all_requests:
        print(json.dumps(req, indent=2, ensure_ascii=False))
    print(f"\nResponses after interaction: {len(all_responses)}")
    for res in all_responses:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    
    browser.close()

