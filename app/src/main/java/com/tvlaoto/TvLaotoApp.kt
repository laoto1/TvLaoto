package com.tvlaoto

import android.app.Application
import android.content.res.Configuration
import coil.ImageLoader
import coil.ImageLoaderFactory
import coil.disk.DiskCache
import coil.memory.MemoryCache
import com.tvlaoto.data.repository.ChannelRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.ConnectionSpec
import okhttp3.TlsVersion
import okhttp3.CipherSuite
import android.webkit.WebSettings
import java.util.Locale
import com.tvlaoto.network.CloudflareInterceptor
import androidx.room.Room
import com.tvlaoto.data.db.AppDatabase
import java.util.concurrent.TimeUnit

class TvLaotoApp : Application(), ImageLoaderFactory {

    private val applicationScope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
    lateinit var repository: ChannelRepository
        private set

    private var deviceUserAgent: String = ""

    override fun onCreate() {
        super.onCreate()
        // Init file logger first
        com.tvlaoto.util.AppLogger.init(this)
        com.tvlaoto.util.AppLogger.i("App", "AFlix TV starting up")

                val db = Room.databaseBuilder(
            applicationContext,
            AppDatabase::class.java, "tvlaoto-db"
        ).build()
        repository = ChannelRepository(this, db.appStateDao())
        
        deviceUserAgent = try {
            WebSettings.getDefaultUserAgent(this)
        } catch (e: Exception) {
            System.getProperty("http.agent") ?: "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        // Apply saved language
        applyLocale(repository.settings.value.languageCode)

        // Preload channels in background
        applicationScope.launch {
            repository.initialize()
            // Fetch pre-resolved m3u8 URLs (from HF Space via gist)
            repository.fetchResolvedPlaylist()
        }
    }

    override fun newImageLoader(): ImageLoader {
                // Tls bypass Cloudflare JA3 fingerprinting
        val spec = ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
            .tlsVersions(TlsVersion.TLS_1_2, TlsVersion.TLS_1_3)
            .cipherSuites(
                CipherSuite.TLS_AES_128_GCM_SHA256,
                CipherSuite.TLS_AES_256_GCM_SHA384,
                CipherSuite.TLS_CHACHA20_POLY1305_SHA256,
                CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
                CipherSuite.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
                CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
                CipherSuite.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
                CipherSuite.TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,
                CipherSuite.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256
            )
            .build()

        val okHttpClient = OkHttpClient.Builder()
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(15, TimeUnit.SECONDS)
            .connectionSpecs(listOf(spec, ConnectionSpec.CLEARTEXT))
                                    .addInterceptor { chain ->
                val request = chain.request().newBuilder()
                    .header("User-Agent", deviceUserAgent)
                    .header("Accept", "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8")
                    .header("Accept-Language", "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7")
                    .header("Sec-Ch-Ua-Mobile", "?1")
                    .header("Sec-Ch-Ua-Platform", "\"Android\"")
                    .header("Sec-Fetch-Dest", "image")
                    .header("Sec-Fetch-Mode", "no-cors")
                    .header("Sec-Fetch-Site", "cross-site")
                    .removeHeader("Referer") // Remove bad referer
                    .build()
                chain.proceed(request)
            }
            .addInterceptor(CloudflareInterceptor(this))
            .build()

        return ImageLoader.Builder(this)
            .okHttpClient(okHttpClient)
            .memoryCache {
                MemoryCache.Builder(this)
                    .maxSizePercent(0.25)
                    .build()
            }
            .diskCache {
                DiskCache.Builder()
                    .directory(cacheDir.resolve("image_cache"))
                    .maxSizeBytes(50L * 1024 * 1024)
                    .build()
            }
            .crossfade(true)
            .build()
    }

    fun applyLocale(langCode: String) {
        val locale = Locale(langCode)
        Locale.setDefault(locale)
        val config = Configuration(resources.configuration).apply {
            setLocale(locale)
        }
        @Suppress("DEPRECATION")
        resources.updateConfiguration(config, resources.displayMetrics)
    }
}







