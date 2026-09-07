import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Step 1: Get guest token (we need correct signature)
# From the Playwright intercept, we can see the enter-guest payload
# Let's replicate it exactly
print("=== STEP 1: GET GUEST TOKEN ===")

import uuid
import hashlib

device_id = str(uuid.uuid4())
version_code = 20260603

# The signature is likely md5 of some combination of fields
# Let's try to capture it from browser JS

# Actually, let's just use the token we already captured from Playwright
# Token: MSQxNzg4MjA0MDMxJDE3ODgyOTA0MzEkMCRHLTM5NTQ2MTkyMjYzJEctMzk1NDYxOTIyNjMkMjYzMDU5MzMtNjI3Mi00NzQyLWEzMzMtODQ0NDEzN2ZkMzJkJENocm9tZS9XaW5kb3dzJDIwMjYwNjAzJDYkJCQxJDEkJCQwMDAxMDM4NjY4OTIkMCQwJDE3MS4yMzUuMjQ4LjQ5JDEkVmlldCBOYW1fRG9uZyBOYWlfQmllbiBIb2EkMyR2aWV0dGVsLmNvbS52biQkMTc4ODIwNDAzMTc2NTczJCQkJCQwJDAkMSQkVk4.jw-1GVEPX4kuWmY9gTZttwpFqy_OK1UVKAzXKSATItg

access_token = "MSQxNzg4MjA0MDMxJDE3ODgyOTA0MzEkMCRHLTM5NTQ2MTkyMjYzJEctMzk1NDYxOTIyNjMkMjYzMDU5MzMtNjI3Mi00NzQyLWEzMzMtODQ0NDEzN2ZkMzJkJENocm9tZS9XaW5kb3dzJDIwMjYwNjAzJDYkJCQxJDEkJCQwMDAxMDM4NjY4OTIkMCQwJDE3MS4yMzUuMjQ4LjQ5JDEkVmlldCBOYW1fRG9uZyBOYWlfQmllbiBIb2EkMyR2aWV0dGVsLmNvbS52biQkMTc4ODIwNDAzMTc2NTczJCQkJCQwJDAkMSQkVk4.jw-1GVEPX4kuWmY9gTZttwpFqy_OK1UVKAzXKSATItg"

print(f"Using token: {access_token[:50]}...")

# Step 2: Get live source
print("\n=== STEP 2: GET LIVE SOURCE (channel 1 = VTV1) ===")
try:
    req = urllib.request.Request(
        "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source",
        method="POST"
    )
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    req.add_header("Origin", "https://vtvgo.vn")
    req.add_header("Referer", "https://vtvgo.vn/")
    req.add_header("Authorization", f"Bearer {access_token}")
    
    data = json.dumps({"channel_id": "1", "platform": "web"}).encode("utf-8")
    
    with urllib.request.urlopen(req, data=data, timeout=10) as response:
        body = json.loads(response.read().decode("utf-8"))
        print(json.dumps(body, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'read'):
        print(f"Response: {e.read().decode('utf-8')}")

# Step 3: Try different catchup/timeshift endpoints
print("\n=== STEP 3: TRY CATCHUP/TIMESHIFT ENDPOINTS ===")

from datetime import datetime, timezone
# Program at 00:00 UTC = 07:00 VN
start_epoch = int(datetime(2026, 9, 1, 0, 0, 0, tzinfo=timezone.utc).timestamp())
stop_epoch = int(datetime(2026, 9, 1, 0, 25, 0, tzinfo=timezone.utc).timestamp())

endpoints = [
    ("POST", "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source", {"channel_id": "1", "platform": "web"}),
    ("POST", "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/timeshift", {"channel_id": "1", "platform": "web", "start": start_epoch, "stop": stop_epoch}),
    ("POST", "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/timeshift", {"channel_id": "1", "platform": "web"}),
    ("POST", "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/catchup", {"channel_id": "1", "platform": "web", "start": start_epoch, "stop": stop_epoch}),
    ("POST", "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/catchup", {"channel_id": "1", "platform": "web"}),
    ("GET", f"https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/1/catchup?start={start_epoch}&stop={stop_epoch}", None),
    ("POST", "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source", {"channel_id": "1", "platform": "web", "type": "timeshift"}),
    ("POST", "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source", {"channel_id": "1", "platform": "web", "mode": "catchup", "start_time": start_epoch, "end_time": stop_epoch}),
]

for method, url, payload in endpoints:
    print(f"\n--- {method} {url} ---")
    if payload:
        print(f"  Payload: {json.dumps(payload)}")
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        req.add_header("Origin", "https://vtvgo.vn")
        req.add_header("Referer", "https://vtvgo.vn/")
        req.add_header("Authorization", f"Bearer {access_token}")
        
        post_data = json.dumps(payload).encode("utf-8") if payload else None
        
        with urllib.request.urlopen(req, data=post_data, timeout=10) as response:
            body = response.read().decode("utf-8")
            print(f"  Status: {response.status}")
            print(f"  Body: {body[:500]}")
    except Exception as e:
        error_body = ""
        if hasattr(e, 'read'):
            try: error_body = e.read().decode('utf-8')
            except: pass
        print(f"  Error: {e}")
        if error_body: print(f"  Response: {error_body[:300]}")

