with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# find the first occurrence and remove it
content = content.replace(
'''    val epgList by playerViewModel.epgList.collectAsState()
    val currentCatchupProgram by playerViewModel.currentCatchupProgram.collectAsState()
    
    val liveProgram = remember(epgList) {''',
'''    val epgList by playerViewModel.epgList.collectAsState()
    
    val liveProgram = remember(epgList) {''')

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed duplicate currentCatchupProgram")
