with open('app/build.gradle.kts', 'r', encoding='utf-8') as f:
    content = f.read()

dep = 'implementation("org.mozilla.geckoview:geckoview:120.0.20231130173617")'

if dep not in content:
    content = content.replace('dependencies {', 'dependencies {\n    ' + dep)
    with open('app/build.gradle.kts', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added geckoview dependency")
else:
    print("Already added")
