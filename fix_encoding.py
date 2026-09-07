with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Dang b? kha lin k?t...", "Đang bẻ khóa liên kết...")
content = content.replace("Đang bẻ khóa liên kết...", "Đang bẻ khóa liên kết...")

while "        }\n        }\n        }\n" in content:
    content = content.replace("        }\n        }\n        }\n", "        }\n        }\n")

with open('app/src/main/java/com/tvlaoto/ui/screens/PlayerScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)


with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Dang b? kha lin k?t...", "Đang bẻ khóa liên kết...")

while "        }\n        }\n        }\n" in content:
    content = content.replace("        }\n        }\n        }\n", "        }\n        }\n")

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed encoding and braces")
