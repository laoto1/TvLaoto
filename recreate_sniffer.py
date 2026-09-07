content = """package com.tvlaoto.network

import android.annotation.SuppressLint
import android.content.Context
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import org.json.JSONArray
import com.tvlaoto.data.model.EpgProgram

class StreamSniffer(private val context: Context) {

    class EpgJsInterface(private val onResult: (String) -> Unit) {
        @JavascriptInterface
        fun postEpg(json: String) {
            onResult(json)
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    suspend fun sniff(url: String): String? = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<String>()
        val webView = WebView(context)
        
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            mediaPlaybackRequiresUserGesture = false
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
                
                if (reqUrl.endsWith(".jpg") || reqUrl.endsWith(".png") || reqUrl.endsWith(".css") || reqUrl.endsWith(".woff2")) {
                    return WebResourceResponse("text/plain", "UTF-8", null)
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
                    "   console.log('Injected JS running!');" +
                    "   setInterval(function() { " +
                    "       var vids = document.getElementsByTagName('video'); " +
                    "       if(vids.length > 0) { " +
                    "           for(var i=0; i<vids.length; i++) { " +
                    "               if (vids[i].paused) { " +
                    "                   vids[i].muted = true; " +
                    "                   vids[i].play(); " +
                    "               } " +
                    "           } " +
                    "       } else { " +
                    "           var centerEl = document.elementFromPoint(960, 540); " +
                    "           if(centerEl) { centerEl.click(); } " +
                    "           var buttons = document.querySelectorAll('button, .play-btn, .vjs-big-play-button'); " +
                    "           for (var i = 0; i < buttons.length; i++) { buttons[i].click(); } " +
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

    @SuppressLint("SetJavaScriptEnabled")
    suspend fun scrapeEpg(url: String): List<EpgProgram> = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<List<EpgProgram>>()
        val webView = WebView(context)
        
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            userAgentString = android.webkit.WebSettings.getDefaultUserAgent(context)
        }

        webView.addJavascriptInterface(EpgJsInterface { json ->
            if (!deferred.isCompleted) {
                try {
                    val arr = JSONArray(json)
                    val list = mutableListOf<EpgProgram>()
                    for (i in 0 until arr.length()) {
                        val obj = arr.getJSONObject(i)
                        list.add(
                            EpgProgram(
                                index = obj.getInt("index"),
                                time = obj.getString("time"),
                                title = obj.getString("title"),
                                isReplayable = obj.getBoolean("isReplayable")
                            )
                        )
                    }
                    deferred.complete(list)
                } catch (e: Exception) {
                    deferred.complete(emptyList())
                }
            }
        }, "AndroidEpg")

        webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, url: String?) {
                view?.evaluateJavascript(
                    "(function() { " +
                    "   var checkEpg = setInterval(function() { " +
                    "       var items = document.querySelectorAll('li'); " +
                    "       var epgs = []; " +
                    "       for(var i=0; i<items.length; i++) { " +
                    "           var text = items[i].innerText; " +
                    "           if (!text) continue; " +
                    "           var timeMatch = text.match(/\\\\b\\\\d{2}:\\\\d{2}\\\\b/); " +
                    "           if(timeMatch) { " +
                    "               var time = timeMatch[0]; " +
                    "               var split = text.split('\\n'); " +
                    "               var title = text.replace(time, '').trim(); " +
                    "               for(var j=0; j<split.length; j++) { " +
                    "                   if(split[j].trim() != time && split[j].trim().length > 2) { " +
                    "                       title = split[j].trim(); break; " +
                    "                   } " +
                    "               } " +
                    "               var html = items[i].innerHTML.toLowerCase(); " +
                    "               var isReplay = html.includes('svg') || html.includes('catchup') || html.includes('replay'); " +
                    "               epgs.push({ " +
                    "                   index: i, time: time, title: title.substring(0, 50), isReplayable: isReplay " +
                    "               }); " +
                    "           } " +
                    "       } " +
                    "       if (epgs.length > 2) { " +
                    "           clearInterval(checkEpg); " +
                    "           AndroidEpg.postEpg(JSON.stringify(epgs)); " +
                    "       } " +
                    "   }, 1000); " +
                    "   setTimeout(function() { clearInterval(checkEpg); AndroidEpg.postEpg('[]'); }, 8000); " +
                    "})();", null
                )
            }
        }
        
        webView.layout(0, 0, 1920, 1080)
        webView.loadUrl(url)

        val result = withTimeoutOrNull(10000L) {
            deferred.await()
        } ?: emptyList()
        
        webView.stopLoading()
        webView.destroy()
        
        return@withContext result
    }

    @SuppressLint("SetJavaScriptEnabled")
    suspend fun sniffCatchup(url: String, programIndex: Int): String? = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<String>()
        val webView = WebView(context)
        
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            mediaPlaybackRequiresUserGesture = false
            userAgentString = android.webkit.WebSettings.getDefaultUserAgent(context)
        }

        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView?,
                request: WebResourceRequest?
            ): WebResourceResponse? {
                val reqUrl = request?.url?.toString() ?: ""
                
                if (reqUrl.endsWith(".jpg") || reqUrl.endsWith(".png") || reqUrl.endsWith(".css") || reqUrl.endsWith(".woff2")) {
                    return WebResourceResponse("text/plain", "UTF-8", null)
                }

                if (reqUrl.contains(".m3u8") && (reqUrl.contains("catchup") || reqUrl.contains("start="))) {
                    if (!deferred.isCompleted) {
                        deferred.complete(reqUrl)
                    }
                }
                return super.shouldInterceptRequest(view, request)
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                view?.evaluateJavascript(
                    "(function() { " +
                    "   setInterval(function() { " +
                    "       var items = document.querySelectorAll('li'); " +
                    "       if(items.length > " + programIndex + ") { " +
                    "           var item = items[" + programIndex + "]; " +
                    "           item.click(); " +
                    "           var btn = item.querySelector('button, a, svg, .replay, .active'); " +
                    "           if (btn) btn.click(); " +
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
print("Recreated StreamSniffer.kt")
