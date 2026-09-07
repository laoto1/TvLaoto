with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    text = f.read()

# find all multiline comments
import re
print("Multiline comments:")
for m in re.finditer(r'/\*.*?\*/', text, re.DOTALL):
    print(m.group(0))

print("Strings with braces:")
for m in re.finditer(r'"[^"\\]*(?:\\.[^"\\]*)*"', text):
    if '{' in m.group(0) or '}' in m.group(0):
        print(m.group(0))

print("Comments with braces:")
for m in re.finditer(r'//.*', text):
    if '{' in m.group(0) or '}' in m.group(0):
        print(m.group(0))
