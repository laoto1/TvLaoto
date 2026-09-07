with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

if "import androidx.compose.ui.graphics.graphicsLayer" not in content:
    content = content.replace(
        "import androidx.compose.ui.graphics.Color", 
        "import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.graphicsLayer\nimport androidx.compose.ui.draw.drawWithCache\nimport androidx.compose.ui.draw.blur"
    )

with open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
