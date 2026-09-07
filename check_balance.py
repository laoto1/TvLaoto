with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

balance = 0
for i, line in enumerate(lines):
    for char in line:
        if char == '{': balance += 1
        elif char == '}': balance -= 1
    if balance == 0 and i > 20: # Exclude imports block if any
        print(f"File balanced at line {i+1}: {line.strip()}")
        break
