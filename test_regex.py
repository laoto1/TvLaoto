import re
url = "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html"
match = re.search(r'-(\w+)\.html', url)
if match:
    print(f"Match: {match.group(1)}")
else:
    print("No match")
