#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne at user level into ~/.themes ONLY (project policy).
# Checks for missing packages/modules per distro + GNOME version before building.
# Usage: tools/install.sh [--wallpaper] [--gtk4-libadwaita] [--install-deps]

set -eu

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
THEME_NAME="MT-Verdant-Nocturne"
THEME_DIR="${HOME}/.themes/${THEME_NAME}"
WANT_WALLPAPER=0
WANT_GTK4_OVERRIDE=0
INSTALL_DEPS=0

for arg in "$@"; do
  case "$arg" in
    --wallpaper) WANT_WALLPAPER=1 ;;
    --gtk4-libadwaita) WANT_GTK4_OVERRIDE=1 ;;
    --install-deps) INSTALL_DEPS=1 ;;
    *) echo "unknown option: $arg" >&2; exit 1 ;;
  esac
done

# ---------- distro + package-manager detection ----------
. /etc/os-release 2>/dev/null || ID=unknown
case "${ID:-unknown}" in
  ubuntu|debian)
    DEP_INSTALL="sudo apt-get install -y gnome-shell python3 python3-gi sassc python3-numpy python3-pil gnome-shell-extension-user-theme" ;;
  fedora)
    DEP_INSTALL="sudo dnf install -y gnome-shell python3 python3-gobject sassc python3-numpy python3-pillow gnome-shell-extension-user-theme" ;;
  arch)
    DEP_INSTALL="sudo pacman -S --needed gnome-shell python python-gobject sassc python-numpy python-pillow gnome-shell-extension-user-theme" ;;
  opensuse*)
    DEP_INSTALL="sudo zypper install gnome-shell python3 python3-gobject sassc python3-numpy python3-Pillow gnome-shell-extension-user-theme" ;;
  *)
    DEP_INSTALL="(unknown distro '${ID:-?}' — install: gnome-shell, python3 + gobject-introspection, sassc, numpy, Pillow, user-theme extension)" ;;
esac

# ---------- helpers ----------
have() { command -v "$1" >/dev/null 2>&1; }
py_has() { python3 -c "import $1" >/dev/null 2>&1; }

MISSING=""
miss() { MISSING="${MISSING}${MISSING:+, }$1"; }

# ---------- GNOME version gate ----------
if ! have gnome-shell; then
  miss "gnome-shell"
else
  SHELL_MAJOR="$(gnome-shell --version | grep -oE '[0-9]+' | head -1)"
  if [ "${SHELL_MAJOR}" -lt 50 ] 2>/dev/null; then
    echo "ERROR: GNOME Shell ${SHELL_MAJOR} is older than the supported minimum (50)." >&2
    exit 1
  fi
  if [ ! -f "${REPO_ROOT}/src/shell/colormap-${SHELL_MAJOR}.json" ]; then
    echo "ERROR: GNOME Shell ${SHELL_MAJOR} has no color map yet (src/shell/colormap-${SHELL_MAJOR}.json missing)." >&2
    exit 1
  fi
  echo "detected: ${PRETTY_NAME:-$ID} · GNOME Shell ${SHELL_MAJOR}"
fi

# ---------- what needs building (builds also imply toolchain needs) ----------
NEED_SHELL_BUILD=0; NEED_GTK_BUILD=0; NEED_WALLPAPER_GEN=0
[ -f "${REPO_ROOT}/build/theme/gnome-shell-${SHELL_MAJOR:-0}/gnome-shell.css" ] || NEED_SHELL_BUILD=1
[ -f "${REPO_ROOT}/build/theme/gtk-3.0/gtk-dark.css" ] || NEED_GTK_BUILD=1
[ "${WANT_WALLPAPER}" -eq 1 ] && [ ! -f "${REPO_ROOT}/wallpaper/dist/mt-verdant-nocturne-3840x2160.png" ] && NEED_WALLPAPER_GEN=1

# ---------- dependency checks (only for what we will actually run) ----------
have python3 || miss "python3"
if [ "${NEED_SHELL_BUILD}" -eq 1 ] || [ "${NEED_GTK_BUILD}" -eq 1 ]; then
  py_has gi || miss "python3 gobject-introspection (gi)"
fi
if [ "${NEED_GTK_BUILD}" -eq 1 ]; then
  have sassc || miss "sassc"
fi
if [ "${NEED_WALLPAPER_GEN}" -eq 1 ]; then
  py_has numpy || miss "python3-numpy"
  py_has PIL || miss "python3-pillow"
fi

