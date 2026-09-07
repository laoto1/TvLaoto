import re

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Logic to determine actual title, time, and if we show the LIVE tag.
logic = """
    if (channel == null) return

    val displayTitle = currentCatchupProgram?.title ?: liveProgram?.title ?: channel.currentProgram
    val displayTime = currentCatchupProgram?.time ?: liveProgram?.time ?: channel.programTime
    val isLiveStream = currentCatchupProgram == null

    Row(
"""

content = content.replace("    if (channel == null) return\n\n    Row(\n", logic)
content = content.replace("text = channel.currentProgram,", "text = displayTitle,")
content = content.replace("text = channel.programTime,", "text = displayTime,")

# Now wrap the LIVE tag inside `if (isLiveStream) { ... }`
# Find the Box that contains the LIVE text
live_tag_pattern = r'Box\(\s*modifier = Modifier\s*\.clip\(GtaShapes\.TagShape\)\s*\.background\(Color\(0xFFEC4899\)\)\s*\.padding\(horizontal = 7\.dp, vertical = 2\.dp\)\s*\)\s*\{\s*Text\(\s*text = "LIVE"[^}]+\)\s*\}'
live_tag_match = re.search(live_tag_pattern, content)
if live_tag_match:
    original = live_tag_match.group(0)
    new_tag = "if (isLiveStream) {\n                " + original.replace('\n', '\n                ') + "\n                }"
    content = content.replace(original, new_tag)

with open('app/src/main/java/com/tvlaoto/ui/components/ProgramInfoPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated ProgramInfoPanel to use dynamic EPG info")
