#!/usr/bin/env bash
set -euo pipefail

# Capture device specs from a connected ADB device for creating a new skin
# Usage: ./scripts/device-info.sh [-s <serial>]

ADB_ARGS=""
[[ "${1:-}" == "-s" ]] && ADB_ARGS="-s $2"

echo "=== POS Terminal Device Info ==="
echo ""

echo "## Identity"
echo "Model:        $(adb $ADB_ARGS shell getprop ro.product.model)"
echo "Manufacturer: $(adb $ADB_ARGS shell getprop ro.product.manufacturer)"
echo "Brand:        $(adb $ADB_ARGS shell getprop ro.product.brand)"
echo "Device:       $(adb $ADB_ARGS shell getprop ro.product.device)"
echo "Product:      $(adb $ADB_ARGS shell getprop ro.product.name)"
echo "Firmware:     $(adb $ADB_ARGS shell getprop ro.build.display.id)"
echo ""

echo "## Display"
adb $ADB_ARGS shell wm size
adb $ADB_ARGS shell wm density
echo "LCD density:  $(adb $ADB_ARGS shell getprop ro.sf.lcd_density)"
echo ""

echo "## Display Detail"
adb $ADB_ARGS shell dumpsys display 2>/dev/null | grep "DisplayDeviceInfo" | head -1
echo ""

echo "## Software"
echo "Android:      $(adb $ADB_ARGS shell getprop ro.build.version.release) (API $(adb $ADB_ARGS shell getprop ro.build.version.sdk))"
echo "CPU ABI:      $(adb $ADB_ARGS shell getprop ro.product.cpu.abi)"
echo "ABI list:     $(adb $ADB_ARGS shell getprop ro.product.cpu.abilist)"
echo "Hardware:     $(adb $ADB_ARGS shell getprop ro.hardware)"
echo "Platform:     $(adb $ADB_ARGS shell getprop ro.board.platform)"
echo ""

echo "## Memory"
adb $ADB_ARGS shell cat /proc/meminfo | head -3
echo ""

echo "## Storage"
adb $ADB_ARGS shell df /data | tail -1
echo ""

echo "## App Viewport"
adb $ADB_ARGS shell dumpsys display 2>/dev/null | grep "mOverrideDisplayInfo" | head -1
