# NetMod Optimizer — Android

A native **Kotlin + Jetpack Compose (Material 3)** port of the single-file
desktop *VLESS Edge Optimizer (NetMod Edition v4)* Tkinter app.

All desktop modules, classes and functions were carried over; only the parts
that are inherently platform-specific (the TUN/Wintun connection layer and the
xray subprocess) were re-implemented using Android's native facilities.

---

## How the desktop modules map to Android

| Desktop module / class            | Android equivalent                                   | Notes |
|-----------------------------------|------------------------------------------------------|-------|
| `constants` (`_LIGHT/_DARK`)      | `core/Constants.kt` (`LightPalette`, `DarkPalette`)  | Same hex values; dark = One UI Eye Comfort |
| `crash`                           | `core/Crash.kt`                                       | Uncaught-exception dumps to `filesDir/crashes` |
| `models` (ProbeResult/Profile)    | `core/Models.kt`                                      | `@Serializable` data classes |
| `persistence`                     | `core/Persistence.kt`                                 | JSON in app `filesDir` instead of next to script |
| `scanner` (`Optimizer`)           | `scanner/Optimizer.kt`                                | asyncio → **coroutines + Semaphore**; TCP/TLS/HTTP/`cdn-cgi/trace` probes preserved |
| `tun_manager` (`TunManager`)      | `vpn/OptimizerVpnService.kt`                          | **Wintun → Android `VpnService`**; routes/gateway handled by the OS |
| `xray_manager` (`XrayManager`)    | `xray/XrayManager.kt` + `xray/XrayConfig.kt`          | subprocess → **libXray bridge**; config builders ported 1:1 |
| `_parse_vless_url` / `_vless`     | `xray/VlessParser.kt`                                 | parse + share-link build |
| `qr` (`_QR`, `show_qr`)           | `qr/QrEncoder.kt`                                     | pure-Kotlin QR → `Bitmap` (no library) |
| `bpb_deploy` (CF deploy + blobs)  | `deploy/CloudflareApi.kt`, `deploy/WorkerDeploy.kt`  | worker JS blobs in `assets/*.b64` |
| `ui_styles` / `ui_widgets`        | `ui/theme/`, `ui/components/`                         | ttk styles → Material 3 |
| `ui_app` (`App`, 165 methods)     | `ui/AppViewModel.kt` + `ui/screens/*`                 | tk tabs → Compose screens |

### The 11 desktop tabs → Compose screens
Home · Config · Scan · Test · Connect · BPB · Worker · Saved (Favorites) ·
History · Settings · About — all in `ui/screens/`.

---

## Connecting on Android (the main behavioural difference)

The desktop app installed **Wintun**, created a TUN adapter, edited the routing
table and ran `xray` as a child process. Android forbids all of that, so:

1. **`OptimizerVpnService`** (a system `VpnService`) calls `Builder.establish()`
   to obtain the tun **file descriptor** — this replaces Wintun + route setup.
   `addRoute("0.0.0.0", 0)` captures all traffic; the OS tears it down on stop.
2. The tun fd + the xray JSON config (built by `XrayConfig`) are handed to
   **xray-core through the libXray bridge** (`XrayManager.XrayBridge`), whose
   tun2socks layer forwards packets into the VLESS outbound.
3. Before the tunnel starts, Android shows the system **VPN consent dialog**
   (handled in `ConnectScreen` via `VpnService.prepare`).

> The app **compiles and runs out of the box** with a `NoopBridge` (UI, scan,
> deploy, QR all work). To enable real tunnelling, add the xray AAR and wire
> the bridge — see `xray/LibXrayBridge.kt.example`.

---

## Build

1. Open the project root in **Android Studio (Hedgehog or newer)**.
2. Let Gradle sync (it pulls Compose BOM 2024.09, Kotlin 2.0.20, AGP 8.5).
3. Run on a device/emulator with **Android 7.0 (API 24)+**.

To enable the live tunnel, follow the steps in `xray/LibXrayBridge.kt.example`.

