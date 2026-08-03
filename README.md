# POS Terminal Emulator Skins

Android emulator skins for POS (Point of Sale) payment terminals. Each skin replicates the physical device's screen dimensions, density, and hardware keypad layout for accurate testing in the Android emulator.

## Supported Devices

| Brand | Model | Screen | Density | API | Keys |
|-------|-------|--------|---------|-----|------|
| Verifone | P630 Plus | 320×480 | 160 (mdpi) | 33 (Android 13) | 15-key numpad |
| Sunmi | P2 Lite SE | 720×1280 | 294 (~xhdpi) | 30 (Android 11) | Power + 2 scan triggers |
| Sunmi | P2 Smartpad | 800×480 (landscape) | 240 (hdpi) | 28 (Android 9) | Hardware QWERTY + D-pad |

## Quick Start

```bash
# 1. Install a skin + create its AVD
./install.sh verifone/p630plus
./install.sh sunmi/p2litese

# 2. Launch the emulator (includes macOS Retina fix)
./launch.sh verifone_p630plus
./launch.sh sunmi_p2litese
```

## Requirements

- Android SDK with `cmdline-tools` and `emulator` installed
- A system image for the target API level (e.g. `system-images;android-33;default;arm64-v8a`)
- macOS (Linux/WSL not yet supported — `install.sh` uses macOS `sed` syntax)

## Repository Structure

```
pos-terminal-skins/
├── README.md
├── install.sh                        # Install skin + create AVD
├── launch.sh                         # Launch emulator with HiDPI fix
├── keys.sh                           # Send hardware key events via ADB
├── scripts/
│   ├── device-info.sh                # Capture specs from a connected device
│   ├── gen_skin.py                   # Verifone P630 Plus skin generator
│   └── gen_p2litese_skin.py          # Sunmi P2 Lite SE skin generator
└── skins/
    ├── verifone/
    │   └── p630plus/                 # Verifone P630 Plus
    │       ├── DEVICE.md
    │       ├── layout
    │       ├── hardware.ini
    │       ├── port_back.png
    │       ├── port_fore.png
    │       ├── key.png
    │       ├── power.png
    │       └── thumb.png
    └── sunmi/
        └── p2litese/                 # Sunmi P2 Lite SE
            ├── DEVICE.md
            ├── layout
            ├── hardware.ini
            ├── port_back.png
            ├── port_fore.png
            ├── power.png
            ├── scan.png
            └── thumb.png
```

## macOS Retina / HiDPI Fix

Custom skin buttons don't respond to clicks on Retina displays due to a [known emulator bug](https://issuetracker.google.com/issues/244063011) — Qt delivers mouse coordinates in logical points but the skin hit-tests in physical pixels.

**The fix:** Launch the emulator with Qt HiDPI scaling disabled:

```bash
QT_ENABLE_HIGHDPI_SCALING=0 emulator -avd <name> -no-snapshot-load
```

The `launch.sh` script does this automatically.

## Adding a New Device

1. Connect the physical device via ADB
2. Run `./scripts/device-info.sh` to capture specs
3. Create `skins/<brand>/<model>/` with skin files
4. Add a `DEVICE.md` with the device specifications
5. Test with `./install.sh <brand>/<model>` and `./launch.sh <brand>_<model>`

## Hardware Key Mapping

### Verifone P630 Plus (15-key numpad)

| Physical Key | Skin Button | KeyEvent | ADB Code |
|---|---|---|---|
| 0–9 | `0`–`9` | KEYCODE_0–9 | 7–16 |
| * | `star` | KEYCODE_STAR | 17 |
| # | `pound` | KEYCODE_POUND | 18 |
| Enter (green) | `dpad-center` | KEYCODE_DPAD_CENTER | 23 |
| Clear (yellow) | `del` | KEYCODE_DEL | 67 |
| Cancel (red) | `phone-hangup` | KEYCODE_ENDCALL | 6 |
| Power | `power` | KEYCODE_POWER | 26 |

### Sunmi P2 Lite SE (side buttons)

| Physical Key | Skin Button | KeyEvent | ADB Code |
|---|---|---|---|
| Power (right) | `power` | KEYCODE_POWER | 26 |
| Right scan trigger (orange) | `camera` | KEYCODE_CAMERA | 27 |
| Left scan trigger (orange) | `search` | KEYCODE_SEARCH | 84 |

### Sending keys via ADB

```bash
./keys.sh 1 2 3 4       # type PIN digits
./keys.sh enter          # confirm
./keys.sh cancel         # cancel
./keys.sh power          # power button
```

## License

MIT
