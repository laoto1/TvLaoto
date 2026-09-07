with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
'''    val errorMessage: StateFlow<String?> = _errorMessage.asStateFlow()''',
'''    val errorMessage: StateFlow<String?> = _errorMessage.asStateFlow()

    fun clearError() {
        _errorMessage.value = null
    }''')

content = content.replace(
'''                _errorMessage.value = "Không thể lấy liên kết xem lại."''',
'''                _errorMessage.value = "Chương trình này hiện không khả dụng hoặc không tồn tại để xem lại!"''')

with open('app/src/main/java/com/tvlaoto/player/PlayerViewModel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated PlayerViewModel")
