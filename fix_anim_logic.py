with open('app/src/main/java/com/tvlaoto/ui/components/SearchOverlayDialog.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the inside LaunchedEffect
content = content.replace("""                // Wait for exit animation to finish before calling real onDismiss
                LaunchedEffect(isVisible) {
                    if (!isVisible) {
                        delay(200)
                        onDismiss()
                    }
                }""", "")

# Replace the top declarations
new_top = """    var isVisible by remember { mutableStateOf(false) }
    var hasOpened by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        isVisible = true
        hasOpened = true
    }

    val triggerDismiss = {
        isVisible = false
    }
    
    LaunchedEffect(isVisible) {
        if (hasOpened && !isVisible) {
            delay(200)
            onDismiss()
        }
    }"""

content = content.replace("""    var isVisible by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        isVisible = true
    }

    val triggerDismiss = {
        isVisible = false
    }""", new_top)

with open('app/src/main/java/com/tvlaoto/ui/components/SearchOverlayDialog.kt', 'w', encoding='utf-8') as f:
    f.write(content)
