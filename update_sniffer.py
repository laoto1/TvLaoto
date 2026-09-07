code = """package com.tvlaoto.network

import android.content.Context
import android.util.Log
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import org.json.JSONArray
import org.json.JSONObject
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.WebExtension
import com.tvlaoto.data.model.EpgProgram

class StreamSniffer(private val context: Context) {

    private val runtime: GeckoRuntime by lazy {
        GeckoRuntime.create(context)
    }

    private var extension: WebExtension? = null

    // Register extension once
    private fun ensureExtension() {
        if (extension == null) {
            val controller = runtime.webExtensionController
            // installBuiltIn is deprecated in some versions, install is used.
            // But let's use installBuiltIn if possible. 
            // In geckoview 154, it's installBuiltIn("resource://android/assets/ext/")
            val extTask = controller.installBuiltIn("resource://android/assets/ext/")
            // We can't await easily outside suspend, so we just let it run.
            // Wait, we need it installed before sniffing.
        }
    }

    suspend fun sniff(url: String): String? = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<String>()
        val session = GeckoSession()
        
        try {
            val ext = runtime.webExtensionController.installBuiltIn("resource://android/assets/ext/").poll(10000)
            
            runtime.webExtensionController.setMessageDelegate(ext, object : WebExtension.MessageDelegate {
                override fun onMessage(nativeApp: String, message: Any, sender: WebExtension.MessageSender): WebExtension.MessageDelegate.GeckoResult<Any>? {
                    if (nativeApp == "sniffer_port" && message is JSONObject) {
                        val type = message.optString("type")
                        if (type == "m3u8") {
                            val m3u8Url = message.optString("url")
                            if (!deferred.isCompleted) {
                                deferred.complete(m3u8Url)
                            }
                        }
                    }
                    return null
                }
            }, "sniffer_port")
        } catch(e: Exception) {
            Log.e("StreamSniffer", "Ext error", e)
        }

        session.open(runtime)
        session.loadUri(url)

        val result = withTimeoutOrNull(15000) {
            deferred.await()
        }
        
        session.close()
        result
    }

    suspend fun sniffCatchup(url: String, programIndex: Int): String? = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<String>()
        val session = GeckoSession()

        try {
            val ext = runtime.webExtensionController.installBuiltIn("resource://android/assets/ext/").poll(10000)
            runtime.webExtensionController.setMessageDelegate(ext, object : WebExtension.MessageDelegate {
                override fun onMessage(nativeApp: String, message: Any, sender: WebExtension.MessageSender): WebExtension.MessageDelegate.GeckoResult<Any>? {
                    if (nativeApp == "sniffer_port" && message is JSONObject) {
                        val type = message.optString("type")
                        if (type == "m3u8") {
                            val m3u8Url = message.optString("url")
                            // Catch-up links usually contain "catchup" or "timeshift"
                            if (m3u8Url.contains("catchup") || m3u8Url.contains("timeshift") || m3u8Url.contains("start=")) {
                                if (!deferred.isCompleted) {
                                    deferred.complete(m3u8Url)
                                }
                            }
                        }
                    }
                    return null
                }
            }, "sniffer_port")
        } catch(e: Exception) { }

        session.open(runtime)
        session.loadUri(url)

        val result = withTimeoutOrNull(20000) {
            deferred.await()
        }
        session.close()
        result
    }

    suspend fun scrapeEpg(url: String): List<EpgProgram> = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<List<EpgProgram>>()
        val session = GeckoSession()

        try {
            val ext = runtime.webExtensionController.installBuiltIn("resource://android/assets/ext/").poll(10000)
            runtime.webExtensionController.setMessageDelegate(ext, object : WebExtension.MessageDelegate {
                override fun onMessage(nativeApp: String, message: Any, sender: WebExtension.MessageSender): WebExtension.MessageDelegate.GeckoResult<Any>? {
                    if (nativeApp == "sniffer_port" && message is JSONObject) {
                        val type = message.optString("type")
                        if (type == "epg") {
                            val dataStr = message.optString("data")
                            val list = mutableListOf<EpgProgram>()
                            try {
                                val arr = JSONArray(dataStr)
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
                            } catch (e: Exception) {}
                        }
                    }
                    return null
                }
            }, "sniffer_port")
        } catch(e: Exception) { }

        session.open(runtime)
        session.loadUri(url)

        val result = withTimeoutOrNull(15000) {
            deferred.await()
        } ?: emptyList()
        
        session.close()
        result
    }
}
"""
with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated StreamSniffer.kt")
