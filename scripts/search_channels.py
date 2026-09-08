import json

with open('scripts/all_next_channels.json', 'r', encoding='utf-8') as f:
    channels = json.load(f)

keywords = ['on ', 'vtvcab', 'phim', 'hài', 'anime', 'k-drama', 'châu á', 'thể thao', 'bibi', 'kids', 'movie', 'echannel', 'style', 'music', 'trending', 'vfamily', 'info', 'cine']

found = []
for ch in channels:
    name = ch.get('name', '')
    if any(k in name.lower() for k in keywords):
        found.append(ch)

with open('scripts/found_channels.json', 'w', encoding='utf-8') as f:
    json.dump(found, f, ensure_ascii=False, indent=2)

print(f"Found {len(found)} channels matching keywords")
for ch in found:
    print(f"{ch['id']} | {ch['name']} | {ch.get('slug')} | isFree={ch.get('isFree')}")

