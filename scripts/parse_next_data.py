import json

with open('scripts/tv360_next_data.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

channels = []
def extract_channels(obj):
    if isinstance(obj, dict):
        if 'id' in obj and 'name' in obj and ('slug' in obj or 'isFree' in obj):
            channels.append(obj)
        for v in obj.values():
            extract_channels(v)
    elif isinstance(obj, list):
        for v in obj:
            extract_channels(v)

extract_channels(data)
seen = {}
for ch in channels:
    cid = ch.get('id')
    if cid and cid not in seen:
        seen[cid] = ch

result = list(seen.values())
with open('scripts/all_next_channels.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Exported {len(result)} channels to scripts/all_next_channels.json")

