# R8 is disabled for the 1.0.0 beta; these rules are kept so enabling
# isMinifyEnabled later does not immediately strip anything Media3 reflects on.
-keep class androidx.media3.** { *; }
-dontwarn androidx.media3.**
-keepclassmembers class androidx.media3.exoplayer.hls.** { *; }
