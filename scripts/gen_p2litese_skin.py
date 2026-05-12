#!/usr/bin/env python3
"""Generate Sunmi P2 Lite SE AVD skin images.

Physical device: 148.5 × 72.5 × 15.6 mm, 720x1280 screen at 294dpi.
Buttons: power (right), 2 orange scan triggers (left + right sides).
Large chin below screen for NFC/chip reader.
"""

from PIL import Image, ImageDraw, ImageFont
import os

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIN_DIR = os.path.join(SCRIPT_DIR, "skins", "sunmi", "p2litese")

# --- Dimensions (1:1 with device pixels) ---
SCREEN_W = 720
SCREEN_H = 1280

# Device body proportions derived from physical measurements:
# Body: 148.5 x 72.5mm, Screen: ~108.8 x 61.2mm
# Scale factor: 720px / 61.2mm ≈ 11.76 px/mm
# Body width: 72.5 * 11.76 ≈ 853px -> use 852 for even number
# Top bezel: ~10mm * 11.76 ≈ 118px
# Bottom chin: ~28mm * 11.76 ≈ 329px
# Side bezels: ~5.6mm * 11.76 ≈ 66px

BEZEL_TOP = 40
BEZEL_SIDE = 16
BEZEL_BOTTOM = 120  # chin for NFC/branding
CORNER_RADIUS = 24

DEVICE_W = SCREEN_W + 2 * BEZEL_SIDE  # 852
DEVICE_H = BEZEL_TOP + SCREEN_H + BEZEL_BOTTOM  # 1727

# Colors
BODY_COLOR = (25, 25, 28)        # Sunmi dark black
BODY_EDGE = (40, 40, 45)
SCREEN_BG = (10, 10, 12)
CHIN_ACCENT = (30, 30, 34)       # slightly lighter chin area
ORANGE = (235, 140, 40)          # Sunmi orange for scan buttons
ORANGE_DARK = (200, 115, 30)
HIGHLIGHT_COLOR = (255, 255, 255, 140)

# Button dimensions (in skin pixels)
POWER_W = 8
POWER_H = 50
SCAN_W = 8
SCAN_H = 70


def rounded_rect(draw, xy, radius, fill, outline=None):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)


