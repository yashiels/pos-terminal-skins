# Verifone P630 Plus

## Device Summary

| Property | Value |
|---|---|
| Model | Verifone P630 Plus |
| Manufacturer | Verifone |
| Device codename | `p630plus` |
| Firmware | P630PLUS-T-6.12.2 |
| Dimensions | 170.26 × 76.58 × 31.85 mm |
| Weight | 303–310 g |

## Display

| Property | Value |
|---|---|
| Resolution | 320 x 480 px |
| Density | 160 dpi (mdpi) |
| Physical DPI | 165.877 x 167.013 |
| Refresh rate | 60 Hz |
| Screen diagonal | ~2.3" (calculated from resolution / physical DPI) |
| Density bucket | mdpi (scale factor 1.0) |
| App viewport | 320 x 432 dp (with system bars) |

## Hardware / OS

| Property | Value |
|---|---|
| Android version | 13 (API 33) |
| CPU ABI | armeabi-v7a (32-bit ARM) |
| Chipset | Qualcomm (bengal) |
| RAM | ~1.8 GB (1,846,340 kB) |
| Storage (data) | ~22 GB total, ~20.7 GB free |

## Hardware Keypad (15 keys)

```
┌─────────────────────┐
│     [ Screen ]      │
│     320 × 480       │
│                     │
├─────────────────────┤
│  [1]   [2]   [3]   │
│        ABC   DEF   │
│  [4]   [5]   [6]   │
│  GHI   JKL   MNO   │
│  [7]   [8]   [9]   │
│  PQRS  TUV   WXYZ  │
│  [*]   [0]   [#]   │
│        +            │
│ [CAN] [CLR] [ENT]  │
│  red   yel   grn   │
└─────────────────────┘
```

- **Number keys (0–9):** Standard telco layout
- **Star / Pound:** Symbol keys flanking 0
- **Cancel (red):** Left function key → maps to `phone-hangup` (KEYCODE_ENDCALL)
- **Clear (yellow):** Centre function key → maps to `del` (KEYCODE_DEL)
- **Enter (green):** Right function key → maps to `dpad-center` (KEYCODE_DPAD_CENTER)
- **Power:** Left side of device

## Other Hardware

- Smart card (EMV chip) reader at bottom
- Magnetic card reader on side
- Contactless / NFC antenna embedded
- 2 MP fixed-focus camera on bottom (QR/barcode)
- Power button on left side
