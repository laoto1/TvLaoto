package com.tvlaoto.ui.theme

import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import androidx.tv.material3.MaterialTheme
import androidx.tv.material3.Typography
import androidx.tv.material3.darkColorScheme

private val GtaColorScheme = darkColorScheme(
    primary = GtaColors.HotPink,
    onPrimary = Color.White,
    primaryContainer = GtaColors.DeepPurple,
    onPrimaryContainer = Color.White,
    secondary = GtaColors.ElectricCyan,
    onSecondary = Color.Black,
    surface = GtaColors.SurfaceDark,
    onSurface = GtaColors.TextPrimary,
    surfaceVariant = Color(0xFF101738), // Opaque dark navy surface
    onSurfaceVariant = GtaColors.TextSecondary,
    background = GtaColors.BackgroundDeep,
    onBackground = GtaColors.TextPrimary,
    error = Color(0xFFFF5252),
    onError = Color.White,
    border = Color(0xFF1E2640) // Opaque subtle border
)

private val GtaTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Black,
        fontSize = 44.sp,
        letterSpacing = 1.sp,
        color = GtaColors.TextPrimary
    ),
    displayMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.ExtraBold,
        fontSize = 32.sp,
        letterSpacing = 0.5.sp,
        color = GtaColors.TextPrimary
    ),
    titleLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Bold,
        fontSize = 22.sp,
        letterSpacing = 0.5.sp,
        color = GtaColors.TextPrimary
    ),
    titleMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.SemiBold,
        fontSize = 17.sp,
        letterSpacing = 0.2.sp,
        color = GtaColors.TextPrimary
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Normal,
        fontSize = 15.sp,
        color = GtaColors.TextSecondary
    ),
    bodyMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Normal,
        fontSize = 13.sp,
        color = GtaColors.TextSecondary
    ),
    labelSmall = TextStyle(
        fontFamily = FontFamily.Monospace,
        fontWeight = FontWeight.Bold,
        fontSize = 11.sp,
        letterSpacing = 0.5.sp,
        color = GtaColors.ElectricCyan
    )
)

@Composable
fun TvLaotoTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = GtaColorScheme,
        typography = GtaTypography,
        content = content
    )
}

