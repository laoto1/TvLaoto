import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# First, check EPG data structure
from datetime import datetime, timedelta

start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
end = start + timedelta(days=1)
epg_url = f"https://cache-api-vtvgo.vtvdigital.vn/cdn/live-channel/api/v1/channels/1/programs?startIsoDate={start.strftime('%Y-%m-%dT%H:%M:%S.000Z')}&endIsoDate={end.strftime('%Y-%m-%dT%H:%M:%S.000Z')}"

req = urllib.request.Request(epg_url)
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode("utf-8"))
    programs = data.get("data", [])
    print(f"Found {len(programs)} programs")
    for i, p in enumerate(programs[:3]):
        print(f"\nProgram {i}:")
        print(json.dumps(p, indent=2, ensure_ascii=False))

# Now test catchup API endpoints
print("\n\n=== TESTING CATCHUP API ENDPOINTS ===")

endpoints = [
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source",
        "data": {"channel_id": "1", "platform": "web"},
        "desc": "Live source API"
    },
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/timeshift",
        "data": {"channel_id": "1", "platform": "web"},
        "desc": "Timeshift API"
    },
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/catchup",
        "data": {"channel_id": "1", "platform": "web"},
        "desc": "Catchup API"
    },
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source",
        "data": {"channel_id": "1", "platform": "web", "type": "timeshift"},
        "desc": "Source API with timeshift type"
    },
]

for ep in endpoints:
    print(f"\n--- {ep['desc']} ---")
    print(f"URL: {ep['url']}")
    try:
        req = urllib.request.Request(ep["url"], method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        req.add_header("Origin", "https://vtvgo.vn")
        req.add_header("Referer", "https://vtvgo.vn/")
        post_data = json.dumps(ep["data"]).encode("utf-8")
        
        with urllib.request.urlopen(req, data=post_data, timeout=10) as response:
            body = response.read().decode("utf-8")
            print(f"Status: {response.status}")
            print(f"Body: {body[:800]}")
    except Exception as e:
        print(f"Error: {e}")

# Test: try to access the catchup URL LO shared directly to verify it works
print("\n\n=== TESTING DIRECT CATCHUP URL ACCESS ===")
test_url = "https://vtvgo-mhtimeshift.vtvdigital.vn/hN4yLx6QqiI9dyflNQVHBA/1788217628/manifest/ebc9b158-c887-4623-8742-f53902bf5a8e/e790e205-286e-4f23-ac9f-f0731df919ca/catchup/1080p/1080p.m3u8?d=eyJjb2RlY3MiOiJhdmMxLjY0MDAyOCxtcDRhLjQwLjIiLCJyZXNvbHV0aW9uIjp7IndpZHRoIjoxOTIwLCJoZWlnaHQiOjEwODB9LCJmcmFtZXJhdGUiOjI1LCJwYXRoIjoiIn0%3D&media=true&segmentPrefix=..%2F..%2F..%2F..%2F..%2Fvtv-timeshift&start=1788195624&stop=1788197484"

try:
    req = urllib.request.Request(test_url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    with urllib.request.urlopen(req, timeout=10) as response:
        body = response.read().decode("utf-8")
        print(f"Status: {response.status}")
        print(f"Body (first 500 chars): {body[:500]}")
except Exception as e:
    print(f"Error: {e}")

