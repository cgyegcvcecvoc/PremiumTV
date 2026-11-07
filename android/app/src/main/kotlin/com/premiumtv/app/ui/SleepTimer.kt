package com.premiumtv.app.ui

import android.content.Context
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/*
 * The 1.1.5 sleep timer.
 *
 * A TV app that can play all night is missing the one control every cable box
 * has. The deadline is a wall-clock epoch in SharedPreferences, not a running
 * coroutine, so it survives the app going to the background, a refresh, or a
 * process restart; AppRoot only has to wait for the instant to arrive.
 *
 * The label and the choices are pure, so the policy is unit-testable without
 * Android; the Surface and the persistence are thin wrappers around them.
 */

internal const val SLEEP_TIMER_PREFS = "premiumtv_sleep_timer"
internal const val SLEEP_TIMER_ENDS_AT = "ends_at_ms"

/** Minutes offered in Settings; 0 is the explicit "Off" choice. */
internal val SLEEP_TIMER_CHOICES = listOf(0, 30, 60, 90)

/** "43 min", "1 hr 30 min", "under a minute" or "Off". */
internal fun sleepTimerLabel(remainingMs: Long): String {
    if (remainingMs <= 0L) return "Off"
    if (remainingMs < 60_000L) return "under a minute"
    val minutes = (remainingMs + 59_999L) / 60_000L
    if (minutes < 60L) return "$minutes min"
    val hours = minutes / 60L
    val rest = minutes % 60L
    return if (rest == 0L) "$hours hr" else "$hours hr $rest min"
}

internal class SleepTimer(context: Context) {
    private val prefs = context.getSharedPreferences(SLEEP_TIMER_PREFS, Context.MODE_PRIVATE)

    fun endAtMillis(): Long = prefs.getLong(SLEEP_TIMER_ENDS_AT, 0L)

    fun setMinutes(minutes: Int) {
        if (minutes <= 0) {
            clear()
            return
        }
        prefs.edit()
            .putLong(SLEEP_TIMER_ENDS_AT, System.currentTimeMillis() + minutes * 60_000L)
            .apply()
    }

    fun clear() {
        prefs.edit().remove(SLEEP_TIMER_ENDS_AT).apply()
    }
}

/** Settings → Sleep timer: the live countdown and the four choices. */
@Composable
internal fun SleepTimerCard(
    now: Long,
    endsAtMillis: Long,
    onSet: (Int) -> Unit,
    onCancel: () -> Unit,
) {
    val remaining = endsAtMillis - now * 1000L
    val active = endsAtMillis > 0L && remaining > 0L
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(14.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, PanelStroke),
    ) {
        Column(modifier = Modifier.padding(horizontal = 18.dp, vertical = 12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "SLEEP TIMER",
                        style = MaterialTheme.typography.labelSmall,
                        color = PremiumGoldDim,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp,
                    )
                    Text(
                        text = if (active) {
                            "Playback stops in ${sleepTimerLabel(remaining)}"
                        } else {
                            "Off — playback keeps going until you close it"
                        },
                        style = MaterialTheme.typography.bodyMedium,
                        color = if (active) PremiumGold else Color.White,
                        fontWeight = if (active) FontWeight.SemiBold else FontWeight.Normal,
                        maxLines = 1,
                    )
                }
                if (active) {
                    Spacer(modifier = Modifier.width(10.dp))
                    FocusButton("Cancel timer", enabled = true) { onCancel() }
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                SLEEP_TIMER_CHOICES.forEach { minutes ->
                    FocusButton(if (minutes == 0) "Off" else "$minutes min") {
                        if (minutes == 0) onCancel() else onSet(minutes)
                    }
                }
            }
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = "When the timer ends the player closes, so a TV left on does not " +
                    "play all night. The deadline survives a refresh or a restart.",
                style = MaterialTheme.typography.labelSmall,
                color = MutedText,
            )
        }
    }
}

/** Shown for a few seconds after a sleep timer stops a playing channel. */
@Composable
fun SleepTimerEndedBanner(onDismiss: () -> Unit, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier.widthIn(max = 520.dp),
        shape = RoundedCornerShape(14.dp),
        color = Color(0xF0111820),
        border = BorderStroke(1.dp, FocusRing.copy(alpha = 0.7f)),
    ) {
        Row(
            modifier = Modifier.padding(start = 18.dp, end = 10.dp, top = 8.dp, bottom = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = "Sleep timer ended — playback stopped.",
                style = MaterialTheme.typography.bodyMedium,
                color = Color.White,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier.weight(1f),
            )
            Spacer(modifier = Modifier.width(12.dp))
            FocusButton("OK") { onDismiss() }
        }
    }
}
