import io
import re

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

new_scrape_epg = """    suspend fun scrapeEpg(url: String): List<EpgProgram> = withContext(Dispatchers.IO) {
        val list = mutableListOf<EpgProgram>()
        try {
            val channelIdMatch = Regex("-(\\\\w+)\\\\.html").find(url)
            val channelId = channelIdMatch?.groupValues?.get(1) ?: return@withContext emptyList()
            
            val sdf = java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", java.util.Locale.US)
            sdf.timeZone = java.util.TimeZone.getTimeZone("UTC")
            
            val startCal = java.util.Calendar.getInstance().apply { add(java.util.Calendar.DAY_OF_YEAR, -1) }
            val endCal = java.util.Calendar.getInstance().apply { add(java.util.Calendar.DAY_OF_YEAR, 2) }
            
            val startIso = sdf.format(startCal.time)
            val endIso = sdf.format(endCal.time)
            
            val apiUrl = "https://cache-api-vtvgo.vtvdigital.vn/cdn/live-channel/api/v1/channels/$channelId/programs?startIsoDate=${java.net.URLEncoder.encode(startIso, "UTF-8")}&endIsoDate=${java.net.URLEncoder.encode(endIso, "UTF-8")}"
            
            val connection = java.net.URL(apiUrl).openConnection() as java.net.HttpURLConnection
            connection.requestMethod = "GET"
            connection.connectTimeout = 10000
            connection.readTimeout = 10000
            
            if (connection.responseCode == 200) {
                val inputStream = connection.inputStream
                val body = inputStream.bufferedReader().use { it.readText() }
                
                val jsonObj = org.json.JSONObject(body)
                val dataArr = jsonObj.optJSONArray("data") ?: return@withContext emptyList()
                
                for (i in 0 until dataArr.length()) {
                    val item = dataArr.getJSONObject(i)
                    var title = item.optString("title", "").trim()
                    
                    // Xóa các tiền tố không cần thiết để giống trên WebView
                    title = title.replace(Regex("^Phim truyện:\\\\s*"), "")
                    
                    val startDateStr = item.optString("startDate")
                    var timeStr = ""
                    if (startDateStr.isNotEmpty()) {
                        try {
                            val date = sdf.parse(startDateStr)
                            val localSdf = java.text.SimpleDateFormat("HH:mm", java.util.Locale.US)
                            localSdf.timeZone = java.util.TimeZone.getDefault()
                            timeStr = date?.let { localSdf.format(it) } ?: ""
                        } catch (e: Exception) {}
                    }
                    
                    list.add(
                        EpgProgram(
                            index = i,
                            time = timeStr,
                            title = title,
                            isReplayable = item.optInt("isPlayable", 1) == 1
                        )
                    )
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        list
    }"""

# Replace the old scrapeEpg
content = re.sub(r'    @SuppressLint\("SetJavaScriptEnabled"\)\s*suspend fun scrapeEpg\(url: String\): List<EpgProgram> = withContext\(Dispatchers.Main\) \{.*?\n    \}', new_scrape_epg, content, flags=re.DOTALL)

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Replaced scrapeEpg with direct API call!")
