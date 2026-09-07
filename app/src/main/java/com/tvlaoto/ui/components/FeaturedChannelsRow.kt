package com.tvlaoto.ui.components

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
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
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
import coil.compose.AsyncImage
import com.tvlaoto.data.model.IptvChannel
import com.tvlaoto.data.provider.ChannelLogoProvider
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes

@Composable
fun FeaturedChannelsRow(
    channels: List<IptvChannel>,
    currentChannelId: String?,
    onChannelClick: (IptvChannel) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(top = 10.dp)
    ) {
        Text(
            text = "KÊNH NỔI BẬT",
            style = TextStyle(
                fontFamily = FontFamily.SansSerif,
                fontWeight = FontWeight.Bold,
                fontSize = 13.sp,
                letterSpacing = 0.5.sp,
                color = Color.White
            ),
            modifier = Modifier.padding(bottom = 8.dp)
        )

        LazyRow(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            contentPadding = PaddingValues(horizontal = 2.dp)
        ) {
            items(
                items = channels.take(6),
                key = { "featured_${it.id}" }
            ) { channel ->
                val isSelected = channel.id == currentChannelId
                FeaturedChannelCard(
                    channel = channel,
                    isSelected = isSelected,
                    onClick = { onChannelClick(channel) }
                )
            }
        }
    }
}

@Composable
fun FeaturedChannelCard(
    channel: IptvChannel,
    isSelected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    val scale by animateFloatAsState(
        targetValue = if (isFocused) 1.04f else 1.0f,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioLowBouncy,
            stiffness = Spring.StiffnessMedium
        ),
        label = "featured_scale"
    )

    val focusedBgBrush = remember {
        Brush.horizontalGradient(
            colors = listOf(Color(0xFF3B1442), Color(0xFF1B1432))
        )
    }
    val selectedBgBrush = remember {
        Brush.horizontalGradient(
            colors = listOf(Color(0xFF2E1038), Color(0xFF151028))
        )
    }
    val defaultBgBrush = remember {
        Brush.horizontalGradient(
            colors = listOf(Color(0xFF11152E), Color(0xFF0D1024))
        )
    }

    val backgroundBrush = when {
        isFocused -> focusedBgBrush
        isSelected -> selectedBgBrush
        else -> defaultBgBrush
    }

    val borderColor = when {
        isFocused -> GtaColors.ElectricCyan
        isSelected -> GtaColors.HotPink
        else -> Color(0x24FFFFFF)
    }
    val borderWidth = if (isFocused || isSelected) 1.5.dp else 1.dp

    val fallbackDrawable = remember(channel) {
        ChannelLogoProvider.getDrawableFallback(channel)
    }
    val logoUrl = remember(channel) {
        ChannelLogoProvider.getLogoUrl(channel)
    }

    val shape = GtaShapes.SmallCardShape

    Box(
        modifier = modifier
            .width(170.dp)
            .height(64.dp)
            .graphicsLayer {
                scaleX = scale
                scaleY = scale
            }
            .clip(shape)
            .background(backgroundBrush)
            .border(
                width = borderWidth,
                color = borderColor,
                shape = shape
            )
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() }
            .padding(horizontal = 10.dp, vertical = 6.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Official Colorful Logo
            Box(
                modifier = Modifier
                    .size(width = 46.dp, height = 30.dp),
                contentAlignment = Alignment.Center
            ) {
                if (fallbackDrawable != null) {
                    Image(
                        painter = painterResource(id = fallbackDrawable),
                        contentDescription = channel.name,
                        modifier = Modifier.size(width = 44.dp, height = 28.dp),
                        contentScale = ContentScale.Fit
                    )
                } else if (logoUrl.isNotBlank()) {
                    AsyncImage(
                        model = logoUrl,
                        contentDescription = channel.name,
                        modifier = Modifier.size(width = 44.dp, height = 28.dp),
                        contentScale = ContentScale.Fit
                    )
                } else {
                    Text(
                        text = channel.name.take(3).uppercase(),
                        style = TextStyle(
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Black,
                            fontSize = 10.sp,
                            color = GtaColors.ElectricCyan
                        )
                    )
                }
            }

            Spacer(modifier = Modifier.width(8.dp))

            // Channel Name, Program Subtext & LIVE Pill
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.Center
            ) {
                Text(
                    text = channel.name,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 11.sp,
                        color = Color.White
                    ),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = channel.currentProgram,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Normal,
                        fontSize = 9.sp,
                        color = GtaColors.TextSecondary
                    ),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Spacer(modifier = Modifier.height(2.dp))
                Box(
                    modifier = Modifier
                        .clip(GtaShapes.TagShape)
                        .background(GtaColors.HotPink)
                        .padding(horizontal = 4.dp, vertical = 1.dp)
                ) {
                    Text(
                        text = "● LIVE",
                        style = TextStyle(
                            fontFamily = FontFamily.SansSerif,
                            fontWeight = FontWeight.Bold,
                            fontSize = 7.sp,
                            color = Color.White
                        )
                    )
                }
            }
        }
    }
}

