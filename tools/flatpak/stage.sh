#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Stage the GTK3 theme for the Flatpak theme extension (tools/flatpak/stage
# consumed by the manifest's dir source). Re-run after rebuilding the GTK theme.

set -eu

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
STAGE="${REPO_ROOT}/flatpak/stage/MT-Verdant-Nocturne"

[ -f "${REPO_ROOT}/build/theme/gtk-3.0/gtk-dark.css" ] || python3 "${REPO_ROOT}/tools/gtk/build.py"

rm -rf "${REPO_ROOT}/flatpak/stage"
mkdir -p "${STAGE}/gtk-3.0"
cp "${REPO_ROOT}/build/theme/gtk-3.0/gtk.css" "${REPO_ROOT}/build/theme/gtk-3.0/gtk-dark.css" "${STAGE}/gtk-3.0/"
cp -r "${REPO_ROOT}/build/theme/gtk-3.0/assets" "${STAGE}/gtk-3.0/"
cp "${REPO_ROOT}/src/index.theme" "${STAGE}/index.theme"

# Weld the rendered base tweaks (tokens, accent, selection, destructive fix).
TMP_TWEAKS="$(mktemp -d)"
trap 'rm -rf "$TMP_TWEAKS"' EXIT
python3 "${REPO_ROOT}/tools/theme/render.py" --accent sage --dir "${REPO_ROOT}/src/tweaks/gtk" --out-dir "$TMP_TWEAKS" >/dev/null
for target in "${STAGE}/gtk-3.0/gtk.css" "${STAGE}/gtk-3.0/gtk-dark.css"; do
  cat "$TMP_TWEAKS/polish.css" >> "$target"
  cat "$TMP_TWEAKS/round.css" >> "$target"
done
echo "staged GTK3 theme at ${REPO_ROOT}/flatpak/stage"
