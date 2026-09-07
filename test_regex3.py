import re
urls = [
    "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html",
    "https://vtvgo.vn/channel/vtv1-1,1.html",
    "https://vtvgo.vn/channel/vtv2-2,1.html"
]
for url in urls:
    match = re.search(r'-(\d+)(?:,|\.html)', url)
    if match:
        print(f"{url} -> Match: {match.group(1)}")
    else:
        print(f"{url} -> No match")
