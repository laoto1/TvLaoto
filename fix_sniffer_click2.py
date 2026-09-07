content = """package com.tvlaoto.network

import android.annotation.SuppressLint
import android.content.Context
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull

class StreamSniffer(private val context: Context) {

    @SuppressLint("SetJavaScriptEnabled")
    suspend fun sniff(url: String): String? = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<String>()
        val webView = WebView(context)
        
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            mediaPlaybackRequiresUserGesture = false
            // Sử dụng User-Agent gốc của thiết bị
            userAgentString = android.webkit.WebSettings.getDefaultUserAgent(context)
        }

        webView.webChromeClient = object : android.webkit.WebChromeClient() {
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
                
                // Bỏ qua các file không cần thiết để tăng tốc
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
                // Ép phát video và click
                view?.evaluateJavascript(
                    "(function() { " +
                    "   console.log('Injected JS running!');" +
                    "   setInterval(function() { " +
                    "       var vids = document.getElementsByTagName('video'); " +
                    "       if(vids.length > 0) { " +
                    "           console.log('Found ' + vids.length + ' videos');" +
                    "           for(var i=0; i<vids.length; i++) { " +
                    "               if (vids[i].paused) { " +
                    "                   vids[i].muted = true; " +
                    "                   vids[i].play().then(() => console.log('Playing!')).catch(e => console.log('Play error: ' + e)); " +
                    "               } " +
                    "           } " +
                    "       } else { " +
                    "           var centerEl = document.elementFromPoint(960, 540); " +
                    "           if(centerEl) { " +
                    "               centerEl.click(); " +
                    "               console.log('Clicked center element'); " +
                    "           } " +
                    "           var buttons = document.querySelectorAll('button, .play-btn, .vjs-big-play-button'); " +
                    "           buttons.forEach(b => { b.click(); console.log('Clicked button'); }); " +
                    "       } " +
                    "   }, 1000); " +
                    "})();", null
                )
            }
        }
        
        webView.layout(0, 0, 1920, 1080)
        webView.loadUrl(url)

        val result = withTimeoutOrNull(15000L) {
            deferred.await()
        }
        
        webView.stopLoading()
        webView.destroy()
        
        return@withContext result
    }
}
"""

with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed StreamSniffer.kt properly")
