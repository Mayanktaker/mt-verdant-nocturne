#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne at user level into ~/.themes ONLY (project policy),
# and companion icon/cursor packs into ~/.icons ONLY.
# Supports interactive CLI wizard, human-friendly settings, modular tweaks, and 4K wallpapers.

set -eu

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
THEME_NAME="MT-Verdant-Nocturne"
THEME_DIR="${HOME}/.themes/${THEME_NAME}"
ICONS_DIR="${HOME}/.icons"

# Defaults
PANEL_STYLE="round-island"   # Choices: round-island, pill, bottom-round, flat
CONTROLS="standard"          # Choices: standard, macos
ACCENT="sage"                # Choices: sage, emerald, moss, pine
THEME_SIZE="standard"        # Choices: standard, compact
WANT_BLUR=1
WANT_ICONS=1
WANT_GTK4_OVERRIDE=1
WANT_WALLPAPER=0
WALLPAPER_CHOICE="none"
INSTALL_DEPS=0
INTERACTIVE=0
EXPLICIT_ARGS=0
TWEAKS_ARG=""

# Detect if stdin is an interactive terminal and no arguments were passed
if [ $# -eq 0 ] && [ -t 0 ]; then
  INTERACTIVE=1
fi

# ---------- argument parsing ----------
while [ $# -gt 0 ]; do
  EXPLICIT_ARGS=1
  case "$1" in
    --wizard)
      INTERACTIVE=1
      ;;
    --non-interactive|--no-interactive)
      INTERACTIVE=0
      ;;
    --panel|--tray)
      shift
      PANEL_STYLE="${1:-round-island}"
      ;;
    --panel=*|--tray=*)
      PANEL_STYLE="${1#*=}"
      ;;
    --controls)
      shift
      CONTROLS="${1:-standard}"
      ;;
    --controls=*)
      CONTROLS="${1#*=}"
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
    --no-icons)
      WANT_ICONS=0
      ;;
    --gtk4-libadwaita)
      WANT_GTK4_OVERRIDE=1
      ;;
    --no-gtk4-libadwaita)
      WANT_GTK4_OVERRIDE=0
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
    --tweaks)
      shift
      TWEAKS_ARG="${1:-float,translucent,round}"
      ;;
    --tweaks=*)
      TWEAKS_ARG="${1#*=}"
      ;;
    --install-deps)
      INSTALL_DEPS=1
      ;;
    -h|--help)
      cat <<EOF
Usage: tools/install.sh [options]

Run without arguments in an interactive terminal to launch the setup wizard.

User-Friendly Options:
  --panel, --tray <style> Top bar / tray style:
                            round-island : 16px curved floating island (Default)
                            pill         : 999px full circular capsule ends
                            bottom-round : Connected to top edge with 16px bottom rounded corners
                            flat         : Classic full-width edge-to-edge square bar
  --controls <style>      Window controls style: standard (native Adwaita) or macos (colored traffic dots)
  --accent <flavor>       Botanical accent color: sage (default), emerald, moss, pine
  --size <type>           Theme density sizing: standard (default) or compact
  --blur / --no-blur      Enable or disable frosted glassmorphism blur and translucency
  --icons / --no-icons    Install companion MT-Verdant-Icons and MT-Verdant-Cursors into ~/.icons
  --gtk4-libadwaita       Link GTK4 styles to ~/.config/gtk-4.0/gtk.css for libadwaita apps
  --wallpaper [choice]    Apply 4K wallpaper (1: Canopy, 2: Aurora, 3: Flora, 4: River, all, none)
  --wizard                Force interactive step-by-step setup wizard
  --non-interactive       Skip wizard and apply specified options or defaults directly
  --install-deps          Automatically install missing system dependencies with sudo
  -h, --help              Show this help message
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

# ---------- interactive wizard ----------
if [ "${INTERACTIVE}" -eq 1 ]; then
  cat <<'EOF'
========================================================================
  🌿 MT Verdant Nocturne — Botanical Dark Theme Suite Installer
