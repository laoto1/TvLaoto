with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
with open('check_home.txt', 'w', encoding='utf-8') as f:
    f.write("".join(lines[360:]))
