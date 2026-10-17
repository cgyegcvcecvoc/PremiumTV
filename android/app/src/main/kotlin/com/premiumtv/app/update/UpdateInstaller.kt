package com.premiumtv.app.update

import android.app.Application
import android.content.ActivityNotFoundException
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.core.content.FileProvider
import com.premiumtv.app.BuildConfig
import java.io.File

/**
 * Hands a verified APK to Android's own package installer.
 *
 * PremiumTV never installs anything silently: the user sees Android's normal
 * "Update app?" confirmation.  On Android 8 and newer the first attempt may
 * open the system screen that grants this app permission to install packages;
 * the same Install button works directly afterwards.
 */
object UpdateInstaller {

    fun install(app: Application, apk: File): String? {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O &&
            !app.packageManager.canRequestPackageInstalls()
        ) {
            return try {
                val settings = Intent(
                    Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                    Uri.parse("package:${app.packageName}"),
                ).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                app.startActivity(settings)
                "Allow PremiumTV to install unknown apps, then press Install update again."
            } catch (e: ActivityNotFoundException) {
                "Android requires permission to install updates, but its settings screen " +
                    "could not be opened: ${e.javaClass.simpleName}"
            }
        }

        val uri = try {
            FileProvider.getUriForFile(
                app,
                "${BuildConfig.APPLICATION_ID}.updates",
                apk,
            )
        } catch (e: Exception) {
            return "The downloaded update could not be opened: ${e.message ?: e.javaClass.simpleName}"
        }

        val intent = Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(uri, "application/vnd.android.package-archive")
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        return try {
            app.startActivity(intent)
            null
        } catch (e: ActivityNotFoundException) {
            "Android has no package installer available to open the update."
        } catch (e: SecurityException) {
            "Android refused to open the update: ${e.message ?: "permission denied"}"
        }
    }
}
