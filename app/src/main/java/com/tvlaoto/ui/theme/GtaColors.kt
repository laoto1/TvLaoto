package com.tvlaoto.ui.theme

import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color

object GtaColors {
    // Vice City Midnight & Sunset Atmosphere Palette
    val BackgroundMidnight = Color(0xFF030510)
    val BackgroundDuskPurple = Color(0xFF1E0C30)
    val BackgroundNavyGlow = Color(0xFF0C142E)
    
    // Glassmorphism Transparency Layers (True Glass)
    val SidebarGlass = Color(0x660B1028)          // 40% translucent dark navy glass
    val SidebarGlassGradientStart = Color(0x80101738)
    val SidebarGlassGradientEnd = Color(0x80080C1E)

    // Luminous Borders (Neon Cyan to Magenta gradient)
    val BorderCyanGlow = Color(0xFF38BDF8)
    val BorderPurpleGlow = Color(0xFFA855F7)
    val BorderPinkGlow = Color(0xFFEC4899)
    val BorderGlassSubtle = Color(0x24FFFFFF)      // 14% white border

    // Active Elements
    val ActivePillBg = Color(0x802E103E)           // Topbar active pill background
    val ActiveCardBgStart = Color(0xD945144F)      // Active channel card rich magenta
    val ActiveCardBgEnd = Color(0xD9201032)        // Active channel card deep purple
    val InactiveCardBg = Color(0x4D0C1126)         // Inactive card dark glass (30%)

    // Action Buttons
    val BtnReplayBgStart = Color(0xFF4C1D95)       // Purple gradient for "Xem lại"
    val BtnReplayBgEnd = Color(0xFF6D28D9)
    val BtnFavoriteBgStart = Color(0xFFD946EF)     // Hot pink gradient for "Yêu thích"
    val BtnFavoriteBgEnd = Color(0xFFEC4899)
    val BtnShareBg = Color(0x801E243E)             // Dark glass for "Chia sẻ"

    // Neon Accents
    val HotPink = Color(0xFFEC4899)
    val NeonMagenta = Color(0xFFD946EF)
    val ElectricCyan = Color(0xFF38BDF8)
    val NeonPurple = Color(0xFFA855F7)
    val LuxuryGold = Color(0xFFFFD700)
    val LiveRed = Color(0xFFEF4444)

    // Typography
    val TextWhite = Color(0xFFFFFFFF)
    val TextLavender = Color(0xFFC4B5FD)
    val TextSecondary = Color(0xFF94A3B8)
    val TextMuted = Color(0xFF64748B)

    // Legacy compat
    val BackgroundDeep = BackgroundMidnight
    val BackgroundPrimary = BackgroundMidnight
    val BackgroundSecondary = BackgroundNavyGlow
    val SurfaceDark = BackgroundNavyGlow
    val SurfaceElevated = SidebarGlass
    val PanelGlass = SidebarGlass
    val PanelGlassBorder = BorderCyanGlow
    val CardGlass = InactiveCardBg
    val CardGlassBorder = BorderGlassSubtle
    val ActiveCardBorder = HotPink
    val BorderPlaying = HotPink
    val BorderUnfocused = BorderGlassSubtle
    val BorderFocused = ElectricCyan
    val BorderActiveCard = HotPink
    val TextPrimary = TextWhite
    val VicePurple = NeonPurple
    val PurplePrimary = NeonPurple
    val PurpleAccent = NeonPurple
    val DeepPurple = BtnReplayBgStart
    val BrightPink = NeonMagenta
    val PanelBackground = SidebarGlass
    val PanelBorder = BorderGlassSubtle

    // Gradients
    val SidebarBorderGradient = Brush.linearGradient(
        colors = listOf(
            Color(0x9938BDF8), // Glowing cyan at top-left
            Color(0x66A855F7), // Purple in middle
            Color(0x44EC4899), // Pink at bottom
            Color(0x15FFFFFF)
        )
    )

    val TopPillActiveBorder = Brush.horizontalGradient(
        colors = listOf(Color(0xFFEC4899), Color(0xFFA855F7))
    )

    val ActiveCardBorderGradient = Brush.horizontalGradient(
        colors = listOf(Color(0xFFFF2D92), Color(0xFFD946EF))
    )

    val ViceGradient = Brush.horizontalGradient(
        colors = listOf(NeonPurple, HotPink)
    )

    val PrimaryGradient = ViceGradient

    val CyanToPinkGradient = Brush.horizontalGradient(
        colors = listOf(ElectricCyan, NeonPurple, HotPink)
    )

    val ActiveCardGradient = Brush.horizontalGradient(
        colors = listOf(ActiveCardBgStart, ActiveCardBgEnd)
    )

    val InactiveCardGradient = Brush.horizontalGradient(
        colors = listOf(Color(0x550E1430), Color(0x55090D22))
    )

    val CardFocusedGradient = ActiveCardGradient
    val CardBackgroundGradient = InactiveCardGradient

    val BackgroundAtmosphere = Brush.verticalGradient(
        colors = listOf(
            BackgroundNavyGlow, // Navy atmosphere
            BackgroundMidnight // Deep midnight
        )
    )
}

