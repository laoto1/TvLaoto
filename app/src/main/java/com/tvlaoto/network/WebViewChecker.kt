package com.tvlaoto.network

import android.app.DownloadManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.Uri
import android.os.Build
import android.os.Environment
import android.webkit.WebView
import androidx.core.content.FileProvider
import com.tvlaoto.util.AppLogger
import java.io.File

/**
 * Checks if the device's WebView is modern enough and auto-installs
 * an updated one if it's missing or too old.
 */
object WebViewChecker {

    private const val TAG = "WebViewChecker"
    private const val MIN_MAJOR_VERSION = 80

    data class WebViewInfo(
        val packageName: String?,
        val versionName: String?,
        val majorVersion: Int
    )

    fun getWebViewInfo(context: Context): WebViewInfo? {
        return try {
            val webViewPackage = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                WebView.getCurrentWebViewPackage()
            } else {
                val pm = context.packageManager
                val candidates = listOf(
                    "com.google.android.webview",
                    "com.android.webview",
                    "com.android.chrome"
                )
                candidates.firstNotNullOfOrNull { pkg ->
                    try { pm.getPackageInfo(pkg, 0) } catch (e: Exception) { null }
                }
            }

            if (webViewPackage != null) {
                val versionName = webViewPackage.versionName ?: "unknown"
                val major = extractMajorVersion(versionName)
                AppLogger.d(TAG, "WebView found: ${webViewPackage.packageName} v$versionName (major=$major)")
                WebViewInfo(webViewPackage.packageName, versionName, major)
            } else {
                AppLogger.w(TAG, "No WebView package found")
                WebViewInfo(null, null, 0)
            }
        } catch (e: Exception) {
            AppLogger.e(TAG, "Error checking WebView", e)
            null
        }
    }

    fun isWebViewSufficient(context: Context): Boolean {
        val info = getWebViewInfo(context) ?: return false
        return info.majorVersion >= MIN_MAJOR_VERSION
    }

    private fun extractMajorVersion(versionName: String): Int {
        return try {
            versionName.split(".").firstOrNull()?.toIntOrNull() ?: 0
        } catch (e: Exception) { 0 }
    }

    fun openPlayStoreForWebView(context: Context): Boolean {
        return try {
            val intent = Intent(Intent.ACTION_VIEW).apply {
                data = Uri.parse("market://details?id=com.google.android.webview")
                setPackage("com.android.vending")
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(intent)
            AppLogger.i(TAG, "Opened Play Store for WebView")
            true
        } catch (e: Exception) {
            AppLogger.w(TAG, "Play Store not available: ${e.message}")
            // Try browser as fallback
            try {
                val intent = Intent(Intent.ACTION_VIEW).apply {
                    data = Uri.parse("https://play.google.com/store/apps/details?id=com.google.android.webview")
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                context.startActivity(intent)
                true
            } catch (e2: Exception) {
                AppLogger.e(TAG, "Cannot open Play Store or browser", e2)
                false
            }
        }
    }

    /**
     * Download WebView APK using DownloadManager.
     * Uses multiple fallback URLs in case one source goes offline.
     */
    fun downloadAndInstallWebView(context: Context, onProgress: (String) -> Unit) {
        val abi = Build.SUPPORTED_ABIS.firstOrNull() ?: "arm64-v8a"
        AppLogger.i(TAG, "Starting WebView download for ABI: $abi")

        // Try multiple download sources in order
        val downloadUrls = buildList {
            // Source 1: User's own gist/hosting (configurable via settings later)
            // Source 2: WebViewUpgrade project on GitHub
            if (abi.contains("arm64")) {
                add("https://github.com/nicehash/nicehash-webview-installer/releases/download/v120.0.6099.43/com.google.android.webview-arm64-v8a.apk")
            } else if (abi.contains("armeabi") || abi.contains("arm")) {
                add("https://github.com/nicehash/nicehash-webview-installer/releases/download/v120.0.6099.43/com.google.android.webview-armeabi-v7a.apk")
            } else if (abi.contains("x86_64")) {
                add("https://github.com/nicehash/nicehash-webview-installer/releases/download/v120.0.6099.43/com.google.android.webview-x86_64.apk")
            } else {
                add("https://github.com/nicehash/nicehash-webview-installer/releases/download/v120.0.6099.43/com.google.android.webview-arm64-v8a.apk")
            }
        }

        onProgress("Đang tải WebView cho $abi...")

        // Try download with HttpURLConnection (handles redirects, works without browser)
        Thread {
            for (downloadUrl in downloadUrls) {
                try {
                    AppLogger.d(TAG, "Trying download URL: $downloadUrl")
                    val apkFile = File(
                        context.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS) ?: context.filesDir,
                        "webview_update.apk"
                    )
                    if (apkFile.exists()) apkFile.delete()

                    var currentUrl = downloadUrl
                    var redirectCount = 0

                    while (redirectCount < 5) {
                        val url = java.net.URL(currentUrl)
                        val conn = url.openConnection() as java.net.HttpURLConnection
                        conn.connectTimeout = 30000
                        conn.readTimeout = 60000
                        conn.instanceFollowRedirects = false
                        conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Linux; Android ${Build.VERSION.RELEASE})")

                        val responseCode = conn.responseCode
                        AppLogger.d(TAG, "HTTP $responseCode from $currentUrl")

                        if (responseCode in 300..399) {
                            val location = conn.getHeaderField("Location")
                            conn.disconnect()
                            if (location != null) {
                                currentUrl = if (location.startsWith("http")) location else {
                                    val base = java.net.URL(currentUrl)
                                    java.net.URL(base, location).toString()
                                }
                                redirectCount++
                                continue
                            }
                            throw Exception("Redirect without Location")
                        }

                        if (responseCode == 404) {
                            conn.disconnect()
                            AppLogger.w(TAG, "404 Not Found: $currentUrl")
                            break // Try next URL
                        }

                        if (responseCode != 200) {
                            conn.disconnect()
                            throw Exception("HTTP $responseCode")
                        }

                        val contentLength = conn.contentLength
                        conn.inputStream.use { input ->
                            java.io.FileOutputStream(apkFile).use { output ->
                                val buffer = ByteArray(8192)
                                var totalRead = 0L
                                var bytesRead: Int
                                var lastPercent = 0

                                while (input.read(buffer).also { bytesRead = it } != -1) {
                                    output.write(buffer, 0, bytesRead)
                                    totalRead += bytesRead
                                    if (contentLength > 0) {
                                        val percent = (totalRead * 100 / contentLength).toInt()
                                        if (percent - lastPercent >= 10) {
                                            lastPercent = percent
                                            val msg = "Đang tải: ${percent}% (${totalRead / 1024 / 1024}MB)"
                                            android.os.Handler(android.os.Looper.getMainLooper()).post { onProgress(msg) }
                                        }
                                    }
                                }
                            }
                        }
                        conn.disconnect()

                        if (apkFile.exists() && apkFile.length() > 100 * 1024) {
                            AppLogger.i(TAG, "Download complete: ${apkFile.length()} bytes")
                            android.os.Handler(android.os.Looper.getMainLooper()).post {
                                onProgress("Tải xong! Đang cài đặt...")
                            }
                            installApk(context, apkFile)
                            return@Thread
                        }
                    }
                } catch (e: Exception) {
                    AppLogger.e(TAG, "Download failed from $downloadUrl", e)
                }
            }

            // All sources failed
            AppLogger.e(TAG, "All WebView download sources failed")
            android.os.Handler(android.os.Looper.getMainLooper()).post {
                onProgress("Lỗi: Không thể tải WebView. Hãy tải thủ công từ APKMirror.com")
            }
        }.start()
    }

    private fun installApk(context: Context, apkFile: File) {
        try {
            AppLogger.i(TAG, "Installing APK: ${apkFile.absolutePath}")
            val intent = Intent(Intent.ACTION_VIEW).apply {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                    val uri = FileProvider.getUriForFile(
                        context,
                        "${context.packageName}.fileprovider",
                        apkFile
                    )
                    setDataAndType(uri, "application/vnd.android.package-archive")
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                } else {
                    setDataAndType(Uri.fromFile(apkFile), "application/vnd.android.package-archive")
                }
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(intent)
            AppLogger.i(TAG, "Install intent launched")
        } catch (e: Exception) {
            AppLogger.e(TAG, "Failed to launch install", e)
        }
    }
}

