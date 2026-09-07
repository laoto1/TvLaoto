"""
AFlix TV — VTVGo/THVL Stream Resolver
Runs on HuggingFace Spaces (Docker SDK, CPU Basic free tier)

Extracts tokenized m3u8 URLs from VTVGo/THVL using Playwright headless browser.
"""

import asyncio
import json
import re
import time
import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from playwright.async_api import async_playwright, Browser

# --- Config ---
CHANNELS_FILE = Path(__file__).parent / "channels.json"
RESOLVE_TIMEOUT = 30_000  # 30s per channel
CACHE_TTL = 1500  # 25 minutes (tokens usually last ~1 hour)

# --- Global state ---
browser: Browser | None = None
cache: dict[str, dict] = {}  # channel_id -> {"url": str, "resolved_at": int}


def load_channels() -> dict:
    with open(CHANNELS_FILE) as f:
        return json.load(f)


CHANNELS = load_channels()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start/stop Playwright browser on app lifecycle."""
    global browser
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-first-run",
            "--no-zygote",
            "--single-process",
            "--disable-extensions",
        ],
    )
    print(f"[Resolver] Browser started. {len(CHANNELS)} channels loaded.")
    yield
    await browser.close()
    await pw.stop()


app = FastAPI(title="AFlix Stream Resolver", lifespan=lifespan)


async def resolve_vtvgo(channel_url: str) -> str | None:
    """
    Open VTVGo page, intercept XHR responses for tokenized m3u8 URL.
    Skips 'failover' URLs (no token, return 403).
    Returns the real URL like: vtvgolive-vtv02.../hash/timestamp/hls/.../master.m3u8
    """
    if browser is None:
        raise RuntimeError("Browser not initialized")

    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720},
    )

    page = await context.new_page()
    result_url: str | None = None
    event = asyncio.Event()

    async def handle_response(response):
        nonlocal result_url
        if result_url:
            return
        try:
            url = response.url
            # Skip non-relevant requests
            if not response.ok:
                return

            content_type = response.headers.get("content-type", "")

            # Method 1: Direct m3u8 request (skip failover)
            if ".m3u8" in url and "failover" not in url and "api" not in url:
                result_url = url
                event.set()
                return

            # Method 2: Parse response body for m3u8 URLs
            if "json" in content_type or "text" in content_type:
                try:
                    body = await response.text()
                    matches = re.findall(
                        r'https?://[^\s"\']+\.m3u8[^\s"\']*', body
                    )
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

        # Click "Đồng ý" / "Agree" button if present
        try:
            agree_btn = page.locator("button", has_text=re.compile(r"ng.*ti|agree|accept", re.IGNORECASE))
            if await agree_btn.count() > 0:
                await agree_btn.first.click()
                print(f"[Resolver] Clicked agree button")
        except Exception:
            pass

        # Wait for m3u8 URL to be intercepted
        try:
            await asyncio.wait_for(event.wait(), timeout=RESOLVE_TIMEOUT / 1000)
        except asyncio.TimeoutError:
            print(f"[Resolver] Timeout waiting for m3u8 from {channel_url}")
    except Exception as e:
        print(f"[Resolver] Error navigating {channel_url}: {e}")
    finally:
        await page.close()
        await context.close()

    return result_url


async def resolve_thvl(channel_url: str) -> str | None:
    """
    THVL channels — similar approach but different site structure.
    """
    if browser is None:
        raise RuntimeError("Browser not initialized")

    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720},
    )

    page = await context.new_page()
    result_url: str | None = None
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
                    matches = re.findall(
                        r'https?://[^\s"\']+\.m3u8[^\s"\']*', body
                    )
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
        try:
            await asyncio.wait_for(event.wait(), timeout=RESOLVE_TIMEOUT / 1000)
        except asyncio.TimeoutError:
            print(f"[Resolver] Timeout for THVL: {channel_url}")
    except Exception as e:
        print(f"[Resolver] THVL error: {e}")
    finally:
        await page.close()
        await context.close()

    return result_url


@app.get("/")
async def root():
    return {
        "service": "AFlix Stream Resolver",
        "channels": len(CHANNELS),
        "cached": len(cache),
    }


@app.get("/resolve")
async def resolve_channel(channel: str, force: bool = False):
    """Resolve a single channel. Returns tokenized m3u8 URL."""
    if channel not in CHANNELS:
        raise HTTPException(404, f"Unknown channel: {channel}")

    # Check cache
    now = int(time.time())
    if not force and channel in cache:
        cached = cache[channel]
        if now - cached["resolved_at"] < CACHE_TTL:
            return {
                "channel": channel,
                "name": CHANNELS[channel]["name"],
                "url": cached["url"],
                "resolved_at": cached["resolved_at"],
                "cached": True,
            }

    # Resolve
    ch = CHANNELS[channel]
    provider = ch.get("provider", "vtvgo")

    if provider == "thvl":
        url = await resolve_thvl(ch["url"])
    else:
        url = await resolve_vtvgo(ch["url"])

    if url:
        cache[channel] = {"url": url, "resolved_at": now}
        return {
            "channel": channel,
            "name": ch["name"],
            "url": url,
            "resolved_at": now,
            "cached": False,
        }
    else:
        raise HTTPException(504, f"Failed to resolve: {channel}")


@app.get("/resolve-all")
async def resolve_all(force: bool = False):
    """Resolve ALL channels. Returns JSON with all tokenized URLs."""
    results = {}
    errors = []
    now = int(time.time())

    for channel_id, ch in CHANNELS.items():
        # Check cache first
        if not force and channel_id in cache:
            cached = cache[channel_id]
            if now - cached["resolved_at"] < CACHE_TTL:
                results[channel_id] = {
                    "name": ch["name"],
                    "url": cached["url"],
                    "resolved_at": cached["resolved_at"],
                    "group": ch["group"],
                    "logo": ch["logo"],
                }
                continue

        # Resolve fresh
        try:
            provider = ch.get("provider", "vtvgo")
            if provider == "thvl":
                url = await resolve_thvl(ch["url"])
            else:
                url = await resolve_vtvgo(ch["url"])

            if url:
                cache[channel_id] = {"url": url, "resolved_at": now}
                results[channel_id] = {
                    "name": ch["name"],
                    "url": url,
                    "resolved_at": now,
                    "group": ch["group"],
                    "logo": ch["logo"],
                }
            else:
                errors.append(channel_id)
        except Exception as e:
            print(f"[Resolver] Error resolving {channel_id}: {e}")
            errors.append(channel_id)

        # Small delay between channels to avoid rate limiting
        await asyncio.sleep(2)

    return {
        "resolved": len(results),
        "errors": errors,
        "channels": results,
        "timestamp": now,
    }


@app.get("/playlist.m3u", response_class=PlainTextResponse)
async def get_playlist(force: bool = False):
    """
    Returns resolved playlist in M3U format.
    Can be used directly by the TV app or any IPTV player.
    """
    data = await resolve_all(force=force)
    channels = data["channels"]

    lines = ["#EXTM3U"]
    for ch_id, ch in channels.items():
        resolved_at = ch["resolved_at"]
        logo = ch["logo"]
        group = ch["group"]
        name = ch["name"]
        url = ch["url"]

        lines.append(
            f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}" '
            f'resolved-at="{resolved_at}",{name}'
        )
        lines.append(url)
        lines.append("")

    return "\n".join(lines)


@app.get("/health")
async def health():
    return {"status": "ok", "browser": browser is not None, "cached": len(cache)}

