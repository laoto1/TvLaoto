# Media3 ProGuard rules
-keep class androidx.media3.** { *; }
-dontwarn androidx.media3.**

# OkHttp ProGuard rules
-dontwarn okhttp3.**
-dontwarn okio.**
-keepnames class okhttp3.internal.publicsuffix.PublicSuffixDatabase

# Coil ProGuard rules
-keep class coil.** { *; }
-dontwarn coil.**

# Kotlin Coroutines
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}

# Compose rules
-keepclassmembers class * extends androidx.compose.runtime.State { *; }

