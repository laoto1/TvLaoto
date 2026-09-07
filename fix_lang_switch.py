import re

# Update MainActivity.kt
with open('app/src/main/java/com/tvlaoto/MainActivity.kt', 'r', encoding='utf-8') as f:
    main_content = f.read()

if "app.applyLocale(" not in main_content:
    main_content = main_content.replace(
        "super.onCreate(savedInstanceState)",
        "val app = application as TvLaotoApp\n        app.applyLocale(app.repository.settings.value.languageCode)\n        super.onCreate(savedInstanceState)"
    )
    # Remove the later declaration of val app if it exists
    main_content = main_content.replace(
        "\n        val app = application as TvLaotoApp",
        ""
    )

with open('app/src/main/java/com/tvlaoto/MainActivity.kt', 'w', encoding='utf-8') as f:
    f.write(main_content)


# Update HomeScreen.kt
with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    home_content = f.read()

home_content = home_content.replace(
    "repository.updateLanguage(newLang)",
    "repository.updateLanguage(newLang)\n                    (context.applicationContext as TvLaotoApp).applyLocale(newLang)\n                    if (context is androidx.activity.ComponentActivity) {\n                        context.recreate()\n                    }"
)
if "import androidx.compose.ui.platform.LocalContext" not in home_content:
    home_content = home_content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.platform.LocalContext\nimport com.tvlaoto.TvLaotoApp")

home_content = home_content.replace("val coroutineScope = rememberCoroutineScope()", "val coroutineScope = rememberCoroutineScope()\n    val context = LocalContext.current")

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'w', encoding='utf-8') as f:
    f.write(home_content)

print("Updated MainActivity and HomeScreen for Language switch")
