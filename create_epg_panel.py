content = """package com.tvlaoto.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.focusable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Replay
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.Icon
import androidx.tv.material3.Text
import com.tvlaoto.data.model.EpgProgram
import com.tvlaoto.ui.theme.GtaColors

@Composable
fun EpgSidePanel(
    visible: Boolean,
    epgList: List<EpgProgram>,
    isLoading: Boolean,
    onClose: () -> Unit,
    onPlayCatchup: (EpgProgram) -> Unit,
    modifier: Modifier = Modifier
) {
    AnimatedVisibility(
        visible = visible,
        enter = slideInHorizontally(initialOffsetX = { it }),
        exit = slideOutHorizontally(targetOffsetX = { it }),
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
                    .background(Color(0x33000000))
                    .clickable { onClose() }
            )
            
            // Panel
            Column(
                modifier = Modifier
                    .fillMaxHeight()
                    .width(400.dp)
                    .background(GtaColors.SurfaceElevated)
                    .border(1.dp, GtaColors.BorderUnfocused)
                    .padding(vertical = 16.dp, horizontal = 20.dp)
            ) {
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Hôm nay",
                        style = TextStyle(
                            fontFamily = FontFamily.SansSerif,
                            fontWeight = FontWeight.Bold,
                            fontSize = 20.sp,
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
                    LazyColumn(
                        modifier = Modifier.fillMaxSize()
                    ) {
                        items(epgList) { program ->
                            EpgProgramItem(
                                program = program,
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
    onClick: () -> Unit
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()
    
    val bgColor = if (isFocused) Brush.horizontalGradient(listOf(GtaColors.ElectricCyan, GtaColors.HotPink)) 
                  else Brush.horizontalGradient(listOf(Color.Transparent, Color.Transparent))
                  
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(bgColor)
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() }
            .padding(vertical = 12.dp, horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = program.time,
            style = TextStyle(
                fontFamily = FontFamily.SansSerif,
                fontWeight = FontWeight.Bold,
                fontSize = 16.sp,
                color = if (isFocused) Color.White else GtaColors.TextPrimary
            ),
            modifier = Modifier.width(60.dp)
        )
        
        Text(
            text = program.title,
            style = TextStyle(
                fontFamily = FontFamily.SansSerif,
                fontWeight = FontWeight.Normal,
                fontSize = 14.sp,
                color = if (isFocused) Color.White else GtaColors.TextSecondary
            ),
            modifier = Modifier.weight(1f),
            maxLines = 2
        )
        
        if (program.isReplayable) {
            Icon(
                imageVector = Icons.Default.Replay,
                contentDescription = "Replay",
                tint = if (isFocused) Color.White else GtaColors.TextMuted,
                modifier = Modifier.size(20.dp)
            )
        }
    }
}
"""
with open('app/src/main/java/com/tvlaoto/ui/components/EpgSidePanel.kt', 'w', encoding='utf-8') as f:
    f.write(content)
print("Created EpgSidePanel.kt")
