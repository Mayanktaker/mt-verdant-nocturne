#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne at user level (no root).
# Usage: tools/install.sh [--wallpaper] [--gtk4-libadwaita]

set -eu

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
THEME_NAME="MT-Verdant-Nocturne"
THEME_DIR="${HOME}/.local/share/themes/${THEME_NAME}"
WANT_WALLPAPER=0
WANT_GTK4_OVERRIDE=0

for arg in "$@"; do
  case "$arg" in
    --wallpaper) WANT_WALLPAPER=1 ;;
    --gtk4-libadwaita) WANT_GTK4_OVERRIDE=1 ;;
    *) echo "unknown option: $arg" >&2; exit 1 ;;
  esac
done

# build outputs must exist; run the builders when missing
SHELL_MAJOR="$(gnome-shell --version | grep -oE '[0-9]+' | head -1)"
[ -f "${REPO_ROOT}/build/theme/gnome-shell-${SHELL_MAJOR}/gnome-shell.css" ] || python3 "${REPO_ROOT}/tools/shell/build.py" --major "${SHELL_MAJOR}"
[ -f "${REPO_ROOT}/build/theme/gtk-3.0/gtk-dark.css" ] || python3 "${REPO_ROOT}/tools/gtk/build.py"

mkdir -p "${THEME_DIR}"
cp "${REPO_ROOT}/src/index.theme" "${THEME_DIR}/index.theme"
rm -rf "${THEME_DIR}/gnome-shell"
cp -r "${REPO_ROOT}/build/theme/gnome-shell-${SHELL_MAJOR}" "${THEME_DIR}/gnome-shell"
cp -r "${REPO_ROOT}/build/theme/gtk-3.0" "${THEME_DIR}/"
mkdir -p "${THEME_DIR}/gtk-4.0"
cp "${REPO_ROOT}/src/gtk-4.0/overrides.css" "${THEME_DIR}/gtk-4.0/gtk.css"
cp "${REPO_ROOT}/src/gtk-4.0/overrides.css" "${THEME_DIR}/gtk-4.0/gtk-dark.css"
echo "installed theme files to ${THEME_DIR}"

if [ "${WANT_WALLPAPER}" -eq 1 ]; then
  PNG="${REPO_ROOT}/wallpaper/dist/mt-verdant-nocturne-3840x2160.png"
  [ -f "${PNG}" ] || python3 "${REPO_ROOT}/tools/wallpaper/generate.py"
  mkdir -p "${HOME}/Pictures"
  DEST="${HOME}/Pictures/mt-verdant-nocturne.png"
  cp "${PNG}" "${DEST}"
  gsettings set org.gnome.desktop.background picture-uri "file://${DEST}"
  gsettings set org.gnome.desktop.background picture-uri-dark "file://${DEST}"
  echo "wallpaper applied from ${DEST}"
fi

if [ "${WANT_GTK4_OVERRIDE}" -eq 1 ]; then
  CONF_DIR="${HOME}/.config/gtk-4.0"
  mkdir -p "${CONF_DIR}"
  [ -f "${CONF_DIR}/gtk.css" ] && [ ! -L "${CONF_DIR}/gtk.css" ] && cp "${CONF_DIR}/gtk.css" "${CONF_DIR}/gtk.css.pre-nocturne"
  ln -sf "${THEME_DIR}/gtk-4.0/gtk.css" "${CONF_DIR}/gtk.css"
  echo "libadwaita best-effort override linked at ${CONF_DIR}/gtk.css (previous file saved as gtk.css.pre-nocturne if it existed)"
fi

cat <<'EOF'

Enable the theme:
  dconf write /org/gnome/shell/extensions/user-theme/name "'MT-Verdant-Nocturne'"
  gsettings set org.gnome.desktop.interface gtk-theme 'MT-Verdant-Nocturne'

Restore defaults (Adwaita):
  dconf write /org/gnome/shell/extensions/user-theme/name "''"
  gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
  rm -f ~/.config/gtk-4.0/gtk.css   # if --gtk4-libadwaita was used
EOF
