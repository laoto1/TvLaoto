import re

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

# We want to replace the JS inside view?.evaluateJavascript(...) in scrapeEpg
# The JS starts at "(function() { " and ends at "})()", null

new_js = """
                view?.evaluateJavascript(
                    "(function() { " +
                    "   var attempts = 0;" +
                    "   var poll = setInterval(function() {" +
                    "       attempts++;" +
                    "       if (attempts > 15) { clearInterval(poll); return; }" + // Give up after 15 attempts (15s)
                    "       var epgList = [];" +
                    "       var items = document.querySelectorAll('.app-program-item');" +
                    "       if (items.length > 0) {" +
                    "           clearInterval(poll);" +
                    "           items.forEach(function(item, index) {" +
                    "               var timeEl = item.querySelector('.time');" +
                    "               var titleEl = item.querySelector('.title');" +
                    "               if (timeEl && titleEl) {" +
                    "                   var time = timeEl.innerText.trim();" +
                    "                   var title = titleEl.innerText.replace(/\\u2022\\s*LIVE/g, '').replace('LIVE', '').trim();" + // Handles the bullet properly
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
"""

# Find the block to replace
start_idx = content.find('view?.evaluateJavascript(\n                    "(function() { " +')
end_idx = content.find('                    "})()", null\n                )') + len('                    "})()", null\n                )')

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_js.strip() + content[end_idx:]
    with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed scrapeEpg JS polling")
else:
    print("Could not find JS block")
