---
title: AFlix Stream Resolver
emoji: 📺
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# AFlix Stream Resolver

Extracts tokenized m3u8 stream URLs from VTVGo and THVL using headless Playwright.

## API Endpoints

- `GET /` — Service info
- `GET /resolve?channel=vtv1` — Resolve single channel
- `GET /resolve-all` — Resolve all channels (JSON)
- `GET /playlist.m3u` — Resolved playlist in M3U format
- `GET /health` — Health check

