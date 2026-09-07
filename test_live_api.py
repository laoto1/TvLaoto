import urllib.request
import json

req = urllib.request.Request("https://web-api-vtvgo.vtvdigital.vn/livechannelsec/api/v2/s-channels/source", method="POST")
req.add_header("Content-Type", "application/json")
req.add_header("User-Agent", "Mozilla/5.0")

data = json.dumps({"channel_id": "1", "platform": "web"}).encode("utf-8")

try:
    with urllib.request.urlopen(req, data=data) as response:
        body = response.read().decode("utf-8")
        print("Response:", body)
except Exception as e:
    print("Error:", e)
