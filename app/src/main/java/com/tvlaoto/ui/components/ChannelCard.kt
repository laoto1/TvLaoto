package com.tvlaoto.ui.components

import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
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
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.Text
import coil.compose.AsyncImage
import com.tvlaoto.data.model.IptvChannel
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes

@Composable
fun ChannelCard(
    channel: IptvChannel,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    isPlaying: Boolean = false
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    // Spring animation for instantaneous, snappy D-pad response (120ms-150ms feel)
    val scale by animateFloatAsState(
        targetValue = if (isFocused) 1.08f else 1.0f,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioLowBouncy,
            stiffness = Spring.StiffnessMedium
        ),
        label = "card_scale"
    )

    val cardShape = GtaShapes.CardShape
    val backgroundBrush = if (isFocused) GtaColors.CardFocusedGradient else GtaColors.CardBackgroundGradient
    val borderColor = when {
        isFocused -> GtaColors.BorderFocused
        isPlaying -> GtaColors.BorderPlaying
        else -> GtaColors.BorderUnfocused
    }
    val borderWidth = if (isFocused) 2.dp else if (isPlaying) 1.5.dp else 1.dp

    Box(
        modifier = modifier
            .width(200.dp)
            .height(130.dp)
            // GPU-only RenderNode transform: ZERO recomposition or relayout passes
            .graphicsLayer {
                scaleX = scale
                scaleY = scale
                shadowElevation = 0f
            }
            .focusable(interactionSource = interactionSource)
            .clickable(
                interactionSource = interactionSource,
                indication = null
            ) {
                onClick()
            }
            .clip(cardShape)
            .background(backgroundBrush)
            .border(
                width = borderWidth,
                color = borderColor,
                shape = cardShape
            )
            .padding(10.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Top row: Channel number badge + Playing status
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .background(
                            color = if (isFocused) Color(0xFF142B44) else Color(0xFF1E1C2E),
                            shape = GtaShapes.TagShape
                        )
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Text(
                        text = String.format("CH %02d", channel.channelNumber),
                        color = if (isFocused) GtaColors.ElectricCyan else GtaColors.TextSecondary,
                        style = MaterialTheme.typography.labelSmall
                    )
                }

                if (isPlaying) {
                    Box(
                        modifier = Modifier
                            .background(
                                color = GtaColors.HotPink,
                                shape = GtaShapes.TagShape
                            )
                            .padding(horizontal = 6.dp, vertical = 2.dp)
                    ) {
                        Text(
                            text = "LIVE",
                            color = Color.White,
                            style = MaterialTheme.typography.labelSmall.copy(
                                fontWeight = FontWeight.Black,
                                fontSize = 9.sp
                            )
                        )
                    }
                }
            }

            // Center: Channel Logo or Placeholder
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp),
                contentAlignment = Alignment.Center
            ) {
                if (!channel.logoUrl.isNullOrBlank()) {
                    AsyncImage(
                        model = channel.logoUrl,
                        contentDescription = channel.name,
                        modifier = Modifier.size(44.dp),
                        contentScale = ContentScale.Fit
                    )
                } else {
                    Text(
                        text = channel.name.take(3).uppercase(),
                        color = if (isFocused) GtaColors.ElectricCyan else GtaColors.TextMuted,
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Black,
                        fontSize = 18.sp
                    )
                }
            }

            // Bottom: Channel Name
            Text(
                text = channel.name,
                color = if (isFocused) Color.White else GtaColors.TextSecondary,
                style = MaterialTheme.typography.titleMedium.copy(
                    fontSize = 13.sp,
                    fontWeight = if (isFocused) FontWeight.Bold else FontWeight.Medium
                ),
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

