package com.tvlaoto.ui.components

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.Spring
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.focusable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Replay
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.Icon
import androidx.tv.material3.Text
import com.tvlaoto.R
import com.tvlaoto.data.model.IptvChannel
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes
import com.tvlaoto.ui.theme.neonBorder
import com.tvlaoto.data.model.EpgProgram

@Composable
fun ProgramInfoPanel(
    channel: IptvChannel?,
    currentCatchupProgram: EpgProgram?,
    liveProgram: EpgProgram?,
    onReplayClick: () -> Unit,
    onFavoriteClick: () -> Unit,
    modifier: Modifier = Modifier
) {

    if (channel == null) return

    val displayTitle = currentCatchupProgram?.title ?: liveProgram?.title ?: channel.currentProgram
    val displayTime = currentCatchupProgram?.time ?: liveProgram?.time ?: channel.programTime
    val isLiveStream = currentCatchupProgram == null

    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(top = 14.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Left Column: Program Title, Time, Description
        Column(modifier = Modifier.weight(1f).padding(end = 16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = displayTitle,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 20.sp,
                        color = Color.White
                    )
                )
                Spacer(modifier = Modifier.width(10.dp))
                if (isLiveStream) {
                Box(
                                    modifier = Modifier
                                        .clip(GtaShapes.TagShape)
                                        .background(Color(0xFFEC4899))
                                        .padding(horizontal = 7.dp, vertical = 2.dp)
                                ) {
                                    Text(
                                        text = "LIVE",
                                        style = TextStyle(
                                            fontFamily = FontFamily.SansSerif,
                                            fontWeight = FontWeight.Bold,
                                            fontSize = 9.sp,
                                            color = Color.White
                                        )
                                    )
                                }
                }
            }

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = displayTime,
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = FontWeight.Normal,
                    fontSize = 12.sp,
                    color = Color(0xFF94A3B8)
                )
            )

            if (channel.programDescription.isNotEmpty()) {
                Spacer(modifier = Modifier.height(5.dp))

                Text(
                    text = channel.programDescription,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Normal,
                        fontSize = 11.5.sp,
                        color = Color(0xFF64748B)
                    ),
                    maxLines = 2
                )
            }
        }

        // Right Row: 2 Action Buttons
        Row(
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 1. Replay
            if (channel.resolvedUrl != null || channel.streamUrl.contains("tv360.vn") || channel.streamUrl.contains("vtvgo.vn")) {
                EpgActionButton(
                    title = stringResource(R.string.replay),
                    icon = Icons.Default.Replay,
                    backgroundBrush = Brush.horizontalGradient(
                        colors = listOf(Color(0xFF6366F1), Color(0xFF8B5CF6))
                    ),
                    borderColor = Color.Transparent,
                    onClick = onReplayClick
                )
            }

            // 2. Favorite
            AnimatedContent(
                targetState = channel.isFavorite,
                transitionSpec = {
                    (fadeIn(animationSpec = tween(300))
                    ).togetherWith(fadeOut(animationSpec = tween(300)))
                },
                label = "FavoriteAnimation"
            ) { isFav ->
                EpgActionButton(
                    title = if (isFav) stringResource(R.string.favorited) else stringResource(R.string.favorite),
                    icon = if (isFav) Icons.Default.Favorite else Icons.Outlined.FavoriteBorder,
                    backgroundBrush = Brush.horizontalGradient(
                        colors = if (isFav) listOf(Color(0xFFF472B6), Color(0xFFEC4899)) else listOf(Color(0x33F472B6), Color(0x33EC4899))
                    ),
                    borderColor = if (isFav) Color.Transparent else Color(0x99F472B6),
                    onClick = onFavoriteClick
                )
            }
        }
    }
}

@Composable
fun EpgActionButton(
    title: String,
    icon: ImageVector,
    backgroundBrush: Brush,
    borderColor: Color,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    val shape = RoundedCornerShape(12.dp)

    Box(
        modifier = modifier
            .height(36.dp)
            .clip(shape)
            .background(if (isFocused) Brush.horizontalGradient(listOf(GtaColors.ElectricCyan, GtaColors.HotPink)) else backgroundBrush)
            .neonBorder(
                brush = SolidColor(if (isFocused) GtaColors.ElectricCyan else borderColor),
                cornerRadius = 12.dp,
                borderWidth = if (isFocused) 1.5.dp else 1.dp,
                glowRadius = 14.dp,
                glowAlpha = 0.6f
            )
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() }
            .padding(horizontal = 14.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(
                imageVector = icon,
                contentDescription = title,
                tint = Color(0xCCFFFFFF),
                modifier = Modifier.size(13.dp)
            )
            Spacer(modifier = Modifier.width(6.dp))
            Text(
                text = title,
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = FontWeight.Medium,
                    fontSize = 12.sp,
                    color = Color.White
                )
            )
        }
    }
}
