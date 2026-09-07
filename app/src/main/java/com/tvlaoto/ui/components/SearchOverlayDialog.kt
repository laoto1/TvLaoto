package com.tvlaoto.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.scaleOut
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
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.Shadow
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import androidx.tv.material3.Icon
import androidx.tv.material3.Text
import com.tvlaoto.R
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes
import com.tvlaoto.ui.theme.neonBorder
import kotlinx.coroutines.delay

@Composable
fun SearchOverlayDialog(
    searchQuery: String,
    onQueryChange: (String) -> Unit,
    onDismiss: () -> Unit
) {
    var isVisible by remember { mutableStateOf(false) }
    var hasOpened by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        isVisible = true
        hasOpened = true
    }

    val triggerDismiss = {
        isVisible = false
    }
    
    LaunchedEffect(isVisible) {
        if (hasOpened && !isVisible) {
            delay(300)
            onDismiss()
        }
    }

    Dialog(
        onDismissRequest = triggerDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0x80000010)) // Deep dark blue tinted dim
                .clickable(indication = null, interactionSource = remember { MutableInteractionSource() }) { triggerDismiss() },
            contentAlignment = Alignment.Center
        ) {
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn(tween(400)) + scaleIn(tween(400), initialScale = 0.85f),
                exit = fadeOut(tween(300)) + scaleOut(tween(300), targetScale = 0.9f)
            ) {
                // Main Glassmorphism Popup Box
                Box(
                    modifier = Modifier
                        .width(600.dp)
                        .clip(RoundedCornerShape(24.dp))
                        .background(
                            Brush.linearGradient(
                                colors = listOf(
                                    Color(0x660F0C29),
                                    Color(0x66302B63),
                                    Color(0x6624243E)
                                )
                            )
                        )
                        .neonBorder(
                            brush = Brush.linearGradient(listOf(GtaColors.ElectricCyan, GtaColors.HotPink)),
                            cornerRadius = 24.dp,
                            borderWidth = 1.5.dp,
                            glowRadius = 30.dp,
                            glowAlpha = 0.4f
                        )
                        .clickable(indication = null, interactionSource = remember { MutableInteractionSource() }) {} 
                        .padding(32.dp)
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        // Header
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            // Glowing Text
                            Text(
                                text = stringResource(R.string.search_title),
                                style = TextStyle(
                                    fontFamily = FontFamily.SansSerif,
                                    fontWeight = FontWeight.Black,
                                    fontSize = 28.sp,
                                    color = Color.White,
                                    shadow = Shadow(
                                        color = GtaColors.ElectricCyan,
                                        blurRadius = 15f
                                    )
                                )
                            )
                            
                            // Glassy Close Button
                            val closeInteraction = remember { MutableInteractionSource() }
                            val isCloseFocused by closeInteraction.collectIsFocusedAsState()
                            
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(CircleShape)
                                    .background(if (isCloseFocused) GtaColors.HotPink else Color(0x33FFFFFF))
                                    .neonBorder(
                                        brush = SolidColor(if (isCloseFocused) Color.White else Color.Transparent),
                                        cornerRadius = 20.dp,
                                        borderWidth = 1.dp,
                                        glowRadius = if (isCloseFocused) 15.dp else 0.dp,
                                        glowAlpha = 0.6f
                                    )
                                    .focusable(interactionSource = closeInteraction)
                                    .clickable(indication = null, interactionSource = closeInteraction) { triggerDismiss() },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Close,
                                    contentDescription = "Close",
                                    tint = Color.White,
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(32.dp))

                        // Search Input Field (Glass Pill)
                        val searchInteractionSource = remember { MutableInteractionSource() }
                        val isSearchFocused by searchInteractionSource.collectIsFocusedAsState()

                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(60.dp)
                                .clip(RoundedCornerShape(16.dp))
                                .background(Color(0x33000000))
                                .neonBorder(
                                    brush = SolidColor(if (isSearchFocused) GtaColors.ElectricCyan else Color(0x4DFFFFFF)),
                                    cornerRadius = 16.dp,
                                    borderWidth = if (isSearchFocused) 2.dp else 1.dp,
                                    glowRadius = if (isSearchFocused) 20.dp else 0.dp,
                                    glowAlpha = 0.6f
                                )
                                .padding(horizontal = 20.dp),
                            contentAlignment = Alignment.CenterStart
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = Icons.Default.Search,
                                    contentDescription = null,
                                    tint = if (isSearchFocused) GtaColors.ElectricCyan else Color(0x99FFFFFF),
                                    modifier = Modifier.size(26.dp)
                                )
                                Spacer(modifier = Modifier.width(16.dp))
                                Box(modifier = Modifier.weight(1f)) {
                                    if (searchQuery.isEmpty()) {
                                        Text(
                                            text = stringResource(R.string.search_placeholder),
                                            color = Color(0x99FFFFFF),
                                            fontSize = 16.sp,
                                            maxLines = 1
                                        )
                                    }
                                    BasicTextField(
                                        value = searchQuery,
                                        onValueChange = onQueryChange,
                                        textStyle = TextStyle(
                                            color = Color.White,
                                            fontSize = 18.sp,
                                            fontFamily = FontFamily.SansSerif,
                                            fontWeight = FontWeight.SemiBold
                                        ),
                                        cursorBrush = SolidColor(GtaColors.ElectricCyan),
                                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                                        keyboardActions = KeyboardActions(onSearch = { triggerDismiss() }),
                                        interactionSource = searchInteractionSource,
                                        modifier = Modifier.fillMaxWidth().focusable(interactionSource = searchInteractionSource)
                                    )
                                }
                            }
                        }

                        Spacer(modifier = Modifier.height(36.dp))

                        // XEM KẾT QUẢ Button (Vice City Gradient)
                        val btnInteraction = remember { MutableInteractionSource() }
                        val isBtnFocused by btnInteraction.collectIsFocusedAsState()
                        
                        val btnGradient = Brush.linearGradient(
                            colors = listOf(Color(0xFFFF3366), Color(0xFFFF9933))
                        )
                        val btnGradientFocused = Brush.linearGradient(
                            colors = listOf(Color(0xFF00FFFF), Color(0xFFFF00FF))
                        )

                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(56.dp)
                                .clip(RoundedCornerShape(14.dp))
                                .background(if (isBtnFocused) btnGradientFocused else btnGradient)
                                .neonBorder(
                                    brush = SolidColor(Color.White),
                                    cornerRadius = 14.dp,
                                    borderWidth = if (isBtnFocused) 2.dp else 0.dp,
                                    glowRadius = 24.dp,
                                    glowAlpha = if (isBtnFocused) 0.8f else 0.3f
                                )
                                .focusable(interactionSource = btnInteraction)
                                .clickable(indication = null, interactionSource = btnInteraction) { triggerDismiss() },
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = stringResource(R.string.search_submit),
                                style = TextStyle(
                                    fontFamily = FontFamily.SansSerif,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 17.sp,
                                    color = Color.White,
                                    letterSpacing = 1.sp,
                                    shadow = Shadow(color = Color(0x80000000), blurRadius = 4f)
                                )
                            )
                        }
                    }
                }
            }
        }
    }
}
