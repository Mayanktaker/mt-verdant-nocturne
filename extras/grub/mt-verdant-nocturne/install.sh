#!/bin/sh
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
echo "1. Edit /etc/default/grub and set: GRUB_THEME=\"${DEST_DIR}/theme.txt\""
echo "2. Update grub: sudo grub-mkconfig -o /boot/grub/grub.cfg"