========================================================================
Welcome! Press Enter at any prompt to accept the [Default] option.
EOF

  # 1. Top Bar / System Tray Style
  echo ""
  echo "1. System Tray & Top Bar Style:"
  echo "   [1] Rounded Modern Island (16px curved floating bar) [Default]"
  echo "   [2] Floating Pill Capsule (Full circular 999px capsule ends)"
  echo "   [3] Connected Bottom-Rounded (Attached to screen top, 16px bottom rounded corners)"
  echo "   [4] Classic Flat Bar (Full-width edge-to-edge square bar)"
  printf "   Select [1-4, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) PANEL_STYLE="pill" ;;
    3) PANEL_STYLE="bottom-round" ;;
    4) PANEL_STYLE="flat" ;;
    *) PANEL_STYLE="round-island" ;;
  esac

  # 2. Window Controls
  echo ""
  echo "2. Window Control Buttons (Titlebar):"
  echo "   [1] Standard Native (Themed Adwaita clean buttons) [Default]"
  echo "   [2] macOS Traffic Lights (Circular red/yellow/green dots)"
  printf "   Select [1-2, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) CONTROLS="macos" ;;
    *) CONTROLS="standard" ;;
  esac

  # 3. Theme Sizing / Density
  echo ""
  echo "3. Theme Density / Padding:"
  echo "   [1] Standard (Balanced comfort spacing for desktop) [Default]"
  echo "   [2] Compact (Slim headerbars & tighter padding for laptops)"
  printf "   Select [1-2, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) THEME_SIZE="compact" ;;
    *) THEME_SIZE="standard" ;;
  esac

  # 4. Glassmorphism / Blur
  echo ""
  echo "4. Glassmorphism & Translucency:"
  echo "   [1] Frosted Blur & Translucency [Default]"
  echo "   [2] Solid Opaque Surfaces (Optimal for low-end GPUs)"
  printf "   Select [1-2, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) WANT_BLUR=0 ;;
    *) WANT_BLUR=1 ;;
  esac

  # 5. Botanical Accent Flavor
  echo ""
  echo "5. Accent Color Variant:"
  echo "   [1] Sage (#7FC8A0 - Balanced mint green) [Default]"
  echo "   [2] Emerald (#3DD68C - Luminous vibrant forest green)"
  echo "   [3] Moss (#9ECB74 - Warm olive foliage)"
  echo "   [4] Pine (#3D8B7A - Deep twilight teal)"
  printf "   Select [1-4, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) ACCENT="emerald" ;;
    3) ACCENT="moss" ;;
    4) ACCENT="pine" ;;
    *) ACCENT="sage" ;;
  esac

  # 6. Companion Icon & Cursor Suite
  echo ""
  echo "6. Install Companion Icon & Cursor Suite (MT-Verdant-Icons & Cursors)?"
  echo "   [1] Yes (Install and activate into ~/.icons) [Default]"
  echo "   [2] No"
  printf "   Select [1-2, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) WANT_ICONS=0 ;;
    *) WANT_ICONS=1 ;;
  esac

  # 7. GTK4 / Libadwaita Override
  echo ""
  echo "7. Apply GTK4 / Libadwaita Theme Override (~/.config/gtk-4.0)?"
  echo "   [1] Yes (Themed style for Settings, Nautilus, Console) [Default]"
  echo "   [2] No"
  printf "   Select [1-2, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) WANT_GTK4_OVERRIDE=0 ;;
    *) WANT_GTK4_OVERRIDE=1 ;;
  esac

  # 8. 4K Botanical Wallpaper
  echo ""
  echo "8. 4K Botanical Canopy Wallpaper:"
  echo "   [1] Canopy (Lush forest leaves) [Default]"
  echo "   [2] Aurora (Emerald northern lights)"
  echo "   [3] Flora (Botanical bloom)"
  echo "   [4] River (Mist river canopy)"
  echo "   [5] All 4 Wallpapers (Copy to ~/Pictures/wallpapers-mt-verdant)"
  echo "   [6] None (Keep current wallpaper)"
  printf "   Select [1-6, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) WANT_WALLPAPER=1; WALLPAPER_CHOICE="2" ;;
    3) WANT_WALLPAPER=1; WALLPAPER_CHOICE="3" ;;
    4) WANT_WALLPAPER=1; WALLPAPER_CHOICE="4" ;;
    5) WANT_WALLPAPER=1; WALLPAPER_CHOICE="all" ;;
    6|none) WANT_WALLPAPER=0; WALLPAPER_CHOICE="none" ;;
    *) WANT_WALLPAPER=1; WALLPAPER_CHOICE="1" ;;
  esac

  echo ""
  echo "Configuration summary:"
  echo "  - Top Bar Style:     ${PANEL_STYLE}"
  echo "  - Window Controls:   ${CONTROLS}"
  echo "  - Theme Density:     ${THEME_SIZE}"
  echo "  - Surface Blur:      $([ "${WANT_BLUR}" -eq 1 ] && echo "Enabled" || echo "Disabled")"
  echo "  - Accent Flavor:     ${ACCENT}"
  echo "  - Icons & Cursors:   $([ "${WANT_ICONS}" -eq 1 ] && echo "Install to ~/.icons" || echo "Skip")"
  echo "  - GTK4 / Libadwaita: $([ "${WANT_GTK4_OVERRIDE}" -eq 1 ] && echo "Linked" || echo "Skip")"
  echo "  - 4K Wallpaper:      ${WALLPAPER_CHOICE}"
  echo ""
