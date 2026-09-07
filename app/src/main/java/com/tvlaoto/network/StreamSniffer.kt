package com.tvlaoto.network

import android.annotation.SuppressLint
import android.content.Context
import android.webkit.JavascriptInterface
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import org.json.JSONArray
import com.tvlaoto.data.model.EpgProgram

class StreamSniffer(private val context: Context) {

    // Cached WebView — kept alive after sniff() for catchup reuse
    private var cachedWebView: WebView? = null
    private var cachedStreamUrl: String? = null

    // Active deferred — swapped between live/catchup modes
    @Volatile
    private var activeDeferred: CompletableDeferred<String>? = null

    // Intercept mode flag
    @Volatile
    private var interceptCatchupOnly = false

    // JS bridge to receive m3u8 URLs from injected JS
    class M3u8Bridge(private val onResult: (String) -> Unit) {
        @JavascriptInterface
        fun onM3u8Found(url: String) {
            onResult(url)
        }
    }

    private fun muteAndPauseWebView(webView: WebView?) {
        webView?.evaluateJavascript(
            "(function() { " +
            "   var videos = document.querySelectorAll('video'); " +
            "   for (var i = 0; i < videos.length; i++) { " +
            "       videos[i].pause(); " +
            "       videos[i].muted = true; " +
            "   } " +
            "})()", null
        )
    }

    @SuppressLint("SetJavaScriptEnabled")
    suspend fun sniff(url: String): String? = withContext(Dispatchers.Main) {
        // Always destroy and clear previous cached WebView first
        cachedWebView?.let { old ->
            old.stopLoading()
            old.loadUrl("about:blank")
            old.destroy()
        }
        cachedWebView = null
        cachedStreamUrl = null

        // Allow WebView engine to settle after destroy
        delay(300)

        // Try up to 2 times (retry once on timeout)
        var attempts = 0
        var result: String? = null

        while (attempts < 2 && result == null) {
            attempts++
            if (attempts > 1) {
                com.tvlaoto.util.AppLogger.d("StreamSniffer", "Retry attempt $attempts...")
                delay(500)
            }

            result = doSniff(url)
        }

        result
    }

    @SuppressLint("SetJavaScriptEnabled")
    private suspend fun doSniff(url: String): String? = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<String>()
        activeDeferred = deferred
        interceptCatchupOnly = false

        val webView = WebView(context)

