import re
with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Fix sniff
sniff_old = """                if (reqUrl.contains(".m3u8")) {
                    if (!deferred.isCompleted) {
                        deferred.complete(reqUrl)
                    }
                }"""
sniff_new = """                if (reqUrl.contains(".m3u8") && !reqUrl.contains("api")) {
                    if (!deferred.isCompleted) {
                        android.util.Log.d("StreamSniffer", "Sniff Live OK: $reqUrl")
                        deferred.complete(reqUrl)
                    }
                }"""
content = content.replace(sniff_old, sniff_new)

# Fix sniffCatchup
catchup_old = """                if (reqUrl.contains("catchup") || reqUrl.contains("timeshift") || reqUrl.contains("start=")) {
                    if (!deferred.isCompleted) {
                        deferred.complete(reqUrl)
                    }
                }"""
catchup_new = """                if ((reqUrl.contains("catchup") || reqUrl.contains("timeshift") || reqUrl.contains("start=")) && reqUrl.contains(".m3u8") && !reqUrl.contains("api")) {
                    if (!deferred.isCompleted) {
                        android.util.Log.d("StreamSniffer", "Sniff Catchup OK: $reqUrl")
                        deferred.complete(reqUrl)
                    }
                }"""
content = content.replace(catchup_old, catchup_new)

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated interceptors to be strictly .m3u8")
