import re
with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("            if (connection.responseCode == 200) {", "            android.util.Log.d(\\"StreamSniffer\\", \\"API Request: $apiUrl\\")\n            val code = connection.responseCode\n            android.util.Log.d(\\"StreamSniffer\\", \\"API Response Code: $code\\")\n            if (code == 200) {")
content = content.replace("                val dataArr = jsonObj.optJSONArray(\\"data\\") ?: return@withContext emptyList()", "                val dataArr = jsonObj.optJSONArray(\\"data\\")\n                if (dataArr == null) {\n                    android.util.Log.e(\\"StreamSniffer\\", \\"dataArr is null. Body: $body\\")\n                    return@withContext emptyList()\n                }\n                android.util.Log.d(\\"StreamSniffer\\", \\"Parsed ${dataArr.length()} items\\")")
content = content.replace("        } catch (e: Exception) {", "        } catch (e: Exception) {\n            android.util.Log.e(\\"StreamSniffer\\", \\"Error in scrapeEpg\\", e)")

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Added logging")
