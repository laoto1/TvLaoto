package com.tvlaoto.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.focusable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsFocusedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import com.tvlaoto.TvLaotoApp
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import kotlinx.coroutines.delay
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.tv.material3.Icon
import androidx.tv.material3.Text
import com.tvlaoto.R
import com.tvlaoto.data.model.IptvChannel
import com.tvlaoto.data.repository.ChannelRepository
import com.tvlaoto.player.PlayerViewModel
import com.tvlaoto.ui.components.BottomStatusBar
import com.tvlaoto.ui.components.ChannelListItem
import com.tvlaoto.ui.components.FeaturedChannelsRow
import com.tvlaoto.ui.components.NeonLoadingIndicator
import com.tvlaoto.ui.components.ProgramInfoPanel
import com.tvlaoto.ui.components.SearchOverlayDialog
import com.tvlaoto.ui.components.SettingsDialog
import com.tvlaoto.ui.components.EpgSidePanel
import com.tvlaoto.ui.components.TopNavigationBar
import com.tvlaoto.ui.components.VideoPlayerPanel
import com.tvlaoto.ui.theme.GtaColors
import com.tvlaoto.ui.theme.GtaShapes
import kotlinx.coroutines.launch
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.draw.drawWithContent
import com.tvlaoto.ui.theme.neonBorder

