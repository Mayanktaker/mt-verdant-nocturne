# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Render desktop UI mockups and app ecosystem showcase with captions.

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = Path(__file__).resolve().parents[2]
SCREENSHOTS = REPO_ROOT / "screenshots"
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

# System fonts
FONT_REG = "/usr/share/fonts/Adwaita/AdwaitaSans-Regular.ttf"
FONT_MONO = "/usr/share/fonts/Adwaita/AdwaitaMono-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/Adwaita/AdwaitaMono-Bold.ttf"

def get_font(path, size):
    # Safely load truetype font with fallback to default
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    # Draw rounded rectangle helper
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def generate_mockup_a():
    # Option A: Canopy Floating Glass (Colloid/WhiteSur float style)
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (15, 20, 27, 255))
    draw = ImageDraw.Draw(im)

    # Background wallpaper gradient
    for y in range(h):
        t = y / h
        r = int(11 * (1 - t) + 18 * t)
        g = int(16 * (1 - t) + 38 * t)
        b = int(22 * (1 - t) + 36 * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Ambient radial glow in center
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([(w//2 - 350, h//2 - 250), (w//2 + 350, h//2 + 250)], fill=(143, 184, 166, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    im = Image.alpha_composite(im, glow)
    draw = ImageDraw.Draw(im)

    # 1. Floating Panel (margin from top and sides)
    panel_y = 12
    panel_h = 36
    panel_margin = 120
    panel_box = [(panel_margin, panel_y), (w - panel_margin, panel_y + panel_h)]
    draw_rounded_rect(draw, panel_box, radius=18, fill=(15, 20, 27, 210), outline=(44, 62, 68, 240), width=1)

    f_ui = get_font(FONT_REG, 13)
    f_bold = get_font(FONT_BOLD, 13)
    f_mono = get_font(FONT_MONO, 12)

    # Panel items
    draw.text((panel_margin + 20, panel_y + 10), "Activities", fill=(233, 241, 236), font=f_ui)
    draw.text((w // 2 - 45, panel_y + 10), "Oct 27  20:15", fill=(233, 241, 236), font=f_bold)

    # Quick settings pill on panel right
    qs_pill = [(w - panel_margin - 110, panel_y + 4), (w - panel_margin - 12, panel_y + panel_h - 4)]
    draw_rounded_rect(draw, qs_pill, radius=14, fill=(29, 50, 56, 180), outline=(143, 184, 166, 120), width=1)
    draw.text((w - panel_margin - 95, panel_y + 10), "📶  🔊  🔋", fill=(143, 184, 166), font=f_ui)

    # 2. Main Window: Text Editor / Code
    win_x, win_y = 160, 75
    win_w, win_h = 620, 420
    # Window shadow
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    draw_rounded_rect(sd, [(win_x - 10, win_y - 5), (win_x + win_w + 10, win_y + win_h + 15)], radius=24, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    im = Image.alpha_composite(im, shadow)
    draw = ImageDraw.Draw(im)

    # Window frame
    draw_rounded_rect(draw, [(win_x, win_y), (win_x + win_w, win_y + win_h)], radius=16, fill=(15, 20, 27, 245), outline=(44, 62, 68, 255), width=1)
    # Headerbar
    draw_rounded_rect(draw, [(win_x, win_y), (win_x + win_w, win_y + 44)], radius=16, fill=(22, 34, 42, 255))
    draw.rectangle([(win_x, win_y + 24), (win_x + win_w, win_y + 44)], fill=(22, 34, 42, 255))
    draw.line([(win_x, win_y + 44), (win_x + win_w, win_y + 44)], fill=(44, 62, 68), width=1)

    # macOS / Colloid style dots
    draw.ellipse([(win_x + 18, win_y + 16), (win_x + 30, win_y + 28)], fill=(229, 115, 127))
    draw.ellipse([(win_x + 38, win_y + 16), (win_x + 50, win_y + 28)], fill=(229, 181, 128))
    draw.ellipse([(win_x + 58, win_y + 16), (win_x + 70, win_y + 28)], fill=(127, 200, 160))

    draw.text((win_x + win_w // 2 - 70, win_y + 14), "tokens.json — Editor", fill=(233, 241, 236), font=f_ui)

    # Code lines
    code_lines = [
        ('{\n  "theme": "MT Verdant Nocturne",\n  "tweaks": ["float", "translucent", "macos"],\n  "size": "standard",\n  "blur": true,\n  "palette": {', (167, 184, 177)),
        ('    "accent": "#8FB8A6",  /* Botanical Sage */', (143, 184, 166)),
        ('    "background": "#0F141B",\n    "surface": "#1D3238",\n    "border": "#2C3E44"', (233, 241, 236)),
        ('  }\n}', (167, 184, 177)),
        ('\n/* Live preview with frosted floating panel */', (82, 115, 111)),
    ]
    cur_y = win_y + 60
    for block, col in code_lines:
        for line in block.split("\n"):
            draw.text((win_x + 24, cur_y), line, fill=col, font=f_mono)
            cur_y += 20

    # 3. Quick Settings Popover Menu (Right side)
    qs_x, qs_y = 820, 60
    qs_w, qs_h = 320, 360
    qshadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    qsd = ImageDraw.Draw(qshadow)
    draw_rounded_rect(qsd, [(qs_x - 6, qs_y - 4), (qs_x + qs_w + 6, qs_y + qs_h + 10)], radius=20, fill=(0, 0, 0, 110))
    qshadow = qshadow.filter(ImageFilter.GaussianBlur(14))
    im = Image.alpha_composite(im, qshadow)
    draw = ImageDraw.Draw(im)

    # Popover body
    draw_rounded_rect(draw, [(qs_x, qs_y), (qs_x + qs_w, qs_y + qs_h)], radius=18, fill=(22, 34, 42, 240), outline=(44, 62, 68, 255), width=1)

    toggles = [
        ("Wi-Fi: Connected", True), ("Bluetooth: On", True),
        ("Dark Style: Active", True), ("Night Light: Off", False)
    ]
    for idx, (label, active) in enumerate(toggles):
        tx = qs_x + 16 + (idx % 2) * 146
        ty = qs_y + 20 + (idx // 2) * 58
        bg_col = (143, 184, 166, 255) if active else (29, 50, 56, 255)
        text_col = (13, 19, 26) if active else (233, 241, 236)
        draw_rounded_rect(draw, [(tx, ty), (tx + 138, ty + 46)], radius=12, fill=bg_col)
        draw.text((tx + 12, ty + 15), label[:12], fill=text_col, font=f_ui)

    # Volume slider
    draw.text((qs_x + 20, qs_y + 150), "Volume", fill=(167, 184, 177), font=f_ui)
    draw_rounded_rect(draw, [(qs_x + 20, qs_y + 172), (qs_x + qs_w - 20, qs_y + 184)], radius=6, fill=(29, 50, 56))
    draw_rounded_rect(draw, [(qs_x + 20, qs_y + 172), (qs_x + 210, qs_y + 184)], radius=6, fill=(143, 184, 166))
    draw.ellipse([(qs_x + 204, qs_y + 168), (qs_x + 218, qs_y + 188)], fill=(233, 241, 236))

    # Floating dock at bottom
    dock_y = h - 110
    dock_w = 340
    dock_x = (w - dock_w) // 2
    draw_rounded_rect(draw, [(dock_x, dock_y), (dock_x + dock_w, dock_y + 50)], radius=22, fill=(15, 20, 27, 210), outline=(44, 62, 68, 200), width=1)
    icons = ["📁", "🌐", "💻", "🎵", "⚙️", "🌿"]
    for i, ic in enumerate(icons):
        ix = dock_x + 25 + i * 50
        draw.text((ix, dock_y + 12), ic, fill=(233, 241, 236), font=get_font(FONT_REG, 20))

    # Bottom caption bar
    draw_rounded_rect(draw, [(30, h - 45), (w - 30, h - 12)], radius=8, fill=(13, 19, 26, 235), outline=(143, 184, 166, 180), width=1)
    draw.text((45, h - 38), "Option A: Canopy Floating Glass — Standard Sizing · Frosted Translucency · macOS Traffic Dots · Glassmorphic Dock", fill=(143, 184, 166), font=f_bold)

    for p in [SCREENSHOTS / "mockup-option-a.png", SCREENSHOTS / "option-a-floating-glass.png"]:
        im.save(p)
        print(f"saved {p}")

def generate_mockup_b():
    # Option B: Obsidian Pro & Compact (TokyoNight/Catppuccin inspired OLED style)
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (7, 11, 14, 255))
    draw = ImageDraw.Draw(im)

    # Midnight Aurora gradient
    for y in range(h):
        t = y / h
        r = int(5 * (1 - t) + 10 * t)
        g = int(12 * (1 - t) + 26 * t)
        b = int(14 * (1 - t) + 22 * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    streak = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(streak)
    sdraw.polygon([(0, 280), (w, 140), (w, 320), (0, 480)], fill=(61, 214, 140, 32))
    streak = streak.filter(ImageFilter.GaussianBlur(70))
    im = Image.alpha_composite(im, streak)
    draw = ImageDraw.Draw(im)

    # 1. Edge-to-edge compact top bar (OLED deep black)
    panel_h = 30
    draw.rectangle([(0, 0), (w, panel_h)], fill=(7, 11, 14, 250), outline=None)
    draw.line([(0, panel_h), (w, panel_h)], fill=(28, 42, 48), width=1)

    f_ui = get_font(FONT_REG, 12)
    f_bold = get_font(FONT_BOLD, 12)
    f_mono = get_font(FONT_MONO, 12)

    draw.text((18, 7), "Activities", fill=(233, 241, 236), font=f_ui)
    draw.text((w // 2 - 40, 7), "Mon Oct 27  20:15", fill=(61, 214, 140), font=f_bold)
    draw.text((w - 120, 7), "📶 98% 🔋  0:42", fill=(167, 184, 177), font=f_ui)

    # 2. Compact Terminal window
    win_x, win_y = 120, 55
    win_w, win_h = 660, 460
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    draw_rounded_rect(sd, [(win_x - 8, win_y - 4), (win_x + win_w + 8, win_y + win_h + 12)], radius=12, fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    im = Image.alpha_composite(im, shadow)
    draw = ImageDraw.Draw(im)

    # Window frame (Rimless crisp design)
    draw_rounded_rect(draw, [(win_x, win_y), (win_x + win_w, win_y + win_h)], radius=8, fill=(7, 11, 14, 255), outline=(61, 214, 140, 180), width=1)
    # Headerbar compact
    draw_rounded_rect(draw, [(win_x, win_y), (win_x + win_w, win_y + 36)], radius=8, fill=(14, 22, 28))
    draw.rectangle([(win_x, win_y + 16), (win_x + win_w, win_y + 36)], fill=(14, 22, 28))
    draw.line([(win_x, win_y + 36), (win_x + win_w, win_y + 36)], fill=(28, 42, 48), width=1)

    # Compact square window buttons
    for i, col in enumerate([(229, 115, 127), (229, 181, 128), (61, 214, 140)]):
        bx = win_x + win_w - 75 + i * 22
        draw_rounded_rect(draw, [(bx, win_y + 10), (bx + 16, win_y + 26)], radius=3, fill=(20, 32, 40))
        draw.rectangle([(bx + 4, win_y + 17), (bx + 12, win_y + 19)], fill=col)

    draw.text((win_x + 16, win_y + 10), "mayank@nocturne: ~/projects/gnome-themes", fill=(233, 241, 236), font=f_ui)

    term_text = [
        ("$ ./tools/install.sh --tweaks black,compact,rimless --size compact --no-blur", (61, 214, 140)),
        ("=> Detected GNOME Shell 51.1 (Wayland)", (167, 184, 177)),
        ("=> Sizing profile: COMPACT (reduced paddings, 36px headerbars, high-DPI density)", (233, 241, 236)),
        ("=> Blur profile: NO-BLUR (pure opaque crisp surfaces, zero GPU compositing overhead)", (167, 184, 177)),
        ("=> Palette flavor: Emerald Aurora (#3DD68C high-contrast)", (61, 214, 140)),
        ("=> WCAG contrast check: 9.82:1 (PASS+)", (127, 200, 160)),
        ("=> Installed successfully into ~/.themes/MT-Verdant-Nocturne", (233, 241, 236)),
        ("=> Terminal color scheme: Ghostty & Kitty installed into ~/.config/", (143, 184, 166)),
    ]
    cur_y = win_y + 52
    for tline, col in term_text:
        draw.text((win_x + 18, cur_y), tline, fill=col, font=f_mono)
        cur_y += 24

    # 3. Quick Settings Panel (High Density / Compact Grid)
    qs_x, qs_y = 820, 50
    qs_w, qs_h = 340, 340
    draw_rounded_rect(draw, [(qs_x, qs_y), (qs_x + qs_w, qs_y + qs_h)], radius=10, fill=(11, 17, 22, 250), outline=(28, 42, 48), width=1)

    grid = [
        ("Wi-Fi", "Connected", True), ("Bluetooth", "5 Devices", True),
        ("Power Mode", "Performance", True), ("OLED Pure Black", "Enabled", True),
        ("Night Light", "Off", False), ("Do Not Disturb", "Off", False)
    ]
    for idx, (title, sub, active) in enumerate(grid):
        gx = qs_x + 14 + (idx % 2) * 156
        gy = qs_y + 16 + (idx // 2) * 56
        bg_col = (20, 38, 32) if active else (15, 23, 29)
        border_col = (61, 214, 140) if active else (28, 42, 48)
        draw_rounded_rect(draw, [(gx, gy), (gx + 148, gy + 48)], radius=6, fill=bg_col, outline=border_col, width=1)
        draw.text((gx + 12, gy + 8), title, fill=(233, 241, 236), font=f_bold)
        draw.text((gx + 12, gy + 28), sub, fill=(120, 140, 134), font=f_ui)

    # Bottom caption bar
    draw_rounded_rect(draw, [(30, h - 45), (w - 30, h - 12)], radius=8, fill=(7, 11, 14, 240), outline=(61, 214, 140, 180), width=1)
    draw.text((45, h - 38), "Option B: Obsidian Pro — Compact Sizing · OLED Pitch-Black · Rimless Sharp Corners · No-Blur Performance", fill=(61, 214, 140), font=f_bold)

    for p in [SCREENSHOTS / "mockup-option-b.png", SCREENSHOTS / "option-b-obsidian-compact.png"]:
        im.save(p)
        print(f"saved {p}")

def generate_mockup_c():
    # Option C: Nordic Evergreen & Organic (Everforest/Material inspired warm tactile style)
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (18, 26, 24, 255))
    draw = ImageDraw.Draw(im)

    # Earthy pine gradient
    for y in range(h):
        t = y / h
        r = int(14 * (1 - t) + 26 * t)
        g = int(22 * (1 - t) + 38 * t)
        b = int(20 * (1 - t) + 32 * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Forest canopy organic rings
    canopy = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(canopy)
    cdraw.ellipse([(-100, -100), (600, 600)], fill=(45, 79, 68, 45))
    cdraw.ellipse([(w - 400, h - 400), (w + 200, h + 200)], fill=(75, 115, 98, 35))
    canopy = canopy.filter(ImageFilter.GaussianBlur(60))
    im = Image.alpha_composite(im, canopy)
    draw = ImageDraw.Draw(im)

    # 1. Native Solid Top Bar
    panel_h = 34
    draw.rectangle([(0, 0), (w, panel_h)], fill=(22, 32, 29, 255))
    draw.line([(0, panel_h), (w, panel_h)], fill=(48, 68, 62), width=1)

    f_ui = get_font(FONT_REG, 13)
    f_bold = get_font(FONT_BOLD, 13)

    draw.text((20, 9), "🌿 Mayank's Desktop", fill=(163, 201, 168), font=f_bold)
    draw.text((w // 2 - 40, 9), "Mon Oct 27  20:15", fill=(216, 226, 220), font=f_ui)
    draw.text((w - 130, 9), "📶  🔊  100%", fill=(163, 201, 168), font=f_ui)

    # 2. Nautilus File Manager Window (Organic curves, warm cards)
    win_x, win_y = 140, 65
    win_w, win_h = 680, 440
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    draw_rounded_rect(sd, [(win_x - 12, win_y - 6), (win_x + win_w + 12, win_y + win_h + 16)], radius=20, fill=(0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    im = Image.alpha_composite(im, shadow)
    draw = ImageDraw.Draw(im)

    # Window frame
    draw_rounded_rect(draw, [(win_x, win_y), (win_x + win_w, win_y + win_h)], radius=18, fill=(22, 32, 29, 255), outline=(48, 68, 62), width=1)
    # Headerbar
    draw_rounded_rect(draw, [(win_x, win_y), (win_x + win_w, win_y + 46)], radius=18, fill=(26, 38, 35))
    draw.rectangle([(win_x, win_y + 24), (win_x + win_w, win_y + 46)], fill=(26, 38, 35))
    draw.line([(win_x, win_y + 46), (win_x + win_w, win_y + 46)], fill=(48, 68, 62), width=1)

    for i, symbol in enumerate(["—", "□", "✕"]):
        bx = win_x + win_w - 100 + i * 30
        draw.ellipse([(bx, win_y + 14), (bx + 22, win_y + 36)], fill=(34, 48, 44))
        draw.text((bx + 6, win_y + 17), symbol, fill=(216, 226, 220), font=f_ui)

    draw.text((win_x + 20, win_y + 14), "Files — Documents", fill=(216, 226, 220), font=f_bold)

    # Sidebar + Content split
    draw.rectangle([(win_x, win_y + 47), (win_x + 160, win_y + win_h - 18)], fill=(18, 26, 24))
    draw.line([(win_x + 160, win_y + 47), (win_x + 160, win_y + win_h)], fill=(48, 68, 62), width=1)

    items = ["Home", "Documents", "Downloads", "Wallpapers", "Themes"]
    for i, it in enumerate(items):
        iy = win_y + 60 + i * 32
        is_sel = it == "Themes"
        if is_sel:
            draw_rounded_rect(draw, [(win_x + 8, iy - 4), (win_x + 152, iy + 24)], radius=8, fill=(45, 79, 68))
        draw.text((win_x + 20, iy), it, fill=(216, 226, 220) if is_sel else (150, 175, 165), font=f_ui)

    cards = ["MT-Verdant-Nocturne", "Wallpapers-4K", "Tokens-Palette", "Upstream-Colormaps"]
    for i, card in enumerate(cards):
        cx = win_x + 180 + (i % 2) * 230
        cy = win_y + 70 + (i // 2) * 120
        draw_rounded_rect(draw, [(cx, cy), (cx + 210, cy + 96)], radius=12, fill=(30, 44, 40), outline=(48, 68, 62), width=1)
        draw.text((cx + 16, cy + 16), "📁", fill=(163, 201, 168), font=get_font(FONT_REG, 24))
        draw.text((cx + 16, cy + 54), card, fill=(216, 226, 220), font=f_bold)
        draw.text((cx + 16, cy + 72), "Updated today", fill=(150, 175, 165), font=f_ui)

    # 3. Quick Settings Card
    qs_x, qs_y = 860, 65
    qs_w, qs_h = 300, 320
    draw_rounded_rect(draw, [(qs_x, qs_y), (qs_x + qs_w, qs_y + qs_h)], radius=16, fill=(26, 38, 35, 245), outline=(48, 68, 62), width=1)
    draw.text((qs_x + 20, qs_y + 20), "Quick Settings", fill=(216, 226, 220), font=f_bold)

    for idx, name in enumerate(["Wi-Fi", "Bluetooth", "Night Light", "Dark Style"]):
        bx = qs_x + 20
        by = qs_y + 55 + idx * 52
        draw_rounded_rect(draw, [(bx, by), (bx + qs_w - 40, by + 42)], radius=12, fill=(45, 79, 68) if idx != 2 else (30, 44, 40))
        draw.text((bx + 16, by + 12), name, fill=(216, 226, 220), font=f_ui)

    # Bottom caption bar
    draw_rounded_rect(draw, [(30, h - 45), (w - 30, h - 12)], radius=8, fill=(18, 26, 24, 240), outline=(163, 201, 168, 180), width=1)
    draw.text((45, h - 38), "Option C: Nordic Evergreen — Standard Sizing · Solid Forest Surfaces · Organic Tactile Cards & Curves", fill=(163, 201, 168), font=f_bold)

    for p in [SCREENSHOTS / "mockup-option-c.png", SCREENSHOTS / "option-c-nordic-organic.png"]:
        im.save(p)
        print(f"saved {p}")

def generate_showcase_apps():
    # Showcase: Multi-App Ecosystem (Kitty, Ghostty, GNOME Terminal Fastfetch, Kate, Nautilus)
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (13, 19, 26, 255))
    draw = ImageDraw.Draw(im)

    # Background gradient
    for y in range(h):
        t = y / h
        r = int(10 * (1 - t) + 16 * t)
        g = int(18 * (1 - t) + 32 * t)
        b = int(22 * (1 - t) + 30 * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Top panel
    draw.rectangle([(0, 0), (w, 32)], fill=(13, 19, 26, 245))
    draw.line([(0, 32), (w, 32)], fill=(37, 53, 59), width=1)
    f_ui = get_font(FONT_REG, 12)
    f_bold = get_font(FONT_BOLD, 12)
    f_mono = get_font(FONT_MONO, 11)
    f_mono_bold = get_font(FONT_BOLD, 11)

    draw.text((20, 8), "Activities", fill=(233, 241, 236), font=f_ui)
    draw.text((w // 2 - 50, 8), "Verdant Nocturne Ecosystem", fill=(143, 184, 166), font=f_bold)
    draw.text((w - 140, 8), "GNOME 51 · Wayland", fill=(167, 184, 177), font=f_ui)

    # Window 1: Terminal running Fastfetch (Kitty/Ghostty/GNOME Terminal)
    w1_x, w1_y, w1_w, w1_h = 30, 48, 590, 325
    draw_rounded_rect(draw, [(w1_x, w1_y), (w1_x + w1_w, w1_y + w1_h)], radius=10, fill=(10, 15, 20, 250), outline=(44, 62, 68), width=1)
    draw_rounded_rect(draw, [(w1_x, w1_y), (w1_x + w1_w, w1_y + 32)], radius=10, fill=(18, 27, 34))
    draw.rectangle([(w1_x, w1_y + 16), (w1_x + w1_w, w1_y + 32)], fill=(18, 27, 34))
    draw.line([(w1_x, w1_y + 32), (w1_x + w1_w, w1_y + 32)], fill=(44, 62, 68), width=1)
    # Window controls
    draw.ellipse([(w1_x + 12, w1_y + 11), (w1_x + 22, w1_y + 21)], fill=(229, 115, 127))
    draw.ellipse([(w1_x + 28, w1_y + 11), (w1_x + 38, w1_y + 21)], fill=(229, 181, 128))
    draw.ellipse([(w1_x + 44, w1_y + 11), (w1_x + 54, w1_y + 21)], fill=(127, 200, 160))
    draw.text((w1_x + 70, w1_y + 9), "Terminal — Ghostty / Kitty / GNOME Terminal (Fastfetch)", fill=(216, 226, 220), font=f_bold)

    # Terminal Fastfetch Output
    ff_lines = [
        ("       ▲        mayank@nocturne", (143, 184, 166)),
        ("      ▲ ▲       -------------------------", (120, 150, 140)),
        ("     ▲ ▲ ▲      OS: Fedora Linux 43 (Rawhide) x86_64", (233, 241, 236)),
        ("    ▲ ▲ ▲ ▲     Host: Nocturne Rig", (233, 241, 236)),
        ("   ▲ ▲ ▲ ▲ ▲    Kernel: 6.14.0-rc3+", (233, 241, 236)),
        ("  ▲ ▲ ▲ ▲ ▲ ▲   DE: GNOME 51.1 (Wayland)", (233, 241, 236)),
        (" ▲ ▲ ▲ ▲ ▲ ▲ ▲  WM Theme: MT-Verdant-Nocturne", (143, 184, 166)),
        ("      |||       Theme: MT-Verdant-Nocturne [GTK2/3/4]", (143, 184, 166)),
        ("      |||       Icons: MT-Verdant-Icons [High-DPI]", (127, 200, 160)),
        ("      |||       Terminal Font: Adwaita Mono 11", (167, 184, 177)),
        ("                Color Palette: Botanical Deep Forest", (143, 184, 166)),
    ]
    cur_y = w1_y + 44
    for line, col in ff_lines:
        draw.text((w1_x + 20, cur_y), line, fill=col, font=f_mono)
        cur_y += 18

    # Terminal Color Blocks Palette
    p_colors = [
        (15, 20, 27), (229, 115, 127), (127, 200, 160), (229, 181, 128),
        (100, 160, 210), (180, 140, 210), (143, 184, 166), (233, 241, 236),
    ]
    for idx, c in enumerate(p_colors):
        px = w1_x + 190 + idx * 24
        draw.rectangle([(px, cur_y + 8), (px + 20, cur_y + 24)], fill=c, outline=(44, 62, 68))

    # Window 2: Kate / GNOME Text Editor
    w2_x, w2_y, w2_w, w2_h = 645, 48, 605, 325
    draw_rounded_rect(draw, [(w2_x, w2_y), (w2_x + w2_w, w2_y + w2_h)], radius=10, fill=(13, 19, 26, 250), outline=(44, 62, 68), width=1)
    draw_rounded_rect(draw, [(w2_x, w2_y), (w2_x + w2_w, w2_y + 32)], radius=10, fill=(20, 31, 38))
    draw.rectangle([(w2_x, w2_y + 16), (w2_x + w2_w, w2_y + 32)], fill=(20, 31, 38))
    draw.line([(w2_x, w2_y + 32), (w2_x + w2_w, w2_y + 32)], fill=(44, 62, 68), width=1)
    # Window controls
    draw.ellipse([(w2_x + 12, w2_y + 11), (w2_x + 22, w2_y + 21)], fill=(229, 115, 127))
    draw.ellipse([(w2_x + 28, w2_y + 11), (w2_x + 38, w2_y + 21)], fill=(229, 181, 128))
    draw.ellipse([(w2_x + 44, w2_y + 11), (w2_x + 54, w2_y + 21)], fill=(127, 200, 160))
    draw.text((w2_x + 70, w2_y + 9), "Kate / Text Editor — MT-Verdant-Nocturne.colors", fill=(216, 226, 220), font=f_bold)

    editor_code = [
        ("1", "import { ThemeManager, BotanicalPalette } from '@mt/theme';", (143, 184, 166)),
        ("2", "", (233, 241, 236)),
        ("3", "export class VerdantEngine {", (127, 200, 160)),
        ("4", "  constructor(readonly options: { size: 'standard' | 'compact' }) {", (216, 226, 220)),
        ("5", "    console.log(`Initialized Verdant Nocturne in ${options.size} mode`);", (229, 181, 128)),
        ("6", "  }", (216, 226, 220)),
        ("7", "  public applyAccent(token = '#8FB8A6'): void {", (143, 184, 166)),
        ("8", "    document.body.style.setProperty('--accent', token);", (233, 241, 236)),
        ("9", "  }", (216, 226, 220)),
        ("10", "}", (127, 200, 160)),
        ("11", "/* Perfectly styled across GNOME, KDE & Terminal ecosystems */", (82, 115, 111)),
    ]
    cur_y = w2_y + 42
    for num, code, col in editor_code:
        draw.text((w2_x + 15, cur_y), num.rjust(2), fill=(70, 95, 90), font=f_mono)
        draw.text((w2_x + 45, cur_y), code, fill=col, font=f_mono)
        cur_y += 20

    # Window 3: Nautilus File Manager (Bottom View with High-DPI Themed Icons)
    w3_x, w3_y, w3_w, w3_h = 30, 390, 1220, 260
    draw_rounded_rect(draw, [(w3_x, w3_y), (w3_x + w3_w, w3_y + w3_h)], radius=12, fill=(15, 23, 28, 250), outline=(44, 62, 68), width=1)
    draw_rounded_rect(draw, [(w3_x, w3_y), (w3_x + w3_w, w3_y + 36)], radius=12, fill=(22, 34, 42))
    draw.rectangle([(w3_x, w3_y + 18), (w3_x + w3_w, w3_y + 36)], fill=(22, 34, 42))
    draw.line([(w3_x, w3_y + 36), (w3_x + w3_w, w3_y + 36)], fill=(44, 62, 68), width=1)

    draw.ellipse([(w3_x + 14, w3_y + 12), (w3_x + 24, w3_y + 22)], fill=(229, 115, 127))
    draw.ellipse([(w3_x + 30, w3_y + 12), (w3_x + 40, w3_y + 22)], fill=(229, 181, 128))
    draw.ellipse([(w3_x + 46, w3_y + 12), (w3_x + 56, w3_y + 22)], fill=(127, 200, 160))
    draw.text((w3_x + 72, w3_y + 10), "Files (Nautilus) — ~/.themes/MT-Verdant-Nocturne/extras/", fill=(216, 226, 220), font=f_bold)

    # Sidebar
    draw.rectangle([(w3_x, w3_y + 37), (w3_x + 180, w3_y + w3_h - 12)], fill=(12, 18, 23))
    draw.line([(w3_x + 180, w3_y + 37), (w3_x + 180, w3_y + w3_h)], fill=(44, 62, 68), width=1)
    side_folders = ["Desktop", "Documents", "Downloads", "Terminals", "Text-Editors", "Fastfetch", "GRUB Boot"]
    for idx, s in enumerate(side_folders):
        sy = w3_y + 48 + idx * 28
        is_sel = idx == 3
        if is_sel:
            draw_rounded_rect(draw, [(w3_x + 8, sy - 2), (w3_x + 172, sy + 22)], radius=6, fill=(29, 50, 56))
        draw.text((w3_x + 20, sy), f"📁 {s}", fill=(216, 226, 220) if is_sel else (140, 165, 155), font=f_ui)

    # Main Grid of Files & Themed Folders with botanical colors
    grid_items = [
        ("📁 kitty/", "Config & colors", "#8FB8A6"),
        ("📁 ghostty/", "24-bit botanical", "#8FB8A6"),
        ("📁 alacritty/", "TOML theme map", "#8FB8A6"),
        ("📁 foot/", "Wayland terminal", "#8FB8A6"),
        ("📄 gnome-terminal.sh", "dconf registration", "#A3C9A8"),
        ("📄 kate-colors.sh", "KDE color scheme", "#A3C9A8"),
        ("📄 fastfetch.jsonc", "Verdant logo ASCII", "#7FB392"),
        ("🖼️ grub-bg-4k.png", "Bootloader 3840x2160", "#64A0D2"),
    ]
    for idx, (title, sub, accent_hex) in enumerate(grid_items):
        col = idx % 4
        row = idx // 4
        gx = w3_x + 205 + col * 248
        gy = w3_y + 52 + row * 94
        draw_rounded_rect(draw, [(gx, gy), (gx + 236, gy + 82)], radius=10, fill=(20, 31, 38), outline=(44, 62, 68), width=1)
        draw.text((gx + 14, gy + 14), title, fill=(233, 241, 236), font=f_bold)
        draw.text((gx + 14, gy + 38), sub, fill=(140, 165, 155), font=f_ui)
        draw_rounded_rect(draw, [(gx + 14, gy + 62), (gx + 110, gy + 74)], radius=4, fill=(29, 50, 56))
        draw.text((gx + 20, gy + 62), "MT-Verdant", fill=(143, 184, 166), font=get_font(FONT_REG, 10))

    # Bottom caption bar
    draw_rounded_rect(draw, [(30, h - 45), (w - 30, h - 12)], radius=8, fill=(10, 15, 20, 245), outline=(143, 184, 166, 180), width=1)
    draw.text((45, h - 38), "Multi-App Ecosystem Showcase — Ghostty · Kitty · GNOME Terminal · Fastfetch · Kate · Nautilus · GRUB", fill=(143, 184, 166), font=f_bold)

    p = SCREENSHOTS / "showcase-terminals-apps.png"
    im.save(p)
    print(f"saved {p}")

if __name__ == "__main__":
    generate_mockup_a()
    generate_mockup_b()
    generate_mockup_c()
    generate_showcase_apps()
