with open('app/build.gradle.kts', 'r', encoding='utf-8') as f:
    content = f.read()

dep_old = 'implementation("org.mozilla.geckoview:geckoview-omni:154.0.20260824154132")'
dep_new = 'implementation("org.mozilla.geckoview:geckoview-omni:121.0.20231214155439")'

content = content.replace(dep_old, dep_new)

with open('app/build.gradle.kts', 'w', encoding='utf-8') as f:
    f.write(content)
print("Downgraded geckoview")
