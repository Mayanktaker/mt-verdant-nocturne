#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT-Verdant-Nocturne theme into KDE Kate / KWrite.

set -eu
SRC_FILE="$(cd "$(dirname "$0")" && pwd)/MT-Verdant-Nocturne.colors"
DEST_DIR="${HOME}/.local/share/org.kde.syntax-highlighting/themes"

mkdir -p "${DEST_DIR}"
cp "${SRC_FILE}" "${DEST_DIR}/"
echo "Installed to ${DEST_DIR}/MT-Verdant-Nocturne.colors"
echo "Select 'MT-Verdant-Nocturne' in Kate Settings -> Configure Kate -> Color Themes."
