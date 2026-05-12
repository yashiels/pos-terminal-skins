#!/usr/bin/env bash
set -euo pipefail

# Install a POS terminal skin and create its AVD
# Usage: ./install.sh <brand/model> [--system-image <image>]
#
# Examples:
#   ./install.sh verifone/p630plus
#   ./install.sh sunmi/p2 --system-image "system-images;android-30;default;arm64-v8a"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SDK_DIR="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-$HOME/Library/Android/sdk}}"
AVDMANAGER="$SDK_DIR/cmdline-tools/latest/bin/avdmanager"

SKIN_PATH=""
SYSTEM_IMAGE=""

usage() {
  echo "Usage: $0 <brand/model> [--system-image <image>]"
  echo ""
  echo "Available skins:"
  find "$SCRIPT_DIR/skins" -name "layout" -exec dirname {} \; | while read -r d; do
    rel="${d#$SCRIPT_DIR/skins/}"
    hw="$d/hardware.ini"
    if [[ -f "$hw" ]]; then
      res=$(grep -E "hw.lcd.width|hw.lcd.height" "$hw" | awk -F= '{printf $2}' | tr -d ' ' | sed 'N;s/\n/x/')
      echo "  $rel  (${res})"
    else
      echo "  $rel"
    fi
  done
  exit 1
}

[[ $# -lt 1 ]] && usage
SKIN_PATH="$1"; shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --system-image) SYSTEM_IMAGE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

SKIN_DIR="$SCRIPT_DIR/skins/$SKIN_PATH"
if [[ ! -f "$SKIN_DIR/layout" ]]; then
  echo "Error: Skin not found at $SKIN_DIR"
  usage
fi

# Read device specs from hardware.ini
HW_FILE="$SKIN_DIR/hardware.ini"
LCD_W=$(grep "hw.lcd.width" "$HW_FILE" | cut -d= -f2)
LCD_H=$(grep "hw.lcd.height" "$HW_FILE" | cut -d= -f2)
LCD_D=$(grep "hw.lcd.density" "$HW_FILE" | cut -d= -f2)
RAM=$(grep "hw.ramSize" "$HW_FILE" | cut -d= -f2)
DISPLAY_NAME=$(grep "avd.ini.displayname" "$HW_FILE" | cut -d= -f2)
TARGET_API=$(grep "target.api" "$HW_FILE" | cut -d= -f2)

# Derive AVD name from path: verifone/p630plus -> verifone_p630plus
AVD_NAME=$(echo "$SKIN_PATH" | tr '/' '_')
SDK_SKIN_NAME="$AVD_NAME"
SDK_SKIN_DIR="$SDK_DIR/skins/$SDK_SKIN_NAME"

echo "=== POS Terminal Skin Installer ==="
echo "Device: $SKIN_PATH"
echo "Screen: ${LCD_W}x${LCD_H} @ ${LCD_D}dpi"
echo "RAM:    ${RAM}MB"
echo "AVD:    $AVD_NAME"
echo ""

# Step 1: Copy skin to SDK
echo "[1/3] Installing skin to SDK..."
rm -rf "$SDK_SKIN_DIR"
cp -r "$SKIN_DIR" "$SDK_SKIN_DIR"
echo "  -> $SDK_SKIN_DIR"

# Step 2: Find or use system image
if [[ -z "$SYSTEM_IMAGE" ]]; then
  # Auto-detect: prefer device's target API, fall back to others
  TARGET="android-${TARGET_API:-33}"
  for api in $TARGET android-33 android-34 android-35 android-30 android-36; do
    for tag in default google_apis; do
      for abi in arm64-v8a x86_64; do
        candidate="system-images;${api};${tag};${abi}"
        img_dir="$SDK_DIR/system-images/${api}/${tag}/${abi}"
        if [[ -d "$img_dir" ]]; then
          SYSTEM_IMAGE="$candidate"
          break 3
        fi
      done
    done
  done
fi

if [[ -z "$SYSTEM_IMAGE" ]]; then
  echo "Error: No system image found. Install one with:"
  echo "  sdkmanager \"system-images;android-33;default;arm64-v8a\""
  exit 1
fi

echo "[2/3] Using system image: $SYSTEM_IMAGE"

# Step 3: Create AVD
echo "[3/3] Creating AVD..."
echo "no" | "$AVDMANAGER" create avd \
  --name "$AVD_NAME" \
  --package "$SYSTEM_IMAGE" \
  --device "pixel" \
  --skin "$SDK_SKIN_NAME" \
  --force 2>&1 | grep -v "^$"

# Step 4: Patch config.ini with device-accurate values
AVD_DIR="$HOME/.android/avd/${AVD_NAME}.avd"
CONFIG="$AVD_DIR/config.ini"

if [[ -f "$CONFIG" ]]; then
  echo ""
  echo "Patching AVD config..."

  # Set display name
  if [[ -n "$DISPLAY_NAME" ]]; then
    if grep -q "avd.ini.displayname" "$CONFIG" 2>/dev/null; then
      sed -i '' "s|avd.ini.displayname=.*|avd.ini.displayname=$DISPLAY_NAME|" "$CONFIG"
    else
      echo "avd.ini.displayname=$DISPLAY_NAME" >> "$CONFIG"
    fi
  fi

  sed -i '' "s|hw.lcd.width=.*|hw.lcd.width=$LCD_W|" "$CONFIG"
  sed -i '' "s|hw.lcd.height=.*|hw.lcd.height=$LCD_H|" "$CONFIG"
  sed -i '' "s|hw.lcd.density=.*|hw.lcd.density=$LCD_D|" "$CONFIG"
  sed -i '' "s|hw.ramSize=.*|hw.ramSize=$RAM|" "$CONFIG"
  sed -i '' "s|hw.keyboard=.*|hw.keyboard=yes|" "$CONFIG"
  sed -i '' "s|hw.keyboard.lid=.*|hw.keyboard.lid=no|" "$CONFIG"
  sed -i '' "s|hw.mainKeys=.*|hw.mainKeys=no|" "$CONFIG"
  sed -i '' "s|hw.dPad=.*|hw.dPad=yes|" "$CONFIG"
  sed -i '' "s|hw.screen=.*|hw.screen=multi-touch|" "$CONFIG"
  sed -i '' "s|hw.gpu.enabled=.*|hw.gpu.enabled=yes|" "$CONFIG"
  sed -i '' "s|hw.camera.back=.*|hw.camera.back=none|" "$CONFIG"
  sed -i '' "s|hw.accelerometer=.*|hw.accelerometer=no|" "$CONFIG"
  sed -i '' "s|hw.gps=.*|hw.gps=no|" "$CONFIG"
  sed -i '' "s|hw.gyroscope=.*|hw.gyroscope=no|" "$CONFIG"
  sed -i '' "s|hw.sensors.orientation=.*|hw.sensors.orientation=no|" "$CONFIG"

  # Also patch hardware-qemu.ini if it exists
  HWQEMU="$AVD_DIR/hardware-qemu.ini"
  if [[ -f "$HWQEMU" ]]; then
    sed -i '' "s|hw.mainKeys = true|hw.mainKeys = false|" "$HWQEMU"
  fi

  # Remove stale snapshots
  rm -rf "$AVD_DIR/snapshots/default_boot" 2>/dev/null
fi

echo ""
echo "Done! Launch with:"
echo "  ./launch.sh $AVD_NAME"
