with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('fun HomeScreen')
balance = 0
for i, char in enumerate(content[idx:]):
    if char == '{': balance += 1
    elif char == '}': balance -= 1
    
    if balance == 0 and char == '}':
        # Found the end of HomeScreen
        # Count what line this is
        line_num = content[:idx+i].count('\n') + 1
        print(f"HomeScreen ends at line {line_num}")
        break
