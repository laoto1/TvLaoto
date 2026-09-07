import re
with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Change startCal to TODAY start (00:00:00) and endCal to TOMORROW start (00:00:00)
new_dates = """              val startCal = java.util.Calendar.getInstance().apply { 
                  set(java.util.Calendar.HOUR_OF_DAY, 0)
                  set(java.util.Calendar.MINUTE, 0)
                  set(java.util.Calendar.SECOND, 0)
              }
              val endCal = java.util.Calendar.getInstance().apply { 
                  add(java.util.Calendar.DAY_OF_YEAR, 1)
                  set(java.util.Calendar.HOUR_OF_DAY, 0)
                  set(java.util.Calendar.MINUTE, 0)
                  set(java.util.Calendar.SECOND, 0)
              }"""

content = re.sub(r'val startCal = java.util.Calendar.getInstance\(\).apply \{ add\(java.util.Calendar.DAY_OF_YEAR, -1\) \}.*?val endCal = java.util.Calendar.getInstance\(\).apply \{ add\(java.util.Calendar.DAY_OF_YEAR, 2\) \}', new_dates, content, flags=re.DOTALL)

with open("app/src/main/java/com/tvlaoto/network/StreamSniffer.kt", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated EPG dates to only today!")
