#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne color scheme into KDE Plasma / Qt.

set -eu
SRC_FILE="$(cd "$(dirname "$0")" && pwd)/MTVerdantNocturne.colors"
DEST_DIR="${HOME}/.local/share/color-schemes"

mkdir -p "${DEST_DIR}"
cp "${SRC_FILE}" "${DEST_DIR}/"
echo "Installed to ${DEST_DIR}/MTVerdantNocturne.colors"
echo "Select 'MT Verdant Nocturne' in KDE System Settings -> Appearance -> Colors."
