with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'rb') as f:
    data = f.read()

# Remove NUL bytes and BOM if any
data = data.replace(b'\x00', b'')

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'wb') as f:
    f.write(data)
