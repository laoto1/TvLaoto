import re

with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'r', encoding='utf-8') as f:
    content = f.read()

imports_to_add = """import android.webkit.JavascriptInterface
import org.json.JSONArray
import com.tvlaoto.data.model.EpgProgram"""

content = content.replace("import kotlinx.coroutines.withTimeoutOrNull", "import kotlinx.coroutines.withTimeoutOrNull\n" + imports_to_add)

new_functions = """
    class EpgJsInterface(private val onResult: (String) -> Unit) {
        @JavascriptInterface
        fun postEpg(json: String) {
            onResult(json)
        }
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
                    "           var btn = item.querySelector('button, a, svg, .replay'); " +
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
"""

content = content.replace("}", new_functions + "\n}")

# Fix nested class issue (we inserted before the last closing brace of StreamSniffer class, but we need to ensure it's inside the class correctly)
# Actually, replacing the very last '}' with 'new_functions \n}' will put them inside the class. Let's make sure it's the last brace.
parts = content.rsplit('}', 1)
content = parts[0] + new_functions + "\n}"

with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated StreamSniffer.kt")
