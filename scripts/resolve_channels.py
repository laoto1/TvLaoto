#!/usr/bin/env python3
"""
Resolve VTVGo/THVL channels using Playwright headless browser.
Outputs JSON with tokenized m3u8 URLs.
Runs in GitHub Actions (ubuntu-latest with Playwright installed).
"""

import asyncio
import json
import re
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright

CHANNELS_FILE = Path(__file__).parent.parent / "space" / "channels.json"
RESOLVE_TIMEOUT = 30_000  # 30 seconds per channel


def load_channels() -> dict:
    with open(CHANNELS_FILE) as f:
        return json.load(f)


async def resolve_vtvgo(browser, channel_url: str) -> str | None:
    """Resolve VTVGo channel — intercept XHR for tokenized m3u8 URL."""
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720},
    )
    page = await context.new_page()
    result_url = None
    event = asyncio.Event()

    async def handle_response(response):
        nonlocal result_url
        if result_url:
            return
        try:
            url = response.url
            if not response.ok:
                return

            content_type = response.headers.get("content-type", "")

            # Direct m3u8 request (skip failover URLs — no token, return 403)
            if ".m3u8" in url and "failover" not in url and "api" not in url:
                result_url = url
                event.set()
                return

            # Parse response body for m3u8 URLs
            if "json" in content_type or "text" in content_type:
                try:
                    body = await response.text()
                    matches = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', body)
                    for m in matches:
                        if "failover" not in m:
                            result_url = m
                            event.set()
                            return
                except Exception:
                    pass
        except Exception:
            pass

    page.on("response", handle_response)

    try:
        await page.goto(channel_url, wait_until="domcontentloaded", timeout=RESOLVE_TIMEOUT)

        # Click "Đồng ý" button if present
        try:
            agree_btn = page.locator("button", has_text=re.compile(r"ng.*ti|agree|accept|đồng", re.IGNORECASE))
            if await agree_btn.count() > 0:
                await agree_btn.first.click()
                print(f"  Clicked agree button", file=sys.stderr)
        except Exception:
            pass

        await asyncio.wait_for(event.wait(), timeout=RESOLVE_TIMEOUT / 1000)
    except asyncio.TimeoutError:
        print(f"  Timeout waiting for m3u8", file=sys.stderr)
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
    finally:
        await page.close()
        await context.close()

    return result_url


async def resolve_thvl(browser, channel_url: str) -> str | None:
    """Resolve THVL channel."""
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720},
    )
    page = await context.new_page()
    result_url = None
    event = asyncio.Event()

    async def handle_response(response):
        nonlocal result_url
        if result_url:
            return
        try:
            url = response.url
            if ".m3u8" in url and response.ok:
                result_url = url
                event.set()
                return

            content_type = response.headers.get("content-type", "")
            if "json" in content_type:
                try:
                    body = await response.text()
                    matches = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', body)
                    if matches:
                        result_url = matches[0]
                        event.set()
                except Exception:
                    pass
        except Exception:
            pass

    page.on("response", handle_response)

    try:
        await page.goto(channel_url, wait_until="domcontentloaded", timeout=RESOLVE_TIMEOUT)
        await asyncio.wait_for(event.wait(), timeout=RESOLVE_TIMEOUT / 1000)
    except asyncio.TimeoutError:
        print(f"  Timeout for THVL", file=sys.stderr)
    except Exception as e:
        print(f"  THVL error: {e}", file=sys.stderr)
    finally:
        await page.close()
        await context.close()

    return result_url


async def resolve_tv360(browser, channel_url: str) -> str | None:
    """Resolve TV360 channel — intercept m3u8 from netcdn.tv360.vn."""
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720},
    )
    page = await context.new_page()
    result_url = None
    event = asyncio.Event()

    async def handle_response(response):
        nonlocal result_url
        if result_url:
            return
        try:
            url = response.url

            # Method 1: Direct m3u8 from netcdn CDN
            if ".m3u8" in url and ("netcdn" in url or "tv360" in url) and response.ok:
                print(f"  [TV360] Found m3u8: {url[:100]}...", file=sys.stderr)
                result_url = url
                event.set()
                return

            # Method 2: Parse encrypted API response for m3u8 URLs
            content_type = response.headers.get("content-type", "")
            if "json" in content_type or "mpegurl" in content_type:
                try:
                    body = await response.text()
                    matches = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', body)
                    for m in matches:
                        if "netcdn" in m or "tv360" in m:
                            print(f"  [TV360] Found m3u8 in body: {m[:100]}...", file=sys.stderr)
                            result_url = m
                            event.set()
                            return
                except Exception:
                    pass
        except Exception:
            pass

    page.on("response", handle_response)

    try:
        await page.goto(channel_url, wait_until="networkidle", timeout=45_000)
        # Wait extra time for JS to decrypt API response and start playback
        if not result_url:
            await asyncio.sleep(5)
        await asyncio.wait_for(event.wait(), timeout=15)
    except asyncio.TimeoutError:
        print(f"  Timeout for TV360: {channel_url}", file=sys.stderr)
    except Exception as e:
        print(f"  TV360 error: {e}", file=sys.stderr)
    finally:
        await page.close()
        await context.close()

    return result_url


async def main():
    channels = load_channels()
    results = {}
    errors = []
    now = int(time.time())

    print(f"Resolving {len(channels)} channels...", file=sys.stderr)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )

        for ch_id, ch in channels.items():
            print(f"Resolving {ch_id} ({ch['name']})...", file=sys.stderr)
            provider = ch.get("provider", "vtvgo")

            try:
                if provider == "thvl":
                    url = await resolve_thvl(browser, ch["url"])
                elif provider == "tv360":
                    url = await resolve_tv360(browser, ch["url"])
                else:
                    url = await resolve_vtvgo(browser, ch["url"])

                if url:
                    print(f"  ✅ {url[:80]}...", file=sys.stderr)
                    results[ch_id] = {
                        "name": ch["name"],
                        "url": url,
                        "resolved_at": now,
                        "group": ch["group"],
                        "logo": ch["logo"],
                    }
                else:
                    print(f"  ❌ Failed", file=sys.stderr)
                    errors.append(ch_id)
            except Exception as e:
                print(f"  ❌ Error: {e}", file=sys.stderr)
                errors.append(ch_id)

            # Small delay between channels
            await asyncio.sleep(2)

        await browser.close()

    output = {
        "resolved": len(results),
        "errors": errors,
        "channels": results,
        "timestamp": now,
    }

    # Output JSON to stdout
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    asyncio.run(main())

