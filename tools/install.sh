#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne at user level into ~/.themes ONLY (project policy),
# and companion icon/cursor packs into ~/.icons ONLY.
# Supports modular --tweaks, --accent flavors, 4K wallpapers, and icon suite.
# Usage: tools/install.sh [--tweaks <list>] [--accent <flavor>] [--wallpaper [1-4|all]] [--icons] [--gtk4-libadwaita] [--install-deps]

set -eu

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
THEME_NAME="MT-Verdant-Nocturne"
THEME_DIR="${HOME}/.themes/${THEME_NAME}"
ICONS_DIR="${HOME}/.icons"
WANT_WALLPAPER=0
WALLPAPER_CHOICE="1"
WANT_GTK4_OVERRIDE=0
WANT_ICONS=0
INSTALL_DEPS=0
TWEAKS_ARG="float,translucent,macos"
ACCENT="sage"
THEME_SIZE="standard"
WANT_BLUR=1

# ---------- argument parsing ----------
while [ $# -gt 0 ]; do
  case "$1" in
    --tweaks)
      shift
      TWEAKS_ARG="${1:-float,translucent,macos}"
      ;;
    --tweaks=*)
      TWEAKS_ARG="${1#*=}"
      ;;
    --accent)
      shift
      ACCENT="${1:-sage}"
      ;;
    --accent=*)
      ACCENT="${1#*=}"
      ;;
    --size)
      shift
      THEME_SIZE="${1:-standard}"
      ;;
    --size=*)
      THEME_SIZE="${1#*=}"
      ;;
    --blur)
      WANT_BLUR=1
      ;;
    --no-blur|--noblur)
      WANT_BLUR=0
      ;;
    --icons)
      WANT_ICONS=1
      ;;
    --wallpaper)
      WANT_WALLPAPER=1
      if [ $# -gt 1 ] && [ "${2#-}" = "$2" ]; then
        shift
        WALLPAPER_CHOICE="$1"
      else
        WALLPAPER_CHOICE="1"
      fi
      ;;
    --wallpaper=*)
      WANT_WALLPAPER=1
      WALLPAPER_CHOICE="${1#*=}"
      ;;
    --gtk4-libadwaita)
      WANT_GTK4_OVERRIDE=1
      ;;
    --install-deps)
      INSTALL_DEPS=1
      ;;
    -h|--help)
      cat <<EOF
Usage: tools/install.sh [options]

Options:
  --tweaks <list>       Comma-separated tweaks (default: float,translucent,macos)
                        Choices: float, translucent, macos, black, compact, round, rimless, all, none
  --accent <flavor>     Accent color variant (default: sage)
                        Choices: sage, emerald, moss, pine
  --size <type>         Theme density sizing (choices: standard, compact; default: standard)
  --blur / --no-blur    Enable or disable glassmorphism blur and translucency
  --icons               Install and activate MT-Verdant-Icons and MT-Verdant-Cursors into ~/.icons
  --wallpaper [1-4|all] Apply 4K wallpaper (1: Canopy, 2: Aurora, 3: Flora, 4: River)
  --gtk4-libadwaita     Link GTK4 styles to ~/.config/gtk-4.0/gtk.css for libadwaita apps
  --install-deps        Automatically install missing system dependencies with sudo
  -h, --help            Show this help message
EOF
      exit 0
      ;;
    *)
      echo "unknown option: $1" >&2
      exit 1
      ;;
  esac
  shift
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

# ---------- what needs building ----------
NEED_SHELL_BUILD=0; NEED_GTK_BUILD=0; NEED_WALLPAPER_GEN=0; NEED_ICONS_GEN=0
[ -f "${REPO_ROOT}/build/theme/gnome-shell-${SHELL_MAJOR:-0}/gnome-shell.css" ] || NEED_SHELL_BUILD=1
[ -f "${REPO_ROOT}/build/theme/gtk-3.0/gtk-dark.css" ] || NEED_GTK_BUILD=1
[ -f "${REPO_ROOT}/wallpaper/dist/mt-verdant-canopy-3840x2160.png" ] || NEED_WALLPAPER_GEN=1
[ -f "${REPO_ROOT}/src/icons/MT-Verdant-Icons/index.theme" ] || NEED_ICONS_GEN=1

# ---------- dependency checks ----------
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

