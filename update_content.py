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
    }
}, 5000);

window.clickProgram = function(index) {
    let items = document.querySelectorAll('.app-program-item');
    if (items[index]) {
        items[index].click();
        // Skip Ad loop
        let skipInt = setInterval(() => {
            let skipBtn = document.querySelector('.videoAdUiSkipButton');
            if (skipBtn) { skipBtn.click(); clearInterval(skipInt); }
            let skip2 = document.querySelector('.ytp-ad-skip-button');
            if (skip2) { skip2.click(); clearInterval(skipInt); }
        }, 1000);
    }
}
"""
with open("app/src/main/assets/ext/content.js", "w") as f:
    f.write(content_js)
print("Updated content.js")
