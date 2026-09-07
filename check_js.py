import re
with open('app/src/main/java/com/tvlaoto/network/StreamSniffer.kt', 'r', encoding='utf-8') as f:
    text = f.read()

scrape_epg = re.search(r'fun scrapeEpg.*?WebViewClient.*?evaluateJavascript\((.*?)\)', text, re.DOTALL).group(1)
print(scrape_epg)