@Composable
fun HomeScreen(
    repository: ChannelRepository,
    playerViewModel: PlayerViewModel,
    onEnterFullscreen: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val playlist by repository.playlist.collectAsState()
    val settings by repository.settings.collectAsState()
    val isLoading by repository.isLoading.collectAsState()

    val currentPlayingChannel by playerViewModel.currentChannel.collectAsState()
    val isPlaying by playerViewModel.isPlaying.collectAsState()
    val isEpgPanelVisible by playerViewModel.isEpgPanelVisible.collectAsState()
    val epgList by playerViewModel.epgList.collectAsState()
    
    val liveProgram = remember(epgList) {
        if (epgList.isEmpty()) null
        else {
            val currentTime = java.util.Calendar.getInstance()
            val currentHour = currentTime.get(java.util.Calendar.HOUR_OF_DAY)
            val currentMinute = currentTime.get(java.util.Calendar.MINUTE)
            val currentTotalMinutes = currentHour * 60 + currentMinute
            var live: com.tvlaoto.data.model.EpgProgram? = null
            for (p in epgList) {
                val timeParts = p.time.split(":")
                if (timeParts.size == 2) {
                    val h = timeParts[0].toIntOrNull() ?: 0
                    val m = timeParts[1].toIntOrNull() ?: 0
                    val totalMins = h * 60 + m
                    if (totalMins <= currentTotalMinutes) {
                        live = p
                    } else break
                }
            }
            live
        }
    }
    val isEpgLoading by playerViewModel.isEpgLoading.collectAsState()
    val currentCatchupProgram by playerViewModel.currentCatchupProgram.collectAsState()
    val isBuffering by playerViewModel.isBuffering.collectAsState()
    val isDecryptingLink by playerViewModel.isDecryptingLink.collectAsState()
    val errorMessage by playerViewModel.errorMessage.collectAsState()

    androidx.compose.runtime.LaunchedEffect(errorMessage) {
        if (errorMessage != null) {
            delay(4000)
            playerViewModel.clearError()
        }
    }

    var selectedCategory by remember { mutableStateOf("Truyền hình") }
    var selectedFilterTab by remember { mutableStateOf("Tất cả") }
    var showAdvancedFilter by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(Unit) {
        selectedFilterTab = repository.getLastFilterTab()
    }
    var searchQuery by remember { mutableStateOf("") }
    var showSettingsDialog by remember { mutableStateOf(false) }
    var showSearchDialog by remember { mutableStateOf(false) }

    val coroutineScope = rememberCoroutineScope()
    val context = LocalContext.current

    // Flatten all channels
    val allChannels = remember(playlist) {
        playlist?.categories?.flatMap { it.channels } ?: emptyList()
    }

    // Auto play first channel on initial load
    LaunchedEffect(allChannels) {
        if (allChannels.isNotEmpty() && currentPlayingChannel == null) {
            val initialChannel = allChannels.find { it.id == settings.lastPlayedChannelId } ?: allChannels.first()
            playerViewModel.playChannel(initialChannel)
        }
    }

    // Filter channels by Tab (Tất cả, Yêu thích, VTV, VTVCab) and Search
    val dynamicGroups = remember(playlist) {
        val groups = playlist?.categories?.map { it.title }?.distinct() ?: emptyList()
        groups
    }

    val displayedChannels = remember(allChannels, selectedFilterTab, searchQuery) {
        var list = allChannels

        // Tab Filter
        list = when (selectedFilterTab) {
            "Tất cả" -> list
            "Yêu thích" -> list.filter { it.isFavorite }
            else -> list.filter { it.groupTitle == selectedFilterTab }
        }

        // Search Filter
        if (searchQuery.isNotBlank()) {
            val q = searchQuery.trim().lowercase()
            list = list.filter {
                it.name.lowercase().contains(q) ||
                it.currentProgram.lowercase().contains(q) ||
                it.channelNumber.toString() == q
            }
        }

        list
    }

    // Root Container
    Box(
        modifier = modifier.fillMaxSize()
    ) {
        // Single solid background — no overdraw
        Box(modifier = Modifier.fillMaxSize().background(Color(0xFF05050A)))

        // 2. Main UI Content
        Column(modifier = Modifier.fillMaxSize()) {

            // Top Navigation Bar            // Top Navigation Bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(Color(0xCC05050A), Color.Transparent),
                            startY = 0f,
                            endY = 300f
                        )
                    )
            ) {
                TopNavigationBar(
                    selectedCategory = selectedCategory,
                    onSelectCategory = { selectedCategory = it },
                    onSearchClick = { showSearchDialog = true },
                    onSettingsClick = { showSettingsDialog = true }
                )
            }

            // Main Center Split-Screen Layout (Left: 28%, Right: 72%)
            Row(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp, vertical = 2.dp),
                horizontalArrangement = Arrangement.spacedBy(14.dp)
            ) {

                // LEFT COLUMN: DANH SÁCH KÊNH (Neon Glowing Frame)
                Column(
                    modifier = Modifier
                        .weight(0.28f)
                        .fillMaxHeight()
                                .clip(GtaShapes.LargeCardShape)
                        .background(Color(0xEB05050A))
                        .border(1.dp, Color(0xFF38BDF8).copy(alpha = 0.3f), GtaShapes.LargeCardShape)
                        .padding(10.dp)
                ) {
                    // Header Title: DANH SÁCH KÊNH
                    Text(
                        text = "DANH SÁCH KÊNH",
                        style = TextStyle(
                            fontFamily = FontFamily.SansSerif,
                            fontWeight = FontWeight.Bold,
                            fontSize = 13.sp,
                            letterSpacing = 0.5.sp,
                            brush = Brush.horizontalGradient(
                                colors = listOf(Color(0xFF38BDF8), Color(0xFFC084FC))
                            )
                        )
                    )

                    Spacer(modifier = Modifier.height(8.dp))

                    // Filter Pills Row
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(4.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        val displayTabs = mutableListOf("Tất cả", "Yêu thích")
                        displayTabs.addAll(dynamicGroups.take(2))
                        
                        if (selectedFilterTab !in displayTabs && selectedFilterTab.isNotBlank()) {
                            if (displayTabs.size > 2) displayTabs[2] = selectedFilterTab
                            else displayTabs.add(selectedFilterTab)
                        }

                        displayTabs.forEach { tab ->
                            val isTabSelected = tab == selectedFilterTab
                            ChannelFilterPill(
                                title = tab,
                                isSelected = isTabSelected,
                                onClick = { 
                                    selectedFilterTab = tab 
                                    scope.launch { repository.saveLastFilterTab(tab) }
                                }
                            )
                        }

                        Box(
                            modifier = Modifier
                                .size(26.dp)
                                .clip(GtaShapes.SmallCardShape)
                                .background(Brush.horizontalGradient(listOf(Color(0x33FFFFFF), Color(0x11FFFFFF))))
                                .border(1.dp, SolidColor(Color(0x33FFFFFF)), GtaShapes.SmallCardShape)
                                .clickable { showAdvancedFilter = true },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Menu,
                                contentDescription = "Bộ lọc nâng cao nâng cao",
                                tint = Color.White,
                                modifier = Modifier.size(16.dp)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    // Channel Items Vertical List
                    if (isLoading) {
                        Box(
                            modifier = Modifier.fillMaxSize(),
                            contentAlignment = Alignment.Center
                        ) {
                            NeonLoadingIndicator()
                        }
                    } else if (displayedChannels.isEmpty()) {
                        Box(
                            modifier = Modifier.fillMaxSize(),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = "Không tìm thấy kênh",
                                color = GtaColors.TextMuted,
                                fontSize = 12.sp
                            )
                        }
                    } else {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            verticalArrangement = Arrangement.spacedBy(4.dp),
                            contentPadding = PaddingValues(vertical = 2.dp)
                        ) {
                            items(
                                items = displayedChannels,
                                key = { ch -> ch.id }
                            ) { channel ->
                                val isChannelSelected = channel.id == currentPlayingChannel?.id
                                ChannelListItem(
                                    channel = channel,
                                    isSelected = isChannelSelected,
                                    onClick = {
                                        playerViewModel.playChannel(channel)
                                    },
                                    onToggleFavorite = { repository.toggleFavorite(channel.id) }
                                )
                            }
                        }
                    }
                }

                // RIGHT COLUMN: Live Video + Program EPG Info (Đã xoá Kênh nổi bật)
                Column(
                    modifier = Modifier
                        .weight(0.72f)
                        .fillMaxHeight(),
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    // 1. Video Player Panel (Phóng to tối đa)
                    VideoPlayerPanel(
                        player = playerViewModel.player,
                        channel = currentPlayingChannel,
                        isPlaying = isPlaying,
                        isBuffering = isBuffering,
                        isDecryptingLink = isDecryptingLink,
                        isCatchup = currentCatchupProgram != null,
                        onTogglePlayPause = {
                            if (isPlaying) playerViewModel.player.pause()
                            else playerViewModel.player.play()
                        },
                        onToggleFullscreen = {
                            currentPlayingChannel?.let { onEnterFullscreen(it.id) }
                        },
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxWidth()
                            .padding(bottom = 14.dp)
                    )                    // 2. Program EPG Info & Action Buttons
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(GtaShapes.LargeCardShape)
                            .background(
                                Brush.verticalGradient(colors = listOf(Color(0x8005050A), Color(0xEB05050A)))
                            )
                            .padding(14.dp)
                    ) {
                        ProgramInfoPanel(
                              channel = currentPlayingChannel,
                              currentCatchupProgram = currentCatchupProgram,
                              liveProgram = liveProgram,
                              onReplayClick = {
                                  playerViewModel.showEpgPanel()
                              },
                              onFavoriteClick = { currentPlayingChannel?.let { repository.toggleFavorite(it.id) } },
                        )
                    }
                }
            }

            // Bottom Status Bar
            BottomStatusBar(
                currentChannelName = currentPlayingChannel?.name
            )
        }

        // Animated Error Toast
        AnimatedVisibility(
            visible = errorMessage != null,
            enter = slideInVertically(initialOffsetY = { -it }) + fadeIn(),
            exit = slideOutVertically(targetOffsetY = { -it }) + fadeOut(),
            modifier = Modifier.align(Alignment.TopCenter).padding(top = 24.dp)
        ) {
            Box(
                modifier = Modifier
                    .clip(GtaShapes.SmallCardShape)
                    .background(Color(0xE6FF003C))
                    .border(1.dp, Color.White.copy(alpha = 0.5f), GtaShapes.SmallCardShape)
                    .padding(horizontal = 24.dp, vertical = 12.dp)
            ) {
                Text(
                    text = errorMessage ?: "",
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp
                )
            }
        }

        
        // Advanced Filter Popup
        if (showAdvancedFilter) {
            androidx.compose.ui.window.Dialog(onDismissRequest = { showAdvancedFilter = false }) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(0.9f)
                        .clip(GtaShapes.LargeCardShape)
                        .background(Brush.linearGradient(listOf(Color(0xE605050A), Color(0xCC1A1A24))))
                        .border(1.dp, SolidColor(Color(0x33FFFFFF)), GtaShapes.LargeCardShape)
                        .padding(16.dp)
                ) {
                    Column {
                        Text(
                            text = "BỘ LỌC NÂNG CAO",
                            color = Color(0xFF38BDF8),
                            fontWeight = FontWeight.Bold,
                            fontSize = 16.sp
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        androidx.compose.foundation.lazy.grid.LazyVerticalGrid(
                            columns = androidx.compose.foundation.lazy.grid.GridCells.Fixed(2),
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp),
                            modifier = Modifier.heightIn(max = 400.dp)
                        ) {
                            val allTabs = mutableListOf("Tất cả", "Yêu thích")
                            allTabs.addAll(dynamicGroups)
                            
                            items(allTabs.size) { index ->
                                val tab = allTabs[index]
                                val isSelected = tab == selectedFilterTab
                                ChannelFilterPill(
                                    title = tab,
                                    isSelected = isSelected,
                                    onClick = {
                                        selectedFilterTab = tab
                                        scope.launch { repository.saveLastFilterTab(tab) }
                                        showAdvancedFilter = false
                                    },
                                    modifier = Modifier.fillMaxWidth()
                                )
                            }
                        }
                    }
                }
            }
        }
        
