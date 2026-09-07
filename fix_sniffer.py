code = """package com.tvlaoto.network

import android.content.Context
import android.util.Log
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import org.json.JSONArray
import org.json.JSONObject
import org.mozilla.geckoview.GeckoResult
import org.mozilla.geckoview.GeckoRuntime
import org.mozilla.geckoview.GeckoSession
import org.mozilla.geckoview.WebExtension
import com.tvlaoto.data.model.EpgProgram

class StreamSniffer(private val context: Context) {

    private val runtime: GeckoRuntime by lazy {
        GeckoRuntime.create(context)
    }
    
    private var extension: WebExtension? = null
    
    private suspend fun getExtension(): WebExtension? = withContext(Dispatchers.Main) {
        if (extension != null) return@withContext extension
        val deferred = CompletableDeferred<WebExtension?>()
        runtime.webExtensionController.installBuiltIn("resource://android/assets/ext/")
            .accept({ ext -> 
                extension = ext
                deferred.complete(ext)
            }, { e -> 
                Log.e("StreamSniffer", "Ext fail", e)
                deferred.complete(null)
            })
        deferred.await()
    }

    suspend fun sniff(url: String): String? = withContext(Dispatchers.Main) {
        val deferred = CompletableDeferred<String>()
        val session = GeckoSession()
        
        val ext = getExtension()
        if (ext != null) {
            runtime.webExtensionController.setMessageDelegate(ext, object : WebExtension.MessageDelegate {
                override fun onMessage(nativeApp: String, message: Any, sender: WebExtension.MessageSender): GeckoResult<Any>? {
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

        val ext = getExtension()
        if (ext != null) {
            runtime.webExtensionController.setMessageDelegate(ext, object : WebExtension.MessageDelegate {
                override fun onMessage(nativeApp: String, message: Any, sender: WebExtension.MessageSender): GeckoResult<Any>? {
                    if (nativeApp == "sniffer_port" && message is JSONObject) {
                        val type = message.optString("type")
                        if (type == "m3u8") {
                            val m3u8Url = message.optString("url")
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
        }

        session.open(runtime)
        // Click program item logic needs to be added via JS, or just use the same URL if it opens that program directly.
        // Wait, Catchup URLs are just the channel url + some query parameters or we have to click!
        // In previous implementation, I added an inject JS to click the `programIndex`.
        // Let's modify content.js to check if we are in catchup mode?
        // Wait, content.js always clicks `playBtn`. How to click `programIndex`?
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

        val ext = getExtension()
        if (ext != null) {
            runtime.webExtensionController.setMessageDelegate(ext, object : WebExtension.MessageDelegate {
                override fun onMessage(nativeApp: String, message: Any, sender: WebExtension.MessageSender): GeckoResult<Any>? {
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
        }

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
print("Fixed StreamSniffer.kt")
