package com.tvlaoto.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.focusable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Replay
import androidx.compose.ui.res.stringResource
import com.tvlaoto.R
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.Icon
import androidx.tv.material3.Text
import com.tvlaoto.data.model.EpgProgram
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes
import com.tvlaoto.ui.theme.neonBorder
import java.util.Calendar
import java.text.SimpleDateFormat
import java.util.Locale
import kotlinx.coroutines.launch

@Composable
fun EpgSidePanel(
    visible: Boolean,
    epgList: List<EpgProgram>,
    isLoading: Boolean,
    currentCatchupProgram: EpgProgram?,
    onClose: () -> Unit,
    onPlayCatchup: (EpgProgram) -> Unit,
    modifier: Modifier = Modifier
) {
    AnimatedVisibility(
        visible = visible,
        enter = slideInHorizontally(
            initialOffsetX = { it },
            animationSpec = tween(durationMillis = 400)
        ),
        exit = slideOutHorizontally(
            targetOffsetX = { it },
            animationSpec = tween(durationMillis = 300)
        ),
        modifier = modifier.fillMaxSize()
    ) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.CenterEnd
        ) {
            // Clickeable backdrop
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color(0x66000000))
                    .clickable { onClose() }
            )
            
            // Glass Panel
            Column(
                modifier = Modifier
                    .fillMaxHeight()
                    .padding(vertical = 24.dp, horizontal = 16.dp)
                    .width(420.dp)
                    .clip(RoundedCornerShape(24.dp))
                    .background(Brush.horizontalGradient(listOf(Color(0xE60A0A14), Color(0xF212121C))))
                    .neonBorder(
                        brush = Brush.linearGradient(listOf(Color(0x66FFFFFF), Color(0x1AFFFFFF))),
                        cornerRadius = 24.dp,
                        borderWidth = 1.dp,
                        glowRadius = 12.dp
                    )
                    .padding(vertical = 20.dp, horizontal = 24.dp)
            ) {
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Hôm nay - " + SimpleDateFormat("dd/MM", Locale.getDefault()).format(Calendar.getInstance().time),
                        style = TextStyle(
                            fontFamily = FontFamily.SansSerif,
                            fontWeight = FontWeight.Bold,
                            fontSize = 24.sp,
                            color = Color.White
                        ),
                        modifier = Modifier.weight(1f)
                    )
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(RoundedCornerShape(18.dp))
                            .background(GtaColors.SurfaceDark)
                            .clickable { onClose() },
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
                
                Spacer(modifier = Modifier.padding(12.dp))
                NeonDivider()
                Spacer(modifier = Modifier.padding(12.dp))
                
                if (isLoading) {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        NeonLoadingIndicator(text = "Đang tải lịch phát sóng...")
                    }
                } else if (epgList.isEmpty()) {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        Text("Không có lịch phát sóng.", color = GtaColors.TextMuted)
                    }
                } else {
                    val listState = rememberLazyListState()
                    val scope = rememberCoroutineScope()
                    
                    // Find current live program
                    val currentTime = Calendar.getInstance()
                    val currentHour = currentTime.get(Calendar.HOUR_OF_DAY)
                    val currentMinute = currentTime.get(Calendar.MINUTE)
                    val currentTotalMinutes = currentHour * 60 + currentMinute
                    
                    var liveIndex = 0
                    for (i in epgList.indices) {
                        val timeParts = epgList[i].time.split(":")
                        if (timeParts.size == 2) {
                            val h = timeParts[0].toIntOrNull() ?: 0
                            val m = timeParts[1].toIntOrNull() ?: 0
                            val totalMins = h * 60 + m
                            if (totalMins <= currentTotalMinutes) {
                                liveIndex = i
                            } else {
                                break
                            }
                        }
                    }

                    LaunchedEffect(visible, epgList) {
                        if (visible && epgList.isNotEmpty()) {
                            // If playing a catchup program, scroll to it. Otherwise scroll to live.
                            val scrollIndex = if (currentCatchupProgram != null) {
                                epgList.indexOfFirst { it.index == currentCatchupProgram.index }.takeIf { it >= 0 } ?: liveIndex
                            } else {
                                liveIndex
                            }
                            
                            // Scroll slightly above center
                            val targetIndex = maxOf(0, scrollIndex - 2)
                            listState.animateScrollToItem(targetIndex)
                        }
                    }

                    LazyColumn(
                        state = listState,
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        itemsIndexed(epgList) { index, program ->
                            val isLive = (index == liveIndex && currentCatchupProgram == null)
                            val isPlayingThis = (currentCatchupProgram?.index == program.index) || isLive
                            
                            EpgProgramItem(
                                program = program,
                                isPlayingThis = isPlayingThis,
                                isLive = isLive,
                                onClick = {
                                    if (program.isReplayable) {
                                        onPlayCatchup(program)
                                    }
                                }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun EpgProgramItem(
    program: EpgProgram,
    isPlayingThis: Boolean,
    isLive: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()
    
    val backgroundBrush = when {
        isFocused || isPlayingThis -> Brush.horizontalGradient(
            colors = listOf(Color(0x66E91E63), Color(0x669C27B0))
        )
        else -> Brush.linearGradient(
            colors = listOf(Color(0x1AFFFFFF), Color(0x1AFFFFFF))
        )
    }

    val borderBrush = when {
        isFocused || isPlayingThis -> Brush.horizontalGradient(
            colors = listOf(Color(0xFFE91E63), Color(0xFF9C27B0))
        )
        else -> SolidColor(Color.Transparent)
    }
    
    Box(
        modifier = modifier
            .fillMaxWidth()
            .clip(GtaShapes.SmallCardShape)
            .background(backgroundBrush)
            .neonBorder(
                brush = borderBrush,
                cornerRadius = 8.dp,
                borderWidth = if (isFocused || isPlayingThis) 2.dp else 1.dp,
                glowRadius = if (isFocused || isPlayingThis) 6.dp else 0.dp
            )
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() }
            .padding(vertical = 12.dp, horizontal = 16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = program.time,
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp,
                    color = if (isFocused || isPlayingThis) Color.White else GtaColors.TextPrimary
                ),
                modifier = Modifier.width(60.dp)
            )
            
            Text(
                text = program.title,
                style = TextStyle(
                    fontFamily = FontFamily.SansSerif,
                    fontWeight = if (isPlayingThis) FontWeight.Bold else FontWeight.Normal,
                    fontSize = 14.sp,
                    color = if (isFocused || isPlayingThis) Color.White else GtaColors.TextSecondary
                ),
                modifier = Modifier.weight(1f),
                maxLines = 2
            )
            
            Spacer(modifier = Modifier.width(8.dp))
            
            if (isLive) {
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(4.dp))
                        .background(GtaColors.ElectricCyan)
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Text(
                        text = "LIVE",
                        style = TextStyle(
                            fontFamily = FontFamily.SansSerif,
                            fontWeight = FontWeight.Bold,
                            fontSize = 10.sp,
                            color = Color.Black
                        )
                    )
                }
            } else if (isPlayingThis) {
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(4.dp))
                        .background(GtaColors.HotPink)
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Text(
                        text = "PLAYING",
                        style = TextStyle(
                            fontFamily = FontFamily.SansSerif,
                            fontWeight = FontWeight.Bold,
                            fontSize = 10.sp,
                            color = Color.White
                        )
                    )
                }
            }
            
            if (program.isReplayable && !isLive) {
                Spacer(modifier = Modifier.width(8.dp))
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(4.dp))
                        .background(if (isFocused) GtaColors.ElectricCyan else Color(0x3300F0FF))
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(3.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Replay,
                            contentDescription = "Replay",
                            tint = if (isFocused) Color.Black else GtaColors.ElectricCyan,
                            modifier = Modifier.size(12.dp)
                        )
                        Text(
                            text = stringResource(R.string.replay).uppercase(),
                            style = TextStyle(
                                fontFamily = FontFamily.SansSerif,
                                fontWeight = FontWeight.Bold,
                                fontSize = 10.sp,
                                color = if (isFocused) Color.Black else GtaColors.ElectricCyan
                            )
                        )
                    }
                }
            }
        }
    }
}
