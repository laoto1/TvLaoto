#!/usr/bin/env python3
"""
Resolve EPG (program guide) and catchup (replay) URLs for VTVGo channels.
Uses VTVGo public API for EPG + Playwright for catchup URL extraction.
Outputs resolved_epg.json committed to repo.
"""

import asyncio
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

from playwright.async_api import async_playwright

CHANNELS_FILE = Path(__file__).parent.parent / "space" / "channels.json"
EPG_API = "https://cache-api-vtvgo.vtvdigital.vn/cdn/live-channel/api/v1/channels/{channel_id}/programs"
CATCHUP_TIMEOUT = 20_000  # 20s per program


def load_channels() -> dict:
    with open(CHANNELS_FILE) as f:
        return json.load(f)


def fetch_epg(vtvgo_id: int) -> list[dict]:
    """Fetch EPG from VTVGo API (pure HTTP, no browser needed)."""
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    start_iso = start.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_iso = end.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    url = (
        f"{EPG_API.format(channel_id=vtvgo_id)}"
        f"?startIsoDate={urllib.parse.quote(start_iso)}"
        f"&endIsoDate={urllib.parse.quote(end_iso)}"
    )

    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"  EPG API error: {e}", file=sys.stderr)
        return []

    programs = []
    for i, item in enumerate(data.get("data", [])):
        title = item.get("title", "").strip()
        title = re.sub(r"^Phim truyện:\s*", "", title)

        start_str = item.get("startDate", "")
        end_str = item.get("endDate", "")

        # Parse to local time (UTC+7)
        time_display = ""
        start_epoch = 0
        end_epoch = 0

        if start_str:
            try:
                dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
                local = dt + timedelta(hours=7)
                time_display = local.strftime("%H:%M")
                start_epoch = int(dt.timestamp())
            except Exception:
                pass

        if end_str:
            try:
                dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
                end_epoch = int(dt.timestamp())
            except Exception:
                pass

        programs.append({
            "index": i,
            "time": time_display,
            "title": title,
            "is_replayable": item.get("isPlayable", 1) == 1,
            "start_epoch": start_epoch,
            "end_epoch": end_epoch,
            "catchup_url": None,  # Will be filled by Playwright
        })

    return programs


async def resolve_catchup_urls(browser, channel_url: str, programs: list[dict]) -> list[dict]:
    """Navigate to VTVGo page, click each past program item, intercept catchup m3u8."""
    now_epoch = int(time.time())

    # Only resolve past programs (ended before now) that are replayable
    past_programs = [
        p for p in programs
        if p["is_replayable"] and p["end_epoch"] > 0 and p["end_epoch"] < now_epoch
    ]

    if not past_programs:
        print("  No past programs to resolve catchup for", file=sys.stderr)
        return programs

    # Limit to most recent 8 programs to save time
    past_programs = past_programs[-8:]
    print(f"  Resolving catchup for {len(past_programs)} past programs...", file=sys.stderr)

    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720},
    )
    page = await context.new_page()

    # Navigate to channel page first
    try:
        await page.goto(channel_url, wait_until="domcontentloaded", timeout=30000)
        # Click agree button if present
        try:
            agree = page.locator("button", has_text=re.compile(r"ng.*ti|agree|đồng", re.IGNORECASE))
            if await agree.count() > 0:
                await agree.first.click()
                await asyncio.sleep(1)
        except Exception:
            pass

        # Wait for program items to appear
        await page.wait_for_selector(".app-program-item", timeout=15000)
        await asyncio.sleep(2)
    except Exception as e:
        print(f"  Page load error: {e}", file=sys.stderr)
        await page.close()
        await context.close()
        return programs

    # For each past program, click and intercept
    for prog in past_programs:
        idx = prog["index"]
        catchup_url = None
        event = asyncio.Event()

        async def handle_response(response):
            nonlocal catchup_url
            if catchup_url:
                return
            try:
                url = response.url
                if ".m3u8" in url and "failover" not in url and response.ok:
                    catchup_url = url
                    event.set()
                    return

                content_type = response.headers.get("content-type", "")
                if "json" in content_type or "text" in content_type:
                    try:
                        body = await response.text()
                        matches = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', body)
                        for m in matches:
                            if "failover" not in m:
                                catchup_url = m
                                event.set()
                                return
                    except Exception:
                        pass
            except Exception:
                pass

        page.on("response", handle_response)

        try:
            # Click the program item
            await page.evaluate(f"""
                (function() {{
                    var items = document.querySelectorAll('.app-program-item');
                    if (items.length > {idx}) {{
                        items[{idx}].click();
                    }}
                }})()
            """)

            await asyncio.wait_for(event.wait(), timeout=15)

            if catchup_url:
                prog["catchup_url"] = catchup_url
                print(f"    ✅ [{prog['time']}] {prog['title'][:30]}", file=sys.stderr)
            else:
                print(f"    ❌ [{prog['time']}] {prog['title'][:30]} (timeout)", file=sys.stderr)

        except asyncio.TimeoutError:
            print(f"    ❌ [{prog['time']}] {prog['title'][:30]} (timeout)", file=sys.stderr)
        except Exception as e:
            print(f"    ❌ [{prog['time']}] {prog['title'][:30]} ({e})", file=sys.stderr)

        page.remove_listener("response", handle_response)
        await asyncio.sleep(2)  # Brief pause between clicks

    await page.close()
    await context.close()

    # Update programs list with resolved catchup URLs
    catchup_map = {p["index"]: p["catchup_url"] for p in past_programs if p["catchup_url"]}
    for p in programs:
        if p["index"] in catchup_map:
            p["catchup_url"] = catchup_map[p["index"]]

    return programs


async def main():
    channels = load_channels()
    result = {}
    now = int(time.time())

    print(f"Resolving EPG + catchup for VTVGo channels...", file=sys.stderr)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        )

        for ch_id, ch in channels.items():
            vtvgo_id = ch.get("vtvgo_id")
            if not vtvgo_id:
                continue  # Skip THVL channels (no EPG/catchup)

            print(f"\n{ch_id} ({ch['name']}):", file=sys.stderr)

            # Step 1: Fetch EPG from API
            programs = fetch_epg(vtvgo_id)
            print(f"  EPG: {len(programs)} programs", file=sys.stderr)

            if not programs:
                continue

            # Step 2: Resolve catchup URLs via Playwright
            programs = await resolve_catchup_urls(browser, ch["url"], programs)

            resolved_count = sum(1 for p in programs if p["catchup_url"])
            print(f"  Catchup resolved: {resolved_count}", file=sys.stderr)

            result[ch_id] = {
                "name": ch["name"],
                "vtvgo_id": vtvgo_id,
                "programs": programs,
            }

        await browser.close()

    output = {
        "timestamp": now,
        "channels": result,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())

