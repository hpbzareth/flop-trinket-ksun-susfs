# Xiaomi Trinket Kernel 4.14 (FloppyKernel-Zareth) — Revision 4

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hpbzareth/flop-trinket-ksun-susfs/build-kernel.yml?branch=main&style=for-the-badge)
![Device](https://img.shields.io/badge/Device-Xiaomi%20Trinket-orange?style=for-the-badge&logo=xiaomi)
![SoC](https://img.shields.io/badge/SoC-Qualcomm%20Snapdragon%20665%20(SM6125)-blue?style=for-the-badge&logo=qualcomm)
![Kernel](https://img.shields.io/badge/Kernel-FloppyKernel--Zareth%204.14.357-green?style=for-the-badge&logo=linux)
![Release](https://img.shields.io/badge/Release-Revision%204-red?style=for-the-badge)

Automated GitHub Actions kernel builder for **Xiaomi Trinket** devices based on [FlopKernel-Series/flop_trinket-mi_kernel](https://github.com/FlopKernel-Series/flop_trinket-mi_kernel) (branch `floppy-unity`). Compiled with **Proton Clang 13** with complete hardware drivers, battery optimizations, and comprehensive multi-root framework integration.

---

## 🚀 What's New in Revision 4 (FloppyKernel-Zareth)

- **🏷️ Official Branding & Clean Kernel String (`FloppyKernel-Zareth`):**
  - Kernel release string cleanly branded as `4.14.357-FloppyKernel-Zareth` without random dirty hash suffixes (`LOCALVERSION_AUTO=n`).
  - AnyKernel3 flash script displays `FloppyKernel-Zareth by Zareth` upon installation in recovery.
- **⚡ ZRAM LZO-RLE Compression Algorithm:**
  - Transitioned ZRAM compression engine to `lzo-rle` (`CONFIG_ZRAM_DEFAULT_COMP_ALGORITHM="lzo-rle"`).
  - Delivers ultra-low latency page compression and decompression with zero CPU bottleneck compared to ZSTD/LZ4.
  - Paired with `/proc/sys/vm/page-cluster = 0` to eliminate swap read-ahead bus latency.
- **🎮 Adreno 610 GPU Turbo (950MHz L0):**
  - Unlocked Level 0 GPU clock up to 950MHz via `kgsl-3d0/max_pwrlevel=0` and removed aggressive GPU thermal throttling limits.
- **⏱️ Frame-Perfect 300Hz Timer Frequency:**
  - `CONFIG_HZ=300`: Divides evenly into 60 FPS (5 ticks/frame) and 30 FPS (10 ticks/frame) for stutter-free UI rendering and touch responsiveness.
- **⚡ CPU Schedutil 500us Auto-Ramp:**
  - Immediate CPU frequency jump to maximum on UI touch/render tasks within 500 microseconds (`up_rate_limit_us=500`).
  - 20ms hold down (`down_rate_limit_us=20000`) to smooth out continuous UI scrolling animations.
- **💾 eMMC 5.1 Storage BFQ Multi-Queue Tuning:**
  - Default MQ I/O scheduler set to BFQ with 128KB read-ahead, `add_random=0`, and `iostats=0` to maximize foreground flash I/O throughput.
- **🌐 Network & TCP Acceleration:**
  - Google BBR TCP congestion control + Fair Queuing (FQ) pacing.
  - Enabled TCP Fast Open (client & server, `tcp_fastopen=3`) and disabled slow-start after idle (`tcp_slow_start_after_idle=0`).
- **🔋 Deep Sleep & Power Efficiency:**
  - Power-efficient workqueues enabled (`CONFIG_WQ_POWER_EFFICIENT_DEFAULT=y`) ensuring background tasks route to power-efficient LITTLE cores during sleep.
- **🛡️ Root Framework Support:**
  - **SukiSU Nova v3.0.0 (UAPI v6):** Pre-matched APK signature hash (`EXPECTED_SIZE_BAKASU 0x35c`), UAPI bumped to version 6, with full SuSFS v2.2+ stealth.
  - **KernelSU-Next UAPI v5 / v6:** Native support for KernelSU-Next managers.
  - **Official KernelSU v0.9.5 & Vanilla (APatch/FolkPatch):** Clean upstream builds.

---

## 📱 Supported Devices

| Device | Codename | SoC | Architecture | AnyKernel3 Target |
|---|---|---|---|---|
| **Redmi Note 8** | `ginkgo` | Snapdragon 665 (SM6125) | ARM64 | `ginkgo` or `mitrinket` |
| **Redmi Note 8T** | `willow` | Snapdragon 665 (SM6125) | ARM64 | `ginkgo` or `mitrinket` |
| **Xiaomi Mi A3** | `laurel_sprout` | Snapdragon 665 (SM6125) | ARM64 | `laurel_sprout` or `mitrinket` |

---

## 🛠️ How to Flash

1. Boot device into custom recovery (TWRP / OrangeFox).
2. Flash `FloppyKernel-Zareth-*.zip`.
3. Wipe Cache / Dalvik (optional).
4. Reboot to System.
