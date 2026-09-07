package com.tvlaoto.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.tvlaoto.ui.theme.GtaColors

private val NeonDividerBrush = Brush.horizontalGradient(
    colors = listOf(
        Color.Transparent,
        Color(0x80EC4899), // GtaColors.HotPink.copy(alpha = 0.5f)
        Color(0xCC38BDF8), // GtaColors.ElectricCyan.copy(alpha = 0.8f)
        Color(0x80EC4899), // GtaColors.HotPink.copy(alpha = 0.5f)
        Color.Transparent
    )
)

@Composable
fun NeonDivider(
    modifier: Modifier = Modifier,
    height: Dp = 1.dp
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(height)
            .background(NeonDividerBrush)
    )
}

