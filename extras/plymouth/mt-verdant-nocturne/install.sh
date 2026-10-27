#!/bin/sh
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
