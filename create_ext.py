import os
import json

os.makedirs("app/src/main/assets/ext", exist_ok=True)

manifest = {
  "manifest_version": 2,
  "name": "TV Sniffer",
  "version": "1.0",
  "background": {
    "scripts": ["background.js"]
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "run_at": "document_end"
    }
  ],
  "permissions": [
    "webRequest",
    "<all_urls>"
  ]
}

with open("app/src/main/assets/ext/manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

background_js = """
browser.webRequest.onBeforeRequest.addListener(
    function(details) {
        if (details.url.includes(".m3u8")) {
            browser.runtime.sendNativeMessage("sniffer_port", { type: "m3u8", url: details.url });
        }
    },
    {urls: ["<all_urls>"]}
);

browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "epg_data") {
        browser.runtime.sendNativeMessage("sniffer_port", { type: "epg", data: message.data });
    }
});
"""
with open("app/src/main/assets/ext/background.js", "w") as f:
    f.write(background_js)

content_js = """
// Auto clicker for player
setTimeout(() => {
    let playBtn = document.querySelector('.vjs-big-play-button');
    if (playBtn) playBtn.click();
    setTimeout(() => {
        let v = document.querySelector('video');
        if (v) v.play();
        let e = document.elementFromPoint(window.innerWidth/2, window.innerHeight/2);
        if (e) e.click();
    }, 1000);
}, 2000);

// Scrape EPG
setTimeout(() => {
    let epgList = [];
    let items = document.querySelectorAll('.app-program-item');
    if (items.length > 0) {
        items.forEach((item, index) => {
            let timeEl = item.querySelector('.time');
            let titleEl = item.querySelector('.title');
            if (timeEl && titleEl) {
                let time = timeEl.innerText.trim();
                let title = titleEl.innerText.replace('• LIVE', '').trim();
                let isLive = item.classList.contains('active');
                let isReplayable = item.classList.contains('past') || isLive;
                epgList.push({
                    index: index,
                    time: time,
                    title: title,
                    isReplayable: isReplayable
                });
            }
        });
        browser.runtime.sendMessage({ type: "epg_data", data: JSON.stringify(epgList) });
    } else {
        // another layout
        let lis = document.querySelectorAll('li');
        lis.forEach((li, index) => {
            let p1 = li.querySelector('p.p1');
            let p2 = li.querySelector('p.p2');
            if (p1 && p2) {
                let time = p1.innerText.trim();
                let title = p2.innerText.trim();
                epgList.push({
                    index: index,
                    time: time,
                    title: title,
                    isReplayable: true
                });
            }
        });
        if(epgList.length > 0) {
            browser.runtime.sendMessage({ type: "epg_data", data: JSON.stringify(epgList) });
        }
    }
}, 5000);
"""
with open("app/src/main/assets/ext/content.js", "w") as f:
    f.write(content_js)

print("Created WebExtension files.")