        // JS bridge for receiving m3u8 URLs from injected JS
        webView.addJavascriptInterface(M3u8Bridge { m3u8Url ->
            if (!deferred.isCompleted) {
                // Skip failover/manifest URLs without token — they return 403
                // Real URL pattern: vtvgolive-vtv02.vtvdigital.vn/{token}/{timestamp}/hls/...
                if (m3u8Url.contains("failover")) {
                    com.tvlaoto.util.AppLogger.d("StreamSniffer", "Bridge SKIP failover URL: $m3u8Url")
                    return@M3u8Bridge
                }
                com.tvlaoto.util.AppLogger.d("StreamSniffer", "Bridge received m3u8: $m3u8Url")
                deferred.complete(m3u8Url)
            }
        }, "M3u8Bridge")

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            mediaPlaybackRequiresUserGesture = false
            userAgentString = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            loadWithOverviewMode = true
            useWideViewPort = true
            cacheMode = android.webkit.WebSettings.LOAD_NO_CACHE
        }

        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView?,
                request: WebResourceRequest?
            ): WebResourceResponse? {
                val reqUrl = request?.url?.toString() ?: ""

                // Block heavy resources to save bandwidth
                if (reqUrl.endsWith(".jpg") || reqUrl.endsWith(".png") || reqUrl.endsWith(".css") || reqUrl.endsWith(".woff2") || reqUrl.endsWith(".ttf")) {
                    return WebResourceResponse("text/plain", "UTF-8", null)
                }

                // Intercept m3u8 URLs (in case the player DOES load on newer WebViews)
                if (reqUrl.contains(".m3u8") && !reqUrl.contains("api") && !reqUrl.contains("failover")) {
                    val currentDeferred = activeDeferred
                    if (currentDeferred != null && !currentDeferred.isCompleted) {
                        if (interceptCatchupOnly) {
                            if (reqUrl.contains("catchup") || reqUrl.contains("timeshift") || reqUrl.contains("start=")) {
                                com.tvlaoto.util.AppLogger.d("StreamSniffer", "Sniff Catchup OK (reuse): $reqUrl")
                                currentDeferred.complete(reqUrl)
                            }
                        } else {
                            com.tvlaoto.util.AppLogger.d("StreamSniffer", "Sniff Live OK: $reqUrl")
                            currentDeferred.complete(reqUrl)
                        }
                    }
                }
                return super.shouldInterceptRequest(view, request)
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                com.tvlaoto.util.AppLogger.d("StreamSniffer", "onPageFinished: $url")

                // Strategy: Monkey-patch fetch/XHR to intercept m3u8 URLs from API responses,
                // AND click the "Agree" button to let the SPA proceed.
                view?.evaluateJavascript(
                    """(function() {
                        // 1. Monkey-patch fetch to intercept m3u8 URLs from decrypted API responses
                        var origFetch = window.fetch;
                        window.fetch = function() {
                            return origFetch.apply(this, arguments).then(function(response) {
                                var cloned = response.clone();
                                var reqUrl = (arguments[0] && arguments[0].url) || arguments[0] || '';
                                cloned.text().then(function(body) {
                                    // Look for m3u8 URLs in any response body
                    var m3u8Match = body.match(/https?:\/\/[^\s"']+\.m3u8[^\s"']*/);
                                    if (m3u8Match && m3u8Match[0].indexOf('failover') === -1) {
                                        console.log('StreamSniffer: fetch intercepted m3u8: ' + m3u8Match[0]);
                                        if (window.M3u8Bridge) { window.M3u8Bridge.onM3u8Found(m3u8Match[0]); }
                                    }
                                }).catch(function(){});
                                return response;
                            });
                        };

                        // 2. Monkey-patch XMLHttpRequest to also intercept m3u8
                        var origXhrOpen = XMLHttpRequest.prototype.open;
                        var origXhrSend = XMLHttpRequest.prototype.send;
                        XMLHttpRequest.prototype.open = function(method, url) {
                            this._url = url;
                            return origXhrOpen.apply(this, arguments);
                        };
                        XMLHttpRequest.prototype.send = function() {
                            var xhr = this;
                            var origOnLoad = xhr.onload;
                            xhr.onload = function() {
                                try {
                                    var body = xhr.responseText || '';
                                    var m3u8Match = body.match(/https?:\/\/[^\s"']+\.m3u8[^\s"']*/);
                                    if (m3u8Match && m3u8Match[0].indexOf('failover') === -1) {
                                        console.log('StreamSniffer: XHR intercepted m3u8: ' + m3u8Match[0]);
                                        if (window.M3u8Bridge) { window.M3u8Bridge.onM3u8Found(m3u8Match[0]); }
                                    }
                                } catch(e) {}
                                if (origOnLoad) origOnLoad.apply(this, arguments);
                            };
                            return origXhrSend.apply(this, arguments);
                        };

                        // 3. Also monitor performance entries for m3u8 requests
                        var perfInterval = setInterval(function() {
                            try {
                                var entries = performance.getEntriesByType('resource');
                                for (var i = 0; i < entries.length; i++) {
                                    if (entries[i].name.indexOf('.m3u8') > -1 && entries[i].name.indexOf('api') === -1) {
                                        console.log('StreamSniffer: perf m3u8: ' + entries[i].name);
                                        if (window.M3u8Bridge) { window.M3u8Bridge.onM3u8Found(entries[i].name); }
                                        clearInterval(perfInterval);
                                        break;
                                    }
                                }
                            } catch(e) {}
                        }, 2000);

                        // 4. Click "Agree" button + play video
                        var attempt = 0;
                        var agreedClicked = false;
                        var clickInterval = setInterval(function() {
                            attempt++;
                            if (!agreedClicked) {
                                var buttons = document.querySelectorAll('button');
                                for (var i = 0; i < buttons.length; i++) {
                                    var txt = buttons[i].textContent || '';
                                    if (txt.indexOf('ng') > -1 && txt.indexOf('ti') > -1) {
                                        buttons[i].click();
                                        agreedClicked = true;
                                        break;
                                    }
                                }
                            }
                            var v = document.querySelector('video');
                            if (v) { v.play(); clearInterval(clickInterval); }
                            if (attempt > 40) { clearInterval(clickInterval); }
                        }, 500);

                        // 5. Debug: log button and video count
                        setTimeout(function() {
                            var btns = document.querySelectorAll('button').length;
                            var vids = document.querySelectorAll('video').length;
                            console.log('StreamSniffer: buttons=' + btns + ' videos=' + vids);
                        }, 3000);
                    })()""", null
                )

                // Also use evaluateJavascript callback to log debug info
                view?.evaluateJavascript("document.querySelectorAll('button').length") { result ->
                    com.tvlaoto.util.AppLogger.d("StreamSniffer", "DEBUG buttons: $result")
                }
            }
        }

        // Capture console.log
        webView.webChromeClient = object : android.webkit.WebChromeClient() {
            override fun onConsoleMessage(consoleMessage: android.webkit.ConsoleMessage?): Boolean {
                val msg = consoleMessage?.message() ?: ""
                com.tvlaoto.util.AppLogger.d("StreamSniffer", "JS: $msg")
                return true
            }
        }

        com.tvlaoto.util.AppLogger.d("StreamSniffer", "Loading URL: $url")
        webView.loadUrl(url)

        val result = withTimeoutOrNull(25000) {
            deferred.await()
        }

        if (result != null) {
            muteAndPauseWebView(webView)
            webView.onPause()
            webView.pauseTimers()
            cachedWebView = webView
            cachedStreamUrl = url
            com.tvlaoto.util.AppLogger.d("StreamSniffer", "WebView cached for catchup reuse (muted & suspended)")
        } else {
            android.util.Log.w("StreamSniffer", "Sniff failed (timeout)")
            webView.stopLoading()
            webView.loadUrl("about:blank")
            webView.destroy()
        }

        result
    }

    @SuppressLint("SetJavaScriptEnabled")
    suspend fun sniffCatchup(url: String, programIndex: Int): String? = withContext(Dispatchers.Main) {
        val existingWebView = cachedWebView

        // FAST PATH: Reuse cached WebView (no page reload needed)
        if (existingWebView != null && cachedStreamUrl == url) {
            com.tvlaoto.util.AppLogger.d("StreamSniffer", "Catchup FAST PATH: reusing cached WebView, clicking item $programIndex")

            existingWebView.resumeTimers()
            existingWebView.onResume()

            val deferred = CompletableDeferred<String>()
            activeDeferred = deferred
            interceptCatchupOnly = true

            existingWebView.evaluateJavascript(
                "(function() { " +
                "   var attempt = 0; " +
                "   var maxAttempts = 60; " +
                "   var clickInterval = setInterval(function() { " +
                "       attempt++; " +
                "       var items = document.querySelectorAll('.app-program-item'); " +
                "       if (items.length > " + programIndex + ") { " +
                "           items[" + programIndex + "].click(); " +
                "           clearInterval(clickInterval); " +
                "           console.log('Catchup FAST: clicked item " + programIndex + " at attempt ' + attempt); " +
                "       } else if (attempt >= maxAttempts) { " +
                "           clearInterval(clickInterval); " +
                "           console.log('Catchup FAST: gave up after ' + attempt + ' attempts'); " +
                "       } " +
                "   }, 500); " +
                "})()", null
            )

            val result = withTimeoutOrNull(20000) {
                deferred.await()
            }

            interceptCatchupOnly = false

            if (result != null) {
                muteAndPauseWebView(existingWebView)
                existingWebView.onPause()
                existingWebView.pauseTimers()
                return@withContext result
            }

            android.util.Log.w("StreamSniffer", "Catchup FAST PATH failed, falling back to full reload")
        }

        // SLOW PATH: Full WebView reload (fallback)
        com.tvlaoto.util.AppLogger.d("StreamSniffer", "Catchup SLOW PATH: full page load")

        val deferred = CompletableDeferred<String>()
        activeDeferred = deferred
        interceptCatchupOnly = true

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

                if ((reqUrl.contains("catchup") || reqUrl.contains("timeshift") || reqUrl.contains("start=")) && reqUrl.contains(".m3u8") && !reqUrl.contains("api")) {
                    if (!deferred.isCompleted) {
                        com.tvlaoto.util.AppLogger.d("StreamSniffer", "Sniff Catchup OK (slow): $reqUrl")
                        deferred.complete(reqUrl)
                    }
                }
                return super.shouldInterceptRequest(view, request)
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                view?.evaluateJavascript(
                    "(function() { " +
                    "   var attempt = 0; " +
                    "   var maxAttempts = 60; " +
                    "   var clickInterval = setInterval(function() { " +
                    "       attempt++; " +
                    "       var items = document.querySelectorAll('.app-program-item'); " +
                    "       if (items.length > " + programIndex + ") { " +
                    "           items[" + programIndex + "].click(); " +
                    "           clearInterval(clickInterval); " +
                    "           console.log('Catchup: clicked item ' + " + programIndex + " + ' at attempt ' + attempt); " +
                    "       } else if (attempt >= maxAttempts) { " +
                    "           clearInterval(clickInterval); " +
                    "           console.log('Catchup: gave up after ' + attempt + ' attempts, found ' + items.length + ' items'); " +
                    "       } " +
                    "   }, 500); " +
                    "})()", null
                )
            }
        }

        webView.loadUrl(url)

        val result = withTimeoutOrNull(35000) {
            deferred.await()
        }

        // Cache this WebView for next catchup
        cachedWebView?.destroy()
        if (result != null) {
            muteAndPauseWebView(webView)
            webView.onPause()
            webView.pauseTimers()
            cachedWebView = webView
            cachedStreamUrl = url
        } else {
            webView.destroy()
        }

        interceptCatchupOnly = false
        result
    }

    fun destroyCachedWebView() {
        cachedWebView?.destroy()
        cachedWebView = null
        cachedStreamUrl = null
    }

    suspend fun scrapeEpg(url: String): List<EpgProgram> = withContext(Dispatchers.IO) {
        val list = mutableListOf<EpgProgram>()
        try {
            val channelIdMatch = Regex("(\\d+)\\.html").find(url)
            val channelId = channelIdMatch?.groupValues?.get(1) ?: return@withContext emptyList()
            
            val sdf = java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", java.util.Locale.US)
            sdf.timeZone = java.util.TimeZone.getTimeZone("UTC")
            
                          val startCal = java.util.Calendar.getInstance().apply { 
                  set(java.util.Calendar.HOUR_OF_DAY, 0)
                  set(java.util.Calendar.MINUTE, 0)
                  set(java.util.Calendar.SECOND, 0)
              }
              val endCal = java.util.Calendar.getInstance().apply { 
                  add(java.util.Calendar.DAY_OF_YEAR, 1)
                  set(java.util.Calendar.HOUR_OF_DAY, 0)
                  set(java.util.Calendar.MINUTE, 0)
                  set(java.util.Calendar.SECOND, 0)
              }
            
            val startIso = sdf.format(startCal.time)
            val endIso = sdf.format(endCal.time)
            
            val apiUrl = "https://cache-api-vtvgo.vtvdigital.vn/cdn/live-channel/api/v1/channels/$channelId/programs?startIsoDate=${java.net.URLEncoder.encode(startIso, "UTF-8")}&endIsoDate=${java.net.URLEncoder.encode(endIso, "UTF-8")}"
            
            val connection = java.net.URL(apiUrl).openConnection() as java.net.HttpURLConnection
            connection.requestMethod = "GET"
            connection.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            connection.connectTimeout = 10000
            connection.readTimeout = 10000
            
            com.tvlaoto.util.AppLogger.d("StreamSniffer", "Requesting: "); val code = connection.responseCode; com.tvlaoto.util.AppLogger.d("StreamSniffer", "Response code: $code"); if (code == 200) {
                val inputStream = connection.inputStream
                val body = inputStream.bufferedReader().use { it.readText() }
                
                val jsonObj = org.json.JSONObject(body)
                val dataArr = jsonObj.optJSONArray("data"); if (dataArr == null) { android.util.Log.e("StreamSniffer", "data is null"); return@withContext emptyList() } else { com.tvlaoto.util.AppLogger.d("StreamSniffer", "Items: ${dataArr.length()}") }
                
                for (i in 0 until dataArr.length()) {
                    val item = dataArr.getJSONObject(i)
                    var title = item.optString("title", "").trim()
                    
                    title = title.replace(Regex("^Phim truyện:\\s*"), "")
                    
                    val startDateStr = item.optString("startDate")
                    var timeStr = ""
                    var startEpochMs = 0L
                    var endEpochMs = 0L
                    if (startDateStr.isNotEmpty()) {
                        try {
                            val date = sdf.parse(startDateStr)
                            val localSdf = java.text.SimpleDateFormat("HH:mm", java.util.Locale.US)
                            localSdf.timeZone = java.util.TimeZone.getDefault()
                            timeStr = date?.let { localSdf.format(it) } ?: ""
                            startEpochMs = date?.time?.div(1000) ?: 0L
                        } catch (e: Exception) {}
                    }
                    val endDateStr = item.optString("endDate")
                    if (endDateStr.isNotEmpty()) {
                        try {
                            val endDate = sdf.parse(endDateStr)
                            endEpochMs = endDate?.time?.div(1000) ?: 0L
                        } catch (e: Exception) {}
                    }
                    
                    list.add(
                        EpgProgram(
                            index = i,
                            time = timeStr,
                            title = title,
                            isReplayable = item.optInt("isPlayable", 1) == 1,
                            startEpoch = startEpochMs,
                            endEpoch = endEpochMs
                        )
                    )
                }
            }
        } catch (e: Exception) {
            android.util.Log.e("StreamSniffer", "Error", e)
        }
        list
    }
}

