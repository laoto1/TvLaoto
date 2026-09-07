package com.tvlaoto.ui.components

import android.view.ViewGroup
import android.widget.FrameLayout
import androidx.annotation.OptIn
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.focusable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.VolumeOff
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.draw.drawWithCache
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.util.UnstableApi
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.AspectRatioFrameLayout
import androidx.media3.ui.PlayerView
import androidx.tv.material3.Icon
import androidx.tv.material3.Text
import com.tvlaoto.data.model.IptvChannel
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes
import com.tvlaoto.ui.theme.neonBorder
import androidx.compose.foundation.Image
import kotlinx.coroutines.delay

@OptIn(UnstableApi::class)
@Composable
fun VideoPlayerPanel(
    player: ExoPlayer,
    channel: IptvChannel?,
    isPlaying: Boolean,
    isBuffering: Boolean,
    isDecryptingLink: Boolean = false,
    isCatchup: Boolean = false,
    onTogglePlayPause: () -> Unit,
    onToggleFullscreen: () -> Unit,
    modifier: Modifier = Modifier
) {
    val containerShape = GtaShapes.LargeCardShape
    var isMuted by remember { mutableStateOf(player.volume == 0f) }

    // Auto-hide controls for catchup mode
    var controlsVisible by remember { mutableStateOf(true) }
    var lastInteractionTime by remember { mutableLongStateOf(System.currentTimeMillis()) }

    // Auto-hide after 4 seconds when playing catchup
    LaunchedEffect(isCatchup, isPlaying, lastInteractionTime) {
        if (isCatchup && isPlaying) {
            delay(4000)
            controlsVisible = false
        }
    }

    // Always show controls when paused
    LaunchedEffect(isPlaying) {
        if (!isPlaying) {
            controlsVisible = true
        }
    }

    // For live mode, controls are always part of the panel
    val showBottomControls = if (isCatchup) controlsVisible else true

    Box(
        modifier = modifier
            .clip(containerShape)
            .background(Color.Black)
    ) {
        // Mock Video Background Image
        Image(
            painter = androidx.compose.ui.res.painterResource(id = com.tvlaoto.R.drawable.bg_vice_city),
            contentDescription = null,
            modifier = Modifier.fillMaxSize(),
            contentScale = androidx.compose.ui.layout.ContentScale.Crop
        )

        // Phủ mờ một chút
        Box(modifier = Modifier.fillMaxSize().background(Color(0x99000000)))

        // SurfaceView Video Layer
        AndroidView(
            factory = { ctx ->
                PlayerView(ctx).apply {
                    this.player = player
                    useController = false
                    resizeMode = AspectRatioFrameLayout.RESIZE_MODE_ZOOM
                    layoutParams = FrameLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT
                    )
                }
            },
            modifier = Modifier.fillMaxSize()
        )

        // Tap Gestures Layer (works for both live and catchup)
        Box(
            modifier = Modifier
                .fillMaxSize()
                .pointerInput(isCatchup) {
                    detectTapGestures(
                        onDoubleTap = { onToggleFullscreen() },
                        onTap = {
                            if (isCatchup) {
                                // Toggle controls visibility
                                controlsVisible = !controlsVisible
                                lastInteractionTime = System.currentTimeMillis()
                            } else {
                                onTogglePlayPause()
                            }
                        }
                    )
                }
        )

        // Top-Right: LIVE Badge
        if (!isCatchup) {
            Box(
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(12.dp)
                    .clip(GtaShapes.TagShape)
                    .background(Color(0xFFEC4899))
                    .padding(horizontal = 8.dp, vertical = 2.dp)
            ) {
                Text(
                    text = "LIVE",
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = FontWeight.Bold,
                    fontSize = 10.sp,
                    color = Color.White
                )
            )
            }
        }

        // Loading Spinner while buffering
        if (isDecryptingLink) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color(0x99000000)),
                contentAlignment = Alignment.Center
            ) {
                NeonLoadingIndicator(text = "Đang bẻ khóa liên kết...")
            }
        } else if (isBuffering) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color(0x66000000)),
                contentAlignment = Alignment.Center
            ) {
                NeonLoadingIndicator(text = channel?.name)
            }
        }

        // Bottom Inside-Video Controls Overlay Bar
        androidx.compose.animation.AnimatedVisibility(
            visible = showBottomControls,
            enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.slideInVertically { it },
            exit = androidx.compose.animation.fadeOut() + androidx.compose.animation.slideOutVertically { it },
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.BottomCenter)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(Color.Transparent, Color(0xE6050711))
                        )
                    )
                    .padding(horizontal = 14.dp, vertical = 8.dp)
            ) {
                Column(modifier = Modifier.fillMaxWidth()) {
                    // Catchup Seek Bar
                    if (isCatchup) {
                        var progress by remember { mutableFloatStateOf(0f) }
                        var currentPos by remember { mutableLongStateOf(0L) }
                        var duration by remember { mutableLongStateOf(0L) }
                        var isSeeking by remember { mutableStateOf(false) }

                        LaunchedEffect(Unit) {
                            while (true) {
                                if (!isSeeking) {
                                    val dur = player.duration
                                    val pos = player.currentPosition
                                    if (dur > 0) {
                                        duration = dur
                                        currentPos = pos
                                        progress = pos.toFloat() / dur.toFloat()
                                    }
                                }
                                delay(250)
                            }
                        }

                        // Seekable progress bar using Slider
                        androidx.compose.material3.Slider(
                            value = progress.coerceIn(0f, 1f),
                            onValueChange = { newValue ->
                                isSeeking = true
                                progress = newValue
                                lastInteractionTime = System.currentTimeMillis()
                                if (duration > 0) {
                                    currentPos = (newValue * duration).toLong()
                                }
                            },
                            onValueChangeFinished = {
                                if (duration > 0) {
                                    player.seekTo((progress * duration).toLong())
                                }
                                isSeeking = false
                                lastInteractionTime = System.currentTimeMillis()
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(24.dp),
                            colors = androidx.compose.material3.SliderDefaults.colors(
                                thumbColor = Color.White,
                                activeTrackColor = GtaColors.HotPink,
                                inactiveTrackColor = Color(0x44FFFFFF)
                            )
                        )

                        // Time labels
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(bottom = 2.dp),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(
                                text = formatTime(currentPos),
                                color = Color.White,
                                style = TextStyle(
                                    fontFamily = FontFamily.Monospace,
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Medium
                                )
                            )
                            Text(
                                text = formatTime(duration),
                                color = Color(0x99FFFFFF),
                                style = TextStyle(
                                    fontFamily = FontFamily.Monospace,
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Medium
                                )
                            )
                        }
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        // Play / Pause
                        PlayerControlIcon(
                            icon = if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                            onClick = {
                                onTogglePlayPause()
                                lastInteractionTime = System.currentTimeMillis()
                            },
                            modifier = Modifier.size(32.dp)
                        )

                        // Action Icons: Volume, Fullscreen
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            PlayerControlIcon(
                                icon = if (isMuted) Icons.Default.VolumeOff else Icons.AutoMirrored.Filled.VolumeUp,
                                onClick = {
                                    if (isMuted) {
                                        player.volume = 1f
                                        isMuted = false
                                    } else {
                                        player.volume = 0f
                                        isMuted = true
                                    }
                                    lastInteractionTime = System.currentTimeMillis()
                                },
                                modifier = Modifier.size(32.dp)
                            )
                            
                            PlayerControlIcon(
                                icon = Icons.Default.Fullscreen, 
                                onClick = {
                                    onToggleFullscreen()
                                    lastInteractionTime = System.currentTimeMillis()
                                },
                                modifier = Modifier.size(32.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun PlayerControlIcon(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    val neonGradient = remember {
        Brush.linearGradient(
            colors = listOf(GtaColors.ElectricCyan, GtaColors.HotPink)
        )
    }
    
    val glassGradient = remember {
        Brush.linearGradient(
            colors = listOf(Color.White, Color(0x99FFFFFF))
        )
    }

    Box(
        modifier = modifier
            .clip(CircleShape)
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() },
        contentAlignment = Alignment.Center
    ) {
        // Glow layer underneath (always visible, stronger when focused)
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier
                .fillMaxSize(),
            tint = if (isFocused) GtaColors.HotPink else Color(0x80FFFFFF)
        )

        // Foreground Icon Layer with Gradient
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier
                .fillMaxSize()
                .graphicsLayer(alpha = 0.99f)
                .drawWithCache {
                    onDrawWithContent {
                        drawContent()
                        drawRect(
                            brush = if (isFocused) neonGradient else glassGradient,
                            blendMode = androidx.compose.ui.graphics.BlendMode.SrcIn
                        )
                    }
                },
            tint = Color.Black
        )
    }
}

private fun formatTime(ms: Long): String {
    val totalSeconds = ms / 1000
    val hours = totalSeconds / 3600
    val minutes = (totalSeconds % 3600) / 60
    val seconds = totalSeconds % 60
    return if (hours > 0) {
        String.format("%d:%02d:%02d", hours, minutes, seconds)
    } else {
        String.format("%02d:%02d", minutes, seconds)
    }
}
