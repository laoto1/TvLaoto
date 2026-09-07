content = """package com.tvlaoto

import android.os.Bundle
import android.view.WindowManager
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import com.tvlaoto.player.PlayerViewModel
import com.tvlaoto.ui.navigation.AppNavigation
import com.tvlaoto.ui.theme.TvLaotoTheme

class MainActivity : ComponentActivity() {

    private lateinit var playerViewModel: PlayerViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        val app = application as TvLaotoApp
        val langCode = app.repository.settings.value.languageCode
        val locale = java.util.Locale(langCode)
        java.util.Locale.setDefault(locale)
        val config = android.content.res.Configuration(resources.configuration).apply {
            setLocale(locale)
        }
        @Suppress("DEPRECATION")
        resources.updateConfiguration(config, resources.displayMetrics)

        super.onCreate(savedInstanceState)

        // Keep TV screen awake during playback & prevent dimming
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        // Fullscreen immersive mode for TV box
        val windowInsetsController = WindowCompat.getInsetsController(window, window.decorView)
        windowInsetsController.systemBarsBehavior =
            WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        windowInsetsController.hide(WindowInsetsCompat.Type.systemBars())

        val repository = app.repository
        playerViewModel = PlayerViewModel(application, repository)

        setContent {
            TvLaotoTheme {
                AppNavigation(
                    repository = repository,
                    playerViewModel = playerViewModel
                )
            }
        }
    }
}
"""
with open('app/src/main/java/com/tvlaoto/MainActivity.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Rewrote MainActivity")