if [ -n "${MISSING}" ]; then
  echo "missing requirements: ${MISSING}"
  echo "install them for this distro with:"
  echo "  ${DEP_INSTALL}"
  if [ "${INSTALL_DEPS}" -eq 1 ]; then
    echo "running (sudo used only here, for system packages):"
    sh -c "${DEP_INSTALL}"
  else
    echo "re-run with --install-deps to install them automatically, then retry."
    exit 1
  fi
fi

# ---------- builds (only the missing outputs) ----------
[ "${NEED_SHELL_BUILD}" -eq 0 ] || python3 "${REPO_ROOT}/tools/shell/build.py" --major "${SHELL_MAJOR}"
[ "${NEED_GTK_BUILD}" -eq 0 ] || python3 "${REPO_ROOT}/tools/gtk/build.py" >/dev/null
[ "${NEED_WALLPAPER_GEN}" -eq 0 ] || python3 "${REPO_ROOT}/tools/wallpaper/generate.py" >/dev/null

# ---------- install into ~/.themes (policy: user themes dir only) ----------
OLD_DIR="${HOME}/.local/share/themes/${THEME_NAME}"
if [ -d "${OLD_DIR}" ]; then
  # never hard-delete: park the previous user-level install inside the repo
  PARK="${REPO_ROOT}/deleted_files_folders"
  mkdir -p "${PARK}"
  mv "${OLD_DIR}" "${PARK}/${THEME_NAME}-local-share"
  echo "moved previous install from ${OLD_DIR} to ${PARK}/${THEME_NAME}-local-share"
fi

mkdir -p "${THEME_DIR}/gtk-4.0"
cp "${REPO_ROOT}/src/index.theme" "${THEME_DIR}/index.theme"
rm -rf "${THEME_DIR}/gnome-shell"
cp -r "${REPO_ROOT}/build/theme/gnome-shell-${SHELL_MAJOR}" "${THEME_DIR}/gnome-shell"
cp -r "${REPO_ROOT}/build/theme/gtk-3.0" "${THEME_DIR}/"
cp "${REPO_ROOT}/src/gtk-4.0/overrides.css" "${THEME_DIR}/gtk-4.0/gtk.css"
cp "${REPO_ROOT}/src/gtk-4.0/overrides.css" "${THEME_DIR}/gtk-4.0/gtk-dark.css"
echo "installed theme files to ${THEME_DIR}"

# ---------- optional: wallpaper (explicit opt-in) ----------
if [ "${WANT_WALLPAPER}" -eq 1 ]; then
  DEST="${HOME}/Pictures/mt-verdant-nocturne.png"
  mkdir -p "${HOME}/Pictures"
  cp "${REPO_ROOT}/wallpaper/dist/mt-verdant-nocturne-3840x2160.png" "${DEST}"
  gsettings set org.gnome.desktop.background picture-uri "file://${DEST}"
  gsettings set org.gnome.desktop.background picture-uri-dark "file://${DEST}"
  echo "wallpaper applied from ${DEST}"
fi

# ---------- optional: libadwaita best-effort override ----------
if [ "${WANT_GTK4_OVERRIDE}" -eq 1 ]; then
  CONF_DIR="${HOME}/.config/gtk-4.0"
  mkdir -p "${CONF_DIR}"
  [ -f "${CONF_DIR}/gtk.css" ] && [ ! -L "${CONF_DIR}/gtk.css" ] && cp "${CONF_DIR}/gtk.css" "${CONF_DIR}/gtk.css.pre-nocturne"
  ln -sf "${THEME_DIR}/gtk-4.0/gtk.css" "${CONF_DIR}/gtk.css"
  echo "libadwaita best-effort override linked at ${CONF_DIR}/gtk.css"
fi

# ---------- activation hint (user-theme extension check) ----------
if have gnome-extensions && ! gnome-extensions list 2>/dev/null | grep -q '^user-theme@'; then
  echo "NOTE: User Themes extension not found/enabled — Shell styling needs it:"
  echo "  ${DEP_INSTALL%%gnome-shell-extension-user-theme*}gnome-shell-extension-user-theme"
  echo "  then: gnome-extensions enable user-theme@gnome-shell-extensions.gcampax.github.com (re-login if new)"
fi

cat <<EOF

Enable the theme (no sudo):
  dconf write /org/gnome/shell/extensions/user-theme/name "'${THEME_NAME}'"
  gsettings set org.gnome.desktop.interface gtk-theme '${THEME_NAME}'

Restore defaults (Adwaita):
  dconf write /org/gnome/shell/extensions/user-theme/name "''"
  gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
  rm -f ~/.config/gtk-4.0/gtk.css   # if --gtk4-libadwaita was used
  gsettings set org.gnome.desktop.background picture-uri "file://\${HOME}/.config/background"  # revert wallpaper if set
EOF
