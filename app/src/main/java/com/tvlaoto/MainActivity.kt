package com.tvlaoto

import android.content.Context
import android.os.Bundle
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import android.view.WindowManager
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import com.tvlaoto.network.WebViewChecker
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

        // Check WebView version
        val webViewInfo = WebViewChecker.getWebViewInfo(this)
        val webViewOk = WebViewChecker.isWebViewSufficient(this)
        val skipKey = "skip_webview_check"
        val userSkipped = prefs.getBoolean(skipKey, false)

        android.util.Log.d("WebViewChecker", 
            "WebView: ${webViewInfo?.packageName} v${webViewInfo?.versionName} (major=${webViewInfo?.majorVersion}), ok=$webViewOk")

        setContent {
            TvLaotoTheme {
                var showWebViewDialog by remember { mutableStateOf(!webViewOk && !userSkipped) }

                if (showWebViewDialog) {
                    WebViewUpdateDialog(
                        currentVersion = webViewInfo?.versionName ?: "Không tìm thấy",
                        majorVersion = webViewInfo?.majorVersion ?: 0,
                        onUpdatePlayStore = {
                            val opened = WebViewChecker.openPlayStoreForWebView(this@MainActivity)
                            if (!opened) {
                                Toast.makeText(this@MainActivity, "Không tìm thấy Google Play Store", Toast.LENGTH_LONG).show()
                            }
                            showWebViewDialog = false
                        },
                        onDownloadDirect = {
                            WebViewChecker.downloadAndInstallWebView(this@MainActivity) { msg ->
                                runOnUiThread {
                                    Toast.makeText(this@MainActivity, msg, Toast.LENGTH_SHORT).show()
                                }
                            }
                            showWebViewDialog = false
                        },
                        onSkip = {
                            showWebViewDialog = false
                        },
                        onSkipForever = {
                            prefs.edit().putBoolean(skipKey, true).apply()
                            showWebViewDialog = false
                        }
                    )
                }

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

@Composable
fun WebViewUpdateDialog(
    currentVersion: String,
    majorVersion: Int,
    onUpdatePlayStore: () -> Unit,
    onDownloadDirect: () -> Unit,
    onSkip: () -> Unit,
    onSkipForever: () -> Unit
) {
    Dialog(
        onDismissRequest = onSkip,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(
            modifier = Modifier
                .width(480.dp)
                .background(Color(0xFF1A1A2E), RoundedCornerShape(16.dp))
                .padding(24.dp)
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text(
                    text = "⚠️ WebView Cần Cập Nhật",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFFE94560)
                )

                Text(
                    text = "WebView hiện tại: v$currentVersion\n" +
                           "Phiên bản quá cũ (Chrome $majorVersion), một số kênh có thể không hoạt động.\n" +
                           "Cần Chrome 80 trở lên để giải mã kênh VTVGo.",
                    fontSize = 14.sp,
                    color = Color.White.copy(alpha = 0.8f),
                    textAlign = TextAlign.Center,
                    lineHeight = 20.sp
                )

                // Update via Play Store
                Button(
                    onClick = onUpdatePlayStore,
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0F3460)),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("Cập nhật qua Google Play", fontSize = 14.sp)
                }

                // Download directly
                Button(
                    onClick = onDownloadDirect,
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF16213E)),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("Tải và cài đặt trực tiếp (TV Box)", fontSize = 14.sp)
                }

                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    // Skip once
                    Button(
                        onClick = onSkip,
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent),
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        Text("Bỏ qua", fontSize = 12.sp, color = Color.White.copy(alpha = 0.5f))
                    }

                    // Skip forever
                    Button(
                        onClick = onSkipForever,
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent),
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        Text("Không nhắc nữa", fontSize = 12.sp, color = Color.White.copy(alpha = 0.5f))
                    }
                }
            }
        }
    }
}
