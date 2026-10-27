# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Generates Plymouth boot splash theme assets for MT Verdant Nocturne.

import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = Path(__file__).resolve().parents[2]
PLYMOUTH_DIR = REPO_ROOT / "extras" / "plymouth" / "mt-verdant-nocturne"
PLYMOUTH_DIR.mkdir(parents=True, exist_ok=True)

def generate_logo():
    # 128x128 nocturnal botanical emblem logo
    size = 128
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # Outer circle border
    d.ellipse([(4, 4), (size - 4, size - 4)], fill=(22, 34, 42, 240), outline=(44, 62, 68, 255), width=2)
    # Sage accent ring
    d.ellipse([(10, 10), (size - 10, size - 10)], outline=(143, 184, 166, 200), width=1)

    # Stylized central fern / leaf frond
    stem = [(size // 2, size - 26), (size // 2, 28)]
    d.line(stem, fill=(143, 184, 166, 255), width=3)

    # Leaf pairs
    for i in range(5):
        y = 36 + i * 12
        span = 24 - i * 3
        # Left leaf
        d.line([(size // 2, y), (size // 2 - span, y - 8)], fill=(61, 214, 140, 240), width=2)
        # Right leaf
        d.line([(size // 2, y), (size // 2 + span, y - 8)], fill=(61, 214, 140, 240), width=2)

    im.save(PLYMOUTH_DIR / "logo.png")
    print("  ✓ generated logo.png")

def generate_progress():
    # 280x10 progress bar box and fill
    box_w, box_h = 280, 10
    box = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box)
    bd.rounded_rectangle([(0, 0), (box_w - 1, box_h - 1)], radius=5, fill=(22, 34, 42, 220), outline=(44, 62, 68, 255), width=1)
    box.save(PLYMOUTH_DIR / "progress_box.png")

    bar_w, bar_h = box_w - 4, box_h - 4
    bar = Image.new("RGBA", (bar_w, bar_h), (0, 0, 0, 0))
    bard = ImageDraw.Draw(bar)
    bard.rounded_rectangle([(0, 0), (bar_w - 1, bar_h - 1)], radius=3, fill=(143, 184, 166, 255))
    bar.save(PLYMOUTH_DIR / "progress_bar.png")
    print("  ✓ generated progress_box.png & progress_bar.png")

def copy_background():
    # Copy 1080p preview background
    bg_src = REPO_ROOT / "wallpaper" / "preview" / "mt-verdant-canopy-1920x1080.jpg"
    if bg_src.exists():
        im = Image.open(bg_src)
        im.save(PLYMOUTH_DIR / "background.png")
        print("  ✓ copied background.png")

def write_configs():
    # Plymouth theme configuration
    plymouth_cfg = """[Plymouth Theme]
Name=MT Verdant Nocturne
Description=Botanical Canopy dark green boot splash theme
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/mt-verdant-nocturne
ScriptFile=/usr/share/plymouth/themes/mt-verdant-nocturne/mt-verdant-nocturne.script
"""
    (PLYMOUTH_DIR / "mt-verdant-nocturne.plymouth").write_text(plymouth_cfg)

    # Plymouth script
    script_content = """# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Plymouth boot script for MT Verdant Nocturne

screen_width = Window.GetWidth();
screen_height = Window.GetHeight();

# 1. Background
bg_image = Image("background.png");
if (bg_image) {
    resized_bg = bg_image.Scale(screen_width, screen_height);
    bg_sprite = Sprite(resized_bg);
    bg_sprite.SetZ(-100);
}

# 2. Centered Logo
logo_image = Image("logo.png");
if (logo_image) {
    logo_sprite = Sprite(logo_image);
    logo_x = screen_width / 2 - logo_image.GetWidth() / 2;
    logo_y = screen_height / 2 - logo_image.GetHeight() / 2 - 30;
    logo_sprite.SetPosition(logo_x, logo_y, 10);
}

# 3. Progress bar
box_image = Image("progress_box.png");
if (box_image) {
    box_sprite = Sprite(box_image);
    box_x = screen_width / 2 - box_image.GetWidth() / 2;
    box_y = logo_y + logo_image.GetHeight() + 35;
    box_sprite.SetPosition(box_x, box_y, 10);

    bar_image = Image("progress_bar.png");
    bar_sprite = Sprite();
    bar_sprite.SetPosition(box_x + 2, box_y + 2, 11);

    fun progress_callback (duration, progress) {
        new_width = (box_image.GetWidth() - 4) * progress;
        if (new_width > 0) {
            bar = bar_image.Scale(new_width, box_image.GetHeight() - 4);
            bar_sprite.SetImage(bar);
        }
    }
    Plymouth.SetBootProgressFunction(progress_callback);
}

fun quit_callback () {
    if (logo_sprite) logo_sprite.SetOpacity(0);
}
Plymouth.SetQuitFunction(quit_callback);
"""
    (PLYMOUTH_DIR / "mt-verdant-nocturne.script").write_text(script_content)

    # Install script
    install_sh = """#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne Plymouth boot theme (requires sudo)

set -eu
THEME_NAME="mt-verdant-nocturne"
DEST_DIR="/usr/share/plymouth/themes/${THEME_NAME}"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing MT Verdant Nocturne Plymouth theme to ${DEST_DIR}..."
sudo mkdir -p "${DEST_DIR}"
sudo cp -r "${SRC_DIR}"/* "${DEST_DIR}/"

if command -v plymouth-set-default-theme >/dev/null 2>&1; then
    echo "Setting default plymouth theme..."
    sudo plymouth-set-default-theme -R "${THEME_NAME}" || true
    echo "Done! Test with: sudo plymouthd && sudo plymouth --show-splash && sleep 5 && sudo plymouth --quit"
else
    echo "Plymouth utility not found. Update your initramfs/mkinitcpio configuration manually."
fi
"""
    (PLYMOUTH_DIR / "install.sh").write_text(install_sh)
    (PLYMOUTH_DIR / "install.sh").chmod(0o755)
    print("  ✓ wrote configs & install.sh")

if __name__ == "__main__":
    generate_logo()
    generate_progress()
    copy_background()
    write_configs()
