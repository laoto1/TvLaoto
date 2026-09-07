import re

with open('app/src/main/java/com/tvlaoto/data/parser/M3uParser.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific lines inside M3uParser
# Old: val (progTitle, progTime, progDesc) = ChannelLogoProvider.getProgramMock(currentChannelName)
# We will just remove it, and also remove assigning it to currentProgram, programTime, programDescription since they have defaults

content = content.replace("val (progTitle, progTime, progDesc) = ChannelLogoProvider.getProgramMock(currentChannelName)", "")
content = content.replace("                        currentProgram = progTitle,\n", "")
content = content.replace("                        programTime = progTime,\n", "")
content = content.replace("                        programDescription = progDesc,\n", "")
content = content.replace("import com.tvlaoto.data.provider.ChannelLogoProvider\n", "")

with open('app/src/main/java/com/tvlaoto/data/parser/M3uParser.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated M3uParser")
