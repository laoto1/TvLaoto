import codecs

content = """package com.tvlaoto.ui.components

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
import kotlinx.coroutines.delay

@Composable
fun SearchOverlayDialog(
    searchQuery: String,
    onQueryChange: (String) -> Unit,
    onDismiss: () -> Unit
) {
    var isVisible by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        isVisible = true
    }

    val triggerDismiss = {
        isVisible = false
    }

    Dialog(
        onDismissRequest = triggerDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0x99000000)) // Dim background
                .clickable(indication = null, interactionSource = remember { MutableInteractionSource() }) { triggerDismiss() },
            contentAlignment = Alignment.Center
        ) {
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn(tween(300)) + scaleIn(tween(300), initialScale = 0.9f),
                exit = fadeOut(tween(200)) + scaleOut(tween(200), targetScale = 0.95f)
            ) {
                // Wait for exit animation to finish before calling real onDismiss
                LaunchedEffect(isVisible) {
                    if (!isVisible) {
                        delay(200)
                        onDismiss()
                    }
                }

                Box(
                    modifier = Modifier
                        .width(560.dp)
                        .clip(GtaShapes.DialogShape)
                        .background(Brush.linearGradient(listOf(Color(0xEB0A0A14), Color(0xEB1A1A2E))))
                        .clickable(indication = null, interactionSource = remember { MutableInteractionSource() }) {} // Prevent click-through
                        .padding(32.dp)
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        // Header
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = stringResource(R.string.search_title),
                                style = TextStyle(
                                    fontFamily = FontFamily.SansSerif,
                                    fontWeight = FontWeight.Black,
                                    fontSize = 24.sp,
                                    color = Color.White
                                )
                            )
                            Box(
                                modifier = Modifier
                                    .size(36.dp)
                                    .clip(GtaShapes.SmallCardShape)
                                    .background(Color(0x33FFFFFF))
                                    .clickable { triggerDismiss() },
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

                        Spacer(modifier = Modifier.height(24.dp))

                        // Search Input Field
                        val searchInteractionSource = remember { MutableInteractionSource() }
                        val isSearchFocused by searchInteractionSource.collectIsFocusedAsState()

                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(56.dp)
                                .clip(GtaShapes.SmallCardShape)
                                .background(Color(0x4D000000))
                                .padding(horizontal = 16.dp),
                            contentAlignment = Alignment.CenterStart
                        ) {
                            // Animated Neon Border when focused
                            if (isSearchFocused) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .com.tvlaoto.ui.theme.neonBorder(
                                            brush = SolidColor(GtaColors.ElectricCyan),
                                            cornerRadius = 12.dp,
                                            borderWidth = 2.dp,
                                            glowRadius = 12.dp,
                                            glowAlpha = 0.5f
                                        )
                                )
                            } else {
                                Box(
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .com.tvlaoto.ui.theme.neonBorder(
                                            brush = SolidColor(Color(0x4DFFFFFF)),
                                            cornerRadius = 12.dp,
                                            borderWidth = 1.dp,
                                            glowRadius = 0.dp,
                                            glowAlpha = 0f
                                        )
                                )
                            }

                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = Icons.Default.Search,
                                    contentDescription = null,
                                    tint = if (isSearchFocused) GtaColors.ElectricCyan else GtaColors.TextMuted,
                                    modifier = Modifier.size(24.dp)
                                )
                                Spacer(modifier = Modifier.width(12.dp))
                                Box(modifier = Modifier.weight(1f)) {
                                    if (searchQuery.isEmpty()) {
                                        Text(
                                            text = stringResource(R.string.search_placeholder),
                                            color = GtaColors.TextMuted,
                                            fontSize = 15.sp,
                                            maxLines = 1
                                        )
                                    }
                                    BasicTextField(
                                        value = searchQuery,
                                        onValueChange = onQueryChange,
                                        textStyle = TextStyle(
                                            color = Color.White,
                                            fontSize = 16.sp,
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

                        Spacer(modifier = Modifier.height(28.dp))

                        // Done Button
                        TvButton(
                            text = stringResource(R.string.search_submit),
                            isSelected = true,
                            onClick = triggerDismiss,
                            modifier = Modifier.fillMaxWidth().height(48.dp)
                        )
                    }
                }
            }
        }
    }
}
"""

with codecs.open('app/src/main/java/com/tvlaoto/ui/components/SearchOverlayDialog.kt', 'w', 'utf-8') as f:
    f.write(content)

print("Updated SearchOverlayDialog")