# ---------- builds (only missing outputs) ----------
[ "${NEED_SHELL_BUILD}" -eq 0 ] || python3 "${REPO_ROOT}/tools/shell/build.py" --major "${SHELL_MAJOR}"
[ "${NEED_GTK_BUILD}" -eq 0 ] || python3 "${REPO_ROOT}/tools/gtk/build.py" >/dev/null
[ "${NEED_WALLPAPER_GEN}" -eq 0 ] || python3 "${REPO_ROOT}/tools/wallpaper/generate.py" >/dev/null
if [ "${NEED_ICONS_GEN}" -eq 1 ]; then
  python3 "${REPO_ROOT}/tools/icons/generate_icons.py" >/dev/null
  python3 "${REPO_ROOT}/tools/icons/generate_cursors.py" >/dev/null
fi

# ---------- install into ~/.themes (policy: user themes dir only) ----------
OLD_DIR="${HOME}/.local/share/themes/${THEME_NAME}"
if [ -d "${OLD_DIR}" ]; then
  PARK="${REPO_ROOT}/deleted_files_folders"
  mkdir -p "${PARK}"
  mv "${OLD_DIR}" "${PARK}/${THEME_NAME}-local-share"
  echo "moved previous install from ${OLD_DIR} to ${PARK}/${THEME_NAME}-local-share"
fi

mkdir -p "${THEME_DIR}/gtk-4.0"
mkdir -p "${THEME_DIR}/wallpapers"
mkdir -p "${THEME_DIR}/extras"
cp "${REPO_ROOT}/src/index.theme" "${THEME_DIR}/index.theme"
rm -rf "${THEME_DIR}/gnome-shell"
cp -r "${REPO_ROOT}/build/theme/gnome-shell-${SHELL_MAJOR}" "${THEME_DIR}/gnome-shell"
cp -r "${REPO_ROOT}/build/theme/gtk-3.0" "${THEME_DIR}/"
cp "${REPO_ROOT}/src/gtk-4.0/overrides.css" "${THEME_DIR}/gtk-4.0/gtk.css"
cp "${REPO_ROOT}/src/gtk-4.0/overrides.css" "${THEME_DIR}/gtk-4.0/gtk-dark.css"

if [ -f "${REPO_ROOT}/src/gtk-2.0/gtkrc" ]; then
  mkdir -p "${THEME_DIR}/gtk-2.0"
  cp "${REPO_ROOT}/src/gtk-2.0/gtkrc" "${THEME_DIR}/gtk-2.0/gtkrc"
fi

# Copy wallpapers and extras into the theme folder
if [ -d "${REPO_ROOT}/wallpaper/dist" ]; then
  cp "${REPO_ROOT}/wallpaper/dist/"*.png "${THEME_DIR}/wallpapers/" 2>/dev/null || true
fi
if [ -d "${REPO_ROOT}/extras" ]; then
  cp -r "${REPO_ROOT}/extras/"* "${THEME_DIR}/extras/" 2>/dev/null || true
fi

# ---------- apply base polish layer ----------
cat "${REPO_ROOT}/src/tweaks/shell/polish.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
cat "${REPO_ROOT}/src/tweaks/gtk/polish.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
cat "${REPO_ROOT}/src/tweaks/gtk/polish.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
cat "${REPO_ROOT}/src/tweaks/gtk/polish.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
cat "${REPO_ROOT}/src/tweaks/gtk/polish.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"

# ---------- apply modular tweaks ----------
if [ "${TWEAKS_ARG}" = "all" ]; then
  TWEAKS_LIST="float,translucent,macos,round"
elif [ "${TWEAKS_ARG}" = "none" ]; then
  TWEAKS_LIST=""
else
  TWEAKS_LIST="$(echo "${TWEAKS_ARG}" | tr ' ' ',')"
fi

echo "applying tweaks: ${TWEAKS_LIST:-default base polish}"

