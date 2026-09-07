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
            // Giả lập Desktop Chrome để vượt qua các web cấm mobile
            userAgentString = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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
        }

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
