import json
import re

CATEGORY_MAP = {
    "Kênh thiết yếu": "Thiết Yếu",
    "Giải trí": "Giải Trí",
    "Thể thao": "Thể Thao",
    "Kênh quốc tế": "Quốc Tế",
    "Kênh HTV": "HTV",
    "Kênh SCTV": "SCTV",
    "Kênh VTV Cab": "VTVCab",
    "Kênh địa phương": "Địa Phương"
}

def main():
    m3u_path = "app/src/main/res/raw/demo_playlist.m3u"
    json_path = "scripts/tv360_working_channels.json"

    with open(m3u_path, "r", encoding="utf-8") as f:
        existing_m3u = f.read()

    with open(json_path, "r", encoding="utf-8-sig") as f:
        channels = json.load(f)

    # Check for existing channel IDs or names
    existing_ch_ids = set(re.findall(r"[?&]ch=(\d+)", existing_m3u))
    print(f"Existing TV360 ch IDs in m3u: {existing_ch_ids}")

    lines_to_append = []
    added_count = 0

    # Group channels by category order
    category_order = [
        "Giải trí",
        "Thể thao",
        "Kênh quốc tế",
        "Kênh HTV",
        "Kênh SCTV",
        "Kênh VTV Cab",
        "Kênh thiết yếu",
        "Kênh địa phương"
    ]

    for cat in category_order:
        cat_channels = [ch for ch in channels if ch.get("category") == cat]
        group_title = CATEGORY_MAP.get(cat, "Tổng Hợp")
        for ch in cat_channels:
            ch_id = str(ch["id"])
            if ch_id in existing_ch_ids:
                print(f"Skipping already existing ID {ch_id}: {ch['name']}")
                continue

            slug = ch.get("slug", f"channel-{ch_id}")
            name = ch.get("name", f"TV360 {ch_id}")
            logo = ch.get("logo", "")
            url = f"https://tv360.vn/tv/{slug}?ch={ch_id}&col=7808476&sect=LIVE&page=home_live&c=0"

            lines_to_append.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group_title}",{name}')
            lines_to_append.append(url)
            lines_to_append.append("")
            added_count += 1

    if added_count == 0:
        print("No new channels to add.")
        return

    new_content = existing_m3u.rstrip() + "\n\n" + "\n".join(lines_to_append)
    with open(m3u_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Successfully added {added_count} channels to {m3u_path}")

if __name__ == "__main__":
    main()

