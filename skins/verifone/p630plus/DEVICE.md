# Verifone P630 Plus

## Physical Device

| Property | Value |
|---|---|
| Manufacturer | Verifone |
| Model | P630 Plus |
| Dimensions | 170.26 × 76.58 × 31.85 mm |
| Weight | 303–310 g |

## Display

| Property | Value |
|---|---|
| Resolution | 320 × 480 px (HVGA) |
| Density | 160 dpi (mdpi) |
| Physical DPI | 165.877 × 167.013 |
| Diagonal | ~2.3" |
| Type | 3.5" capacitive touchscreen, LED backlit |
| Refresh Rate | 60 Hz |

## Software

| Property | Value |
|---|---|
| Android Version | 13 (API 33) |
| CPU ABI | armeabi-v7a (32-bit ARM) |
| Chipset | Qualcomm (bengal) |
| RAM | ~1.8 GB |
| Storage | ~22 GB |

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
