package com.tvlaoto.network

import android.annotation.SuppressLint
import android.content.Context
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.core.content.ContextCompat
import okhttp3.Interceptor
import okhttp3.Request
import okhttp3.Response
import java.io.IOException
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

class CloudflareInterceptor(private val context: Context) : Interceptor {

    private val executor = ContextCompat.getMainExecutor(context)
    private val cookieManager = CookieManager.getInstance()

    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        
        // Inject any existing cf_clearance cookie from WebView
        var request = injectWebViewCookies(originalRequest)
        
        var response = chain.proceed(request)

        if (isCloudflareChallenge(response)) {
            response.close()
            try {
                val success = resolveWithWebView(request)
                if (success) {
                    request = injectWebViewCookies(originalRequest)
                    response = chain.proceed(request)
                } else {
                    throw IOException("Cloudflare challenge failed")
                }
            } catch (e: Exception) {
                throw IOException("Cloudflare bypass error: {e.message}", e)
            }
        }
        
        return response
    }

    private fun isCloudflareChallenge(response: Response): Boolean {
        return (response.code == 403 || response.code == 503) &&
                (response.header("Server")?.contains("cloudflare", ignoreCase = true) == true ||
                 response.header("cf-mitigated") == "challenge")
    }

    private fun injectWebViewCookies(request: Request): Request {
        val url = request.url.toString()
        val webViewCookies = cookieManager.getCookie(url)
        return if (!webViewCookies.isNullOrBlank()) {
            request.newBuilder()
                .header("Cookie", webViewCookies)
                .build()
        } else {
            request
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun resolveWithWebView(request: Request): Boolean {
        val latch = CountDownLatch(1)
        var webview: WebView? = null
        var isBypassed = false
        val origRequestUrl = request.url.toString()

        executor.execute {
            webview = WebView(context).apply {
                settings.javaScriptEnabled = true
                settings.domStorageEnabled = true
                settings.databaseEnabled = true
                settings.userAgentString = request.header("User-Agent") ?: settings.userAgentString

                webViewClient = object : WebViewClient() {
                    override fun onPageFinished(view: WebView, url: String) {
                        val cookies = cookieManager.getCookie(origRequestUrl)
                        if (cookies != null && cookies.contains("cf_clearance")) {
                            isBypassed = true
                            latch.countDown()
                        }
                        
                        // Wait a bit just in case
                        view.postDelayed({ latch.countDown() }, 8000)
                    }

                    override fun onReceivedHttpError(
                        view: WebView,
                        request: WebResourceRequest,
                        errorResponse: WebResourceResponse
                    ) {
                        // Ignore standard 403/503 during challenge, we wait for cf_clearance
                    }
                }
                loadUrl(origRequestUrl)
            }
        }

        // Wait up to 15 seconds for Cloudflare challenge to pass
        latch.await(15, TimeUnit.SECONDS)

        executor.execute {
            webview?.stopLoading()
            webview?.destroy()
        }

        return isBypassed
    }
}
