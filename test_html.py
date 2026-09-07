import urllib.request
try:
    req = urllib.request.Request('https://vtvgo.vn/channel/vtv1-1,1.html', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    import re
    # Find list items or anything containing time HH:MM
    print("Total lines:", len(html.split('\n')))
    matches = re.findall(r'<[^>]*>.*?\d{2}:\d{2}.*?</[^>]*>', html)
    print("Found time matches:", len(matches))
    for m in matches[:10]:
        print(m[:100])
except Exception as e:
    print(e)
