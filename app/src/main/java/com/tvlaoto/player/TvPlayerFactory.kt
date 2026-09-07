package com.tvlaoto.player

import android.content.Context
import androidx.annotation.OptIn
import androidx.media3.common.C
import androidx.media3.common.MediaItem
import androidx.media3.common.MimeTypes
import androidx.media3.common.util.UnstableApi
import androidx.media3.datasource.DefaultHttpDataSource
import androidx.media3.datasource.okhttp.OkHttpDataSource
import androidx.media3.exoplayer.DefaultLoadControl
import androidx.media3.exoplayer.DefaultRenderersFactory
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.hls.HlsMediaSource
import androidx.media3.exoplayer.source.MediaSource
import androidx.media3.exoplayer.source.ProgressiveMediaSource
import com.tvlaoto.data.model.IptvChannel
import okhttp3.OkHttpClient
import java.util.concurrent.TimeUnit

@OptIn(UnstableApi::class)
object TvPlayerFactory {

    private const val DEFAULT_USER_AGENT =
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    private val sharedOkHttpClient = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .followRedirects(true)
        .followSslRedirects(true)
        .build()

    fun createPlayer(context: Context): ExoPlayer {
        // Tuned for instant TV channel zapping (1s start buffer) & minimal memory footprint on weak TV boxes
        val loadControl = DefaultLoadControl.Builder()
            .setBufferDurationsMs(
                /* minBufferMs = */ 10_000,
                /* maxBufferMs = */ 25_000,
                /* bufferForPlaybackMs = */ 1_000,
                /* bufferForPlaybackAfterRebufferMs = */ 2_000
            )
            .setPrioritizeTimeOverSizeThresholds(true)
            .build()

        // Prioritize hardware decoders on TV chips (Amlogic/Rockchip/Allwinner)
        val renderersFactory = DefaultRenderersFactory(context.applicationContext).apply {
            setExtensionRendererMode(DefaultRenderersFactory.EXTENSION_RENDERER_MODE_OFF)
            setEnableDecoderFallback(true)
        }

        return ExoPlayer.Builder(context.applicationContext)
            .setRenderersFactory(renderersFactory)
            .setLoadControl(loadControl)
            .setSeekBackIncrementMs(10_000)
            .setSeekForwardIncrementMs(10_000)
            .build().apply {
                playWhenReady = true
                videoScalingMode = C.VIDEO_SCALING_MODE_SCALE_TO_FIT_WITH_CROPPING
            }
    }

    fun createMediaSource(channel: IptvChannel): MediaSource {
        val userAgent = channel.userAgent ?: DEFAULT_USER_AGENT
        
        // Auto-detect VTVGo referer requirement if not explicitly provided
        val referer = channel.httpReferrer ?: when {
            channel.streamUrl.contains("vtvdigital.vn", ignoreCase = true) -> "https://vtvgo.vn/"
            channel.streamUrl.contains("tv360.vn", ignoreCase = true) -> "https://tv360.vn/"
            else -> null
        }

        val customClient = sharedOkHttpClient.newBuilder()
            .addInterceptor { chain ->
                val requestBuilder = chain.request().newBuilder()
                    .header("User-Agent", userAgent)

                if (referer != null) {
                    requestBuilder.header("Referer", referer)
                    requestBuilder.header("Origin", referer)
                }

                chain.proceed(requestBuilder.build())
            }
            .build()

        val dataSourceFactory = OkHttpDataSource.Factory(customClient)

        val uri = channel.streamUrl
        val isHls = uri.contains(".m3u8", ignoreCase = true) ||
                    uri.contains("/hls", ignoreCase = true) ||
                    uri.contains("/manifest", ignoreCase = true)

        return if (isHls) {
            val mediaItem = MediaItem.Builder()
                .setUri(uri)
                .setMimeType(MimeTypes.APPLICATION_M3U8)
                .build()

            HlsMediaSource.Factory(dataSourceFactory)
                .setAllowChunklessPreparation(true)
                .createMediaSource(mediaItem)
        } else {
            val mediaItem = MediaItem.Builder()
                .setUri(uri)
                .build()

            ProgressiveMediaSource.Factory(dataSourceFactory)
                .createMediaSource(mediaItem)
        }
    }
}

