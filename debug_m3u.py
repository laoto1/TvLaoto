with open('app/src/main/java/com/tvlaoto/data/parser/M3uParser.kt', 'rb') as f:
    content = f.read()

idx = content.find(b'ng H')
if idx != -1:
    print('Tong Hop:', content[idx-10:idx+20])

idx = content.find(b'K')
if idx != -1:
    print('Kenh:', content[idx:idx+20])
