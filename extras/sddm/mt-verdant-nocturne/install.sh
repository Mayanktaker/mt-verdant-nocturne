#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne SDDM login theme (requires sudo)

set -eu
THEME_NAME="mt-verdant-nocturne"
DEST_DIR="/usr/share/sddm/themes/${THEME_NAME}"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing MT Verdant Nocturne SDDM theme to ${DEST_DIR}..."
sudo mkdir -p "${DEST_DIR}"
sudo cp -r "${SRC_DIR}"/* "${DEST_DIR}/"

if command -v sddm-greeter >/dev/null 2>&1; then
    echo "To test theme: sddm-greeter --test-mode --theme ${DEST_DIR}"
fi
echo "To activate: set 'Current=${THEME_NAME}' in /etc/sddm.conf under [Theme]."
