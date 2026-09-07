import io

code = """package com.tvlaoto.network

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

        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView?,
                request: WebResourceRequest?
            ): WebResourceResponse? {
                val reqUrl = request?.url?.toString() ?: ""
                
                if (reqUrl.endsWith(".jpg") || reqUrl.endsWith(".png") || reqUrl.endsWith(".css") || reqUrl.endsWith(".woff2")) {
                    return WebResourceResponse("text/plain", "UTF-8", null)
                }

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
                    "   var playBtn = document.querySelector('.vjs-big-play-button');" +
                    "   if (playBtn) { playBtn.click(); }" +
                    "   setTimeout(function() {" +
                    "       var v = document.querySelector('video');" +
                    "       if(v) { v.play(); }" +
                    "       var e = document.elementFromPoint(window.innerWidth/2, window.innerHeight/2);" +
                    "       if (e) { e.click(); }" +
                    "   }, 1000);" +
                    "})()", null
                )
            }
        }

        webView.loadUrl(url)

        val result = withTimeoutOrNull(15000) {
            deferred.await()
        }
        
        webView.destroy()
        result
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
                
                if (reqUrl.contains("catchup") || reqUrl.contains("timeshift") || reqUrl.contains("start=")) {
                    if (!deferred.isCompleted) {
                        deferred.complete(reqUrl)
                    }
                }
                return super.shouldInterceptRequest(view, request)
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                if (!url!!.contains("/ts/")) {
                    view?.evaluateJavascript(
                        "(function() { " +
                        "   var items = document.querySelectorAll('.app-program-item');" +
                        "   if (items.length > " + programIndex + ") {" +
                        "       items[" + programIndex + "].click();" +
                        "   }" +
                        "})()", null
                    )
                } else {
                    view?.evaluateJavascript(
                        "(function() { " +
                        "   var skipInt = setInterval(function() {" +
                        "       var skipBtn = document.querySelector('.videoAdUiSkipButton');" +
                        "       if (skipBtn) { skipBtn.click(); clearInterval(skipInt); }" +
                        "       var skip2 = document.querySelector('.ytp-ad-skip-button');" +
                        "       if (skip2) { skip2.click(); clearInterval(skipInt); }" +
                        "   }, 1000);" +
                        "})()", null
                    )
                }
            }
        }

        webView.loadUrl(url)

        val result = withTimeoutOrNull(20000) {
            deferred.await()
        }
        
        webView.destroy()
        result
    }

    @SuppressLint("SetJavaScriptEnabled")
    suspend fun scrapeEpg(url: String): List<EpgProgram> = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<List<EpgProgram>>()
        val webView = WebView(context)
        
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
        }

        webView.addJavascriptInterface(EpgJsInterface { json ->
            val list = mutableListOf<EpgProgram>()
            try {
                if (json == "[]" || json == "ERROR") {
                    if (!deferred.isCompleted) deferred.complete(list)
                    return@EpgJsInterface
                }
                val arr = JSONArray(json)
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
                if (!deferred.isCompleted) {
                    deferred.complete(list)
                }
            } catch (e: Exception) {
                if (!deferred.isCompleted) deferred.complete(list)
            }
        }, "AndroidEpg")

        webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                view?.evaluateJavascript(
                    "(function() { " +
                    "   var attempts = 0;" +
                    "   function checkEpg() {" +
                    "       attempts++;" +
                    "       if (attempts > 15) { window.AndroidEpg.postEpg('[]'); return; }" + 
                    "       var epgList = [];" +
                    "       var items = document.querySelectorAll('.app-program-item');" +
                    "       if (items && items.length > 0) {" +
                    "           for(var i=0; i<items.length; i++) {" +
                    "               var item = items[i];" +
                    "               var timeEl = item.querySelector('.time');" +
                    "               var titleEl = item.querySelector('.title');" +
                    "               if (timeEl && titleEl) {" +
                    "                   var time = timeEl.innerText.trim();" +
                    "                   var title = titleEl.innerText.replace(/•\\\\s*LIVE/g, '').replace('LIVE', '').trim();" + 
                    "                   var isLive = item.classList.contains('active');" +
                    "                   var isReplayable = item.classList.contains('past') || isLive;" +
                    "                   epgList.push({" +
                    "                       index: i," +
                    "                       time: time," +
                    "                       title: title," +
                    "                       isReplayable: isReplayable" +
                    "                   });" +
                    "               }" +
                    "           }" +
                    "           window.AndroidEpg.postEpg(JSON.stringify(epgList));" +
                    "       } else {" +
                    "           var lis = document.querySelectorAll('li');" +
                    "           var found = false;" +
                    "           if (lis && lis.length > 0) {" +
                    "               for(var j=0; j<lis.length; j++) {" +
                    "                   var li = lis[j];" +
                    "                   var p1 = li.querySelector('p.p1');" +
                    "                   var p2 = li.querySelector('p.p2');" +
                    "                   if (p1 && p2) {" +
                    "                       found = true;" +
                    "                       var time = p1.innerText.trim();" +
                    "                       var title = p2.innerText.trim();" +
                    "                       epgList.push({" +
                    "                           index: j," +
                    "                           time: time," +
                    "                           title: title," +
                    "                           isReplayable: true" +
                    "                       });" +
                    "                   }" +
                    "               }" +
                    "           }" +
                    "           if (found) {" +
                    "               window.AndroidEpg.postEpg(JSON.stringify(epgList));" +
                    "           } else {" +
                    "               setTimeout(checkEpg, 1000);" +
                    "           }" +
                    "       }" +
                    "   }" +
                    "   checkEpg();" +
                    "})()", null
                )
            }
        }

        webView.loadUrl(url)

        val result = withTimeoutOrNull(20000) {
            deferred.await()
        } ?: emptyList()
        
        webView.destroy()
        result
    }
}
"""

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(code)
print("Rewrote StreamSniffer.kt ES5 safe recursive setTimeout")
