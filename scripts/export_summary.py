import json

with open('scripts/all_next_channels.json', 'r', encoding='utf-8') as f:
    channels = json.load(f)

with open('scripts/channels_summary.txt', 'w', encoding='utf-8') as out:
    for ch in sorted(channels, key=lambda x: (x.get('display', 1), str(x.get('id', '')))):
        cid = ch.get('id')
        name = ch.get('name')
        slug = ch.get('slug')
        is_free = ch.get('isFree')
        is_drm = ch.get('isDrm')
        out.write(f"ID={cid} | Name={name} | Slug={slug} | isFree={is_free} | isDrm={is_drm}\n")

print("Written to scripts/channels_summary.txt")

