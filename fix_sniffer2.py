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
            // Sử dụng User-Agent gốc của thiết bị (giống cách Tachiyomi/Mihon vượt Cloudflare)
            userAgentString = android.webkit.WebSettings.getDefaultUserAgent(context)
        }

        webView.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(
                view: WebView?,
                request: WebResourceRequest?
            ): WebResourceResponse? {
                val reqUrl = request?.url?.toString() ?: ""
                
                if (reqUrl.contains(".m3u8")) {
                    if (!deferred.isCompleted) {
                        deferred.complete(reqUrl)
                    }
                }
                return super.shouldInterceptRequest(view, request)
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                // Force play all videos and trigger network requests even if headless
                view?.evaluateJavascript(
                    "(function() { " +
                    "   setInterval(function() { " +
                    "       var vids = document.getElementsByTagName('video'); " +
                    "       for(var i=0; i<vids.length; i++) { " +
                    "           vids[i].muted = true; " +
                    "           vids[i].play(); " +
                    "       } " +
                    "   }, 1000); " +
                    "})();", null
                )
            }
        }
        
        // Cấp kích thước giả để lừa các trình phát video dùng IntersectionObserver (lười tải)
        webView.layout(0, 0, 1920, 1080)

        webView.loadUrl(url)

        // Đợi tối đa 15 giây để tránh treo app nếu không tìm thấy link
        val result = withTimeoutOrNull(15000L) {
            deferred.await()
        }
        
        // Dọn dẹp WebView để giải phóng RAM
        webView.stopLoading()
        webView.destroy()
        
        return@withContext result
    }
}
"""

with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed StreamSniffer.kt")
