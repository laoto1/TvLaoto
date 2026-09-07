with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'rb') as f:
    content = f.read()

idx = content.find(b'Truy')
if idx != -1:
    print('Truy:', content[idx:idx+20])

idx = content.find(b'T')
# let's just find "T?t c?"
idx = content.find(b'T?t c')
if idx != -1:
    print('Tat ca:', content[idx:idx+20])
