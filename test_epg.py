import urllib.request
import json
from datetime import datetime, timedelta

start = datetime.now() - timedelta(days=1)
end = datetime.now() + timedelta(days=1)
url = f"https://cache-api-vtvgo.vtvdigital.vn/cdn/live-channel/api/v1/channels/1/programs?startIsoDate={start.strftime('%Y-%m-%dT00:00:00.000Z')}&endIsoDate={end.strftime('%Y-%m-%dT00:00:00.000Z')}"

req = urllib.request.Request(url)
req.add_header("User-Agent", "Mozilla/5.0")
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        print(json.dumps(data['data'][0], indent=2, ensure_ascii=False))
except Exception as e:
    print(e)
