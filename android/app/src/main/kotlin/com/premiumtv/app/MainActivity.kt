package com.premiumtv.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.core.view.WindowCompat
import com.premiumtv.app.ui.AppRoot
import com.premiumtv.app.ui.PremiumTvTheme

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Compose draws the whole screen, including behind the system bars.
        WindowCompat.setDecorFitsSystemWindows(window, false)
        setContent {
            PremiumTvTheme {
                AppRoot()
            }
        }
    }
}
