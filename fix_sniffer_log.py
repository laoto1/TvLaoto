with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'r', encoding='utf-8') as f:
    content = f.read()

new_webview_client = """        webView.webChromeClient = object : android.webkit.WebChromeClient() {
            override fun onConsoleMessage(consoleMessage: android.webkit.ConsoleMessage?): Boolean {
                android.util.Log.d("StreamSniffer_JS", consoleMessage?.message() ?: "")
                return super.onConsoleMessage(consoleMessage)
            }
        }

        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView?,
                request: WebResourceRequest?
            ): WebResourceResponse? {
                val reqUrl = request?.url?.toString() ?: ""
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
                    "   console.log('Injected JS running!');" +
                    "   setInterval(function() { " +
                    "       var vids = document.getElementsByTagName('video'); " +
                    "       if(vids.length > 0) console.log('Found ' + vids.length + ' videos');" +
                    "       for(var i=0; i<vids.length; i++) { " +
                    "           vids[i].muted = true; " +
                    "           vids[i].play().then(() => console.log('Playing!')).catch(e => console.log('Play error: ' + e)); " +
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
print("Updated StreamSniffer.kt with logging")