fi

# ---------- legacy tweaks mapping (backwards compatibility) ----------
if [ -n "${TWEAKS_ARG}" ]; then
  echo "${TWEAKS_ARG}" | grep -q "macos" && CONTROLS="macos"
  echo "${TWEAKS_ARG}" | grep -q "compact" && THEME_SIZE="compact"
  if echo "${TWEAKS_ARG}" | grep -q "float"; then
    PANEL_STYLE="pill"
  elif echo "${TWEAKS_ARG}" | grep -q "round"; then
    PANEL_STYLE="round-island"
  fi
  echo "${TWEAKS_ARG}" | grep -q "noblur" && WANT_BLUR=0
fi

# ---------- distro + package-manager detection ----------
. /etc/os-release 2>/dev/null || ID=unknown
case "${ID:-unknown}" in
  ubuntu|debian)
    DEP_INSTALL="sudo apt-get install -y gnome-shell python3 python3-gi sassc python3-numpy python3-pil gnome-shell-extension-user-theme" ;;
  fedora)
    DEP_INSTALL="sudo dnf install -y gnome-shell python3 python3-gobject sassc python3-numpy python3-pillow gnome-shell-extension-user-theme" ;;
  arch|cachyos)
    DEP_INSTALL="sudo pacman -S --needed gnome-shell python python-gobject sassc python-numpy python-pillow gnome-shell-extension-user-theme" ;;
  opensuse*)
    DEP_INSTALL="sudo zypper install gnome-shell python3 python3-gobject sassc python3-numpy python3-Pillow gnome-shell-extension-user-theme" ;;
  *)
    DEP_INSTALL="(unknown distro '${ID:-?}' — install: gnome-shell, python3 + gobject-introspection, sassc, numpy, Pillow, user-theme extension)" ;;
esac

# ---------- helpers ----------
have() { command -v "$1" >/dev/null 2>&1; }
py_has() { python3 -c "import $1" >/dev/null 2>&1; }
miss() { MISSING="${MISSING:-}${MISSING:+; }$1"; }

# ---------- shell version detection & build check ----------
have gnome-shell || { echo "gnome-shell not found on PATH" >&2; exit 1; }
SHELL_VERSION="$(gnome-shell --version)"
SHELL_MAJOR="$(echo "${SHELL_VERSION}" | sed -E 's/[^0-9]*([0-9]+).*/\1/')"

if [ "${SHELL_MAJOR}" -lt 50 ]; then
  echo "GNOME Shell ${SHELL_MAJOR} is unsupported; MT Verdant Nocturne targets 50.x and 51.x." >&2
  exit 1
