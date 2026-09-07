with open('app/src/main/java/com/tvlaoto/MainActivity.kt', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """        val app = application as TvLaotoApp
        val langCode = app.repository.settings.value.languageCode
        val locale = java.util.Locale(langCode)
        java.util.Locale.setDefault(locale)
        val config = android.content.res.Configuration(resources.configuration).apply {
            setLocale(locale)
        }
        @Suppress("DEPRECATION")
        resources.updateConfiguration(config, resources.displayMetrics)
        super.onCreate(savedInstanceState)"""

content = content.replace(
    "val app = application as TvLaotoApp\n        app.applyLocale(app.repository.settings.value.languageCode)\n        super.onCreate(savedInstanceState)",
    replacement
)

with open('app/src/main/java/com/tvlaoto/MainActivity.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated MainActivity to apply locale to its own resources")
