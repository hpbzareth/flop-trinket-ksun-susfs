#!/system/bin/sh
# FloppyKernel-Zareth Revision 5 Auto-Perf & Max Internet Service

# 1. ZRAM LZO-RLE Runtime Enforcement & Memory Tuning
if [ -e /sys/block/zram0/comp_algorithm ]; then
  echo "lzo-rle" > /sys/block/zram0/comp_algorithm 2>/dev/null
fi
echo 0 > /proc/sys/vm/page-cluster 2>/dev/null
echo 100 > /proc/sys/vm/swappiness 2>/dev/null

# 2. GPU Adreno 610 Max Power & Turbo 950MHz (keep default 320MHz idle floor)
echo 0 > /sys/class/kgsl/kgsl-3d0/max_pwrlevel 2>/dev/null
echo 0 > /sys/class/kgsl/kgsl-3d0/throttling 2>/dev/null

# 3. CPU Auto-Perf Schedutil Ramp-Up
for pol in /sys/devices/system/cpu/cpufreq/policy*; do
  echo 500 > "$pol/schedutil/up_rate_limit_us" 2>/dev/null
  echo 20000 > "$pol/schedutil/down_rate_limit_us" 2>/dev/null
done

# 4. Storage & eMMC 5.1 Optimization (BFQ + 128KB Read-ahead)
for blk in /sys/block/mmcblk*; do
  echo bfq > "$blk/queue/scheduler" 2>/dev/null
  echo 128 > "$blk/queue/read_ahead_kb" 2>/dev/null
  echo 0 > "$blk/queue/add_random" 2>/dev/null
  echo 0 > "$blk/queue/iostats" 2>/dev/null
  echo 0 > "$blk/queue/rotational" 2>/dev/null
done

# 5. Storage & VM Memory Tuning
echo 5 > /proc/sys/vm/dirty_background_ratio 2>/dev/null
echo 15 > /proc/sys/vm/dirty_ratio 2>/dev/null
echo 100 > /proc/sys/vm/vfs_cache_pressure 2>/dev/null
echo 10 > /proc/sys/vm/stat_interval 2>/dev/null

# 6. Max Internet TCP/Socket/NAPI Stack (Google BBRv2 + FQ Pacing + RPS/RFS)
echo fq > /proc/sys/net/core/default_qdisc 2>/dev/null
echo bbr2 > /proc/sys/net/ipv4/tcp_congestion_control 2>/dev/null
echo 131072 > /proc/sys/net/ipv4/tcp_notsent_lowat 2>/dev/null
echo 0 > /proc/sys/net/ipv4/tcp_slow_start_after_idle 2>/dev/null
echo 3 > /proc/sys/net/ipv4/tcp_fastopen 2>/dev/null
echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse 2>/dev/null
echo 1 > /proc/sys/net/ipv4/tcp_mtu_probing 2>/dev/null
echo 60 > /proc/sys/net/ipv4/tcp_default_init_rwnd 2>/dev/null
echo 15 > /proc/sys/net/ipv4/tcp_fin_timeout 2>/dev/null
echo 50 > /proc/sys/net/core/busy_poll 2>/dev/null
echo 50 > /proc/sys/net/core/busy_read 2>/dev/null
echo 4194304 > /proc/sys/net/core/rmem_max 2>/dev/null
echo 4194304 > /proc/sys/net/core/wmem_max 2>/dev/null
echo "4096 131072 6291456" > /proc/sys/net/ipv4/tcp_rmem 2>/dev/null
echo "4096 65536 4194304" > /proc/sys/net/ipv4/tcp_wmem 2>/dev/null
echo 2500 > /proc/sys/net/core/netdev_max_backlog 2>/dev/null
echo 600 > /proc/sys/net/core/netdev_budget 2>/dev/null

echo 32768 > /proc/sys/net/core/rps_sock_flow_entries 2>/dev/null
for rxq in /sys/class/net/*/queues/rx-*; do
  [ -d "$rxq" ] || continue
  case "$rxq" in
    */lo/*) continue ;;
  esac
  echo ff > "$rxq/rps_cpus" 2>/dev/null
  echo 2048 > "$rxq/rps_flow_cnt" 2>/dev/null
done

# 7. Power Efficiency for Sleep / Idle
echo Y > /sys/module/workqueue/parameters/power_efficient 2>/dev/null
