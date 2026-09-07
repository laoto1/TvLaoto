with open('app/build.gradle.kts', 'r', encoding='utf-8') as f:
    content = f.read()

dep_old = 'implementation("org.mozilla.geckoview:geckoview:120.0.20231130173617")'
dep_new = 'implementation("org.mozilla.geckoview:geckoview-omni:154.0.20260824154132")'

if dep_old in content:
    content = content.replace(dep_old, dep_new)
else:
    content = content.replace('dependencies {', 'dependencies {\n    ' + dep_new)

with open('app/build.gradle.kts', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added geckoview-omni dependency")
