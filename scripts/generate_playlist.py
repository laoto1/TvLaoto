#!/usr/bin/env python3
"""
Generate M3U playlist from resolved channels JSON.
Usage: python generate_playlist.py <input.json> <output.m3u>
"""

import json
import sys


def generate_playlist(input_path: str, output_path: str):
    with open(input_path) as f:
        data = json.load(f)

    channels = data.get("channels", {})
    timestamp = data.get("timestamp", 0)

    lines = ["#EXTM3U"]
    lines.append(f"# Generated at: {timestamp}")
    lines.append(f"# Resolved: {data.get('resolved', 0)} channels")
    if data.get("errors"):
        lines.append(f"# Errors: {', '.join(data['errors'])}")
    lines.append("")

    for ch_id, ch in channels.items():
        name = ch["name"]
        url = ch["url"]
        logo = ch.get("logo", "")
        group = ch.get("group", "")
        resolved_at = ch.get("resolved_at", timestamp)

        extinf = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}" resolved-at="{resolved_at}"'

        # Mark as sup=false since URLs are already resolved (no sniffing needed)
        extinf += ',{}'.format(name)

        lines.append(extinf)
        lines.append(url)
        lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Generated {len(channels)} channels -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.json> <output.m3u>")
        sys.exit(1)

    generate_playlist(sys.argv[1], sys.argv[2])

