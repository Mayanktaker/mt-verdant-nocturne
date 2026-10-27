# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Generates GRUB bootloader theme assets for MT Verdant Nocturne.

from pathlib import Path
from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parents[2]
GRUB_DIR = REPO_ROOT / "extras" / "grub" / "mt-verdant-nocturne"
GRUB_DIR.mkdir(parents=True, exist_ok=True)

def generate_selection():
    # Selection bar in sage #8FB8A6
    w, h = 420, 38
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([(0, 0), (w - 1, h - 1)], radius=8, fill=(143, 184, 166, 255), outline=(61, 214, 140, 255), width=1)
    im.save(GRUB_DIR / "select_box.png")
    print("  ✓ generated select_box.png")

def copy_background():
    bg_src = REPO_ROOT / "wallpaper" / "preview" / "mt-verdant-canopy-1920x1080.jpg"
    if bg_src.exists():
        im = Image.open(bg_src)
        im.save(GRUB_DIR / "background.png")
        print("  ✓ copied background.png")

def write_theme_txt():
    txt = """# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# GRUB2 theme: MT Verdant Nocturne

title-text: "MT Verdant Nocturne"
title-color: "#8FB8A6"
title-font: "Unifont Regular 16"
message-font: "Unifont Regular 14"
message-color: "#A7B8B1"
terminal-font: "Unifont Regular 14"
terminal-box: "select_box.png"

desktop-image: "background.png"
desktop-color: "#0F141B"

# Boot Menu
+ boot_menu {
  left = 30%
  top = 35%
  width = 40%
  height = 40%
  item_font = "Unifont Regular 16"
  item_color = "#E9F1EC"
  selected_item_color = "#0D131A"
  selected_item_pixmap_style = "select_box.png"
  item_height = 40
  item_padding = 10
  item_spacing = 8
}

# Timeout progress bar
+ progress_bar {
  id = "__timeout__"
  left = 35%
  top = 80%
  width = 30%
  height = 12
  text = "@TIMEOUT_NOTIFICATION_MIDDLE@"
  text_color = "#8FB8A6"
  font = "Unifont Regular 12"
  bg_color = "#16222A"
  fg_color = "#3DD68C"
  border_color = "#2C3E44"
}
"""
    (GRUB_DIR / "theme.txt").write_text(txt)

    install_sh = """#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne GRUB theme (requires sudo)

set -eu
THEME_NAME="mt-verdant-nocturne"
DEST_DIR="/boot/grub/themes/${THEME_NAME}"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing GRUB theme to ${DEST_DIR}..."
sudo mkdir -p "${DEST_DIR}"
sudo cp -r "${SRC_DIR}"/* "${DEST_DIR}/"

echo "To activate:"
echo "1. Edit /etc/default/grub and set: GRUB_THEME=\\"${DEST_DIR}/theme.txt\\""
echo "2. Update grub: sudo grub-mkconfig -o /boot/grub/grub.cfg"
"""
    (GRUB_DIR / "install.sh").write_text(install_sh)
    (GRUB_DIR / "install.sh").chmod(0o755)
    print("  ✓ wrote theme.txt & install.sh")

if __name__ == "__main__":
    generate_selection()
    copy_background()
    write_theme_txt()
