#!/usr/bin/env bash
# Send hardware key events to a POS terminal emulator via ADB
# Usage: ./keys.sh <key> [key...]
#
# Examples:
#   ./keys.sh 1 2 3 4 enter     # type PIN and confirm
#   ./keys.sh cancel             # press cancel
#   ./keys.sh clear              # press clear/backspace

ADB_TARGET="${ADB_TARGET:--e}"

send_key() {
  local key="$1"
  case "$key" in
    0) adb $ADB_TARGET shell input keyevent 7  ;;
    1) adb $ADB_TARGET shell input keyevent 8  ;;
    2) adb $ADB_TARGET shell input keyevent 9  ;;
    3) adb $ADB_TARGET shell input keyevent 10 ;;
    4) adb $ADB_TARGET shell input keyevent 11 ;;
    5) adb $ADB_TARGET shell input keyevent 12 ;;
    6) adb $ADB_TARGET shell input keyevent 13 ;;
    7) adb $ADB_TARGET shell input keyevent 14 ;;
    8) adb $ADB_TARGET shell input keyevent 15 ;;
    9) adb $ADB_TARGET shell input keyevent 16 ;;
    star|'*')    adb $ADB_TARGET shell input keyevent 17 ;;
    pound|'#')   adb $ADB_TARGET shell input keyevent 18 ;;
    enter)       adb $ADB_TARGET shell input keyevent 23 ;;
    clear|del)   adb $ADB_TARGET shell input keyevent 67 ;;
    cancel)      adb $ADB_TARGET shell input keyevent 6  ;;
    power)       adb $ADB_TARGET shell input keyevent 26 ;;
    back)        adb $ADB_TARGET shell input keyevent 4  ;;
    home)        adb $ADB_TARGET shell input keyevent 3  ;;
    recents)     adb $ADB_TARGET shell input keyevent 187 ;;
    up)          adb $ADB_TARGET shell input keyevent 19 ;;
    down)        adb $ADB_TARGET shell input keyevent 20 ;;
    left)        adb $ADB_TARGET shell input keyevent 21 ;;
    right)       adb $ADB_TARGET shell input keyevent 22 ;;
    menu)        adb $ADB_TARGET shell input keyevent 82 ;;
    f1)          adb $ADB_TARGET shell input keyevent 131 ;;
    f2)          adb $ADB_TARGET shell input keyevent 132 ;;
    f3)          adb $ADB_TARGET shell input keyevent 133 ;;
    f4)          adb $ADB_TARGET shell input keyevent 134 ;;
    *)
      echo "Unknown key: $key"
      echo ""
      echo "Numeric:  0 1 2 3 4 5 6 7 8 9"
      echo "Symbols:  star  pound"
      echo "Function: enter  clear  cancel"
      echo "Nav:      up  down  left  right  back  home  recents  menu"
      echo "System:   power"
      echo "Fn keys:  f1  f2  f3  f4"
      echo ""
      echo "Env: ADB_TARGET=-s <serial>  (default: -e for emulator)"
      return 1
      ;;
  esac
}

if [[ $# -eq 0 ]]; then
  echo "Usage: ./keys.sh <key> [key...]"
  echo ""
  echo "Numeric:  0 1 2 3 4 5 6 7 8 9"
  echo "Symbols:  star  pound"
  echo "Function: enter  clear  cancel"
  echo "Nav:      up  down  left  right  back  home  recents  menu"
  echo "System:   power"
  echo "Fn keys:  f1  f2  f3  f4"
  echo ""
  echo "Env: ADB_TARGET=-s <serial>  (default: -e for emulator)"
  exit 1
fi

for key in "$@"; do
  send_key "$key"
done
