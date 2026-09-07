with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("            }\n        }\n        }\n\n        // Error", "            }\n        }\n\n        // Error")

with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("            }\n        }\n        }\n\n        // Controls", "            }\n        }\n\n        // Controls")
content = content.replace("            }\n        }\n        }\n\n        // Volume", "            }\n        }\n\n        // Volume")
content = content.replace("            }\n        }\n        }\n\n", "            }\n        }\n\n")

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed extra braces")
