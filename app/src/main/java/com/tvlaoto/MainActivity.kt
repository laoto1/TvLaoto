package com.tvlaoto

import android.content.Context
import android.os.Bundle
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import android.view.WindowManager
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import com.tvlaoto.player.PlayerViewModel
import com.tvlaoto.ui.navigation.AppNavigation
import com.tvlaoto.ui.theme.TvLaotoTheme
import java.util.Locale
import android.content.res.Configuration

class MainActivity : ComponentActivity() {

    private lateinit var playerViewModel: PlayerViewModel

    override fun attachBaseContext(newBase: Context) {
        val prefs = newBase.getSharedPreferences("tvlaoto_prefs", Context.MODE_PRIVATE)
        val langCode = prefs.getString("language_code", "vi") ?: "vi"
        
        val locale = Locale(langCode)
        Locale.setDefault(locale)
        val config = Configuration(newBase.resources.configuration)
        config.setLocale(locale)
        val context = newBase.createConfigurationContext(config)
        super.attachBaseContext(context)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        // Dismiss Android 12+ system splash screen immediately
        installSplashScreen()
        super.onCreate(savedInstanceState)
        
        // Cập nhật lại config lần nữa cho chắc ăn đối với một số dòng máy cũ
        val prefs = getSharedPreferences("tvlaoto_prefs", Context.MODE_PRIVATE)
        val langCode = prefs.getString("language_code", "vi") ?: "vi"
        val locale = Locale(langCode)
        Locale.setDefault(locale)
        val config = Configuration(resources.configuration)
        config.setLocale(locale)
        @Suppress("DEPRECATION")
        resources.updateConfiguration(config, resources.displayMetrics)

        // Keep TV screen awake during playback & prevent dimming
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        // Fullscreen immersive mode for TV box
        val windowInsetsController = WindowCompat.getInsetsController(window, window.decorView)
        windowInsetsController.systemBarsBehavior =
            WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        windowInsetsController.hide(WindowInsetsCompat.Type.systemBars())

        val app = application as TvLaotoApp
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

    override fun dispatchKeyEvent(event: android.view.KeyEvent): Boolean {
        // Right-click (mouse) = Back
        if (event.action == android.view.KeyEvent.ACTION_DOWN &&
            event.keyCode == android.view.KeyEvent.KEYCODE_BUTTON_B) {
            onBackPressedDispatcher.onBackPressed()
            return true
        }
        return super.dispatchKeyEvent(event)
    }

    override fun onGenericMotionEvent(event: android.view.MotionEvent): Boolean {
        // Right mouse button click = Back
        if (event.action == android.view.MotionEvent.ACTION_DOWN &&
            event.buttonState and android.view.MotionEvent.BUTTON_SECONDARY != 0) {
            onBackPressedDispatcher.onBackPressed()
            return true
        }
        return super.onGenericMotionEvent(event)
    }
}
