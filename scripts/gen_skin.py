#!/usr/bin/env python3
"""Generate Verifone P630 Plus AVD skin images.

Physical device: 170.26mm x 76.58mm, 320x480 screen at 160dpi.
Keypad: 3x5 grid (1-9, *, 0, #, Cancel, Clear, Enter).
"""

from PIL import Image, ImageDraw, ImageFont
import os

SKIN_DIR = os.path.expanduser("~/Library/Android/sdk/skins/verifone_p630plus")

# --- Dimensions (pixels in skin coordinate space) ---
# Scale: real device is 76.58mm wide. Screen is 320px at ~166dpi ≈ 48.9mm.
# We'll use 2x scale for the skin so it looks decent on screen.
# Screen = 320x480 at 2x = 640x960 in skin pixels.
# But to keep it manageable let's use 1.5x: screen area = 480x720 skin px.

SCALE = 1.0
SCREEN_W = int(320 * SCALE)  # 320
SCREEN_H = int(480 * SCALE)  # 480

# Device frame dimensions
BEZEL_TOP = 40
BEZEL_SIDE = 28
BEZEL_MID = 14  # gap between screen and keypad
KEY_ROWS = 5
KEY_COLS = 3
KEY_W = 60
KEY_H = 40
KEY_GAP_X = 12
KEY_GAP_Y = 8
KEYPAD_MARGIN_SIDE = 28
BEZEL_BOTTOM = 28
CORNER_RADIUS = 16

# Keypad area dimensions
KEYPAD_W = KEY_COLS * KEY_W + (KEY_COLS - 1) * KEY_GAP_X
KEYPAD_H = KEY_ROWS * KEY_H + (KEY_ROWS - 1) * KEY_GAP_Y
KEYPAD_X = (SCREEN_W + 2 * BEZEL_SIDE - KEYPAD_W) // 2
KEYPAD_Y = BEZEL_TOP + SCREEN_H + BEZEL_MID

# Total device dimensions
DEVICE_W = SCREEN_W + 2 * BEZEL_SIDE  # 560
DEVICE_H = BEZEL_TOP + SCREEN_H + BEZEL_MID + KEYPAD_H + BEZEL_BOTTOM

# Colors
BODY_COLOR = (45, 45, 50)       # dark charcoal body
BODY_EDGE = (35, 35, 40)
SCREEN_BG = (15, 15, 18)        # screen bezel (black)
KEY_COLOR = (60, 60, 65)        # default key
KEY_BORDER = (80, 80, 85)
CANCEL_COLOR = (180, 50, 50)    # red cancel
CLEAR_COLOR = (200, 170, 50)    # yellow clear
ENTER_COLOR = (50, 160, 70)     # green enter
KEY_TEXT = (220, 220, 220)
KEY_SUBTEXT = (160, 160, 160)
HIGHLIGHT_COLOR = (255, 255, 255, 80)  # button press overlay

# Key labels: row by row, top to bottom
KEY_LABELS = [
    [("1", ""), ("2", "ABC"), ("3", "DEF")],
    [("4", "GHI"), ("5", "JKL"), ("6", "MNO")],
    [("7", "PQRS"), ("8", "TUV"), ("9", "WXYZ")],
    [("*", ""), ("0", "+"), ("#", "")],
    [("CANCEL", "cancel"), ("CLEAR", "clear"), ("ENTER", "enter")],
]

# Color overrides for bottom row
BOTTOM_ROW_COLORS = [CANCEL_COLOR, CLEAR_COLOR, ENTER_COLOR]


def rounded_rect(draw, xy, radius, fill, outline=None):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)


