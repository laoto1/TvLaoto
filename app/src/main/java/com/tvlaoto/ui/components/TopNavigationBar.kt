package com.tvlaoto.ui.components

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
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.Icon
import androidx.tv.material3.Text
import com.tvlaoto.R
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes

data class NavCategoryItem(
    val title: String,
    val iconRes: Int
)

@Composable
fun TopNavigationBar(
    selectedCategory: String,
    onSelectCategory: (String) -> Unit,
    onSearchClick: () -> Unit,
    onSettingsClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val navItems = remember {
        listOf(
            NavCategoryItem("Truyền hình", R.drawable.ic_nav_tv),
            NavCategoryItem("Phim bộ", R.drawable.ic_nav_movie),
            NavCategoryItem("Thể thao", R.drawable.ic_nav_sports),
            NavCategoryItem("Thiếu nhi", R.drawable.ic_nav_kids),
            NavCategoryItem("Tin tức", R.drawable.ic_nav_news),
            NavCategoryItem("Radio", R.drawable.ic_nav_radio)
        )
    }

    val tvLogoBrush = remember {
        Brush.horizontalGradient(
            colors = listOf(Color(0xFF38BDF8), Color(0xFF818CF8), Color(0xFFD946EF))
        )
    }

    val avatarBrush = remember {
        Brush.linearGradient(
            colors = listOf(Color(0xFFF1F5F9), Color(0xFF94A3B8))
        )
    }

    Row(
        modifier = modifier
            .fillMaxWidth()
            .height(50.dp)
            .padding(horizontal = 20.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Left: TV VIP Logo
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(end = 14.dp)
        ) {
            Text(
                text = "TV",
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = FontWeight.Black,
                    fontSize = 26.sp,
                    letterSpacing = (-0.5).sp,
                    brush = tvLogoBrush
                )
            )
            Spacer(modifier = Modifier.width(3.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "👑",
                    fontSize = 10.sp
                )
                Text(
                    text = "VIP",
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Black,
                        fontSize = 14.sp,
                        color = Color(0xFFEC4899)
                    )
                )
            }
        }

        // Center: Compact Category Pills with crisp SVG Icons
        Row(
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            navItems.forEach { item ->
                val isSelected = item.title == selectedCategory
                NavPillButton(
                    item = item,
                    isSelected = isSelected,
                    onClick = { onSelectCategory(item.title) }
                )
            }
        }

        // Right: Search, Settings, and VIP Avatar
        Row(
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(start = 10.dp)
        ) {
            // Search Button
            CircularGlassButton(
                icon = {
                    Icon(
                        imageVector = Icons.Default.Search,
                        contentDescription = "Search",
                        tint = Color(0xFFCBD5E1),
                        modifier = Modifier.size(16.dp)
                    )
                },
                onClick = onSearchClick
            )

            // Settings Button
            CircularGlassButton(
                icon = {
                    Icon(
                        imageVector = Icons.Default.Settings,
                        contentDescription = "Settings",
                        tint = Color(0xFFCBD5E1),
                        modifier = Modifier.size(16.dp)
                    )
                },
                onClick = onSettingsClick
            )

            // User Avatar with Gold VIP Tag
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier
                    .clip(CircleShape)
                    .background(Color(0x401E2238))
                    .border(1.dp, Color(0x33FFFFFF), CircleShape)
                    .padding(2.dp)
            ) {
                Box(
                    modifier = Modifier
                        .size(28.dp)
                        .clip(CircleShape)
                        .background(avatarBrush),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "👩",
                        fontSize = 14.sp
                    )
                }
                Spacer(modifier = Modifier.width(4.dp))
                Text(
                    text = "👑 VIP",
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 9.sp,
                        color = GtaColors.LuxuryGold
                    ),
                    modifier = Modifier.padding(end = 5.dp)
                )
            }
        }
    }
}

@Composable
fun NavPillButton(
    item: NavCategoryItem,
    isSelected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    val focusedBgBrush = remember {
        Brush.horizontalGradient(
            colors = listOf(Color(0xE6EC4899), Color(0xE6A855F7))
        )
    }
    val selectedBgBrush = remember {
        Brush.horizontalGradient(
            colors = listOf(Color(0x22E91E63), Color(0x189C27B0))
        )
    }
    val transparentBrush = remember {
        Brush.linearGradient(
            colors = listOf(Color.Transparent, Color.Transparent)
        )
    }

    val focusedBorderBrush = remember {
        Brush.horizontalGradient(
            colors = listOf(Color(0xFF38BDF8), Color(0xFFFFFFFF))
        )
    }
    val selectedBorderBrush = remember {
        Brush.horizontalGradient(
            colors = listOf(Color(0xFF38BDF8), Color(0xFFEC4899))
        )
    }
    val defaultBorderBrush = remember {
        Brush.linearGradient(
            colors = listOf(Color(0x14FFFFFF), Color(0x14FFFFFF))
        )
    }

    val backgroundBrush = when {
        isFocused -> focusedBgBrush
        isSelected -> selectedBgBrush
        else -> transparentBrush
    }

    val borderBrush = when {
        isFocused -> focusedBorderBrush
        isSelected -> selectedBorderBrush
        else -> defaultBorderBrush
    }

    val shape = GtaShapes.SmallCardShape

    Box(
        modifier = modifier
            .height(34.dp)
            .clip(shape)
            .background(backgroundBrush)
            .border(
                width = if (isFocused) 1.dp else 0.5.dp,
                brush = borderBrush,
                shape = shape
            )
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() }
            .padding(horizontal = 14.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            Icon(
                painter = painterResource(id = item.iconRes),
                contentDescription = item.title,
                tint = if (isSelected || isFocused) Color(0xFFF472B6) else Color(0x8894A3B8), 
                modifier = Modifier.size(14.dp)
            )
            Spacer(modifier = Modifier.width(6.dp))
            Text(
                text = item.title,
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = if (isSelected || isFocused) FontWeight.Medium else FontWeight.Normal,
                    fontSize = 12.sp,
                    color = if (isSelected || isFocused) Color(0xFFF472B6) else Color(0xAA94A3B8)
                )
            )
        }
    }
}

@Composable
fun CircularGlassButton(
    icon: @Composable () -> Unit,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    Box(
        modifier = modifier
            .size(32.dp)
            .clip(CircleShape)
            .background(if (isFocused) GtaColors.HotPink else Color(0x4D141A32))
            .border(
                width = if (isFocused) 1.5.dp else 1.dp,
                color = if (isFocused) GtaColors.ElectricCyan else Color(0x2BFFFFFF),
                shape = CircleShape
            )
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() },
        contentAlignment = Alignment.Center
    ) {
        icon()
    }
}

