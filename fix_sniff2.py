with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We want to replace the `onPageFinished` inside `sniffCatchup`
# Find `sniffCatchup` position
idx = content.find('fun sniffCatchup')

# Extract from idx to end
part2 = content[idx:]
part1 = content[:idx]

replacement = """            override fun onPageFinished(view: WebView?, url: String?) {
                view?.evaluateJavascript(
                    "(function() { " +
                    "   if (window.location.href.includes('/ts/')) { " +
                    "       setInterval(function() { " +
                    "           var vids = document.getElementsByTagName('video'); " +
                    "           if(vids.length > 0) { " +
                    "               for(var i=0; i<vids.length; i++) { " +
                    "                   if (vids[i].paused) { " +
                    "                       vids[i].muted = true; " +
                    "                       vids[i].play(); " +
                    "                   } " +
                    "               } " +
                    "           } " +
                    "           var skip = document.querySelector('.skip-btn, .ima-skip-btn'); " +
                    "           if(skip) skip.click(); " +
                    "           var centerEl = document.elementFromPoint(960, 540); " +
                    "           if(centerEl) { centerEl.click(); } " +
                    "       }, 1000); " +
                    "       return; " +
                    "   } " +
                    "   var clicked = false; " +
                    "   setInterval(function() { " +
                    "       var agree = Array.from(document.querySelectorAll('button, a, .btn')).find(b => b.innerText && b.innerText.includes('Đồng ý'));" +
                    "       if (agree) agree.click();" +
                    "       if (clicked) return; " +
                    "       var items = document.querySelectorAll('.app-program-item, li'); " +
                    "       if(items.length > " + programIndex + ") { " +
                    "           var item = items[" + programIndex + "]; " +
                    "           item.click(); " +
                    "           clicked = true; " +
                    "           var btn = item.querySelector('button, a, svg, .replay, .active'); " +
                    "           if (btn && btn.click) btn.click(); " +
                    "       } " +
                    "   }, 1000); " +
                    "})();", null
                )
            }"""

part2 = re.sub(r'            override fun onPageFinished\(view: WebView\?, url: String\?\).*?}\)\(\)";, null\n                \)\n            }', replacement, part2, flags=re.DOTALL)

with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'w', encoding='utf-8') as f:
    f.write(part1 + part2)

print("Updated StreamSniffer")
