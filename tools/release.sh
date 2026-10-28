#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Build everything and assemble the vX.Y release tarball + wallpaper into dist/.
# Usage: tools/release.sh <version>   (e.g. tools/release.sh 0.1.0)

set -eu

VERSION="${1:?usage: tools/release.sh <version>}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="${REPO_ROOT}/dist/mt-verdant-nocturne-v${VERSION}"
TARBALL="${REPO_ROOT}/dist/mt-verdant-nocturne-v${VERSION}.tar.xz"

# rebuild all layers from tokens
python3 "${REPO_ROOT}/tools/dev/check_contrast.py" > /dev/null
python3 "${REPO_ROOT}/tools/wallpaper/generate.py" > /dev/null
python3 "${REPO_ROOT}/tools/wallpaper/process_light.py" > /dev/null
python3 "${REPO_ROOT}/tools/icons/generate_icons.py" > /dev/null
python3 "${REPO_ROOT}/tools/icons/generate_cursors.py" > /dev/null
python3 "${REPO_ROOT}/tools/shell/build.py" --all
python3 "${REPO_ROOT}/tools/gtk/build.py" > /dev/null

# assemble the installable tree (installer layout) per supported shell major
rm -rf "${DIST}"
mkdir -p "${DIST}"
cp "${REPO_ROOT}/src/index.theme" "${DIST}/index.theme"
for major_dir in "${REPO_ROOT}"/build/theme/gnome-shell-*; do
  major="${major_dir##*-}"
  cp -r "${major_dir}" "${DIST}/gnome-shell-${major}"
done
cp -r "${REPO_ROOT}/build/theme/gtk-3.0" "${DIST}/gtk-3.0"
cp -r "${REPO_ROOT}/src/gtk-4.0" "${DIST}/gtk-4.0-src"
cp -r "${REPO_ROOT}/src/tweaks" "${DIST}/tweaks"
cp -r "${REPO_ROOT}/src/icons" "${DIST}/icons"
cp -r "${REPO_ROOT}/src/cursors" "${DIST}/cursors"
cp -r "${REPO_ROOT}/extras" "${DIST}/extras"
cp "${REPO_ROOT}/tools/install.sh" "${DIST}/install.sh"
mkdir -p "${DIST}/wallpapers/light"
cp "${REPO_ROOT}/wallpaper/dist/"*.png "${DIST}/wallpapers/"
cp "${REPO_ROOT}/wallpaper/dist/"*.xml* "${DIST}/wallpapers/" 2>/dev/null || true
cp "${REPO_ROOT}/wallpaper/dist/light/"*.png "${DIST}/wallpapers/light/"
cp "${REPO_ROOT}/wallpaper/dist/mt-verdant-canopy-3840x2160.png" "${DIST}/wallpaper.png"
cp "${REPO_ROOT}/wallpaper/dist/light/mt-verdant-canopy-dawn-3840x2160.png" "${DIST}/wallpaper-light.png"
cp "${REPO_ROOT}/README.md" "${REPO_ROOT}/LICENSES/GPL-3.0.txt" "${REPO_ROOT}/LICENSES/CC-BY-SA-4.0.txt" "${DIST}/"

mkdir -p "${REPO_ROOT}/dist"
tar -C "${REPO_ROOT}/dist" -cJf "${TARBALL}" "mt-verdant-nocturne-v${VERSION}"
echo "release ready: ${TARBALL}"
echo "attach to: git tag v${VERSION} && gh release create v${VERSION} ${TARBALL} wallpaper/dist/mt-verdant-nocturne-3840x2160.png wallpaper/dist/light/mt-verdant-canopy-dawn-3840x2160.png"