fi

[ -f "${REPO_ROOT}/src/shell/colormap-${SHELL_MAJOR}.json" ] || {
  echo "missing src/shell/colormap-${SHELL_MAJOR}.json — Shell ${SHELL_MAJOR} not yet mapped." >&2
  exit 1
}

echo "detected: ${ID:-unknown} · GNOME Shell ${SHELL_MAJOR}"

# Determine which build artifacts are missing
NEED_SHELL_BUILD=0
NEED_GTK_BUILD=0
NEED_WALLPAPER_GEN=0
NEED_ICONS_GEN=0

[ -f "${REPO_ROOT}/build/theme/gnome-shell-${SHELL_MAJOR}/gnome-shell.css" ] || NEED_SHELL_BUILD=1
[ -f "${REPO_ROOT}/build/theme/gtk-3.0/gtk.css" ] || NEED_GTK_BUILD=1
[ -f "${REPO_ROOT}/wallpaper/dist/mt-verdant-canopy-3840x2160.png" ] || NEED_WALLPAPER_GEN=1
[ -d "${REPO_ROOT}/src/icons/MT-Verdant-Icons" ] || NEED_ICONS_GEN=1

MISSING=""

# ---------- dependency checks ----------
have python3 || miss "python3"
if [ "${NEED_SHELL_BUILD}" -eq 1 ] || [ "${NEED_GTK_BUILD}" -eq 1 ]; then
  py_has gi || miss "python3 gobject-introspection (gi)"
fi
if [ "${NEED_GTK_BUILD}" -eq 1 ]; then
  have sassc || miss "sassc"
fi
if [ "${NEED_WALLPAPER_GEN}" -ne 0 ]; then
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
if [ "${NEED_WALLPAPER_GEN}" -ne 0 ]; then
  python3 "${REPO_ROOT}/tools/wallpaper/generate.py" >/dev/null
  python3 "${REPO_ROOT}/tools/wallpaper/process_light.py" >/dev/null
fi
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

# Copy wallpapers, instantiate dynamic XMLs, and register with GNOME Settings
if [ -d "${REPO_ROOT}/wallpaper/dist" ]; then
  cp -r "${REPO_ROOT}/wallpaper/dist/"* "${THEME_DIR}/wallpapers/" 2>/dev/null || true
  if [ -f "${THEME_DIR}/wallpapers/mt-verdant-timed.xml.in" ]; then
    sed "s|@WALLPAPER_DIR@|${THEME_DIR}/wallpapers|g" "${THEME_DIR}/wallpapers/mt-verdant-timed.xml.in" > "${THEME_DIR}/wallpapers/mt-verdant-timed.xml"
  fi
  if [ -f "${THEME_DIR}/wallpapers/gnome-background-properties.xml.in" ]; then
    sed "s|@WALLPAPER_DIR@|${THEME_DIR}/wallpapers|g" "${THEME_DIR}/wallpapers/gnome-background-properties.xml.in" > "${THEME_DIR}/wallpapers/gnome-background-properties.xml"
  fi
  mkdir -p "${HOME}/.local/share/gnome-background-properties"
  cp "${THEME_DIR}/wallpapers/gnome-background-properties.xml" "${HOME}/.local/share/gnome-background-properties/mt-verdant.xml" 2>/dev/null || true
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