def draw_key(draw, x, y, w, h, label, sublabel, color, text_color):
    rounded_rect(draw, (x, y, x + w, y + h), 6, color, outline=KEY_BORDER)
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 8)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    if sublabel in ("cancel", "clear", "enter"):
        try:
            font_fn = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 10)
        except Exception:
            font_fn = font_large
        bbox = draw.textbbox((0, 0), label, font=font_fn)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x + (w - tw) // 2, y + (h - th) // 2 - 1), label, fill=(255, 255, 255), font=font_fn)
    else:
        bbox = draw.textbbox((0, 0), label, font=font_large)
        tw = bbox[2] - bbox[0]
        if sublabel:
            draw.text((x + (w - tw) // 2, y + 5), label, fill=text_color, font=font_large)
            bbox2 = draw.textbbox((0, 0), sublabel, font=font_small)
            tw2 = bbox2[2] - bbox2[0]
            draw.text((x + (w - tw2) // 2, y + h - 14), sublabel, fill=KEY_SUBTEXT, font=font_small)
        else:
            th = bbox[3] - bbox[1]
            draw.text((x + (w - tw) // 2, y + (h - th) // 2 - 1), label, fill=text_color, font=font_large)


def generate_background():
    img = Image.new("RGBA", (DEVICE_W, DEVICE_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Device body
    rounded_rect(draw, (0, 0, DEVICE_W - 1, DEVICE_H - 1), CORNER_RADIUS, BODY_COLOR, outline=BODY_EDGE)

    # Screen cutout (dark)
    sx = BEZEL_SIDE
    sy = BEZEL_TOP
    rounded_rect(draw, (sx - 3, sy - 3, sx + SCREEN_W + 2, sy + SCREEN_H + 2), 4, SCREEN_BG)

    # Verifone branding above screen
    try:
        brand_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except Exception:
        brand_font = ImageFont.load_default()
    draw.text((DEVICE_W // 2 - 22, 14), "verifone", fill=(130, 130, 135), font=brand_font)

    # Draw keypad
    for row_idx, row in enumerate(KEY_LABELS):
        for col_idx, (label, sublabel) in enumerate(row):
            kx = KEYPAD_X + col_idx * (KEY_W + KEY_GAP_X)
            ky = KEYPAD_Y + row_idx * (KEY_H + KEY_GAP_Y)
            if row_idx == 4:
                color = BOTTOM_ROW_COLORS[col_idx]
            else:
                color = KEY_COLOR
            draw_key(draw, kx, ky, KEY_W, KEY_H, label, sublabel, color, KEY_TEXT)

    # Power button on left side
    pw = 5
    ph = 22
    px = -1
    py = BEZEL_TOP + 50
    rounded_rect(draw, (px, py, px + pw, py + ph), 3, (70, 70, 75))

    return img


def generate_foreground():
    """Subtle gloss overlay."""
    img = Image.new("RGBA", (DEVICE_W, DEVICE_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Slight highlight at top
    for i in range(30):
        alpha = int(15 * (1 - i / 30))
        draw.line([(CORNER_RADIUS, i), (DEVICE_W - CORNER_RADIUS, i)], fill=(255, 255, 255, alpha))
    return img


def generate_button_highlight(w, h, color=HIGHLIGHT_COLOR):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rounded_rect(draw, (0, 0, w - 1, h - 1), 6, color)
    return img


def generate_power_highlight():
    img = Image.new("RGBA", (5, 22), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, 4, 21), radius=3, fill=(255, 255, 255, 100))
    return img


def compute_button_positions():
    """Return dict of button_name -> (x, y) in skin coordinates."""
    buttons = {}
    # Number keys
    num_labels = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["star", "0", "pound"],
    ]
    for row_idx, row in enumerate(num_labels):
        for col_idx, name in enumerate(row):
            kx = KEYPAD_X + col_idx * (KEY_W + KEY_GAP_X)
            ky = KEYPAD_Y + row_idx * (KEY_H + KEY_GAP_Y)
            buttons[name] = (kx, ky)

    # Function keys (bottom row, row_idx=4)
    fn_names = ["phone-hangup", "del", "dpad-center"]  # Cancel=hangup, Clear=del, Enter=dpad-center
    for col_idx, name in enumerate(fn_names):
        kx = KEYPAD_X + col_idx * (KEY_W + KEY_GAP_X)
        ky = KEYPAD_Y + 4 * (KEY_H + KEY_GAP_Y)
        buttons[name] = (kx, ky)

    # Power button
    buttons["power"] = (-1, BEZEL_TOP + 50)

    return buttons


def main():
    os.makedirs(SKIN_DIR, exist_ok=True)

    # Background
    bg = generate_background()
    bg.save(os.path.join(SKIN_DIR, "port_back.png"))

    # Foreground
    fg = generate_foreground()
    fg.save(os.path.join(SKIN_DIR, "port_fore.png"))

    # Key highlight
    key_hl = generate_button_highlight(KEY_W, KEY_H)
    key_hl.save(os.path.join(SKIN_DIR, "key.png"))

    # Power highlight
    power_hl = generate_power_highlight()
    power_hl.save(os.path.join(SKIN_DIR, "power.png"))

    # Thumbnail (scaled down)
    thumb = bg.copy()
    thumb.thumbnail((200, 400))
    thumb.save(os.path.join(SKIN_DIR, "thumb.png"))

    # Print dimensions for layout file
    print(f"Device: {DEVICE_W} x {DEVICE_H}")
    print(f"Screen at: ({BEZEL_SIDE}, {BEZEL_TOP})")
    print(f"Screen size: {SCREEN_W} x {SCREEN_H}")
    print()
    buttons = compute_button_positions()
    for name, (x, y) in buttons.items():
        print(f"  {name}: x={x} y={y}")


if __name__ == "__main__":
    main()