def generate_background():
    img = Image.new("RGBA", (DEVICE_W, DEVICE_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Device body
    rounded_rect(draw, (0, 0, DEVICE_W - 1, DEVICE_H - 1), CORNER_RADIUS, BODY_COLOR, outline=BODY_EDGE)

    # Screen cutout
    sx = BEZEL_SIDE
    sy = BEZEL_TOP
    rounded_rect(draw, (sx - 2, sy - 2, sx + SCREEN_W + 1, sy + SCREEN_H + 1), 8, SCREEN_BG)

    # Front camera dot (top center, above screen)
    cam_x = DEVICE_W // 2
    cam_y = BEZEL_TOP // 2
    draw.ellipse((cam_x - 4, cam_y - 4, cam_x + 4, cam_y + 4), fill=(20, 20, 25), outline=(50, 50, 55))
    draw.ellipse((cam_x - 2, cam_y - 2, cam_x + 2, cam_y + 2), fill=(30, 30, 50))

    # SUNMI branding in chin area
    try:
        brand_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except Exception:
        brand_font = ImageFont.load_default()
    chin_center_y = BEZEL_TOP + SCREEN_H + BEZEL_BOTTOM // 3 - 5
    bbox = draw.textbbox((0, 0), "SUNMI", font=brand_font)
    tw = bbox[2] - bbox[0]
    draw.text((DEVICE_W // 2 - tw // 2, chin_center_y), "SUNMI", fill=(80, 80, 85), font=brand_font)

    # NFC indicator in chin (subtle contactless symbol)
    nfc_y = BEZEL_TOP + SCREEN_H + BEZEL_BOTTOM * 2 // 3
    nfc_x = DEVICE_W // 2
    for i, r in enumerate([12, 18, 24]):
        draw.arc((nfc_x - r, nfc_y - r, nfc_x + r, nfc_y + r), start=-45, end=45, fill=(55, 55, 60), width=2)

    # Power button (right side, upper area)
    power_x = DEVICE_W - 1
    power_y = BEZEL_TOP + 60
    rounded_rect(draw, (power_x - POWER_W + 1, power_y, power_x + 1, power_y + POWER_H), 4, (55, 55, 60))

    # Right scan button (orange, right side, mid-height)
    rscan_x = DEVICE_W - 1
    rscan_y = BEZEL_TOP + SCREEN_H // 2 - SCAN_H // 2
    rounded_rect(draw, (rscan_x - SCAN_W + 1, rscan_y, rscan_x + 1, rscan_y + SCAN_H), 4, ORANGE, outline=ORANGE_DARK)

    # Left scan button (orange, left side, mid-height)
    lscan_x = 0
    lscan_y = BEZEL_TOP + SCREEN_H // 2 - SCAN_H // 2
    rounded_rect(draw, (lscan_x - 1, lscan_y, lscan_x + SCAN_W, lscan_y + SCAN_H), 4, ORANGE, outline=ORANGE_DARK)

    # USB-C port indicator at bottom
    usb_w = 20
    usb_h = 5
    usb_x = DEVICE_W // 2 - usb_w // 2
    usb_y = DEVICE_H - 3
    rounded_rect(draw, (usb_x, usb_y, usb_x + usb_w, usb_y + usb_h), 3, (50, 50, 55))

    return img


def generate_foreground():
    img = Image.new("RGBA", (DEVICE_W, DEVICE_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i in range(40):
        alpha = int(12 * (1 - i / 40))
        draw.line([(CORNER_RADIUS, i), (DEVICE_W - CORNER_RADIUS, i)], fill=(255, 255, 255, alpha))
    return img


def generate_button_highlight(w, h):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=4, fill=HIGHLIGHT_COLOR)
    return img


def compute_button_positions():
    buttons = {}
    # Power: right side, upper area
    buttons["power"] = (DEVICE_W - POWER_W, BEZEL_TOP + 60, POWER_W, POWER_H)
    # Right scan trigger -> map to camera (common for barcode scan)
    rscan_y = BEZEL_TOP + SCREEN_H // 2 - SCAN_H // 2
    buttons["camera"] = (DEVICE_W - SCAN_W, rscan_y, SCAN_W, SCAN_H)
    # Left scan trigger -> map to search (secondary function key)
    lscan_y = BEZEL_TOP + SCREEN_H // 2 - SCAN_H // 2
    buttons["search"] = (0, lscan_y, SCAN_W, SCAN_H)
    return buttons


def main():
    os.makedirs(SKIN_DIR, exist_ok=True)

    bg = generate_background()
    bg.save(os.path.join(SKIN_DIR, "port_back.png"))

    fg = generate_foreground()
    fg.save(os.path.join(SKIN_DIR, "port_fore.png"))

    # Button highlights
    power_hl = generate_button_highlight(POWER_W, POWER_H)
    power_hl.save(os.path.join(SKIN_DIR, "power.png"))

    scan_hl = generate_button_highlight(SCAN_W, SCAN_H)
    scan_hl.save(os.path.join(SKIN_DIR, "scan.png"))

    thumb = bg.copy()
    thumb.thumbnail((200, 400))
    thumb.save(os.path.join(SKIN_DIR, "thumb.png"))

    print(f"Device: {DEVICE_W} x {DEVICE_H}")
    print(f"Screen at: ({BEZEL_SIDE}, {BEZEL_TOP})")
    print(f"Screen size: {SCREEN_W} x {SCREEN_H}")
    print()
    buttons = compute_button_positions()
    for name, (x, y, w, h) in buttons.items():
        print(f"  {name}: x={x} y={y} ({w}x{h})")


if __name__ == "__main__":
    main()
