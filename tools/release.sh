#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Build every accent preset and assemble the release archive with the packaged layout.
# Usage: tools/release.sh <version>   (e.g. tools/release.sh 0.4.0)

set -eu

VERSION="${1:?usage: tools/release.sh <version>}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PKG_NAME="mt-verdant-nocturne-v${VERSION}"
DIST="${REPO_ROOT}/dist/${PKG_NAME}"
TARBALL="${REPO_ROOT}/dist/${PKG_NAME}.tar.xz"
ACCENTS="sage emerald moss pine"

# Rebuild every layer from tokens and fail the release on any gate.
python3 "${REPO_ROOT}/tools/dev/check_contrast.py"
python3 "${REPO_ROOT}/tools/dev/check_colors.py"
python3 "${REPO_ROOT}/tools/dev/check_selectors.py"
python3 "${REPO_ROOT}/tools/dev/check_version.py"
python3 "${REPO_ROOT}/tools/wallpaper/generate.py" --which all
python3 "${REPO_ROOT}/tools/wallpaper/generate.py" --verify
python3 "${REPO_ROOT}/tools/shell/build.py" --all --accent sage --out-dir "${REPO_ROOT}/build/theme"
python3 "${REPO_ROOT}/tools/gtk/build.py" --accent sage --out "${REPO_ROOT}/build/theme/gtk-3.0"

rm -rf "${DIST}"
mkdir -p "${DIST}/presets" "${DIST}/tweaks" "${DIST}/gtk4" "${DIST}/gtk2" "${DIST}/wallpapers/light" "${DIST}/extras"

# Per-accent build presets so the release installer never needs sassc
for accent in ${ACCENTS}; do
  python3 "${REPO_ROOT}/tools/shell/build.py" --all --accent "${accent}" --out-dir "${DIST}/presets/${accent}"
  python3 "${REPO_ROOT}/tools/gtk/build.py" --accent "${accent}" --out "${DIST}/presets/${accent}/gtk-3.0" >/dev/null
  python3 "${REPO_ROOT}/tools/theme/render.py" --accent "${accent}" --dir "${REPO_ROOT}/src/tweaks" --out-dir "${DIST}/tweaks/${accent}"
  mkdir -p "${DIST}/gtk4/${accent}"
  python3 "${REPO_ROOT}/tools/theme/render.py" --accent "${accent}" --in "${REPO_ROOT}/src/gtk-4.0/overrides.css" --out "${DIST}/gtk4/${accent}/gtk.css"
  mkdir -p "${DIST}/gtk2/${accent}"
  python3 "${REPO_ROOT}/tools/theme/render.py" --accent "${accent}" --in "${REPO_ROOT}/src/gtk-2.0/gtkrc" --out "${DIST}/gtk2/${accent}/gtkrc"
done

cp "${REPO_ROOT}/src/index.theme" "${DIST}/index.theme"
cp "${REPO_ROOT}/src/thumbnail.png" "${DIST}/thumbnail.png"
cp "${REPO_ROOT}/VERSION" "${DIST}/VERSION"
cp "${REPO_ROOT}/wallpaper/dist/"*.jpg "${DIST}/wallpapers/" 2>/dev/null || true
cp "${REPO_ROOT}/wallpaper/dist/"*.xml* "${DIST}/wallpapers/" 2>/dev/null || true
cp "${REPO_ROOT}/wallpaper/dist/light/"*.jpg "${DIST}/wallpapers/light/" 2>/dev/null || true
cp -r "${REPO_ROOT}/extras/." "${DIST}/extras/"
cp "${REPO_ROOT}/tools/install.sh" "${DIST}/install.sh"
mkdir -p "${DIST}/LICENSES" "${DIST}/wallpaper"
cp "${REPO_ROOT}/README.md" "${DIST}/"
cp "${REPO_ROOT}/LICENSES/"*.txt "${REPO_ROOT}/LICENSES/UPSTREAM-ATTRIBUTION.md" "${DIST}/LICENSES/"
cp -r "${REPO_ROOT}/screenshots" "${DIST}/screenshots"
cp -r "${REPO_ROOT}/wallpaper/preview" "${DIST}/wallpaper/preview"

# Sanity: the packaged installer must be able to install the packaged tree.
HOME_DIR="$(mktemp -d)"
BIN_DIR="$(mktemp -d)"
trap 'rm -rf "$HOME_DIR" "$BIN_DIR"' EXIT
printf '#!/bin/sh\necho "GNOME Shell 51.1"\n' > "${BIN_DIR}/gnome-shell"
printf '#!/bin/sh\nexit 0\n' > "${BIN_DIR}/dconf"
printf '#!/bin/sh\nexit 0\n' > "${BIN_DIR}/gsettings"
printf '#!/bin/sh\nexit 0\n' > "${BIN_DIR}/gnome-extensions"
chmod +x "${BIN_DIR}"/*
HOME="${HOME_DIR}" PATH="${BIN_DIR}:${PATH}" sh "${DIST}/install.sh" --non-interactive --accent emerald >/dev/null
test -s "${HOME_DIR}/.themes/MT-Verdant-Nocturne/gnome-shell/gnome-shell.css"
test -s "${HOME_DIR}/.themes/MT-Verdant-Nocturne/gtk-3.0/gtk.css"
grep -qi "#3dd68c" "${HOME_DIR}/.themes/MT-Verdant-Nocturne/gnome-shell/gnome-shell.css"
grep -qi "#3dd68c" "${HOME_DIR}/.themes/MT-Verdant-Nocturne/gtk-3.0/gtk.css"
echo "packaged installer smoke test: PASS"

mkdir -p "${REPO_ROOT}/dist"
tar -C "${REPO_ROOT}/dist" -cJf "${TARBALL}" "${PKG_NAME}"
rm -rf "${DIST}"
BYTES="$(wc -c < "${TARBALL}")"
if [ "${BYTES}" -gt 35000000 ]; then
  echo "release archive is ${BYTES} bytes (budget 35 MB)" >&2
  exit 1
fi

echo "release ready:"
echo "  - Theme bundle: ${TARBALL}"
echo "  - attach to: git tag v${VERSION} && gh release create v${VERSION} ${TARBALL}"