OLD_IFS="${IFS}"
IFS=","
for tweak in ${TWEAKS_LIST}; do
  case "${tweak}" in
    float)
      [ -f "${REPO_ROOT}/src/tweaks/shell/float.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/float.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
      echo "  + float (floating pill top bar)"
      ;;
    translucent)
      [ -f "${REPO_ROOT}/src/tweaks/shell/translucent.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/translucent.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
      echo "  + translucent (frosted glass panel)"
      ;;
    macos|circle)
      if [ -f "${REPO_ROOT}/src/tweaks/gtk/macos.css" ]; then
        cat "${REPO_ROOT}/src/tweaks/gtk/macos.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/macos.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/macos.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/macos.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
      fi
      echo "  + macos (circular window control dots)"
      ;;
    black|oled)
      [ -f "${REPO_ROOT}/src/tweaks/shell/black.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/black.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
      if [ -f "${REPO_ROOT}/src/tweaks/gtk/black.css" ]; then
        cat "${REPO_ROOT}/src/tweaks/gtk/black.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/black.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/black.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/black.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
      fi
      echo "  + black (OLED pitch-black background)"
      ;;
    compact)
      [ -f "${REPO_ROOT}/src/tweaks/shell/compact.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/compact.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
      if [ -f "${REPO_ROOT}/src/tweaks/gtk/compact.css" ]; then
        cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
      fi
      echo "  + compact (slim headerbars & padding)"
      ;;
    round)
      [ -f "${REPO_ROOT}/src/tweaks/shell/round.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/round.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
      if [ -f "${REPO_ROOT}/src/tweaks/gtk/round.css" ]; then
        cat "${REPO_ROOT}/src/tweaks/gtk/round.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/round.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/round.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/round.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
      fi
      echo "  + round (16px modern curved geometry)"
      ;;
    rimless)
      if [ -f "${REPO_ROOT}/src/tweaks/gtk/rimless.css" ]; then
        cat "${REPO_ROOT}/src/tweaks/gtk/rimless.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/rimless.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/rimless.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
        cat "${REPO_ROOT}/src/tweaks/gtk/rimless.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
      fi
      echo "  + rimless (borderless clean windows)"
      ;;
    noblur|no-blur)
      WANT_BLUR=0
      ;;
    blur)
      WANT_BLUR=1
      ;;
    *)
      [ -z "${tweak}" ] || echo "  ! unknown tweak: ${tweak} (ignored)"
      ;;
  esac
done
IFS="${OLD_IFS}"

# ---------- apply sizing and blur overrides ----------
if [ "${THEME_SIZE}" = "compact" ] && ! echo "${TWEAKS_LIST}" | grep -q "compact"; then
  [ -f "${REPO_ROOT}/src/tweaks/shell/compact.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/compact.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
  if [ -f "${REPO_ROOT}/src/tweaks/gtk/compact.css" ]; then
    cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
  fi
  echo "  + sizing: compact"
fi

if [ "${WANT_BLUR}" -eq 0 ]; then
  [ -f "${REPO_ROOT}/src/tweaks/shell/noblur.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/noblur.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
  if [ -f "${REPO_ROOT}/src/tweaks/gtk/noblur.css" ]; then
    cat "${REPO_ROOT}/src/tweaks/gtk/noblur.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/noblur.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/noblur.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/noblur.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
  fi
  echo "  + blur: disabled (solid opaque surfaces)"
fi

# ---------- apply accent flavor ----------
if [ "${ACCENT}" != "sage" ] && [ -f "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" ]; then
  cat "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
  cat "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
  cat "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
  cat "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
  echo "applied accent flavor: ${ACCENT}"
fi

echo "installed theme files to ${THEME_DIR}"

# ---------- optional: icons & cursors (user ~/.icons only) ----------
if [ "${WANT_ICONS}" -eq 1 ]; then
  mkdir -p "${ICONS_DIR}"
  if [ -d "${REPO_ROOT}/src/icons/MT-Verdant-Icons" ]; then
    rm -rf "${ICONS_DIR}/MT-Verdant-Icons"
    cp -r "${REPO_ROOT}/src/icons/MT-Verdant-Icons" "${ICONS_DIR}/"
    have gtk-update-icon-cache && gtk-update-icon-cache -f -t "${ICONS_DIR}/MT-Verdant-Icons" >/dev/null 2>&1 || true
    gsettings set org.gnome.desktop.interface icon-theme 'MT-Verdant-Icons' || true
    echo "installed and activated icon pack in ${ICONS_DIR}/MT-Verdant-Icons"
  fi
  if [ -d "${REPO_ROOT}/src/cursors/MT-Verdant-Cursors" ]; then
    rm -rf "${ICONS_DIR}/MT-Verdant-Cursors"
    cp -r "${REPO_ROOT}/src/cursors/MT-Verdant-Cursors" "${ICONS_DIR}/"
    gsettings set org.gnome.desktop.interface cursor-theme 'MT-Verdant-Cursors' || true
    echo "installed and activated cursor pack in ${ICONS_DIR}/MT-Verdant-Cursors"
  fi
fi

# ---------- optional: wallpaper (explicit opt-in) ----------
if [ "${WANT_WALLPAPER}" -eq 1 ]; then
  case "${WALLPAPER_CHOICE}" in
    1|canopy)
      WP_SRC="${REPO_ROOT}/wallpaper/dist/mt-verdant-canopy-3840x2160.png"
      WP_NAME="mt-verdant-canopy.png"
      ;;
    2|aurora)
      WP_SRC="${REPO_ROOT}/wallpaper/dist/mt-verdant-aurora-3840x2160.png"
      WP_NAME="mt-verdant-aurora.png"
      ;;
    3|flora)
      WP_SRC="${REPO_ROOT}/wallpaper/dist/mt-verdant-flora-3840x2160.png"
      WP_NAME="mt-verdant-flora.png"
      ;;
    4|river)
      WP_SRC="${REPO_ROOT}/wallpaper/dist/mt-verdant-river-3840x2160.png"
      WP_NAME="mt-verdant-river.png"
      ;;
    all)
      WP_SRC="${REPO_ROOT}/wallpaper/dist/mt-verdant-canopy-3840x2160.png"
      WP_NAME="mt-verdant-canopy.png"
      mkdir -p "${HOME}/Pictures/wallpapers-mt-verdant"
      cp "${REPO_ROOT}/wallpaper/dist/"*.png "${HOME}/Pictures/wallpapers-mt-verdant/"
      echo "all 4 wallpapers copied to ~/Pictures/wallpapers-mt-verdant/"
      ;;
    *)
      WP_SRC="${REPO_ROOT}/wallpaper/dist/mt-verdant-canopy-3840x2160.png"
      WP_NAME="mt-verdant-canopy.png"
      ;;
  esac

  DEST="${HOME}/Pictures/${WP_NAME}"
  mkdir -p "${HOME}/Pictures"
  cp "${WP_SRC}" "${DEST}"
  gsettings set org.gnome.desktop.background picture-uri "file://${DEST}"
  gsettings set org.gnome.desktop.background picture-uri-dark "file://${DEST}"
  echo "wallpaper applied: ${DEST}"
