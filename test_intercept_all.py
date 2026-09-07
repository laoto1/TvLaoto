from playwright.sync_api import sync_playwright
import time
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    source_calls = []
    
    def handle_request(req):
        url = req.url
        if "vtvdigital.vn" in url and ("source" in url or "timeshift" in url or "catchup" in url or "enter-guest" in url):
            source_calls.append({
                "phase": "request",
                "url": url,
                "method": req.method,
                "post_data": req.post_data,
                "headers": dict(req.headers)
            })
    
    def handle_response(res):
        url = res.url
        if "vtvdigital.vn" in url and ("source" in url or "timeshift" in url or "catchup" in url or "enter-guest" in url or "m3u8" in url):
            try:
                body = res.text()
                source_calls.append({
                    "phase": "response",
                    "url": url,
                    "status": res.status,
                    "body": body[:3000]
                })
            except:
                source_calls.append({"phase": "response", "url": url, "error": "cant read"})
    
    page.on("request", handle_request)
    page.on("response", handle_response)
    
    # Load VTV1 channel page
    page.goto("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html")
    time.sleep(15)  # Wait for React to fully render and fetch data
    
    print(f"=== CAPTURED {len(source_calls)} CALLS ===")
    for call in source_calls:
        print(json.dumps(call, indent=2, ensure_ascii=False))
    
    # Now try to find and click a catchup program after React renders
    print("\n\n=== TRYING TO FIND EPG ELEMENTS ===")
    
    # Check if there are any clickable program items 
    result = page.evaluate("""
        () => {
            // Search for all text content that looks like a time format (HH:mm)
            const allElements = document.querySelectorAll('*');
            const timeElements = [];
            for (const el of allElements) {
                if (el.children.length === 0 || el.children.length <= 3) {
                    const text = (el.textContent || '').trim();
                    if (/^\\d{2}:\\d{2}$/.test(text)) {
                        const parent = el.parentElement;
                        const grandparent = parent ? parent.parentElement : null;
                        timeElements.push({
                            tag: el.tagName,
                            cls: (el.className || '').substring(0, 100),
                            text: text,
                            parentTag: parent ? parent.tagName : 'none',
                            parentCls: parent ? (parent.className || '').substring(0, 100) : '',
                            grandparentCls: grandparent ? (grandparent.className || '').substring(0, 100) : ''
                        });
                    }
                }
            }
            return JSON.stringify(timeElements.slice(0, 10));
        }
    """)
    print(f"Time elements: {result}")
    
    # Click on the first schedule item
    print("\n=== CLICKING FIRST SCHEDULE ITEM ===")
    source_calls.clear()
    
    click_result = page.evaluate("""
        () => {
            const allElements = document.querySelectorAll('*');
            for (const el of allElements) {
                if (el.children.length === 0 || el.children.length <= 3) {
                    const text = (el.textContent || '').trim();
                    if (/^\\d{2}:\\d{2}$/.test(text)) {
                        // Found a time element, click its closest interactive parent
                        let target = el;
                        for (let i = 0; i < 5; i++) {
                            if (target.parentElement) target = target.parentElement;
                            if (target.onclick || target.tagName === 'A' || target.tagName === 'BUTTON') break;
                        }
                        target.click();
                        return 'Clicked: ' + text + ' on ' + target.tagName + '.' + (target.className || '').substring(0, 50);
                    }
                }
            }
            return 'No time elements found';
        }
    """)
    print(f"Click result: {click_result}")
    time.sleep(8)
    
    print(f"\n=== CALLS AFTER CLICK ({len(source_calls)}) ===")
    for call in source_calls:
        print(json.dumps(call, indent=2, ensure_ascii=False))
    
    browser.close()

