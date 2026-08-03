# Sunmi P2 Smartpad

> **Landscape** device with a hardware QWERTY keypad + D-pad (P630-class ergonomics).

## Device Summary

| Property | Value |
|---|---|
| Model | Sunmi P2 Smartpad |
| Manufacturer | SUNMI |
| Device codename | `P2_SMARTPAD` |
| Firmware | PKQ1.200813.001 release-keys |

## Display

| Property | Value |
|---|---|
| Panel resolution | 480 × 800 px (portrait-native panel) |
| **In-use orientation** | **Landscape** (rotation 3) |
| Real display (landscape) | 800 × 480 px |
| App viewport | 728 × 480 px (nav bar takes 72 px) |
| Density | 240 dpi (hdpi, 1.5×) |
| Physical DPI | 320.8 × 317.5 |
| Logical size | sw320dp · 485dp × 296dp usable landscape |
| Refresh rate | 60 Hz |

## Hardware / OS

| Property | Value |
|---|---|
| Android version | 9 (API 28) |
| CPU ABI | armeabi-v7a (32-bit ARM) |
| Chipset | Qualcomm msm8937 (Snapdragon 425) |
| RAM | ~1.93 GB (1,931,708 kB) |
| Storage (data) | ~12 GB total, ~11.5 GB free |

## Input / Keypad

`am get-config` qualifiers: `…-land-…-keysexposed-qwerty-navexposed-dpad-728x480-v28`

- **Hardware QWERTY keyboard** (`qwerty`, keys always exposed)
- **D-pad** navigation (`dpad`) — arrows + center
- Finger touchscreen
- Like the Verifone P630: physical keypad below/beside a small landscape screen

## Resource config (for layout targeting)

```
en-rGB-ldltr-sw320dp-w485dp-h296dp-normal-notlong-notround-lowdr-nowidecg-land-notnight-hdpi-finger-keysexposed-qwerty-navexposed-dpad-728x480-v28
```

## Raw captures

- `device-info.txt` — `scripts/device-info.sh` output
- `getprop.txt` — full `getprop` dump
- `am-get-config.txt` — resource config string

## TODO (artwork — the "make our own" step)

Skin still needs, mirroring `verifone/p630plus/`:
- `layout` — landscape display block + keypad button hit-boxes
- `port_back.png` / `port_fore.png` (bezel), `key.png`, `power.png`, `thumb.png`
- Map the physical QWERTY + D-pad keys to emulator key events (see `keys.sh`)
