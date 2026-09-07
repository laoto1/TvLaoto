with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'rb') as f:
    content = f.read()

idx = content.find(b'T\xe1\xba\xa5t')
if idx != -1:
    print('Tat ca:', content[idx:idx+20])
else:
    print('Tat ca (UTF-8) not found!')

idx = content.find(b'T\x3ft')
if idx != -1:
    print('Tat ca (?):', content[idx:idx+20])