fi

# ---------- optional: libadwaita best-effort override ----------
if [ "${WANT_GTK4_OVERRIDE}" -eq 1 ]; then
  CONF_DIR="${HOME}/.config/gtk-4.0"
  mkdir -p "${CONF_DIR}"
  [ -f "${CONF_DIR}/gtk.css" ] && [ ! -L "${CONF_DIR}/gtk.css" ] && cp "${CONF_DIR}/gtk.css" "${CONF_DIR}/gtk.css.pre-nocturne"
  [ -f "${CONF_DIR}/gtk-dark.css" ] && [ ! -L "${CONF_DIR}/gtk-dark.css" ] && cp "${CONF_DIR}/gtk-dark.css" "${CONF_DIR}/gtk-dark.css.pre-nocturne"
  ln -sf "${THEME_DIR}/gtk-4.0/gtk.css" "${CONF_DIR}/gtk.css"
  ln -sf "${THEME_DIR}/gtk-4.0/gtk-dark.css" "${CONF_DIR}/gtk-dark.css"
  echo "libadwaita best-effort override linked at ${CONF_DIR}/gtk.css and gtk-dark.css"
fi

# ---------- activation hint ----------
if have gnome-extensions && ! gnome-extensions list 2>/dev/null | grep -q '^user-theme@'; then
  echo "NOTE: User Themes extension not found/enabled — Shell styling needs it:"
  echo "  ${DEP_INSTALL%%gnome-shell-extension-user-theme*}gnome-shell-extension-user-theme"
  echo "  then: gnome-extensions enable user-theme@gnome-shell-extensions.gcampax.github.com (re-login if new)"
fi

cat <<EOF

Enable the theme (no sudo):
  dconf write /org/gnome/shell/extensions/user-theme/name "'${THEME_NAME}'"
  gsettings set org.gnome.desktop.interface gtk-theme '${THEME_NAME}'
  gsettings set org.gnome.desktop.interface icon-theme 'MT-Verdant-Icons'
  gsettings set org.gnome.desktop.interface cursor-theme 'MT-Verdant-Cursors'

Assets location:
  Theme directory:    ${THEME_DIR}
  Wallpapers (4K):    ${THEME_DIR}/wallpapers/
  Extras (Firefox):   ${THEME_DIR}/extras/firefox/
  Extras (VS Code):   ${THEME_DIR}/extras/vscode/
  Extras (Plymouth):  ${THEME_DIR}/extras/plymouth/

Restore defaults (Adwaita):
  dconf write /org/gnome/shell/extensions/user-theme/name "''"
  gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
  gsettings set org.gnome.desktop.interface icon-theme 'Adwaita'
  gsettings set org.gnome.desktop.interface cursor-theme 'Adwaita'
  rm -f ~/.config/gtk-4.0/gtk.css   # if --gtk4-libadwaita was used
EOF
