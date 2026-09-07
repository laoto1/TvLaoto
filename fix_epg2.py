import re

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

original_sniff_js = """view?.evaluateJavascript(
                    "(function() { " +
                    "   var playBtn = document.querySelector('.vjs-big-play-button');" +
                    "   if (playBtn) { playBtn.click(); }" +
                    "   setTimeout(function() {" +
                    "       var v = document.querySelector('video');" +
                    "       if(v) { v.play(); }" +
                    "       var e = document.elementFromPoint(window.innerWidth/2, window.innerHeight/2);" +
                    "       if (e) { e.click(); }" +
                    "   }, 1000);" +
                    "})()", null
                )"""

# I need to find the WRONG JS block that I inserted into sniff() and replace it with the original.
# The wrong block starts after "override fun onPageFinished(view: WebView?, url: String?) {\n                super.onPageFinished(view, url)\n" in the `sniff` method.

pattern_wrong_sniff = r'view\?\.evaluateJavascript\(\s*"\([^"]+"\s*\+\s*"   var attempts = 0;" \+\s*"   var poll = setInterval\(function\(\) \{" \+.*?\}\)\(\)", null\s*\)'

content = re.sub(pattern_wrong_sniff, original_sniff_js, content, count=1, flags=re.DOTALL)


# Now fix scrapeEpg
new_scrape_js = """view?.evaluateJavascript(
                    "(function() { " +
                    "   var attempts = 0;" +
                    "   var poll = setInterval(function() {" +
                    "       attempts++;" +
                    "       if (attempts > 15) { clearInterval(poll); return; }" + 
                    "       var epgList = [];" +
                    "       var items = document.querySelectorAll('.app-program-item');" +
                    "       if (items.length > 0) {" +
                    "           clearInterval(poll);" +
                    "           items.forEach(function(item, index) {" +
                    "               var timeEl = item.querySelector('.time');" +
                    "               var titleEl = item.querySelector('.title');" +
                    "               if (timeEl && titleEl) {" +
                    "                   var time = timeEl.innerText.trim();" +
                    "                   var title = titleEl.innerText.replace(/\\\\u2022\\\\s*LIVE/g, '').replace('LIVE', '').trim();" + 
                    "                   var isLive = item.classList.contains('active');" +
                    "                   var isReplayable = item.classList.contains('past') || isLive;" +
                    "                   epgList.push({" +
                    "                       index: index," +
                    "                       time: time," +
                    "                       title: title," +
                    "                       isReplayable: isReplayable" +
                    "                   });" +
                    "               }" +
                    "           });" +
                    "           window.AndroidEpg.postEpg(JSON.stringify(epgList));" +
                    "       } else {" +
                    "           var lis = document.querySelectorAll('li');" +
                    "           var found = false;" +
                    "           lis.forEach(function(li, index) {" +
                    "               var p1 = li.querySelector('p.p1');" +
                    "               var p2 = li.querySelector('p.p2');" +
                    "               if (p1 && p2) {" +
                    "                   found = true;" +
                    "                   var time = p1.innerText.trim();" +
                    "                   var title = p2.innerText.trim();" +
                    "                   epgList.push({" +
                    "                       index: index," +
                    "                       time: time," +
                    "                       title: title," +
                    "                       isReplayable: true" +
                    "                   });" +
                    "               }" +
                    "           });" +
                    "           if (found) {" +
                    "               clearInterval(poll);" +
                    "               window.AndroidEpg.postEpg(JSON.stringify(epgList));" +
                    "           }" +
                    "       }" +
                    "   }, 1000);" +
                    "})()", null
                )"""

pattern_scrape = r'view\?\.evaluateJavascript\(\s*"\([^"]+"\s*\+\s*"   var epgList = \[\];" \+.*?\}\)\(\)", null\s*\)'

content = re.sub(pattern_scrape, new_scrape_js, content, count=1, flags=re.DOTALL)

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Restored sniff and updated scrapeEpg")
