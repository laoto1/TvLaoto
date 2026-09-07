code = """package com.tvlaoto.ui.theme

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
    val glowPx = glowRadius.toPx()
    val cornerPx = cornerRadius.toPx()
    val borderPx = borderWidth.toPx()
    
    // Opt: if no glow or transparent brush (SolidColor(Transparent)), just draw border.
    val isTransparent = brush is SolidColor && brush.value == Color.Transparent
    
    onDrawBehind {
        if (!isTransparent) {
            // Draw glow layers only if glowRadius > 0
            if (glowPx > 0) {
                // Reduced steps for better performance on weak TV boxes
                val steps = 3
                for (i in steps downTo 1) {
                    val strokeWidth = glowPx * (i.toFloat() / steps)
                    val alpha = glowAlpha * (1f / steps) * (1f - (i.toFloat() / steps))
                    
                    drawRoundRect(
                        brush = brush,
                        size = size,
                        cornerRadius = CornerRadius(cornerPx),
                        style = Stroke(width = strokeWidth),
                        alpha = alpha
                    )
                }
            }
            
            // Draw the core solid bright line
            drawRoundRect(
                brush = brush,
                size = size,
                cornerRadius = CornerRadius(cornerPx),
                style = Stroke(width = borderPx)
            )
        }
    }
}
"""
with open('app/src/main/java/com/tvlaoto/ui/theme/GtaEffects.kt', 'w', encoding='utf-8') as f:
    f.write(code)
print("Optimized GtaEffects.kt")
