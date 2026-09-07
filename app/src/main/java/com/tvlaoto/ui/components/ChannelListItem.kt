package com.tvlaoto.ui.components

import androidx.compose.animation.animateColorAsState

import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Image
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
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.fillMaxHeight
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
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.Text
import coil.compose.SubcomposeAsyncImage
import coil.compose.AsyncImagePainter
import coil.compose.SubcomposeAsyncImageContent
import androidx.compose.ui.text.style.TextAlign
import com.tvlaoto.data.model.IptvChannel
import com.tvlaoto.data.provider.ChannelLogoProvider
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes
import com.tvlaoto.ui.theme.neonBorder
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.ui.draw.scale
import androidx.compose.animation.core.*

@Composable
fun ChannelListItem(
    channel: IptvChannel,
    isSelected: Boolean,
    onClick: () -> Unit,
    onToggleFavorite: (IptvChannel) -> Unit,
    modifier: Modifier = Modifier
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    val scale by animateFloatAsState(
        targetValue = if (isFocused) 1.02f else 1.0f,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioLowBouncy,
            stiffness = Spring.StiffnessMedium
        ),
        label = "item_scale"
    )

    val glowAlpha by animateFloatAsState(
        targetValue = if (isFocused || isSelected) 0.5f else 0.0f,
        animationSpec = spring(stiffness = Spring.StiffnessMedium),
        label = "item_glow"
    )

    // Cached brushes — avoid per-recomposition allocation
    val backgroundBrush = remember(isFocused, isSelected) {
        if (isFocused || isSelected) {
            Brush.horizontalGradient(listOf(Color(0x334C1D95), Color(0x339C27B0)))
        } else {
            Brush.horizontalGradient(listOf(Color.Transparent, Color.Transparent))
        }
    }

    val borderColor = when {
        isFocused -> Color.White
        isSelected -> Color(0xFF38BDF8)
        else -> Color(0x11FFFFFF)
    }

    val logoUrl = remember(channel) {
        ChannelLogoProvider.getLogoUrl(channel)
    }
    val fallbackDrawable = remember(channel) {
        ChannelLogoProvider.getDrawableFallback(channel)
    }

    val shape = GtaShapes.CardShape

    // Unified modifier chain — no branching to avoid modifier node churn
    val modifierWithBorder = modifier
        .fillMaxWidth()
        .height(58.dp)
        .graphicsLayer {
            scaleX = scale
            scaleY = scale
        }
        .clip(shape)
        .background(backgroundBrush)
        .border(
            width = if (isFocused || isSelected) 1.dp else 0.5.dp,
            color = borderColor,
            shape = shape
        )

    Box(
        modifier = modifierWithBorder
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() }
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Channel Number (01, 02...) & Signal Indicator (ılI)
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
                modifier = Modifier.width(26.dp)
            ) {
                Text(
                    text = String.format("%02d", channel.channelNumber),
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 13.sp,
                        color = if (isSelected || isFocused) Color.White else Color(0xFF8E95AF) // Trả lại màu trắng cho text khi active (như ảnh 1)
                    )
                )
                if (isSelected) {
                    AnimatedSoundWave(modifier = Modifier.padding(top = 2.dp))
                }
            }

            Spacer(modifier = Modifier.width(10.dp))

            // Channel Official Colorful Logo Box (Thu nhỏ kích thước lại cho tinh tế)
            Box(
                modifier = Modifier
                    .size(width = 44.dp, height = 28.dp),
                contentAlignment = Alignment.Center
            ) {
                if (fallbackDrawable != null) {
                    Image(
                        painter = painterResource(id = fallbackDrawable),
                        contentDescription = channel.name,
                        modifier = Modifier.size(width = 42.dp, height = 26.dp),
                        contentScale = ContentScale.Fit
                    )
                } else if (logoUrl.isNotBlank()) {
                                        SubcomposeAsyncImage(
                        model = logoUrl,
                        contentDescription = channel.name,
                        modifier = Modifier.size(width = 42.dp, height = 26.dp),
                        contentScale = ContentScale.Fit
                    ) {
                        val state = painter.state
                        if (state is AsyncImagePainter.State.Error) {
                            Text(
                                text = channel.name.take(3).uppercase(),
                                style = TextStyle(
                                    fontFamily = FontFamily.Monospace,
                                    fontWeight = FontWeight.Black,
                                    fontSize = 11.sp,
                                    color = GtaColors.ElectricCyan
                                ),
                                maxLines = 1,
                                textAlign = TextAlign.Center
                            )
                        } else {
                            SubcomposeAsyncImageContent()
                        }
                    }
                } else {
                    Text(
                        text = channel.name.take(3).uppercase(),
                        style = TextStyle(
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Black,
                            fontSize = 11.sp,
                            color = GtaColors.ElectricCyan
                        )
                    )
                }
            }

            Spacer(modifier = Modifier.width(12.dp))

            // Channel Name & Program Subtitle
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.Center
            ) {
                Text(
                    text = channel.name,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 13.sp,
                        color = Color.White
                    ),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = channel.currentProgram,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Normal,
                        fontSize = 11.sp,
                        color = Color(0xFF8E95AF)
                    ),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }

                        // Heart Icon
            Box(
                modifier = Modifier
                    .size(28.dp)
                    .clickable { onToggleFavorite(channel) },
                contentAlignment = Alignment.Center
            ) {
                val scale by animateFloatAsState(
                    targetValue = if (channel.isFavorite) 1.2f else 1.0f,
                    animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy, stiffness = Spring.StiffnessLow)
                )
                val tint by animateColorAsState(
                    targetValue = if (channel.isFavorite) Color(0xFFF472B6) else Color(0x4DFFFFFF)
                )

                androidx.tv.material3.Icon(
                    imageVector = if (channel.isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                    contentDescription = "Favorite",
                    tint = tint,
                    modifier = Modifier.scale(scale).size(18.dp)
                )
            }
        }
    }
}

@Composable
fun AnimatedSoundWave(modifier: Modifier = Modifier) {
    val infiniteTransition = androidx.compose.animation.core.rememberInfiniteTransition()
    val heights = List(3) { index ->
        infiniteTransition.animateFloat(
            initialValue = 0.3f,
            targetValue = 1.0f,
            animationSpec = androidx.compose.animation.core.infiniteRepeatable(
                animation = androidx.compose.animation.core.tween(durationMillis = 400 + (index * 150), easing = androidx.compose.animation.core.FastOutLinearInEasing),
                repeatMode = androidx.compose.animation.core.RepeatMode.Reverse
            )
        )
    }

    Row(
        modifier = modifier.height(10.dp),
        horizontalArrangement = Arrangement.spacedBy(2.dp),
        verticalAlignment = Alignment.Bottom
    ) {
        heights.forEach { heightRatio ->
            Box(
                modifier = Modifier
                    .width(3.dp)
                    .fillMaxHeight()
                    .graphicsLayer {
                        scaleY = heightRatio.value
                        transformOrigin = androidx.compose.ui.graphics.TransformOrigin(0.5f, 1f)
                    }
                    .background(Color(0xFFF472B6), androidx.compose.foundation.shape.RoundedCornerShape(1.5.dp))
            )
        }
    }
}







