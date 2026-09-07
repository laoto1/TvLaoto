import codecs

content = """package com.tvlaoto.ui.components

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
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.VolumeOff
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
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

@OptIn(UnstableApi::class)
@Composable
fun VideoPlayerPanel(
    player: ExoPlayer,
    channel: IptvChannel?,
    isPlaying: Boolean,
    isBuffering: Boolean,
    onTogglePlayPause: () -> Unit,
    onToggleFullscreen: () -> Unit,
    modifier: Modifier = Modifier
) {
    val containerShape = GtaShapes.LargeCardShape
    var isMuted by remember { mutableStateOf(player.volume == 0f) }

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

        // Tap Gestures Layer
        Box(
            modifier = Modifier
                .fillMaxSize()
                .pointerInput(Unit) {
                    detectTapGestures(
                        onDoubleTap = { onToggleFullscreen() },
                        onTap = { onTogglePlayPause() }
                    )
                }
        )

        // Top-Right: LIVE Badge
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

        // Loading Spinner while buffering
        if (isBuffering) {
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
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.BottomCenter)
                .background(
                    Brush.verticalGradient(
                        colors = listOf(Color.Transparent, Color(0xE6050711))
                    )
                )
                .padding(horizontal = 14.dp, vertical = 8.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                // Play / Pause
                PlayerControlIcon(
                    icon = if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                    onClick = onTogglePlayPause,
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
                        },
                        modifier = Modifier.size(32.dp)
                    )
                    
                    PlayerControlIcon(
                        icon = Icons.Default.Fullscreen, 
                        onClick = onToggleFullscreen,
                        modifier = Modifier.size(32.dp)
                    )
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

    Box(
        modifier = modifier
            .clip(CircleShape)
            .background(if (isFocused) Brush.horizontalGradient(listOf(GtaColors.ElectricCyan, GtaColors.HotPink)) else SolidColor(Color(0x4D000000)))
            .neonBorder(
                brush = SolidColor(if (isFocused) GtaColors.ElectricCyan else Color(0x99F472B6)),
                shape = CircleShape,
                borderWidth = 1.5.dp,
                blurRadius = if (isFocused) 8.dp else 4.dp
            )
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() },
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = Color.White,
            modifier = Modifier.size(18.dp)
        )
    }
}
"""

with codecs.open('app/src/main/java/com/tvlaoto/ui/components/VideoPlayerPanel.kt', 'w', 'utf-8') as f:
    f.write(content)

print("VideoPlayerPanel updated successfully")
