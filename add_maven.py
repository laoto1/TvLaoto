with open('settings.gradle.kts', 'r', encoding='utf-8') as f:
    content = f.read()

target = """    repositories {
        google()
        mavenCentral()"""
        
replacement = """    repositories {
        google()
        mavenCentral()
        maven("https://maven.mozilla.org/maven2/")"""
        
if target in content and "maven.mozilla.org" not in content:
    content = content.replace(target, replacement)
    with open('settings.gradle.kts', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added Mozilla maven to settings")
else:
    print("Mozilla maven already present or target not found")
