package com.tvlaoto.ui.components

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
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
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
import androidx.tv.material3.Text
import com.tvlaoto.R
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes

@Composable
fun SettingsDialog(
    currentUrl: String,
    currentLang: String,
    onSaveUrl: (String) -> Unit,
    onResetToDemo: () -> Unit,
    onSwitchLanguage: (String) -> Unit,
    onDismiss: () -> Unit
) {
    var urlText by remember { mutableStateOf(currentUrl) }

    Dialog(onDismissRequest = onDismiss) {
        Box(
            modifier = Modifier
                .width(580.dp)
                .clip(GtaShapes.DialogShape)
                .background(GtaColors.SurfaceElevated)
                .border(2.dp, GtaColors.ElectricCyan, GtaShapes.DialogShape)
                .padding(28.dp)
        ) {
            Column(modifier = Modifier.fillMaxWidth()) {
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    GradientHeader(title = stringResource(R.string.settings))
                    Text(
                        text = "AFlix TV",
                        style = TextStyle(
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            fontSize = 11.sp,
                            color = GtaColors.LuxuryGold
                        )
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))
                NeonDivider()
                Spacer(modifier = Modifier.height(20.dp))

                // Custom M3U URL Input
                Text(
                    text = stringResource(R.string.custom_m3u_url),
                    color = Color.White,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 14.sp
                    )
                )

                Spacer(modifier = Modifier.height(8.dp))

                val inputInteractionSource = remember { MutableInteractionSource() }
                val isInputFocused by inputInteractionSource.collectIsFocusedAsState()

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(48.dp)
                        .clip(GtaShapes.SmallCardShape)
                        .background(GtaColors.SurfaceDark)
                        .border(
                            width = if (isInputFocused) 2.dp else 1.dp,
                            color = if (isInputFocused) GtaColors.ElectricCyan else GtaColors.BorderUnfocused,
                            shape = GtaShapes.SmallCardShape
                        )
                        .padding(horizontal = 14.dp, vertical = 12.dp)
                ) {
                    if (urlText.isEmpty()) {
                        Text(
                            text = stringResource(R.string.enter_m3u_hint),
                            color = GtaColors.TextMuted,
                            fontSize = 13.sp
                        )
                    }
                    BasicTextField(
                        value = urlText,
                        onValueChange = { urlText = it },
                        textStyle = TextStyle(
                            color = Color.White,
                            fontSize = 13.sp,
                            fontFamily = FontFamily.Monospace
                        ),
                        cursorBrush = SolidColor(GtaColors.ElectricCyan),
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                        keyboardActions = KeyboardActions(onDone = { onSaveUrl(urlText) }),
                        interactionSource = inputInteractionSource,
                        modifier = Modifier.fillMaxWidth()
                    )
                }

                Spacer(modifier = Modifier.height(20.dp))

                // Language Selection
                Text(
                    text = stringResource(R.string.language),
                    color = Color.White,
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 14.sp
                    )
                )

                Spacer(modifier = Modifier.height(8.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    TvButton(
                        text = "Tiếng Việt",
                        isSelected = currentLang == "vi",
                        onClick = { onSwitchLanguage("vi") },
                        modifier = Modifier.weight(1f)
                    )
                    TvButton(
                        text = stringResource(R.string.english),
                        isSelected = currentLang == "en",
                        onClick = { onSwitchLanguage("en") },
                        modifier = Modifier.weight(1f)
                    )
                }

                Spacer(modifier = Modifier.height(24.dp))
                NeonDivider()
                Spacer(modifier = Modifier.height(18.dp))

                // Action Buttons
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    TvButton(
                        text = stringResource(R.string.reset_default),
                        isSelected = false,
                        isDanger = true,
                        onClick = {
                            urlText = ""
                            onResetToDemo()
                        },
                        modifier = Modifier.weight(1.2f)
                    )

                    TvButton(
                        text = stringResource(R.string.save),
                        isSelected = true,
                        onClick = { onSaveUrl(urlText) },
                        modifier = Modifier.weight(1f)
                    )

                    TvButton(
                        text = stringResource(R.string.cancel),
                        isSelected = false,
                        onClick = onDismiss,
                        modifier = Modifier.weight(0.8f)
                    )
                }
            }
        }
    }
}

@Composable
fun TvButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    isSelected: Boolean = false,
    isDanger: Boolean = false
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    val backgroundColor = when {
        isFocused -> if (isDanger) Color(0xFF7F1D1D) else GtaColors.HotPink
        isSelected -> GtaColors.DeepPurple
        else -> GtaColors.SurfaceDark
    }

    val borderColor = when {
        isFocused -> GtaColors.ElectricCyan
        isSelected -> GtaColors.HotPink
        else -> GtaColors.BorderUnfocused
    }

    Box(
        modifier = modifier
            .height(44.dp)
            .clip(GtaShapes.SmallCardShape)
            .background(backgroundColor)
            .border(
                width = if (isFocused) 2.dp else 1.dp,
                color = borderColor,
                shape = GtaShapes.SmallCardShape
            )
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() },
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = text.uppercase(),
            style = TextStyle(
                fontFamily = FontFamily.SansSerif,
                fontWeight = FontWeight.Bold,
                fontSize = 12.sp,
                letterSpacing = 0.5.sp,
                color = if (isFocused || isSelected) Color.White else GtaColors.TextSecondary
            )
        )
    }
}

