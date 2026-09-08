import json

with open('scripts/all_next_channels.json', 'r', encoding='utf-8') as f:
    channels = json.load(f)

ids = [9903, 10009, 10010, 10011, 10012, 10013, 10055, 195, 180, 175, 176, 177, 178, 179, 181, 182, 184, 185, 186, 187, 188, 189]
found = {c['id']: c for c in channels if c.get('id') in ids}

output = []
for cid in ids:
    c = found.get(cid)
    if c:
        img = c.get('coverImage') or c.get('horizontalImage') or ''
        output.append({
            'id': cid,
            'name': c.get('name'),
            'slug': c.get('slug'),
            'logo': img,
            'isFree': c.get('isFree')
        })

with open('scripts/channels_22.json', 'w', encoding='utf-8') as out:
    json.dump(output, out, ensure_ascii=False, indent=2)

print(f"Saved {len(output)} channels to scripts/channels_22.json")

