package com.tvlaoto.ui.theme

import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithCache
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

fun Modifier.neonBorder(
    brush: Brush,
    cornerRadius: Dp,
    borderWidth: Dp = 1.dp,
    glowRadius: Dp = 8.dp,
    glowAlpha: Float = 0.5f
): Modifier = this.drawWithCache {
    val cornerPx = cornerRadius.toPx()
    val borderPx = borderWidth.toPx()
    val isTransparent = brush is SolidColor && brush.value == Color.Transparent

    onDrawBehind {
        if (!isTransparent) {
            // Single-pass border only — no glow loops for TV box performance
            drawRoundRect(
                brush = brush,
                size = size,
                cornerRadius = CornerRadius(cornerPx),
                style = Stroke(width = borderPx)
            )
        }
    }
}