// Search Overlay Modal Dialog
        if (showSearchDialog) {
            SearchOverlayDialog(
                searchQuery = searchQuery,
                onQueryChange = { searchQuery = it },
                onDismiss = { showSearchDialog = false }
            )
        }

        // Settings Modal Dialog
        if (showSettingsDialog) {


        SettingsDialog(
                currentUrl = settings.customM3uUrl,
                currentLang = settings.languageCode,
                onSaveUrl = { newUrl ->
                    showSettingsDialog = false
                    coroutineScope.launch {
                        repository.loadFromUrl(newUrl)
                    }
                },
                onResetToDemo = {
                    showSettingsDialog = false
                    coroutineScope.launch {
                        repository.updateCustomUrl("")
                        repository.loadBundledDemoPlaylist()
                    }
                },
                onSwitchLanguage = { newLang ->
                    repository.updateLanguage(newLang)
                    (context.applicationContext as TvLaotoApp).applyLocale(newLang)
                    if (context is androidx.activity.ComponentActivity) {
                        context.recreate()
                    }
                },
                onDismiss = { showSettingsDialog = false }
            )
        }
        EpgSidePanel(
            visible = isEpgPanelVisible,
            epgList = epgList,
            isLoading = isEpgLoading,
            currentCatchupProgram = currentCatchupProgram,
            onClose = { playerViewModel.hideEpgPanel() },
            onPlayCatchup = { program -> playerViewModel.playCatchup(program) }
        )
    }
}

