import java.util.Properties
import org.gradle.api.file.DuplicatesStrategy
import org.gradle.api.tasks.Copy
import org.gradle.api.tasks.testing.Test

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

// The current version is NOT written here. `VERSION` at the repository root is
// the single source of truth, and scripts/version_sync.py generates
// android/version.properties (version + the versionCode derived by
// scripts/release_version.py) from it. A release build can still override both
// with -PpremiumTvVersion=... -PpremiumTvVersionCode=..., which is what the
// Android build workflow does for a tag; a plain local build reads the
// generated properties.
//
// See scripts/release_version.py for the one shared version policy: plain
// three-part versions from 1.0.9 on; the V-patch/alias scheme is retired.
val generatedVersion = Properties().apply {
    val file = rootProject.file("version.properties")
    if (file.isFile) {
        file.inputStream().use { load(it) }
    }
}
val premiumTvVersion = providers.gradleProperty("premiumTvVersion")
    .orElse(generatedVersion.getProperty("version", "0.0.0"))
    .get()
val premiumTvVersionCode = providers.gradleProperty("premiumTvVersionCode")
    .orElse(generatedVersion.getProperty("versionCode", "0"))
    .get()
    .toInt()

// Every published APK must carry the *same* signing identity, otherwise
// Android refuses to install a newer PremiumTV over the installed one
// (INSTALL_FAILED_UPDATE_INCOMPATIBLE).  GitHub's hosted runners start with no
// debug keystore, so the old "standard debug key" was actually a brand-new
// random key on every run - which would have broken Settings -> App updates.
//
// The long-lived update key is intentionally checked in: this is a sideloaded,
// open-source TV app, and shipping the key with the build is what lets anyone
// reproduce an installable, self-updating APK.  Set the PREMIUMTV_ANDROID_*
// environment variables to use a private key instead.
val updateKeyStore = rootProject.file(
    System.getenv("PREMIUMTV_ANDROID_KEYSTORE") ?: "keystore/premiumtv-updates.p12"
)
val updateKeyStorePassword =
    System.getenv("PREMIUMTV_ANDROID_KEYSTORE_PASSWORD") ?: "premiumtv-updates"
val updateKeyAlias = System.getenv("PREMIUMTV_ANDROID_KEY_ALIAS") ?: "premiumtv-updates"
val updateKeyPassword =
    System.getenv("PREMIUMTV_ANDROID_KEY_PASSWORD") ?: updateKeyStorePassword

android {
    namespace = "com.premiumtv.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.premiumtv.app"
        minSdk = 23
        targetSdk = 34
        versionCode = premiumTvVersionCode
        versionName = premiumTvVersion
        vectorDrawables.useSupportLibrary = true
    }

    signingConfigs {
        create("updates") {
            storeFile = updateKeyStore
            storeType = "PKCS12"
            storePassword = updateKeyStorePassword
            keyAlias = updateKeyAlias
            keyPassword = updateKeyPassword
        }
    }

    buildTypes {
        debug {
            isMinifyEnabled = false
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
            // Signed with the one update key so the next release installs
            // straight over this build from Settings -> App updates.
            signingConfig = signingConfigs.getByName("updates")
        }
        release {
            // R8 is off so a stack trace from a TV device maps straight back
            // to this source tree.
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            // No release signing config: CI publishes the debug build, which
            // is signed with the pinned update key and installs as-is on a TV.
            // An unsigned release APK cannot be installed, so it is not built.
        }
    }

    compileOptions {
        isCoreLibraryDesugaringEnabled = true
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    testOptions {
        unitTests.isIncludeAndroidResources = true
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

// Robolectric 4.14.1 fetches its Android 9 (SDK 28) runtime jar with a direct
// HttpURLConnection, outside Gradle's dependency cache. On 2026-11-19 that
// fetch failed on GitHub-hosted CI and 21 repository/VOD tests aborted with
// `MavenArtifactFetcher` IOExceptions. Resolve the exact jar through Gradle,
// copy it to a local dependency directory, and tell Robolectric to read it
// there instead of making an uncontrolled network call during the test run.
fun hermeticSdkConfiguration(name: String) = configurations.create(name) {
    isCanBeResolved = true
    isCanBeConsumed = false
    isTransitive = false
}

val robolectricInstrumentedSdk28 = hermeticSdkConfiguration("robolectricInstrumentedSdk28")
val robolectricLegacySdk28 = hermeticSdkConfiguration("robolectricLegacySdk28")
val robolectricSdkDir = layout.buildDirectory.dir("robolectric")
val copyRobolectricSdk = tasks.register<Copy>("copyRobolectricSdk") {
    // LocalDependencyResolver builds the filename from the DependencyJar's
    // artifactId/version, not from whatever name Gradle's cache happens to use.
    // Give each resolved artifact exactly the name Robolectric will request.
    from(robolectricInstrumentedSdk28) {
        include("*.jar")
        rename(".*", "android-all-instrumented-9-robolectric-4913185-2-i7.jar")
    }
    from(robolectricLegacySdk28) {
        include("*.jar")
        rename(".*", "android-all-9-robolectric-4913185-2.jar")
    }
    into(robolectricSdkDir)
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
    doLast {
        robolectricSdkDir.get().asFile.listFiles().orEmpty().sortedBy { it.name }.forEach {
            println("[robolectric] ${it.name} (${it.length()} bytes)")
        }
    }
}

tasks.withType<Test>().configureEach {
    dependsOn(copyRobolectricSdk)
    systemProperty("robolectric.dependency.dir", robolectricSdkDir.get().asFile.absolutePath)
    systemProperty("robolectric.offline", "true")
    systemProperty("robolectric.usePreinstrumentedJars", "true")
    systemProperty("robolectric.logging.enabled", "true")
    testLogging {
        showStandardStreams = true
        exceptionFormat = org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL
    }
    doFirst {
        println("[robolectric] dependency.dir=${systemProperties["robolectric.dependency.dir"]}")
        robolectricSdkDir.get().asFile.listFiles().orEmpty().sortedBy { it.name }.forEach {
            println("[robolectric] ${it.absolutePath} (${it.length()} bytes)")
        }
    }
}

dependencies {
    add("robolectricInstrumentedSdk28", "org.robolectric:android-all-instrumented:9-robolectric-4913185-2-i7")
    // Also cover a run configured with robolectric.usePreinstrumentedJars=false.
    add("robolectricLegacySdk28", "org.robolectric:android-all:9-robolectric-4913185-2")
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.0.4")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.robolectric:robolectric:4.14.1")

    implementation(platform("androidx.compose:compose-bom:2024.09.03"))
    implementation("androidx.activity:activity-compose:1.9.1")
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.6")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.6")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.6")
    implementation("androidx.work:work-runtime-ktx:2.9.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")

    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.foundation:foundation")

    implementation("androidx.media3:media3-exoplayer:1.4.1")
    implementation("androidx.media3:media3-exoplayer-hls:1.4.1")
    implementation("androidx.media3:media3-exoplayer-dash:1.4.1")
    implementation("androidx.media3:media3-ui:1.4.1")
    // Bundled FFmpeg audio decoder (AC-3, E-AC-3, DTS, FLAC, ALAC, PCM, MP2/MP3/AAC)
    // auto-discovered by DefaultRenderersFactory when MediaCodec lacks broadcast codecs.
    implementation("org.jellyfin.media3:media3-ffmpeg-decoder:1.3.1+2")

    implementation("io.coil-kt:coil-compose:2.6.0")
    implementation("io.coil-kt:coil-svg:2.6.0")

    debugImplementation("androidx.compose.ui:ui-tooling")
}
