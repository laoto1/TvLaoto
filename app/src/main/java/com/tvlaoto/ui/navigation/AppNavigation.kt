package com.tvlaoto.ui.navigation

import android.net.Uri
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.tvlaoto.data.repository.ChannelRepository
import com.tvlaoto.player.PlayerViewModel
import com.tvlaoto.ui.screens.HomeScreen
import com.tvlaoto.ui.screens.PlayerScreen
import com.tvlaoto.ui.screens.SplashScreen

object Routes {
    const val SPLASH = "splash"
    const val HOME = "home"
    const val PLAYER = "player/{channelId}"

    fun player(channelId: String): String {
        return "player/${Uri.encode(channelId)}"
    }
}

@Composable
fun AppNavigation(
    repository: ChannelRepository,
    playerViewModel: PlayerViewModel,
    modifier: Modifier = Modifier
) {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Routes.SPLASH,
        enterTransition = { fadeIn() },
        exitTransition = { fadeOut() },
        modifier = modifier
    ) {
        composable(Routes.SPLASH) {
            SplashScreen(
                onSplashFinished = {
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.SPLASH) { inclusive = true }
                    }
                }
            )
        }

        composable(Routes.HOME) {
            HomeScreen(
                repository = repository,
                playerViewModel = playerViewModel,
                onEnterFullscreen = { channelId ->
                    navController.navigate(Routes.player(channelId))
                }
            )
        }

        composable(
            route = Routes.PLAYER,
            arguments = listOf(
                navArgument("channelId") { type = NavType.StringType }
            )
        ) { backStackEntry ->
            val channelId = backStackEntry.arguments?.getString("channelId") ?: ""
            PlayerScreen(
                channelId = channelId,
                viewModel = playerViewModel,
                onBack = { navController.popBackStack() }
            )
        }
    }
}

