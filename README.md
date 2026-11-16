# Xiaomi Trinket Kernel 4.14 (FloppyKernel Unity) — Revision 1

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hpbzareth/flop-trinket-ksun-susfs/build-kernel.yml?branch=main&style=for-the-badge)
![Device](https://img.shields.io/badge/Device-Xiaomi%20Trinket-orange?style=for-the-badge&logo=xiaomi)
![SoC](https://img.shields.io/badge/SoC-Qualcomm%20Snapdragon%20665%20(SM6125)-blue?style=for-the-badge&logo=qualcomm)
![Kernel](https://img.shields.io/badge/Kernel-Linux%204.14.357-green?style=for-the-badge&logo=linux)
![Release](https://img.shields.io/badge/Release-Revision%201-red?style=for-the-badge)

Automated GitHub Actions kernel builder for **Xiaomi Trinket** devices based on [FlopKernel-Series/flop_trinket-mi_kernel](https://github.com/FlopKernel-Series/flop_trinket-mi_kernel) (branch `floppy-unity`). Built with **Proton Clang 13** with full hardware drivers and multi-SU root variants.

---

## 📱 Thiết bị hỗ trợ (Supported Devices)

| Thiết bị | Mã Codename | Vi xử lý (SoC) | Kiến trúc | Target AnyKernel3 |
|---|---|---|---|---|
| **Redmi Note 8** | `ginkgo` | Snapdragon 665 (SM6125) | ARM64 | `ginkgo` hoặc `mitrinket` |
| **Redmi Note 8T** | `willow` | Snapdragon 665 (SM6125) | ARM64 | `ginkgo` hoặc `mitrinket` |
| **Xiaomi Mi A3** | `laurel_sprout` | Snapdragon 665 (SM6125) | ARM64 | `laurel_sprout` hoặc `mitrinket` |
| **Gói hợp nhất (Unified)** | `mitrinket` | Snapdragon 665 (SM6125) | ARM64 | Tự động nhận diện thiết bị khi flash qua recovery |

---

## 🌐 Khả năng tương thích ROM (ROM Compatibility)

### 1. MIUI & HyperOS (Android 10 → Android 14)
Kernel hoàn toàn tương thích và hỗ trợ đầy đủ phần cứng trên các bản ROM MIUI và HyperOS:
- **Hỗ trợ đầy đủ các phiên bản:** MIUI 12, MIUI 12.5, MIUI 13, MIUI 14 và HyperOS 1.0 (ports / GSIs).
- **Cơ chế khởi động:** Hỗ trợ đồng thời cả Xiaomi legacy init lẫn `tsinit` (two-stage init).
- **Màn hình & Cảm ứng:** Tự động nhận diện (auto-detect) các panel cảm ứng Novatek, Focaltech, Goodix và Synaptics (`CONFIG_MI_DETECT=y`).
- **Cảm biến vân tay:** Hỗ trợ tự động nhận diện cả vân tay Goodix (`gf3208`, `gf3626`) lẫn FPC (`fpc1020`).
- **Mắt hồng ngoại (IR Blaster):** Tương thích hoàn toàn với Xiaomi IR HAL (`/dev/lirc0` / `spidev`).
- **Camera & Âm thanh:** Tích hợp Qualcomm MSM camera sub-driver và Xiaomi dual/quad camera ISP bindings.

### 2. AOSP ROMs (Android 10 → Android 17)
Kernel tương thích mượt mà với tất cả các bản ROM AOSP phổ biến (LineageOS, PixelOS, Evolution X, crDroid, HalcyonOS, AOSP GSIs...):
- **Hỗ trợ phiên bản Android:** Từ Android 10, 11, 12, 13, 14, 15, 16 đến Android 17.
- **Bypass netbpfload trên Android 14/15/16 (`uname_bpf_spoof`):**
  - Từ Android 14 trở đi, Google giới thiệu daemon mạng `netbpfload` bắt buộc kernel Linux 4.19+ hoặc 5.4+. Nếu chạy kernel 4.14 gốc, `netbpfload` sẽ từ chối khởi chạy và gây bootloop hệ thống.
  - FloppyKernel kết hợp cùng AnyKernel3 đã tích hợp sẵn cơ chế spoof cmdline `uname_bpf_spoof=1 / 2`: khi `netbpfload` gọi syscall `uname()`, kernel sẽ tự động trả về version giả lập 5.4.0+, cho phép thiết bị boot và sử dụng mạng trơn tru trên Android 14, 15 và 16.

---

## 🛡️ Danh mục các bản build Root (Revision 1)

Tất cả các bản build zip và APK Manager tương ứng được đính kèm tại mục **[Releases (Revision 1)](https://github.com/hpbzareth/flop-trinket-ksun-susfs/releases/tag/Revision-1)**:

| Tên gói ZIP | Biến thể Root | UAPI | SuSFS Stealth | APK Manager tương ứng |
|---|---|:---:|:---:|---|
| `Floppy_v2.0b-KSUNext-uapi6-SUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v6** | ✅ v2.2.0 | `KernelSU_Next_v3.4.2_uapi6-33553-release.apk` |
| `Floppy_v2.0b-KSUNext-uapi6-NoSUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v6** | ❌ Không | `KernelSU_Next_v3.4.2_uapi6-33553-release.apk` |
| `Floppy_v2.0b-KSUNext-uapi5-SUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v5** | ✅ v2.2.0 | `KernelSU_Next_v3.4.2_uapi5-33355-release.apk` |
| `Floppy_v2.0b-KSUNext-uapi5-NoSUSFS-mitrinket-*.zip` | **KernelSU-Next v3.4.2** | **v5** | ❌ Không | `KernelSU_Next_v3.4.2_uapi5-33355-release.apk` |
| `Floppy_v2.0b-SukiSU-uapi5-SUSFS-mitrinket-*.zip` | **SukiSU Ultra (BakaSU)** | **v5** | ✅ v2.2.0 + KPM | `SukiSU_Nova_v3.0.0_30000-release.apk` |
| `Floppy_v2.0b-KowSU-XXKSU-mitrinket-*.zip` | **KowSU / XXKSU (Legacy)** | **v6** | Tùy chọn | `KernelSU_v3.3.1-50_32730-release.apk` |
| `Floppy_v2.0b-Official-KernelSU-v0.9.5-mitrinket-*.zip` | **Official KernelSU (tiann v0.9.5)** | **v1** | ❌ Không | `KernelSU_v0.9.5_11858-release.apk` hoặc `KernelSU_v3.3.1_32680-release.apk` |
| `Floppy_v2.0b-Vanilla-APatch-Folkpatch-mitrinket-*.zip` | **Vanilla (APatch & FolkPatch Ready)** | — | — | Dùng **APatch Manager** (`APatch_11282_*.apk`) hoặc **FolkPatch Manager** (`FolkPatch_115404_*.apk`) để patch `boot.img` |

---

### 📦 Các file APK Manager đính kèm trong Release Revision-1:
- `KernelSU_Next_v3.4.2_uapi6-33553-release.apk`: Dành cho KernelSU-Next UAPI 6.
- `KernelSU_Next_v3.4.2_uapi5-33355-release.apk`: Dành cho KernelSU-Next UAPI 5 (bản phát hành chính thức).
- `SukiSU_Nova_v3.0.0_30000-release.apk`: Dành cho SukiSU Ultra (BakaSU) có hỗ trợ KernelPatch Module (KPM).
- `KernelSU_v3.3.1-50_32730-release.apk`: Dành cho biến thể KowSU / XXKSU.
- `KernelSU_v0.9.5_11858-release.apk`: Dành cho Official KernelSU v0.9.5 legacy.
- `KernelSU_v3.3.1_32680-release.apk`: Dành cho Official KernelSU hiện đại (tiann).
- `APatch_11282_e8e4651_HEAD-release-signed.apk`: Quản lý root APatch qua KernelPatch.
- `FolkPatch_115404_0f3f42ba_on_main-release.apk`: Quản lý root FolkPatch giao diện hiện đại mới nhất.

---

### 💡 Hướng dẫn cài đặt Root APatch / FolkPatch trên bản Vanilla:
1. Flash file zip `Floppy_v2.0b-Vanilla-APatch-Folkpatch-mitrinket-*.zip` qua TWRP hoặc OrangeFox recovery.
2. Khởi động vào Android, cài đặt file `APatch_11282_*.apk` hoặc `FolkPatch_115404_*.apk`.
3. Mở ứng dụng APatch / FolkPatch, nhấn nút **Install / Patch**, nhập **SuperKey** (mật khẩu cấp quyền root cá nhân của bạn) rồi chọn boot image hoặc Patch Kernel.
4. Khởi động lại máy. Kernel hoàn toàn hỗ trợ `CONFIG_KALLSYMS=y`, `CONFIG_KALLSYMS_ALL=y` và `CONFIG_KPROBES=y` cho APatch/FolkPatch.

---

## ⚡ Hướng dẫn cài đặt (Flashing Guide)

1. Tải bản build `.zip` mong muốn từ mục **[Releases](https://github.com/hpbzareth/flop-trinket-ksun-susfs/releases/tag/Revision-1)**.
2. Khởi động điện thoại vào **OrangeFox** hoặc **TWRP Recovery**.
3. *(Khuyến nghị)* Sao lưu (Backup) phân vùng `Boot` và `DTBO` trước khi flash.
4. Chọn `Install` → chọn file zip FloppyKernel → Kéo thanh trượt để flash.
5. Khởi động lại vào hệ thống (Reboot System).
6. Cài đặt file **APK Manager** tương ứng với biến thể đã flash để quản lý quyền root và module.

---

## 🚀 Tự build qua GitHub Actions (Workflow Dispatch)

1. Vào tab **Actions** trên repository này.
2. Chọn workflow **Build Xiaomi Trinket Kernel with KernelSU-Next & SuSFS**.
3. Nhấn **Run workflow**:
   - **Target Device:** Chọn `mitrinket` (hợp nhất), `ginkgo` hoặc `laurel_sprout`.
   - **SU / Root Variant:** Chọn `all_variants` để build song song tất cả các bản cùng lúc (ma trận matrix) hoặc chọn lẻ từng bản (`ksun_uapi6_nosusfs`, `ksun_uapi5_susfs`, `ksun_uapi5_nosusfs`, `sukisu_uapi5`, `kowsu`...).
   - **Release Tag:** Mặc định là `Revision-1` (tự động đính kèm zip vào release Revision 1).
4. Nhấn **Run workflow** và chờ GitHub Actions hoàn thành.

---

## 🤝 Lời cảm ơn (Credits)

- [FlopKernel-Series](https://github.com/FlopKernel-Series/flop_trinket-mi_kernel) — Cây nguồn FloppyKernel Trinket.
- [tiann/KernelSU](https://github.com/tiann/KernelSU) — Dự án gốc KernelSU.
- [KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next) & [pershoot](https://github.com/pershoot/KernelSU-Next) — KernelSU-Next.
- [SukiSU-Nova](https://github.com/SukiSU-Nova/SukiSU-Nova) & [Baka-SU](https://github.com/Baka-SU/BakaSU) — SukiSU Ultra & KPM.
- [backslashxx](https://github.com/backslashxx/KernelSU) & [KOWX712](https://github.com/KOWX712/KernelSU) — XXKSU & KowSU.
- [bmax121/APatch](https://github.com/bmax121/APatch) — Dự án root APatch & KernelPatch.
- [LyraVoid/FolkPatch](https://github.com/LyraVoid/FolkPatch) — FolkPatch modern Root Manager.
- [simonpunk](https://gitlab.com/simonpunk/susfs4ksu) — Siêu cơ chế ẩn root SuSFS.
- [osm0sis](https://github.com/osm0sis/AnyKernel3) — AnyKernel3.
- [kdrag0n](https://github.com/kdrag0n) — Toolchain Proton Clang.
