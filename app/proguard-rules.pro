# Keep Xray / Go-mobile bridge classes if you add the AAR
-keep class go.** { *; }
-keep class libv2ray.** { *; }
-keep class libXray.** { *; }
-keepclassmembers class * { @kotlinx.serialization.Serializable *; }


# AndroidLibXrayLite / gomobile bindings — never strip or rename.
-keep class libv2ray.** { *; }
-keep class go.** { *; }
-keep interface libv2ray.** { *; }
