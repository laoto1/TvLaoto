with open('app/src/main/res/raw/demo_playlist.m3u', 'r', encoding='utf-8') as f:
    content = f.read()

new_channel = """#EXTINF:-1 tvg-id="" tvg-name="VTV1 (Sniff)" tvg-logo="https://vtv1.vtv.vn/vtv1.png" group-title="Đặc Biệt" sup="true",VTV1 (Sniff)
https://vtvgo.vn/channel/vtv1-1,1.html
"""
content = content + "\n" + new_channel

with open('app/src/main/res/raw/demo_playlist.m3u', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added VTV1 Sniff channel to demo playlist")