# ---------- apply top bar / system tray style ----------
case "${PANEL_STYLE}" in
  round-island)
    [ -f "${REPO_ROOT}/src/tweaks/shell/tray-round.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/tray-round.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
    echo "  + top bar: rounded modern island (16px curved floating bar)"
    # Disable blur-my-shell panel blur to eliminate duplicate background actor collision
    if have dconf && [ -d "${HOME}/.local/share/gnome-shell/extensions/blur-my-shell@aunetx" ]; then
      dconf write /org/gnome/shell/extensions/blur-my-shell/panel/blur false 2>/dev/null || true
      dconf write /org/gnome/shell/extensions/blur-my-shell/panel/override-background false 2>/dev/null || true
    fi
    ;;
  pill)
    [ -f "${REPO_ROOT}/src/tweaks/shell/tray-pill.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/tray-pill.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
    echo "  + top bar: floating pill capsule (999px circular ends)"
    if have dconf && [ -d "${HOME}/.local/share/gnome-shell/extensions/blur-my-shell@aunetx" ]; then
      dconf write /org/gnome/shell/extensions/blur-my-shell/panel/blur false 2>/dev/null || true
      dconf write /org/gnome/shell/extensions/blur-my-shell/panel/override-background false 2>/dev/null || true
    fi
    ;;
  bottom-round)
    [ -f "${REPO_ROOT}/src/tweaks/shell/tray-bottom-round.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/tray-bottom-round.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
    echo "  + top bar: bottom-rounded (connected to top edge)"
    if have dconf && [ -d "${HOME}/.local/share/gnome-shell/extensions/blur-my-shell@aunetx" ]; then
      dconf write /org/gnome/shell/extensions/blur-my-shell/panel/blur false 2>/dev/null || true
      dconf write /org/gnome/shell/extensions/blur-my-shell/panel/override-background false 2>/dev/null || true
    fi
    ;;
  flat)
    echo "  + top bar: classic edge-to-edge square bar"
    if have dconf && [ -d "${HOME}/.local/share/gnome-shell/extensions/blur-my-shell@aunetx" ]; then
      dconf write /org/gnome/shell/extensions/blur-my-shell/panel/blur true 2>/dev/null || true
      dconf write /org/gnome/shell/extensions/blur-my-shell/panel/corner-radius 0 2>/dev/null || true
    fi
    ;;
esac

