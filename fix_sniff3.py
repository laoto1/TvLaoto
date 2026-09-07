with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'r', encoding='utf-8') as f:
    content = f.read()

target = """            override fun onPageFinished(view: WebView?, url: String?) {
                view?.evaluateJavascript(
                    "(function() { " +
                    "   setInterval(function() { " +
                    "       var agree = Array.from(document.querySelectorAll('button, a, .btn')).find(b => b.innerText && b.innerText.includes('Đồng ý'));" +
                    "       if (agree) agree.click();" +
                    "       var items = document.querySelectorAll('.app-program-item, li'); " +
                    "       if(items.length > " + programIndex + ") { " +
                    "           var item = items[" + programIndex + "]; " +
                    "           item.click(); " +
                    "           var btn = item.querySelector('button, a, svg, .replay, .active'); " +
                    "           if (btn) btn.click(); " +
                    "       } " +
                    "   }, 1000); " +
                    "})();", null
                )
            }"""

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
                    "           var skip = document.querySelector('.skip-btn, .ima-skip-btn, button'); " +
                    "           if(skip && skip.innerText && skip.innerText.toLowerCase().includes('bỏ qua')) skip.click(); " +
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

if target in content:
    content = content.replace(target, replacement)
    with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced exact string.")
else:
    print("Target string not found!")
