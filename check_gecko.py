import urllib.request
import re
try:
    url = "https://maven.mozilla.org/maven2/org/mozilla/geckoview/geckoview-default/maven-metadata.xml"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        xml = response.read().decode('utf-8')
        match = re.search(r"<release>([^<]+)</release>", xml)
        if match:
            print("Latest release:", match.group(1))
        else:
            print("Could not parse version.")
except Exception as e:
    print(e)
