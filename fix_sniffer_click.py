with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'r', encoding='utf-8') as f:
    content = f.read()

new_webview_client = """        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView?,
                request: WebResourceRequest?
            ): WebResourceResponse? {
                val reqUrl = request?.url?.toString() ?: ""
                
                // Bỏ qua ảnh và css
                if (reqUrl.endsWith(".jpg") || reqUrl.endsWith(".png") || reqUrl.endsWith(".css") || reqUrl.endsWith(".woff2")) {
                    // return WebResourceResponse("text/plain", "UTF-8", null)
                }

                android.util.Log.d("StreamSniffer_REQ", reqUrl)
                
                if (reqUrl.contains(".m3u8")) {
                    if (!deferred.isCompleted) {
                        deferred.complete(reqUrl)
                    }
                }
                return super.shouldInterceptRequest(view, request)
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                view?.evaluateJavascript(
                    "(function() { " +
                    "   setInterval(function() { " +
                    "       var vids = document.getElementsByTagName('video'); " +
                    "       if(vids.length > 0) { " +
                    "           for(var i=0; i<vids.length; i++) { " +
                    "               if (vids[i].paused) { vids[i].muted = true; vids[i].play(); } " +
                    "           } " +
                    "       } else { " +
                    "           var centerEl = document.elementFromPoint(960, 540); " +
                    "           if(centerEl) centerEl.click(); " +
                    "           var buttons = document.querySelectorAll('button, .play-btn, .vjs-big-play-button'); " +
                    "           buttons.forEach(b => b.click()); " +
                    "       } " +
                    "   }, 1000); " +
                    "})();", null
                )
            }
        }"""

import re
content = re.sub(r'        webView.webViewClient = object : WebViewClient\(\) \{.*?        \}', new_webview_client, content, flags=re.DOTALL)

with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated StreamSniffer.kt to click buttons")
