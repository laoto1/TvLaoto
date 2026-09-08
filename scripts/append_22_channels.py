import json

def main():
    m3u_path = "app/src/main/res/raw/demo_playlist.m3u"
    json_path = "scripts/channels_22.json"

    with open(m3u_path, "r", encoding="utf-8") as f:
        existing_m3u = f.read()

    with open(json_path, "r", encoding="utf-8") as f:
        channels = json.load(f)

    lines_to_append = []

    for ch in channels:
        cid = ch["id"]
        name = ch["name"]
        slug = ch["slug"]
        logo = ch.get("logo", "")

        if cid in [175, 176, 177, 178, 179, 180, 181, 182, 184, 185, 186, 187, 188, 189]:
            group = "VTVCab"
        elif cid == 195:
            group = "HTV"
        else:
            group = "Giải Trí"

        url = f"https://tv360.vn/tv/{slug}?ch={cid}&col=7808476&sect=LIVE&page=home_live&c=0"

        lines_to_append.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}')
        lines_to_append.append(url)
        lines_to_append.append("")

    new_content = existing_m3u.rstrip() + "\n\n" + "\n".join(lines_to_append)
    with open(m3u_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Successfully added {len(channels)} channels to {m3u_path}")

if __name__ == "__main__":
    main()

