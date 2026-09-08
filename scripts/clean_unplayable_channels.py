import re

m3u_path = "app/src/main/res/raw/demo_playlist.m3u"
with open(m3u_path, "r", encoding="utf-8") as f:
    content = f.read()

bad_ids = {'9903', '10009', '10010', '10011', '10012', '10013', '10055', '195'}

pattern = re.compile(r'(#EXTINF:[^\n]+\n[^\n]+)', re.MULTILINE)
entries = pattern.findall(content)

filtered_entries = []
removed_count = 0
for entry in entries:
    m = re.search(r'[?&]ch=(\d+)', entry)
    if m and m.group(1) in bad_ids:
        removed_count += 1
    else:
        filtered_entries.append(entry)

new_content = "#EXTM3U\n\n" + "\n\n".join(filtered_entries) + "\n"
with open(m3u_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Done. Removed {removed_count} unplayable channels. Total left: {len(filtered_entries)}")

