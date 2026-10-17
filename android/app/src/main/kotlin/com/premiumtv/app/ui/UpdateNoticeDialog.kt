package com.premiumtv.app.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
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
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.layout.size
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
 * @param onUpdate    the primary action: open Settings' update centre and start
 *                    the download, which is the whole point of the newest build.
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
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xCC05070B)),
            contentAlignment = Alignment.Center,
        ) {
            Surface(
                modifier = Modifier
                    .widthIn(max = 620.dp)
                    .padding(24.dp),
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
                        )
                    }

                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = notice.title,
                        style = MaterialTheme.typography.headlineSmall,
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                    )

                    Column(
                        modifier = Modifier
                            .heightIn(max = 260.dp)
                            .verticalScroll(rememberScrollState()),
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

                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = if (updateAvailable && newestVersion != null) {
                            "Installed $installedVersion  ·  newest on GitHub $newestVersion"
                        } else {
                            "Installed $installedVersion"
                        },
                        style = MaterialTheme.typography.bodySmall,
                        color = MutedText,
                    )
                    Spacer(modifier = Modifier.height(4.dp))
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
                            "This build no longer receives channel or guide updates from GitHub. " +
                                "Back dismisses this message for now; it returns every launch."
                        } else {
                            "Back dismisses this message for now; it returns every launch until " +
                                "PremiumTV is updated."
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
