with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# find all strings with ? or replacement chars inside them
import re
matches = re.findall(r'"[^"]*[\x80-\xFF\?][^"]*"', content)
print('Suspicious strings:', matches)
