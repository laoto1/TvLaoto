with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """            repository.playlist.collect { playlist ->
                allChannels = playlist?.categories?.flatMap { it.channels } ?: emptyList()
                val current = _currentChannel.value
                if (current != null) {
                    val updated = allChannels.find { it.id == current.id }
                    if (updated != null && updated.isFavorite != current.isFavorite) {
                        _currentChannel.value = updated
                    }
                }
            }"""

content = content.replace(
    "repository.playlist.collect { playlist ->\n                allChannels = playlist?.categories?.flatMap { it.channels } ?: emptyList()\n            }",
    replacement
)

with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated PlayerViewModel to sync currentChannel")
