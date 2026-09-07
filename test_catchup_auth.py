import urllib.request
import json
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

# Step 1: Get guest token
print("=== STEP 1: GET GUEST TOKEN ===")
guest_data = json.dumps({
    "deviceId": "android-tvlaoto-001",
    "deviceName": "Chrome/Windows",
    "dtId": 1,
    "spId": "1",
    "platform": 6,
    "clientId": "null",
    "signature": "9ff524f035e4d172eef895de52d3c8b9",
    "versionCode": 20260603
}).encode("utf-8")

req = urllib.request.Request("https://web-api-vtvgo.vtvdigital.vn/user/nt/api/v1/auth/enter-guest", method="POST")
req.add_header("Content-Type", "application/json")
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
req.add_header("Origin", "https://vtvgo.vn")
req.add_header("Referer", "https://vtvgo.vn/")

with urllib.request.urlopen(req, data=guest_data, timeout=10) as response:
    auth_body = json.loads(response.read().decode("utf-8"))
    print(json.dumps(auth_body, indent=2, ensure_ascii=False))
    
    access_token = auth_body["data"]["accessToken"]
    print(f"\nAccess Token: {access_token[:50]}...")

# Step 2: Try to get live source with token
print("\n=== STEP 2: GET LIVE SOURCE ===")
source_data = json.dumps({
    "channel_id": "1",
    "platform": "web"
}).encode("utf-8")

req = urllib.request.Request("https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source", method="POST")
req.add_header("Content-Type", "application/json")
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
req.add_header("Origin", "https://vtvgo.vn")
req.add_header("Referer", "https://vtvgo.vn/")
req.add_header("Authorization", f"Bearer {access_token}")

try:
    with urllib.request.urlopen(req, data=source_data, timeout=10) as response:
        body = json.loads(response.read().decode("utf-8"))
        print(json.dumps(body, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'read'):
        print(f"Response: {e.read().decode('utf-8')}")

# Step 3: Try various endpoints for timeshift/catchup
print("\n=== STEP 3: TRY CATCHUP ENDPOINTS ===")

# Get the epoch timestamps from EPG
from datetime import datetime, timezone
start_epoch = int(datetime(2026, 9, 1, 0, 0, 0, tzinfo=timezone.utc).timestamp())
stop_epoch = int(datetime(2026, 9, 1, 0, 25, 0, tzinfo=timezone.utc).timestamp())
print(f"Start epoch: {start_epoch}, Stop epoch: {stop_epoch}")

endpoints = [
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/timeshift",
        "data": {"channel_id": "1", "platform": "web"},
        "desc": "Timeshift endpoint"
    },
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/timeshift",
        "data": {"channel_id": "1", "platform": "web", "start": start_epoch, "stop": stop_epoch},
        "desc": "Timeshift with start/stop"
    },
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/catchup",
        "data": {"channel_id": "1", "platform": "web", "start": start_epoch, "stop": stop_epoch},
        "desc": "Catchup with start/stop"
    },
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source",
        "data": {"channel_id": "1", "platform": "web", "type": "catchup", "start": start_epoch, "stop": stop_epoch},
        "desc": "Source with catchup type and times"
    },
    {
        "url": f"https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/1/timeshift?start={start_epoch}&stop={stop_epoch}",
        "data": None,
        "desc": "GET timeshift with channel in path",
        "method": "GET"
    },
]

for ep in endpoints:
    print(f"\n--- {ep['desc']} ---")
    method = ep.get("method", "POST")
    try:
        req = urllib.request.Request(ep["url"], method=method)
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        req.add_header("Origin", "https://vtvgo.vn")
        req.add_header("Referer", "https://vtvgo.vn/")
        req.add_header("Authorization", f"Bearer {access_token}")
        
        post_data = json.dumps(ep["data"]).encode("utf-8") if ep["data"] else None
        
        with urllib.request.urlopen(req, data=post_data, timeout=10) as response:
            body = response.read().decode("utf-8")
            print(f"Status: {response.status}")
            print(f"Body: {body[:1000]}")
    except Exception as e:
        error_body = ""
        if hasattr(e, 'read'):
            try:
                error_body = e.read().decode('utf-8')
            except:
                pass
        print(f"Error: {e}")
        if error_body:
            print(f"Response: {error_body[:500]}")

