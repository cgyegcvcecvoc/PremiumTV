package com.premiumtv.app.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.focusable
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.key.Key
import androidx.compose.ui.input.key.KeyEventType
import androidx.compose.ui.input.key.key
import androidx.compose.ui.input.key.onKeyEvent
import androidx.compose.ui.input.key.type
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.premiumtv.app.update.AppUpdateNotice
import com.premiumtv.app.update.NoticeLevel

/**
 * The startup popup that sends an older build to GitHub for the newest release.
 *
 * It is shown by AppRoot whenever [AppUpdateNotice] applies to this build, and
 * it is *dismissible on purpose*: a TV remote can arrive here mid-evening, and
 * an app that refuses to run turns "please update" into "your TV is broken".
 * The dismissal lasts one launch, so the notice is back the next time PremiumTV
 * opens and cannot be forgotten by accident.
 *
 * The remote controls the copy, the targeted version range and the support-end
 * date (`app-update-notice.json`), so this dialog never has to be rebuilt to
 * change what it says. Once the published support window closes the same rule
 * escalates to [NoticeLevel.EndOfSupport] and the accents turn red.
 *
 * @param onUpdate    the primary action: open Settings' update centre and check
 *                    GitHub again. The installer still downloads only on the
 *                    Settings button - rule 5 in docs/UPDATES.md.
 * @param onDismiss   "Remind me next time" - and the remote's Back key.
 */