# ---------- apply surface blur & translucency ----------
if [ "${WANT_BLUR}" -eq 1 ]; then
  [ -f "${REPO_ROOT}/src/tweaks/shell/translucent.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/translucent.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
  echo "  + surface: frosted glass translucency & blur enabled"
else
  [ -f "${REPO_ROOT}/src/tweaks/shell/noblur.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/noblur.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
  if [ -f "${REPO_ROOT}/src/tweaks/gtk/noblur.css" ]; then
    cat "${REPO_ROOT}/src/tweaks/gtk/noblur.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/noblur.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/noblur.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/noblur.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
  fi
  echo "  + surface: solid opaque surfaces"
fi

# ---------- apply modern 16px geometry ----------
[ -f "${REPO_ROOT}/src/tweaks/shell/round.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/round.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
if [ -f "${REPO_ROOT}/src/tweaks/gtk/round.css" ]; then
  cat "${REPO_ROOT}/src/tweaks/gtk/round.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
  cat "${REPO_ROOT}/src/tweaks/gtk/round.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
  cat "${REPO_ROOT}/src/tweaks/gtk/round.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
  cat "${REPO_ROOT}/src/tweaks/gtk/round.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
fi

# ---------- apply window controls (buttons) ----------
if [ "${CONTROLS}" = "macos" ]; then
  if [ -f "${REPO_ROOT}/src/tweaks/gtk/macos.css" ]; then
    cat "${REPO_ROOT}/src/tweaks/gtk/macos.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/macos.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/macos.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/macos.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
  fi
  echo "  + window controls: macOS traffic dots (red/yellow/green)"
else
  echo "  + window controls: standard Adwaita clean buttons"
fi

# ---------- apply theme sizing / density ----------
if [ "${THEME_SIZE}" = "compact" ]; then
  [ -f "${REPO_ROOT}/src/tweaks/shell/compact.css" ] && cat "${REPO_ROOT}/src/tweaks/shell/compact.css" >> "${THEME_DIR}/gnome-shell/gnome-shell.css"
  if [ -f "${REPO_ROOT}/src/tweaks/gtk/compact.css" ]; then
    cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
    cat "${REPO_ROOT}/src/tweaks/gtk/compact.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
  fi
  echo "  + theme density: compact (slim padding)"
else
  echo "  + theme density: standard"
fi

# ---------- apply accent flavor ----------
if [ "${ACCENT}" != "sage" ] && [ -f "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" ]; then
  cat "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" >> "${THEME_DIR}/gtk-3.0/gtk.css"
  cat "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" >> "${THEME_DIR}/gtk-3.0/gtk-dark.css"
  cat "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" >> "${THEME_DIR}/gtk-4.0/gtk.css"
  cat "${REPO_ROOT}/src/tweaks/gtk/accent-${ACCENT}.css" >> "${THEME_DIR}/gtk-4.0/gtk-dark.css"
  echo "  + accent color: ${ACCENT}"
else
  echo "  + accent color: sage (#7FC8A0)"
fi

echo "installed theme files to ${THEME_DIR}"

# ---------- optional: icons & cursors (user ~/.icons only) ----------
if [ "${WANT_ICONS}" -eq 1 ]; then
  mkdir -p "${ICONS_DIR}"
  if [ -d "${REPO_ROOT}/src/icons/MT-Verdant-Icons" ]; then
    rm -rf "${ICONS_DIR}/MT-Verdant-Icons"
    cp -r "${REPO_ROOT}/src/icons/MT-Verdant-Icons" "${ICONS_DIR}/"
    if command -v gtk-update-icon-cache >/dev/null 2>&1; then
      gtk-update-icon-cache -f -t "${ICONS_DIR}/MT-Verdant-Icons" >/dev/null 2>&1 || true
    fi
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
if [ "${WANT_WALLPAPER}" -eq 1 ] && [ "${WALLPAPER_CHOICE}" != "none" ]; then
  WP_SRC=""
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

  if [ -n "${WP_SRC}" ] && [ -f "${WP_SRC}" ]; then
    DEST="${HOME}/Pictures/${WP_NAME}"
    mkdir -p "${HOME}/Pictures"
    cp "${WP_SRC}" "${DEST}"
    gsettings set org.gnome.desktop.background picture-uri "file://${DEST}"
    gsettings set org.gnome.desktop.background picture-uri-dark "file://${DEST}"
    echo "wallpaper applied: ${DEST}"
  fi
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

# ---------- GNOME settings activation ----------
if have dconf; then
  dconf write /org/gnome/shell/extensions/user-theme/name "'${THEME_NAME}'" || true
fi
if have gsettings; then
  gsettings set org.gnome.desktop.interface gtk-theme "${THEME_NAME}" || true
  if [ "${WANT_ICONS}" -eq 1 ]; then
    gsettings set org.gnome.desktop.interface icon-theme 'MT-Verdant-Icons' || true
    gsettings set org.gnome.desktop.interface cursor-theme 'MT-Verdant-Cursors' || true
  fi
fi

# ---------- activation hint ----------
if have gnome-extensions && ! gnome-extensions list 2>/dev/null | grep -q '^user-theme@'; then
  echo "NOTE: User Themes extension not found/enabled — Shell styling needs it:"
  echo "  ${DEP_INSTALL%%gnome-shell-extension-user-theme*}gnome-shell-extension-user-theme"
  echo "  then: gnome-extensions enable user-theme@gnome-shell-extensions.gcampax.github.com (re-login if new)"
fi

cat <<EOF

========================================================================
  ✨ Theme Installation Complete!
========================================================================
Theme Name:       ${THEME_NAME}
Installed To:     ${THEME_DIR}
Top Bar Style:    ${PANEL_STYLE}
Window Controls:  ${CONTROLS}
Density:          ${THEME_SIZE}

Settings Applied:
  Shell Theme:    ${THEME_NAME}
  GTK Theme:      ${THEME_NAME}
  Icon Theme:     MT-Verdant-Icons
  Cursor Theme:   MT-Verdant-Cursors

Restore Defaults (Adwaita):
  dconf write /org/gnome/shell/extensions/user-theme/name "''"
  gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
  gsettings set org.gnome.desktop.interface icon-theme 'Adwaita'
  gsettings set org.gnome.desktop.interface cursor-theme 'Adwaita'
  rm -f ~/.config/gtk-4.0/gtk.css
EOF
