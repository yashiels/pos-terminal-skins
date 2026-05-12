#!/usr/bin/env bash
set -euo pipefail

# Launch a POS terminal emulator with the HiDPI skin button fix
# Usage: ./launch.sh <avd_name> [extra emulator flags...]
#
# Examples:
#   ./launch.sh verifone_p630plus
#   ./launch.sh sunmi_p2litese -no-audio

SDK_DIR="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-$HOME/Library/Android/sdk}}"
EMULATOR="$SDK_DIR/emulator/emulator"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <avd_name> [extra emulator flags...]"
  echo ""
  echo "Available AVDs:"
  "$SDK_DIR/cmdline-tools/latest/bin/avdmanager" list avd 2>/dev/null | grep "Name:" | sed 's/.*Name: /  /'
  exit 1
fi

AVD_NAME="$1"; shift

# Disable Qt HiDPI scaling — fixes skin button click detection on Retina/HiDPI displays
# See: https://issuetracker.google.com/issues/244063011
export QT_ENABLE_HIGHDPI_SCALING=0
export QT_AUTO_SCREEN_SCALE_FACTOR=0

exec "$EMULATOR" -avd "$AVD_NAME" -no-snapshot-load "$@"
