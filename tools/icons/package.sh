#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Packages MT-Verdant-Icons and MT-Verdant-Cursors into a standalone .tar.xz archive.
# Usage: tools/icons/package.sh <version>  (e.g. tools/icons/package.sh 0.2.0)

set -eu

VERSION="${1:-0.2.0}"
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DIST_ROOT="${REPO_ROOT}/dist"
ICONS_DIST="${DIST_ROOT}/mt-verdant-icons-v${VERSION}"
TARBALL="${DIST_ROOT}/mt-verdant-icons-v${VERSION}.tar.xz"

# Ensure output directory exists
mkdir -p "${DIST_ROOT}"
rm -rf "${ICONS_DIST}"
mkdir -p "${ICONS_DIST}"

# Copy icon and cursor suites
cp -r "${REPO_ROOT}/src/icons/MT-Verdant-Icons" "${ICONS_DIST}/"
cp -r "${REPO_ROOT}/src/cursors/MT-Verdant-Cursors" "${ICONS_DIST}/"

# Copy licenses
mkdir -p "${ICONS_DIST}/LICENSES"
cp "${REPO_ROOT}/LICENSES/GPL-3.0.txt" "${ICONS_DIST}/LICENSES/"
cp "${REPO_ROOT}/LICENSES/CC-BY-SA-4.0.txt" "${ICONS_DIST}/LICENSES/"

# Create standalone installer script
cat <<'EOF' > "${ICONS_DIST}/install.sh"
#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Standalone installer for MT-Verdant-Icons and MT-Verdant-Cursors
set -eu

ICONS_DIR="${HOME}/.icons"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ensure user icons folder exists
mkdir -p "${ICONS_DIR}"

# Install and activate icons
if [ -d "${SCRIPT_DIR}/MT-Verdant-Icons" ]; then
  echo "Installing MT-Verdant-Icons..."
  rm -rf "${ICONS_DIR}/MT-Verdant-Icons"
  cp -r "${SCRIPT_DIR}/MT-Verdant-Icons" "${ICONS_DIR}/"
  if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t "${ICONS_DIR}/MT-Verdant-Icons" >/dev/null 2>&1 || true
  fi
  if command -v gsettings >/dev/null 2>&1; then
    gsettings set org.gnome.desktop.interface icon-theme 'MT-Verdant-Icons' || true
  fi
  echo "  ✓ MT-Verdant-Icons installed to ${ICONS_DIR}/MT-Verdant-Icons"
fi

# Install and activate cursors
if [ -d "${SCRIPT_DIR}/MT-Verdant-Cursors" ]; then
  echo "Installing MT-Verdant-Cursors..."
  rm -rf "${ICONS_DIR}/MT-Verdant-Cursors"
  cp -r "${SCRIPT_DIR}/MT-Verdant-Cursors" "${ICONS_DIR}/"
  if command -v gsettings >/dev/null 2>&1; then
    gsettings set org.gnome.desktop.interface cursor-theme 'MT-Verdant-Cursors' || true
  fi
  echo "  ✓ MT-Verdant-Cursors installed to ${ICONS_DIR}/MT-Verdant-Cursors"
fi

echo "Done! Icons and cursors have been successfully installed and activated."
EOF
chmod +x "${ICONS_DIST}/install.sh"

# Create standalone README
cat <<'EOF' > "${ICONS_DIST}/README.md"
# MT-Verdant-Icons & MT-Verdant-Cursors

© Mayanktaker Computers & Web Development | https://mayanktaker.com

An ultra-crisp botanical dark icon and cursor suite for Linux desktops with 100+ native application icons and full Adwaita symbolic coverage.

## Quick Installation

Run the included installer:
```bash
./install.sh
```

## Manual Installation

Copy both folders to your user `~/.icons` directory:
```bash
mkdir -p ~/.icons
cp -r MT-Verdant-Icons MT-Verdant-Cursors ~/.icons/
gtk-update-icon-cache -f -t ~/.icons/MT-Verdant-Icons
gsettings set org.gnome.desktop.interface icon-theme 'MT-Verdant-Icons'
gsettings set org.gnome.desktop.interface cursor-theme 'MT-Verdant-Cursors'
```
EOF

# Pack into tar.xz
rm -f "${TARBALL}"
tar -C "${DIST_ROOT}" -cJf "${TARBALL}" "mt-verdant-icons-v${VERSION}"
rm -rf "${ICONS_DIST}"

echo "Icon pack ready: ${TARBALL}"
