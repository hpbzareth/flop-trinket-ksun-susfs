#!/usr/bin/env bash
set -euo pipefail

CFG="${1:?Usage: verify_zareth_config.sh <path/to/.config>}"
echo "=== Verifying Zareth Revision 5 Kernel .config ($CFG) ==="

REQUIRED=(
  'CONFIG_TCP_CONG_BBR=y'
  'CONFIG_TCP_CONG_BBR2=y'
  'CONFIG_DEFAULT_BBR2=y'
  'CONFIG_DEFAULT_TCP_CONG="bbr2"'
  'CONFIG_NET_SCH_FQ=y'
  'CONFIG_DEFAULT_FQ=y'
  'CONFIG_DEFAULT_NET_SCH="fq"'
  'CONFIG_NET_SCH_CAKE=y'
  'CONFIG_IOSCHED_BFQ=y'
  'CONFIG_BFQ_GROUP_IOSCHED=y'
  'CONFIG_DEFAULT_MQ_BFQ=y'
  'CONFIG_DEFAULT_MQ_IOSCHED="bfq"'
  'CONFIG_HZ_300=y'
  'CONFIG_HZ=300'
  'CONFIG_ZRAM=y'
  'CONFIG_ZRAM_DEFAULT_COMP_ALGORITHM="lzo-rle"'
)

FAILED=0
for sym in "${REQUIRED[@]}"; do
  if ! grep -qxF "$sym" "$CFG"; then
    echo "::error::Missing expected config symbol: $sym" >&2
    FAILED=1
  fi
done

if [ "$FAILED" -ne 0 ]; then
  echo "--- Actual Congestion / Sched / IO / HZ / ZRAM lines in $CFG ---" >&2
  grep -E 'CONFIG_(TCP_CONG|DEFAULT_BBR|DEFAULT_CUBIC|DEFAULT_TCP_CONG|NET_SCH_FQ|NET_SCH_CAKE|DEFAULT_FQ|DEFAULT_NET_SCH|IOSCHED_BFQ|BFQ_GROUP|DEFAULT_MQ|HZ|ZRAM)' "$CFG" >&2 || true
  exit 1
fi

echo "All Zareth Revision 5 .config assertions passed!"
