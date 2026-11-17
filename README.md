# Xiaomi Trinket Kernel 4.14 (FloppyKernel Unity) — Revision 2

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hpbzareth/flop-trinket-ksun-susfs/build-kernel.yml?branch=main&style=for-the-badge)
![Device](https://img.shields.io/badge/Device-Xiaomi%20Trinket-orange?style=for-the-badge&logo=xiaomi)
![SoC](https://img.shields.io/badge/SoC-Qualcomm%20Snapdragon%20665%20(SM6125)-blue?style=for-the-badge&logo=qualcomm)
![Kernel](https://img.shields.io/badge/Kernel-Linux%204.14.357-green?style=for-the-badge&logo=linux)
![Release](https://img.shields.io/badge/Release-Revision%202-red?style=for-the-badge)

Automated GitHub Actions kernel builder for **Xiaomi Trinket** devices based on [FlopKernel-Series/flop_trinket-mi_kernel](https://github.com/FlopKernel-Series/flop_trinket-mi_kernel) (branch `floppy-unity`). Compiled with **Proton Clang 13** with complete hardware drivers, battery optimizations, and comprehensive multi-root framework integration.

---

## 🚀 What's New in Revision 2 (R2)

- **🌐 Google BBR TCP Congestion Control:**
  - Configured `CONFIG_TCP_CONG_ADVANCED=y`, `CONFIG_TCP_CONG_BBR=y`, and `CONFIG_DEFAULT_TCP_CONG="bbr"`.
  - Delivers lower network latency, faster connection ramp-up, and reduced packet jitter over Wi-Fi and 4G/LTE mobile data.
- **⚡ ZRAM ZSTD Ultra Compression:**
  - Switched default ZRAM compression algorithm from legacy `lz4` to modern `zstd` with `CONFIG_CRYPTO_ZSTD=y`.
  - Achieves 20–30% higher RAM compression ratio, keeping dozens more background apps in memory and eliminating multitasking app kills on 3GB/4GB/6GB RAM models.
- **🔋 Instant Deep Sleep (`CONFIG_SUSPEND_SKIP_SYNC=y`):**
  - Eliminates redundant filesystem sync bottlenecks upon screen-off suspend, allowing the device to enter Deep Sleep instantly without screen-off lag or idle battery drain.
- **🎨 KCAL Hardware Display Calibration:**
  - Full sysfs hardware color tuning at `/sys/devices/platform/kcal_ctrl.0` (RGB balance, saturation boost, contrast calibration).
- **⚡ Fast Charging (Sustained 18W QC 3.0):**
  - Integrated `CONFIG_FORCE_FAST_CHARGE=y` for sustained quick charging curves.
- **🛡️ Root Framework Updates:**
  - **SukiSU Ultra (Nova v3.0.0):** Pre-matched APK signature hash (`EXPECTED_SIZE_BAKASU 0x35c`), UAPI bumped to version 6, with full SuSFS v2.2+ stealth and KPM (KernelPatch Modules) support.
  - **KernelSU-Next UAPI v5:** Native rock-solid support for KernelSU-Next v3.4.2 manager.
  - **Official KernelSU v0.9.5 & Vanilla (APatch/FolkPatch):** Clean upstream builds.

---

## 📱 Supported Devices

| Device | Codename | SoC | Architecture | AnyKernel3 Target |
|---|---|---|---|---|
| **Redmi Note 8** | `ginkgo` | Snapdragon 665 (SM6125) | ARM64 | `ginkgo` or `mitrinket` |
| **Redmi Note 8T** | `willow` | Snapdragon 665 (SM6125) | ARM64 | `ginkgo` or `mitrinket` |
| **Xiaomi Mi A3** | `laurel_sprout` | Snapdragon 665 (SM6125) | ARM64 | `laurel_sprout` or `mitrinket` |
| **Unified Package** | `mitrinket` | Snapdragon 665 (SM6125) | ARM64 | Auto-detects device during recovery flash |

---

## 🌐 ROM Compatibility

### 1. MIUI & HyperOS (Android 10 → Android 14)
Fully compatible with official Xiaomi firmware and ported distributions:
- **Supported Versions:** MIUI 12, MIUI 12.5, MIUI 13, MIUI 14, and HyperOS 1.0 (ports / GSIs).
- **Init Systems:** Dual support for Xiaomi legacy init and modern `tsinit` (two-stage init).
- **Touch Panels:** Built-in auto-detection for Novatek, Focaltech, Goodix, and Synaptics panels (`CONFIG_MI_DETECT=y`).
- **Fingerprint Sensors:** Native auto-detection for both Goodix (`gf3208`, `gf3626`) and FPC (`fpc1020`) hardware.
- **Infrared Blaster:** Full compatibility with Xiaomi IR HAL (`/dev/lirc0` / `spidev`).
- **Camera & Audio:** Integrated Qualcomm MSM camera sub-driver with Xiaomi camera ISP tuning.

### 2. AOSP Custom ROMs (Android 10 → Android 17)
Flawless compatibility across all major AOSP distributions (LineageOS, PixelOS, Evolution X, crDroid, HalcyonOS, AOSP GSIs):
- **Supported Android Versions:** Android 10, 11, 12, 13, 14, 15, 16, and Android 17.
- **Bypass netbpfload on Android 14/15/16 (`uname_bpf_spoof`):**
  - Starting with Android 14, Google's `netbpfload` daemon requires Linux 4.19+ or 5.4+. Stock 4.14 kernels cause bootloops on Android 14+.
  - FloppyKernel integrates `uname_bpf_spoof=1 / 2`: when `netbpfload` queries the `uname()` syscall, the kernel spoofs version 5.4.0+, allowing clean boot and normal network functionality on Android 14, 15, and 16.

---

## 🛡️ Available Kernel Builds (Revision 2)

All AnyKernel3 flashable packages and corresponding Manager APKs are published under **[Releases (Revision 2)](https://github.com/hpbzareth/flop-trinket-ksun-susfs/releases/tag/Revision-2)**:

| Flashable ZIP Package | Root Solution | UAPI | SuSFS Stealth | Recommended Manager APK |
|---|---|:---:|:---:|---|
| `Floppy_v2.0-R2-SukiSU-uapi6-SUSFS-mitrinket-*.zip` | **SukiSU Ultra (Nova Ready)** | **v6** | ✅ v2.2.0 + KPM | `SukiSU_Nova_v3.0.0_30000-release.apk` |
| `Floppy_v2.0-R2-KSUNext-uapi5-SUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v5** | ✅ v2.2.0 | `KernelSU_Next_v3.4.2_uapi5-33355-release.apk` |
| `Floppy_v2.0-R2-KSUNext-uapi5-NoSUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v5** | ❌ None | `KernelSU_Next_v3.4.2_uapi5-33355-release.apk` |
| `Floppy_v2.0-R2-KSUNext-uapi6-NoSUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v6** | ❌ None | `KernelSU_Next_v3.4.2_uapi6-33553-release.apk` |
| `Floppy_v2.0-R2-Official-KernelSU-v0.9.5-mitrinket-*.zip` | **Official KernelSU (tiann v0.9.5)** | **v1** | ❌ None | `KernelSU_v0.9.5_11872-release.apk` / `KernelSU_v3.3.1_32680-release.apk` |
| `Floppy_v2.0-R2-Vanilla-APatch-Folkpatch-mitrinket-*.zip` | **Vanilla (APatch & FolkPatch Ready)** | — | — | Use `APatch_11282_*.apk` or `FolkPatch_115404_*.apk` |
| `Floppy_v2.0-R2-KowSU-XXKSU-mitrinket-*.zip` | **KowSU / XXKSU (Legacy)** | **v6** | Configurable | `KernelSU_v3.3.1-50_32730-release.apk` |

---

## 📦 Root Manager APKs Provided:
- **`SukiSU_Nova_v3.0.0_30000-release.apk`**: For SukiSU Ultra (supports KPM KernelPatch Modules and UAPI v6).
- **`KernelSU_Next_v3.4.2_uapi5-33355-release.apk`**: For KernelSU-Next UAPI v5 (rock-solid stability).
- **`KernelSU_Next_v3.4.2_uapi6-33553-release.apk`**: For KernelSU-Next UAPI v6.
- **`APatch_11282_e8e4651_HEAD-release-signed.apk`**: Official APatch Manager (KernelPatch).
- **`FolkPatch_115404_0f3f42ba_on_main-release.apk`**: FolkPatch Manager (modern APatch redesign).
- **`KernelSU_v0.9.5_11872-release.apk`**: For Official KernelSU v0.9.5 legacy.
- **`KernelSU_v3.3.1_32680-release.apk`**: For Official KernelSU modern.

---

## 💡 APatch & FolkPatch Installation Guide (Vanilla Build):
1. Flash `Floppy_v2.0-R2-Vanilla-APatch-Folkpatch-mitrinket-*.zip` via TWRP or OrangeFox Recovery.
2. Boot into Android and install `APatch_11282_*.apk` or `FolkPatch_115404_*.apk`.
3. Open the app, click **Install / Patch**, enter your chosen **SuperKey**, and select the boot partition or patch kernel.
4. Reboot your phone to activate root. The kernel is pre-configured with `CONFIG_KALLSYMS=y`, `CONFIG_KALLSYMS_ALL=y`, and `CONFIG_KPROBES=y`.

---

## ⚡ Flashing Instructions

1. Download your preferred `.zip` package from **[Releases](https://github.com/hpbzareth/flop-trinket-ksun-susfs/releases/tag/Revision-2)**.
2. Boot into **OrangeFox** or **TWRP Recovery**.
3. *(Recommended)* Backup your current `Boot` and `DTBO` partitions.
4. Tap **Install** → Select the downloaded FloppyKernel `.zip` → Swipe to flash.
5. Reboot to System.
6. Install the corresponding **APK Manager** to manage root access and modules.

---

## 🚀 Building via GitHub Actions (Workflow Dispatch)

1. Navigate to the **Actions** tab on this repository.
2. Select **Build Xiaomi Trinket Kernel with KernelSU-Next & SuSFS**.
3. Click **Run workflow**:
   - **Target Device:** Choose `mitrinket` (unified), `ginkgo`, or `laurel_sprout`.
   - **SU / Root Variant:** Select `sukisu_uapi6_susfs` (recommended) or `all_variants`.
   - **Toolchain:** `proton` (Proton Clang 13, recommended).
   - **Release Tag:** Defaults to `Revision-2`.
