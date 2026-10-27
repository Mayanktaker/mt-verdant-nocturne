#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne theme into Fish shell.

set -eu
THEME_NAME="mt_verdant_nocturne"
DEST_DIR="${HOME}/.config/fish/themes"
SRC_FILE="$(cd "$(dirname "$0")" && pwd)/${THEME_NAME}.theme"

mkdir -p "${DEST_DIR}"
cp "${SRC_FILE}" "${DEST_DIR}/"
echo "Theme copied to ${DEST_DIR}/${THEME_NAME}.theme"

if command -v fish >/dev/null 2>&1; then
    fish -c "fish_config theme choose ${THEME_NAME}" 2>/dev/null || true
    echo "Theme activated in Fish shell!"
fi
