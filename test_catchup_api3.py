import urllib.request
import json

# Try the VTVGo source API that the website calls to get stream URLs
# Based on the URL pattern LO shared, the catchup URL looks like it comes from 
# an API that provides timeshift stream data

# First, let's check what the EPG data looks like for channel 1 (VTV1)
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
    if programs:
        # Print first program's full data
        print("\nFirst program:")
        print(json.dumps(programs[0], indent=2, ensure_ascii=False))
        print("\nSecond program:")
        if len(programs) > 1:
            print(json.dumps(programs[1], indent=2, ensure_ascii=False))

# Now let's try different API endpoints for getting catchup/timeshift URLs
print("\n\n=== TESTING CATCHUP API ENDPOINTS ===")

# Try 1: web-api-vtvgo source endpoint with timeshift params
endpoints = [
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source",
        "data": {"channel_id": "1", "platform": "web"},
        "desc": "Live source API"
    },
    {
        "url": "https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source",
        "data": {"channel_id": "1", "platform": "web", "type": "catchup"},
        "desc": "Live source API with catchup type"
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
            print(f"Body: {body[:500]}")
    except Exception as e:
        print(f"Error: {e}")

