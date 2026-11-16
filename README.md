# Xiaomi Trinket Kernel 4.14 with KernelSU-Next & SuSFS 2.x

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hpbzareth/flop-trinket-ksun-susfs/build-kernel.yml?branch=main&style=for-the-badge)
![Device](https://img.shields.io/badge/Device-Xiaomi%20Trinket-orange?style=for-the-badge&logo=xiaomi)
![SoC](https://img.shields.io/badge/SoC-Qualcomm%20Snapdragon%20665%20(SM6125)-blue?style=for-the-badge&logo=qualcomm)
![Kernel](https://img.shields.io/badge/Kernel-4.14.357-green?style=for-the-badge&logo=linux)
![KernelSU-Next](https://img.shields.io/badge/Root-KernelSU--Next%20(v3.4.2)-red?style=for-the-badge)
![SuSFS](https://img.shields.io/badge/Stealth-SuSFS%202.x-purple?style=for-the-badge)

Automated GitHub Actions kernel builder for **Xiaomi Trinket** devices based on the active upstream [FlopKernel-Series/flop_trinket-mi_kernel](https://github.com/FlopKernel-Series/flop_trinket-mi_kernel) source with integrated **KernelSU-Next v3.4.2** (UAPI v5/v6) and **SuSFS 2.x** stealth root hiding.

---

## 📱 Supported Devices

| Model | Codename | SoC | Architecture | AnyKernel3 Target |
|---|---|---|---|---|
| **Redmi Note 8** | `ginkgo` | Snapdragon 665 (SM6125) | ARM64 | `ginkgo` / `mitrinket` |
| **Redmi Note 8T** | `willow` | Snapdragon 665 (SM6125) | ARM64 | `ginkgo` / `mitrinket` |
| **Xiaomi Mi A3** | `laurel_sprout` | Snapdragon 665 (SM6125) | ARM64 | `laurel_sprout` / `mitrinket` |
| **Unified Package** | `mitrinket` | Snapdragon 665 (SM6125) | ARM64 | Flashes dynamically based on device! |

---

## ✨ Features & Enhancements

- **KernelSU-Next v3.4.2:**
  - Modern root management solution with UAPI v5 and v6 support.
  - Native `module_blacklist` boot protection.
  - Fast-path app profile and allowlist isolation.
  - SELinux hide enhancements avoiding time-based side channels.
- **SuSFS 2.x (Non-GKI 4.14):**
  - Advanced stealth subsystem ported directly into the kernel VFS and syscall layers.
  - `CONFIG_KSU_SUSFS_SUS_PATH`: Hides sensitive file/folder paths from user apps.
  - `CONFIG_KSU_SUSFS_SUS_MOUNT`: Hides root mount entries from `/proc/self/mounts`, `mountinfo`, and `mountstat`.
  - `CONFIG_KSU_SUSFS_SUS_KSTAT`: Inode and stat spoofer to defeat sophisticated root detection apps.
  - `CONFIG_KSU_SUSFS_OPEN_REDIRECT`: Path redirection support.
  - `CONFIG_KSU_SUSFS_SUS_MEMFD`: Blocks creation of suspicious memory-backed file descriptors.
  - `CONFIG_KSU_SUSFS_SPOOF_UNAME`: Kernel release/version spoofing.
- **Direct Inline Hooking:**
  - `CONFIG_KSU_MANUAL_HOOK=y` hooked directly into the kernel filesystem and syscall entry points without relying on detectable kprobes or exposed tracepoints.
- **Optimized Toolchain:**
  - Default compilation with **Proton Clang 13** (`kdrag0n/proton-clang`) tuned for Qualcomm MSM/SM platforms, with support for AOSP Clang and ZyC Clang.
- **AnyKernel3 Flashable ZIP:**
  - Packaged with automatic device identification, boot partition flashing, and DTBO image flashing for seamless installation via recovery.

---

## 🚀 How to Build via GitHub Actions

1. Open this repository on GitHub.
2. Navigate to the **Actions** tab.
3. In the left sidebar, click on **Build Xiaomi Trinket Kernel with KernelSU-Next & SuSFS**.
4. Click the **Run workflow** dropdown button.
5. Configure your desired options:
   - **Target Device:**
     - `mitrinket` *(Recommended)*: Unified flashable zip supporting Redmi Note 8, 8T, and Mi A3.
     - `ginkgo`: Dedicated build for Redmi Note 8/8T.
     - `laurel_sprout`: Dedicated build for Xiaomi Mi A3.
     - `all`: Builds both ginkgo and laurel_sprout.
   - **SU / Root Variant:**
     - `k` *(Default)*: KernelSU-Next 3.4.2 + SuSFS 2.x.
     - `s`: BakaSU / SukiSU.
     - `x`: XXKSU.
     - `vanilla`: Clean stock build without root modifications.
   - **Toolchain:**
     - `proton` *(Recommended)*: Proton Clang 13.
     - `aosp`: Latest AOSP Clang with GCC 4.9 binutils.
     - `zyc`: ZyC Clang release.
   - **Publish GitHub Release:** Checked by default to automatically publish a tagged release with download links.
6. Click **Run workflow**. The build takes ~8 to 15 minutes to compile and package.

---

## ⚡ Flashing Instructions

1. Download the generated `Floppy_v2.0b-*.zip` from the **Releases** section or **Workflow Artifacts**.
2. Reboot your device into **TWRP** or **OrangeFox Recovery**.
3. *(Optional but recommended)* Perform a backup of your `Boot` and `DTBO` partitions.
4. Select `Install` and flash the downloaded `.zip` file.
5. Reboot to System.
6. Install the [KernelSU-Next Manager APK](https://github.com/KernelSU-Next/KernelSU-Next/releases) to configure root access and modules.

---

## 🤝 Credits & Acknowledgements

- [FlopKernel-Series](https://github.com/FlopKernel-Series/flop_trinket-mi_kernel) for the FloppyKernel source and unified trinket tree.
- [KernelSU-Next Team](https://github.com/KernelSU-Next/KernelSU-Next) & [pershoot](https://github.com/pershoot/KernelSU-Next) for the KernelSU-Next framework.
- [simonpunk](https://gitlab.com/simonpunk/susfs4ksu) for SuSFS (SuperUser FileSystem).
- [osm0sis](https://github.com/osm0sis/AnyKernel3) for AnyKernel3.
- [kdrag0n](https://github.com/kdrag0n) for Proton Clang.
