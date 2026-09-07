with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    text = f.read()

open_braces = text.count('{')
close_braces = text.count('}')
print("Open:", open_braces, "Close:", close_braces)