@Composable
fun ChannelFilterPill(
    title: String,
    isSelected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val interactionSource = remember { MutableInteractionSource() }
    val isFocused by interactionSource.collectIsFocusedAsState()

    val backgroundBrush = when {
        isFocused || isSelected -> Brush.horizontalGradient(
            colors = listOf(Color(0x4DE91E63), Color(0x339C27B0)) // Nền hồng mờ dịu mắt
        )
        else -> Brush.linearGradient(
            colors = listOf(Color(0x1AFFFFFF), Color(0x1AFFFFFF)) // Nền xám mờ trong suốt
        )
    }

    val borderColor = when {
        isFocused || isSelected -> Color(0x99E91E63)
        else -> Color(0x11FFFFFF)
    }

    Box(
        modifier = modifier
            .height(26.dp)
                        .clip(GtaShapes.SmallCardShape)
            .background(backgroundBrush)
            .border(0.8.dp, borderColor, GtaShapes.SmallCardShape)
            .focusable(interactionSource = interactionSource)
            .clickable(interactionSource = interactionSource, indication = null) { onClick() }
            .padding(horizontal = 10.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = title,
            style = TextStyle(
                fontFamily = FontFamily.SansSerif,
                fontWeight = if (isSelected || isFocused) FontWeight.Bold else FontWeight.Medium,
                fontSize = 11.sp,
                color = if (isSelected || isFocused) Color.White else Color(0xFF94A3B8)
            )
        )


    }}

