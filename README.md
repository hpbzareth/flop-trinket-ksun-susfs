# Xiaomi Trinket Kernel 4.14 (FloppyKernel Unity) — Revision 1

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hpbzareth/flop-trinket-ksun-susfs/build-kernel.yml?branch=main&style=for-the-badge)
![Device](https://img.shields.io/badge/Device-Xiaomi%20Trinket-orange?style=for-the-badge&logo=xiaomi)
![SoC](https://img.shields.io/badge/SoC-Qualcomm%20Snapdragon%20665%20(SM6125)-blue?style=for-the-badge&logo=qualcomm)
![Kernel](https://img.shields.io/badge/Kernel-Linux%204.14.357-green?style=for-the-badge&logo=linux)
![Release](https://img.shields.io/badge/Release-Revision%201-red?style=for-the-badge)

Automated GitHub Actions kernel builder for **Xiaomi Trinket** devices based on [FlopKernel-Series/flop_trinket-mi_kernel](https://github.com/FlopKernel-Series/flop_trinket-mi_kernel) (branch `floppy-unity`). Compiled with **Proton Clang 13** with complete hardware drivers, battery optimizations, and comprehensive multi-root framework integration.

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

## 🛡️ Available Kernel Builds (Revision 1)

All AnyKernel3 flashable packages and corresponding Manager APKs are published under **[Releases (Revision 1)](https://github.com/hpbzareth/flop-trinket-ksun-susfs/releases/tag/Revision-1)**:

| Flashable ZIP Package | Root Solution | UAPI | SuSFS Stealth | Recommended Manager APK |
|---|---|:---:|:---:|---|
| `Floppy_v2.0b-KSUNext-uapi6-SUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v6** | ✅ v2.2.0 | `KernelSU_Next_v3.4.2_uapi6-33553-release.apk` |
| `Floppy_v2.0b-KSUNext-uapi6-NoSUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v6** | ❌ None | `KernelSU_Next_v3.4.2_uapi6-33553-release.apk` |
| `Floppy_v2.0b-KSUNext-uapi5-SUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v5** | ✅ v2.2.0 | `KernelSU_Next_v3.4.2_uapi5-33355-release.apk` |
| `Floppy_v2.0b-KSUNext-uapi5-NoSUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v5** | ❌ None | `KernelSU_Next_v3.4.2_uapi5-33355-release.apk` |
| `Floppy_v2.0b-SukiSU-uapi5-SUSFS-mitrinket-*.zip` | **SukiSU Ultra (BakaSU)** | **v5** | ✅ v2.2.0 + KPM | `SukiSU_Nova_v3.0.0_30000-release.apk` |
| `Floppy_v2.0b-KowSU-XXKSU-mitrinket-*.zip` | **KowSU / XXKSU (Legacy)** | **v6** | Configurable | `KernelSU_v3.3.1-50_32730-release.apk` |
| `Floppy_v2.0b-Official-KernelSU-v0.9.5-mitrinket-*.zip` | **Official KernelSU (tiann v0.9.5)** | **v1** | ❌ None | `KernelSU_v0.9.5_11858-release.apk` / `KernelSU_v3.3.1_32680-release.apk` |
| `Floppy_v2.0b-Vanilla-APatch-Folkpatch-mitrinket-*.zip` | **Vanilla (APatch & FolkPatch Ready)** | — | — | Use `APatch_11282_*.apk` or `FolkPatch_115404_*.apk` |

---

### 📦 Root Manager APKs Provided:
- **`KernelSU_Next_v3.4.2_uapi6-33553-release.apk`**: For KernelSU-Next UAPI v6.
- **`KernelSU_Next_v3.4.2_uapi5-33355-release.apk`**: For KernelSU-Next UAPI v5 (stable release).
- **`SukiSU_Nova_v3.0.0_30000-release.apk`**: For SukiSU Ultra (supports KPM KernelPatch Modules).
- **`KernelSU_v3.3.1-50_32730-release.apk`**: For KowSU / XXKSU builds.
- **`KernelSU_v0.9.5_11858-release.apk`**: For Official KernelSU v0.9.5 legacy.
- **`KernelSU_v3.3.1_32680-release.apk`**: For Official KernelSU modern.
- **`APatch_11282_e8e4651_HEAD-release-signed.apk`**: Official APatch Manager (KernelPatch).
- **`FolkPatch_115404_0f3f42ba_on_main-release.apk`**: FolkPatch Manager (modern APatch redesign).

---

### 💡 APatch & FolkPatch Installation Guide (Vanilla Build):
1. Flash `Floppy_v2.0b-Vanilla-APatch-Folkpatch-mitrinket-*.zip` via TWRP or OrangeFox Recovery.
2. Boot into Android and install `APatch_11282_*.apk` or `FolkPatch_115404_*.apk`.
3. Open the app, click **Install / Patch**, enter your chosen **SuperKey**, and select the boot partition or patch kernel.
4. Reboot your phone to activate root. The kernel is pre-configured with `CONFIG_KALLSYMS=y`, `CONFIG_KALLSYMS_ALL=y`, and `CONFIG_KPROBES=y`.

---

## ⚡ Flashing Instructions

1. Download your preferred `.zip` package from **[Releases](https://github.com/hpbzareth/flop-trinket-ksun-susfs/releases/tag/Revision-1)**.
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
   - **SU / Root Variant:** Select `all_variants` to build the entire matrix concurrently, or pick a specific variant (`official_ksu`, `vanilla`, `ksun_uapi6_susfs`, etc.).
   - **Toolchain:** `proton` (Proton Clang 13, recommended).
   - **Release Tag:** Defaults to `Revision-1` (auto-attaches artifacts to the release).
4. Click **Run workflow** and monitor the build jobs.

---

## 🤝 Credits & Acknowledgements

- [FlopKernel-Series](https://github.com/FlopKernel-Series/flop_trinket-mi_kernel) — Upstream FloppyKernel source tree.
- [tiann/KernelSU](https://github.com/tiann/KernelSU) — The original KernelSU project.
- [KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next) & [pershoot](https://github.com/pershoot/KernelSU-Next) — KernelSU-Next.
- [SukiSU-Nova](https://github.com/SukiSU-Nova/SukiSU-Nova) & [Baka-SU](https://github.com/Baka-SU/BakaSU) — SukiSU Ultra & KPM.
- [backslashxx](https://github.com/backslashxx/KernelSU) & [KOWX712](https://github.com/KOWX712/KernelSU) — XXKSU & KowSU.
- [bmax121/APatch](https://github.com/bmax121/APatch) — APatch & KernelPatch root engine.
- [LyraVoid/FolkPatch](https://github.com/LyraVoid/FolkPatch) — FolkPatch modern Root Manager.
- [simonpunk](https://gitlab.com/simonpunk/susfs4ksu) — SuSFS stealth subsystem.
- [osm0sis](https://github.com/osm0sis/AnyKernel3) — AnyKernel3 flashing framework.
- [kdrag0n](https://github.com/kdrag0n) — Proton Clang toolchain.