CLI build (if you have a JDK 17 + Android SDK):
```
gradle wrapper        # generates the wrapper jar once
./gradlew assembleDebug
```

---

## Tech
- Kotlin 2.0.20, Jetpack Compose (Material 3), Coroutines, kotlinx.serialization
- minSdk 24, targetSdk 34
- No third-party networking lib — uses JDK sockets/`HttpURLConnection`, matching
  the original's zero-dependency philosophy.


---

## Changelog — parity fixes ported from desktop v4.5

These mirror the desktop `.pyw` fixes:

1. **Parallel testing** — `AppViewModel.quickTestTop()` / `testBatch()` re-probe
   configs with bounded concurrency (Semaphore, up to 64) instead of one-by-one.
   Per-IP jitter/loss stays accurate (computed across each IP's own retries);
   only the IPs are fanned out. A real bandwidth phase (sequential, winners
   first) is stubbed for when the xray engine is wired in.
2. **QR dialog** — new `components/QrDialog.kt` (`QrDialog`) renders a scannable
   QR via the pure-Kotlin `QrEncoder`. Wired into Home config rows ("QR" button).
3. **Auto-Best Connect** — `pickAutoBest()` / `connectAutoBest()` prefer
   proxy-verified (`latMs`) → tested → reachable, so the tunnel isn't brought up
   on a dead edge. Surfaced as the "⚡ Auto-Best Connect" button on Connect.
4. **Scanner real-verify (Phase 3)** — `startScan()` runs a real end-to-end
   proxy-verify of the top candidates **when the xray engine is installed**
   (skipped under NoopBridge), matching the desktop Phase 3.
5. **Developer log + Diagnostic Report** — `diagnosticReport()` /
   `shareDiagnostics()` produce a full, shareable system snapshot (device, engine
   status, profile with UUID masked, pool stats, recent log). Button on About.

### Engine auto-wiring
`OptimizerVpnService.wireBridgeIfAvailable()` now looks up
`com.netmod.optimizer.xray.LibXrayBridge` by **reflection**, so the app compiles
and runs today on `NoopBridge`, and auto-activates the real engine the instant
you add the AAR + rename `LibXrayBridge.kt.example` → `LibXrayBridge.kt`.

---

## Building & signing the APK (Android Studio)

> ✅ The xray engine is **already bundled** — `app/libs/libv2ray.aar`
> (AndroidLibXrayLite v26.6.22) is included and wired, so the live tunnel works
> out of the box. No extra setup needed; just build & sign.

1. **Open** the project root in Android Studio (Hedgehog or newer); let Gradle sync.
2. **Debug APK:** `Build → Build Bundle(s)/APK(s) → Build APK(s)` → `app/build/outputs/apk/debug/`.
3. **Signed release APK:**
   - `Build → Generate Signed Bundle / APK… → APK`.
   - Create or select a keystore (`.jks`), set key alias/passwords, pick `release`.
   - Output: `app/build/outputs/apk/release/app-release.apk` (signed & zipaligned).
   - CLI equivalent once a keystore exists:
     ```
     ./gradlew assembleRelease
     # then sign if not configured in gradle:
     apksigner sign --ks my.jks --out app-release-signed.apk \
       app/build/outputs/apk/release/app-release-unsigned.apk
     ```

### How the live tunnel works (engine notes)
- `xray/LibXrayBridge.kt` drives `libv2ray` (`Libv2ray.newCoreController` →
  `controller.startLoop(configJson, tunFd)` / `stopLoop()` / `queryStats()`).
- `OptimizerVpnService.wireBridgeIfAvailable()` installs it by reflection.
- `XrayConfig.buildTun()` emits a native xray **`tun` inbound**; `startLoop`
  exports the VpnService fd via `xray.tun.fd`, so xray reads packets straight
  from the tunnel — **no tun2socks**. The app excludes itself from the VPN
  (`addDisallowedApplication`) so the proxy's own dial-out can't loop.
- geoip/geosite ship inside the AAR (auto-loaded), so routing works offline.

