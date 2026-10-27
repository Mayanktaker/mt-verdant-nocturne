#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne style scheme into GtkSourceView (GNOME Text Editor, Gedit).

set -eu
SRC_FILE="$(cd "$(dirname "$0")" && pwd)/mt-verdant-nocturne.xml"

for ver in 4 5; do
  DEST_DIR="${HOME}/.local/share/gtksourceview-${ver}/styles"
  mkdir -p "${DEST_DIR}"
  cp "${SRC_FILE}" "${DEST_DIR}/"
  echo "Installed to ${DEST_DIR}/mt-verdant-nocturne.xml"
done

echo "Select 'MT Verdant Nocturne' in GNOME Text Editor / Gedit preferences!"
