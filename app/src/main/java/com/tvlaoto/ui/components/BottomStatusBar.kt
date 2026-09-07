package com.tvlaoto.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Campaign
import androidx.compose.material.icons.filled.Wifi
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.Icon
import androidx.tv.material3.Text
import com.tvlaoto.R
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes
import kotlinx.coroutines.delay
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
private fun StatusClock() {
    val timeFormat = remember { SimpleDateFormat("HH:mm", Locale.getDefault()) }
    val dateFormat = remember { SimpleDateFormat("EEE, dd/MM/yyyy", Locale("vi")) }

    var currentTime by remember {
        mutableStateOf(timeFormat.format(Date()))
    }
    var currentDate by remember {
        mutableStateOf(dateFormat.format(Date()))
    }

    LaunchedEffect(Unit) {
        while (true) {
            delay(1000)
            val now = Date()
            val newTime = timeFormat.format(now)
            if (newTime != currentTime) {
                currentTime = newTime
            }
            val newDate = dateFormat.format(now)
            if (newDate != currentDate) {
                currentDate = newDate
            }
        }
    }

    Text(
        text = currentTime,
        style = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Bold,
            fontSize = 14.sp,
            color = Color.White
        )
    )
    Spacer(modifier = Modifier.width(10.dp))
    Text(
        text = currentDate,
        style = TextStyle(
            fontFamily = FontFamily.SansSerif,
            fontWeight = FontWeight.Normal,
            fontSize = 11.sp,
            color = Color(0xFF8E95AF)
        )
    )
}

@Composable
fun BottomStatusBar(
    currentChannelName: String?,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(42.dp)
            .padding(horizontal = 24.dp, vertical = 2.dp)
            .clip(GtaShapes.PillShape)
            .background(Color(0x990A0D1E))
            .border(1.dp, Color(0x15FFFFFF), GtaShapes.PillShape)
            .padding(horizontal = 16.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Left: Neon Pink Palm Tree + Clock + Date
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    painter = painterResource(id = R.drawable.ic_palm_tree),
                    contentDescription = "Vice City Palm",
                    tint = Color(0xFFEC4899),
                    modifier = Modifier.size(18.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                StatusClock()
            }

            // Center: Broadcast Announcement
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Default.Campaign,
                    contentDescription = "Announcement",
                    tint = Color(0xFFEC4899),
                    modifier = Modifier
                        .size(16.dp)
                        .padding(end = 4.dp)
                )
                Text(
                    text = "Thông báo: Lịch phát sóng có thể thay đổi tùy theo nhà đài.",
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Normal,
                        fontSize = 11.sp,
                        color = Color(0xFF8E95AF)
                    )
                )
            }

            // Right: Wi-Fi status + Now Playing channel
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Default.Wifi,
                    contentDescription = "Wi-Fi",
                    tint = Color(0xFF38BDF8),
                    modifier = Modifier
                        .size(16.dp)
                        .padding(end = 6.dp)
                )
                Text(
                    text = "Đang phát: ",
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Normal,
                        fontSize = 11.sp,
                        color = Color(0xFF8E95AF)
                    )
                )
                Text(
                    text = currentChannelName ?: "VTV1 HD",
                    style = TextStyle(
                        fontFamily = FontFamily.SansSerif,
                        fontWeight = FontWeight.Bold,
                        fontSize = 11.sp,
                        color = Color(0xFF38BDF8)
                    )
                )
                Spacer(modifier = Modifier.width(6.dp))
                Text(
                    text = "ılı",
                    style = TextStyle(
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Black,
                        fontSize = 11.sp,
                        color = Color(0xFFEC4899)
                    )
                )
            }
        }
    }
}

