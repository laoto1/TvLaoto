package com.tvlaoto.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.tvlaoto.data.model.IptvCategory
import com.tvlaoto.data.model.IptvChannel

@Composable
fun CategoryRow(
    category: IptvCategory,
    onChannelSelected: (IptvChannel) -> Unit,
    modifier: Modifier = Modifier,
    currentPlayingChannelId: String? = null
) {
    val listState = rememberLazyListState()

    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 10.dp)
    ) {
        // Gradient Category Title
        GradientHeader(
            title = category.title,
            tag = "${category.channels.size} CH",
            modifier = Modifier.padding(horizontal = 36.dp)
        )

        Spacer(modifier = Modifier.height(12.dp))

        // Virtualized Horizontal Row of Channels
        LazyRow(
            state = listState,
            contentPadding = PaddingValues(horizontal = 36.dp, vertical = 6.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            items(
                items = category.channels,
                key = { channel -> channel.id }
            ) { channel ->
                ChannelCard(
                    channel = channel,
                    isPlaying = channel.id == currentPlayingChannelId,
                    onClick = { onChannelSelected(channel) }
                )
            }
        }
    }
}