@Composable
fun UpdateNoticeDialog(
    notice: AppUpdateNotice,
    installedVersion: String,
    newestVersion: String?,
    updateAvailable: Boolean,
    onUpdate: () -> Unit,
    onDismiss: () -> Unit,
) {
    val ended = notice.level == NoticeLevel.EndOfSupport
    val accent = if (ended) LiveRed else PremiumGold
    // A dialog window is clipped by the screen, not scrolled by it: on a short
    // TV panel the buttons used to fall off the bottom edge, which left the
    // message with no way to act on it. The card is capped to the screen and
    // only the middle scrolls, so the two buttons are always on screen.
    val screenHeightDp = LocalConfiguration.current.screenHeightDp
    val cardMaxHeight = (screenHeightDp - 32).coerceAtLeast(240).dp
    // A remote has no pointer: the primary action takes focus as soon as the
    // dialog opens, so one press of the centre key starts the update.
    val actionFocus = remember { FocusRequester() }
    LaunchedEffect(notice.id) {
        runCatching { actionFocus.requestFocus() }
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(
            // Back dismisses; tapping the dimmed background does not, so a
            // stray touch cannot hide the message without a deliberate action.
            dismissOnBackPress = true,
            dismissOnClickOutside = false,
            usePlatformDefaultWidth = false,
        ),
    ) {
        // The dialog window dims everything behind it already, so this only has
        // to centre the card and keep it off the screen edges.
        Box(
            modifier = Modifier.fillMaxWidth(),
            contentAlignment = Alignment.Center,
        ) {
            Surface(
                modifier = Modifier
                    .widthIn(max = 620.dp)
                    .padding(24.dp)
                    .heightIn(max = (cardMaxHeight - 48.dp).coerceAtLeast(200.dp)),
                shape = RoundedCornerShape(20.dp),
                color = CardBackground,
                border = BorderStroke(1.dp, accent.copy(alpha = 0.55f)),
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 28.dp, vertical = 24.dp),
                ) {
                    // The marquee plaque: one short line naming the notice, so
                    // the dialog reads as an announcement and not as an error.
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(accent.copy(alpha = 0.14f), RoundedCornerShape(8.dp))
                            .padding(horizontal = 12.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Box(
                            modifier = Modifier
                                .padding(end = 8.dp)
                                .size(8.dp)
                                .background(accent, RoundedCornerShape(4.dp)),
                        )
                        Text(
                            text = if (ended) "SUPPORT HAS ENDED" else "PREMIUMTV UPDATE",
                            style = MaterialTheme.typography.labelMedium,
                            color = accent,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.6.sp,
                            modifier = Modifier.weight(1f),
                        )
                        // The version lives in the plaque rather than on its own
                        // line: on a short panel every line saved here is a line
                        // of the surprise that stays above the fold.
                        Text(
                            text = if (updateAvailable && newestVersion != null) {
                                "installed $installedVersion · newest $newestVersion"
                            } else {
                                "installed $installedVersion"
                            },
                            style = MaterialTheme.typography.labelSmall,
                            color = accent.copy(alpha = 0.75f),
                        )
                    }

                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = notice.title,
                        style = MaterialTheme.typography.headlineSmall,
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                    )

                    // A capped card has less room than the copy sometimes needs,
                    // and a remote cannot drag a scrollbar. Making this region
                    // focusable and answering the D-pad means the rest of the
                    // message is reachable on a TV: Up/Down from either button
                    // lands here and scrolls.
                    val bodyScroll = rememberScrollState()
                    Column(
                        modifier = Modifier
                            // weight(fill = false) keeps its natural height when
                            // there is room and shrinks only when the card is
                            // capped, which is what keeps the footer on screen.
                            .weight(1f, fill = false)
                            .verticalScroll(bodyScroll)
                            .focusable()
                            .onKeyEvent { event ->
                                if (event.type != KeyEventType.KeyDown) return@onKeyEvent false
                                when (event.key) {
                                    Key.DirectionDown -> {
                                        bodyScroll.dispatchRawDelta(72f)
                                        true
                                    }
                                    Key.DirectionUp -> {
                                        bodyScroll.dispatchRawDelta(-72f)
                                        true
                                    }
                                    else -> false
                                }
                            },
                    ) {
                        if (notice.message.isNotBlank()) {
                            Spacer(modifier = Modifier.height(10.dp))
                            Text(
                                text = notice.message,
                                style = MaterialTheme.typography.bodyMedium,
                                color = Color(0xFFE6EBF2),
                                lineHeight = 21.sp,
                            )
                        }
                        if (notice.surprise.isNotBlank()) {
                            Spacer(modifier = Modifier.height(14.dp))
                            // The "great surprise" gets its own lit panel: this
                            // is the sentence that makes updating worth doing.
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .background(Color(0xFF1A222D), RoundedCornerShape(12.dp))
                                    .border(
                                        1.dp,
                                        PanelStroke,
                                        RoundedCornerShape(12.dp),
                                    )
                                    .padding(14.dp),
                            ) {
                                Text(
                                    text = "THE SURPRISE",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = PremiumGold,
                                    fontWeight = FontWeight.Bold,
                                    letterSpacing = 1.4.sp,
                                )
                                Spacer(modifier = Modifier.height(6.dp))
                                Text(
                                    text = notice.surprise,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = Color(0xFFDCE4EE),
                                    lineHeight = 19.sp,
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(14.dp))
                    // Named on screen because an Android TV usually has no
                    // browser to open: this is the address to visit on a phone.
                    Text(
                        text = notice.releasesUrl,
                        style = MaterialTheme.typography.bodySmall,
                        color = PremiumGoldDim,
                    )

                    Spacer(modifier = Modifier.height(20.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        FocusButton(
                            label = notice.actionLabel,
                            modifier = Modifier
                                .weight(1f)
                                .focusRequester(actionFocus),
                        ) { onUpdate() }
                        FocusButton(
                            label = notice.dismissLabel,
                            modifier = Modifier.weight(1f),
                        ) { onDismiss() }
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(
                        text = if (ended) {
                            "Back dismisses for now; it returns every launch."
                        } else {
                            "Back dismisses for now; it returns every launch until you update."
                        },
                        style = MaterialTheme.typography.labelSmall,
                        color = MutedText,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.fillMaxWidth(),
                    )
                }
            }
        }
    }
}
