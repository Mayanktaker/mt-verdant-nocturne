#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Install MT Verdant Nocturne at user level into ~/.themes ONLY (project policy).
# Works from the git checkout and from the release archive (single installer, two layouts).

set -eu

# ---------------------------------------------------------------- paths / defaults
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -d "$SELF_DIR/../build/theme" ] || [ -d "$SELF_DIR/../src/tweaks" ]; then
  REPO_ROOT="$(cd "$SELF_DIR/.." && pwd)"
  LAYOUT="source"
elif [ -d "$SELF_DIR/tweaks" ] && [ -d "$SELF_DIR/presets" ]; then
  REPO_ROOT="$SELF_DIR"
  LAYOUT="release"
else
  echo "cannot find theme sources next to $0" >&2
  exit 1
fi

THEME_NAME="MT-Verdant-Nocturne"
THEME_DIR="${HOME}/.themes/${THEME_NAME}"
VERSION="$(cat "${REPO_ROOT}/VERSION" 2>/dev/null || echo "0.0.0")"
MANIFEST="${THEME_DIR}/.mt-verdant-manifest"

PANEL_STYLE="round-island"   # round-island | pill | bottom-round | flat
CONTROLS="standard"          # standard | macos
ACCENT="sage"                # sage | emerald | moss | pine
THEME_SIZE="standard"        # standard | compact
WANT_BLUR=1
WANT_GTK4_OVERRIDE=0
WANT_OLED=0
WANT_RIMLESS=0
WANT_WALLPAPER=0
WALLPAPER_CHOICE="none"
INSTALL_DEPS=0
INTERACTIVE=0
EXPLICIT_ARGS=0
DO_UNINSTALL=0
TWEAKS_ARG=""

# ---------------------------------------------------------------- parsing
if [ $# -eq 0 ] && [ -t 0 ]; then
  INTERACTIVE=1
fi

while [ $# -gt 0 ]; do
  EXPLICIT_ARGS=1
  case "$1" in
    --wizard) INTERACTIVE=1 ;;
    --non-interactive|--no-interactive) INTERACTIVE=0 ;;
    --panel) shift; PANEL_STYLE="${1:-}" ;;
    --panel=*) PANEL_STYLE="${1#*=}" ;;
    --controls) shift; CONTROLS="${1:-}" ;;
    --controls=*) CONTROLS="${1#*=}" ;;
    --accent) shift; ACCENT="${1:-}" ;;
    --accent=*) ACCENT="${1#*=}" ;;
    --size) shift; THEME_SIZE="${1:-}" ;;
    --size=*) THEME_SIZE="${1#*=}" ;;
    --wallpaper) shift; WANT_WALLPAPER=1; WALLPAPER_CHOICE="${1:-}" ;;
    --wallpaper=*) WANT_WALLPAPER=1; WALLPAPER_CHOICE="${1#*=}" ;;
    --blur) WANT_BLUR=1 ;;
    --no-blur|--noblur) WANT_BLUR=0 ;;
    --oled|--black) WANT_OLED=1 ;;
    --rimless) WANT_RIMLESS=1 ;;
    --gtk4-libadwaita) WANT_GTK4_OVERRIDE=1 ;;
    --no-gtk4) WANT_GTK4_OVERRIDE=0 ;;
    --install-deps) INSTALL_DEPS=1 ;;
    --uninstall) DO_UNINSTALL=1 ;;
    --tweaks) shift; TWEAKS_ARG="${1:-}" ;;
    --tweaks=*) TWEAKS_ARG="${1#*=}" ;;
    -h|--help) INTERACTIVE=0; PRINT_HELP=1 ;;
    *)
      echo "unknown option: $1" >&2
      echo "run with --help for the accepted flags" >&2
      exit 2
      ;;
  esac
  shift
done

PRINT_HELP="${PRINT_HELP:-0}"
if [ "$PRINT_HELP" -eq 1 ]; then
  cat <<EOF
MT Verdant Nocturne ${VERSION} — installer

  --panel round-island|pill|bottom-round|flat
  --controls standard|macos
  --accent sage|emerald|moss|pine
  --size standard|compact
  --blur | --no-blur
  --oled | --rimless
  --wallpaper 1|2|3|4|light-1|light-2|light-3|light-4|dynamic|timed|all|none
  --gtk4-libadwaita | --no-gtk4
  --install-deps        install missing system packages with sudo
  --tweaks a,b,c        legacy comma list (float, round, translucent, black, compact, macos, rimless, noblur)
  --uninstall           remove this theme and restore GTK4 backups
  --non-interactive     skip the wizard
EOF
  exit 0
fi

# ---------------------------------------------------------------- uninstall
if [ "$DO_UNINSTALL" -eq 1 ]; then
  if [ -f "$MANIFEST" ]; then
    while IFS= read -r path; do
      [ -n "$path" ] || continue
      case "$path" in
        "${HOME}/.config/gtk-4.0/gtk.css"|"${HOME}/.config/gtk-4.0/gtk-dark.css")
          [ -L "$path" ] && rm -f "$path"
          ;;
        "${HOME}/.config/gtk-4.0/gtk.css.pre-nocturne")
          [ -f "$path" ] && mv "$path" "${HOME}/.config/gtk-4.0/gtk.css"
          ;;
        "${HOME}/.config/gtk-4.0/gtk-dark.css.pre-nocturne")
          [ -f "$path" ] && mv "$path" "${HOME}/.config/gtk-4.0/gtk-dark.css"
          ;;
        "${HOME}/.config/gtk-4.0/gtk.css.pre-nocturne-link")
          if [ -f "$path" ]; then
            target="$(cat "$path")"
            [ -n "$target" ] && ln -sf "$target" "${HOME}/.config/gtk-4.0/gtk.css"
            rm -f "$path"
          fi
          ;;
        "${HOME}/.config/gtk-4.0/gtk-dark.css.pre-nocturne-link")
          if [ -f "$path" ]; then
            target="$(cat "$path")"
            [ -n "$target" ] && ln -sf "$target" "${HOME}/.config/gtk-4.0/gtk-dark.css"
            rm -f "$path"
          fi
          ;;
        *) [ -f "$path" ] && rm -f "$path" ;;
      esac
    done < "$MANIFEST"
  fi
  if [ -d "$THEME_DIR" ]; then
    PARK="${REPO_ROOT}/deleted_files_folders"
    mkdir -p "$PARK"
    mv "$THEME_DIR" "${PARK}/${THEME_NAME}-uninstalled-$(date +%Y%m%d-%H%M%S)"
    echo "theme moved to ${PARK} (nothing was hard-deleted)"
  fi
  echo "uninstalled. Reset the shell theme with:"
  echo "  dconf write /org/gnome/shell/extensions/user-theme/name \"''\""
  echo "  gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'"
  exit 0
fi

# ---------------------------------------------------------------- legacy --tweaks + validation
if [ -n "$TWEAKS_ARG" ]; then
  OLDIFS="$IFS"; IFS=','
  for token in $TWEAKS_ARG; do
    token="$(echo "$token" | tr -d '[:space:]')"
    case "$token" in
      "") ;;
      float) PANEL_STYLE="pill" ;;
      round) PANEL_STYLE="round-island" ;;
      black|oled) WANT_OLED=1 ;;
      rimless) WANT_RIMLESS=1 ;;
      compact) THEME_SIZE="compact" ;;
      macos) CONTROLS="macos" ;;
      translucent|blur) WANT_BLUR=1 ;;
      noblur|no-blur) WANT_BLUR=0 ;;
      *) echo "unknown tweak '$token' (accepted: float, round, black, rimless, compact, macos, translucent, noblur)" >&2; exit 2 ;;
    esac
  done
  IFS="$OLDIFS"
fi

validate_choice() {
  # Reject unknown values instead of silently falling back to a default.
  value="$1"; allowed="$2"; label="$3"
  case " $allowed " in
    *" $value "*) ;;
    *) echo "invalid $label '$value' (choose one of: $allowed)" >&2; exit 2 ;;
  esac
}

validate_choice "$PANEL_STYLE" "round-island pill bottom-round flat" "--panel"
validate_choice "$CONTROLS" "standard macos" "--controls"
validate_choice "$ACCENT" "sage emerald moss pine" "--accent"
validate_choice "$THEME_SIZE" "standard compact" "--size"
if [ "$WANT_WALLPAPER" -eq 1 ]; then
  validate_choice "$WALLPAPER_CHOICE" "1 2 3 4 canopy aurora flora river light-1 light-2 light-3 light-4 light-canopy-dawn light-celestial-rift light-cosmic-dawn light-botanical-horizon dynamic timed all none" "--wallpaper"
fi

# ---------------------------------------------------------------- distro packages
. /etc/os-release 2>/dev/null || ID=unknown
case "${ID:-unknown}" in
  ubuntu|debian)
    USER_THEME_PKG="gnome-shell-extensions"
    DEPS="gnome-shell python3 python3-gi sassc python3-numpy python3-pil ${USER_THEME_PKG}"
    DEP_INSTALL="sudo apt-get install -y ${DEPS}" ;;
  fedora)
    USER_THEME_PKG="gnome-shell-extension-user-theme"
    DEPS="gnome-shell python3 python3-gobject sassc python3-numpy python3-pillow ${USER_THEME_PKG}"
    DEP_INSTALL="sudo dnf install -y ${DEPS}" ;;
  arch|cachyos)
    USER_THEME_PKG="gnome-shell-extensions"
    DEPS="gnome-shell python python-gobject sassc python-numpy python-pillow ${USER_THEME_PKG}"
    DEP_INSTALL="sudo pacman -S --needed ${DEPS}" ;;
  opensuse*)
    USER_THEME_PKG="gnome-shell-extension-user-theme"
    DEPS="gnome-shell python3 python3-gobject sassc python3-numpy python3-Pillow ${USER_THEME_PKG}"
    DEP_INSTALL="sudo zypper install ${DEPS}" ;;
  *)
    USER_THEME_PKG="gnome-shell-extensions"
    DEPS="gnome-shell, python3 + gobject-introspection, sassc, numpy, Pillow, ${USER_THEME_PKG}"
    DEP_INSTALL="(unknown distro '${ID:-?}' — install: ${DEPS})" ;;
esac

have() { command -v "$1" >/dev/null 2>&1; }
py_has() { python3 -c "import $1" >/dev/null 2>&1; }

if ! have gnome-shell; then
  echo "gnome-shell not found on PATH" >&2
  exit 1
fi
SHELL_MAJOR="$(gnome-shell --version | sed -E 's/[^0-9]*([0-9]+).*/\1/')"
if [ "${SHELL_MAJOR}" -lt 50 ]; then
  echo "GNOME Shell ${SHELL_MAJOR} is unsupported; MT Verdant Nocturne targets 50.x and 51.x." >&2
  exit 1
fi
if [ ! -f "${REPO_ROOT}/src/shell/colormap-${SHELL_MAJOR}.json" ] && [ "$LAYOUT" = "source" ]; then
  echo "missing src/shell/colormap-${SHELL_MAJOR}.json — Shell ${SHELL_MAJOR} not yet mapped." >&2
  exit 1
fi

echo "detected: ${ID:-unknown} · GNOME Shell ${SHELL_MAJOR} · ${LAYOUT} layout · v${VERSION}"

# ---------------------------------------------------------------- interactive wizard
if [ "$INTERACTIVE" -eq 1 ]; then
  echo ""
  echo "1. Top Bar Style:"
  echo "   [1] Rounded Island (Floating pill with soft glass) [Default]"
  echo "   [2] Classic Pill (Edge-to-edge capsule)"
  echo "   [3] Bottom-Rounded (Connected to top edge)"
  echo "   [4] Flat (No radius, edge-to-edge)"
  printf "   Select [1-4, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) PANEL_STYLE="pill" ;;
    3) PANEL_STYLE="bottom-round" ;;
    4) PANEL_STYLE="flat" ;;
    *) PANEL_STYLE="round-island" ;;
  esac

  echo ""
  echo "2. Window Controls:"
  echo "   [1] Standard GNOME (native layout) [Default]"
  echo "   [2] macOS Traffic Lights (also sets close,minimize,maximize on the left)"
  printf "   Select [1-2, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) CONTROLS="macos" ;;
    *) CONTROLS="standard" ;;
  esac

  echo ""
  echo "3. Accent Flavor:"
  echo "   [1] Sage (Botanical) [Default]"
  echo "   [2] Emerald (Vivid)"
  echo "   [3] Moss (Earthy)"
  echo "   [4] Pine (Nordic)"
  printf "   Select [1-4, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) ACCENT="emerald" ;;
    3) ACCENT="moss" ;;
    4) ACCENT="pine" ;;
    *) ACCENT="sage" ;;
  esac

  echo ""
  echo "4. Theme Density:"
  echo "   [1] Standard (comfortable) [Default]"
  echo "   [2] Compact (slimmer rows and headerbars)"
  printf "   Select [1-2, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) THEME_SIZE="compact" ;;
    *) THEME_SIZE="standard" ;;
  esac

  echo ""
  echo "5. Surface Treatment:"
  echo "   [1] Translucent + Blur My Shell (when available) [Default]"
  echo "   [2] Solid opaque surfaces"
  echo "   [3] OLED pure black (also enables solid surfaces)"
  printf "   Select [1-3, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) WANT_BLUR=0 ;;
    3) WANT_OLED=1; WANT_BLUR=0 ;;
    *) WANT_BLUR=1 ;;
  esac

  echo ""
  echo "6. GTK4 / Libadwaita override:"
  echo "   [1] Skip (recommended; libadwaita ignores third-party themes) [Default]"
  echo "   [2] Apply best-effort override (~/.config/gtk-4.0/gtk.css)"
  printf "   Select [1-2, default=1]: "
  read -r choice || choice=""
  case "${choice}" in
    2) WANT_GTK4_OVERRIDE=1 ;;
    *) WANT_GTK4_OVERRIDE=0 ;;
  esac

  echo ""
  echo "7. 4K Botanical Wallpaper:"
  echo "   [1] Canopy (default, dark)"
  echo "   [2] Aurora (dark)"
  echo "   [3] Flora (dark)"
  echo "   [4] River (dark)"
  echo "   [5] Light suite (choose 1-4 next run with --wallpaper light-N)"
  echo "   [6] Dynamic (light by day, Canopy by night)"
  echo "   [7] All (copy the suite to ~/Pictures/wallpapers-mt-verdant)"
  echo "   [8] None (keep current wallpaper)"
  printf "   Select [1-8, default=8]: "
  read -r choice || choice=""
  case "${choice}" in
    1) WANT_WALLPAPER=1; WALLPAPER_CHOICE="1" ;;
    2) WANT_WALLPAPER=1; WALLPAPER_CHOICE="2" ;;
    3) WANT_WALLPAPER=1; WALLPAPER_CHOICE="3" ;;
    4) WANT_WALLPAPER=1; WALLPAPER_CHOICE="4" ;;
    6) WANT_WALLPAPER=1; WALLPAPER_CHOICE="dynamic" ;;
    7) WANT_WALLPAPER=1; WALLPAPER_CHOICE="all" ;;
    8|"") WANT_WALLPAPER=0; WALLPAPER_CHOICE="none" ;;
    5) echo "   Use --non-interactive --wallpaper light-1 (..light-4) after this run." ;;
    *) WANT_WALLPAPER=0; WALLPAPER_CHOICE="none" ;;
  esac

  echo ""
  echo "Configuration summary:"
  echo "  - Top Bar Style:     ${PANEL_STYLE}"
  echo "  - Window Controls:   ${CONTROLS}"
  echo "  - Accent Flavor:     ${ACCENT}"
  echo "  - Theme Density:     ${THEME_SIZE}"
  echo "  - Surface:           $([ "$WANT_OLED" -eq 1 ] && echo "OLED black" || { [ "$WANT_BLUR" -eq 1 ] && echo "Translucent + blur" || echo "Solid"; })"
  echo "  - GTK4 override:     $([ "$WANT_GTK4_OVERRIDE" -eq 1 ] && echo "Apply" || echo "Skip")"
  echo "  - Wallpaper:         ${WALLPAPER_CHOICE}"
  echo ""
fi

# ---------------------------------------------------------------- dependencies
NEED_BUILD=0
if [ "$LAYOUT" = "source" ]; then
  NEED_BUILD=1
fi

MISSING=""
if [ "$LAYOUT" = "source" ]; then have python3 || MISSING="${MISSING}python3; "; fi
if [ "$NEED_BUILD" -eq 1 ]; then
  have sassc || MISSING="${MISSING}sassc; "
fi

if [ -n "$MISSING" ]; then
  echo "missing requirements: ${MISSING%; }"
  echo "install them for this distro with:"
  echo "  ${DEP_INSTALL}"
  if [ "$INSTALL_DEPS" -eq 1 ]; then
    echo "running (sudo is used only here, for system packages):"
    sh -c "${DEP_INSTALL}"
  else
    echo "re-run with --install-deps to install them automatically, then retry."
    exit 1
  fi
fi

# ---------------------------------------------------------------- build (source layout only)
PRESET_DIR=""
if [ "$LAYOUT" = "source" ]; then
  python3 "${REPO_ROOT}/tools/shell/build.py" --major "${SHELL_MAJOR}" --accent "${ACCENT}" --out-dir "${REPO_ROOT}/build/presets/${ACCENT}" >/dev/null
  python3 "${REPO_ROOT}/tools/gtk/build.py" --accent "${ACCENT}" --out "${REPO_ROOT}/build/presets/${ACCENT}/gtk-3.0" >/dev/null
  PRESET_DIR="${REPO_ROOT}/build/presets/${ACCENT}"
else
  PRESET_DIR="${REPO_ROOT}/presets/${ACCENT}"
fi

SHELL_SRC="${PRESET_DIR}/gnome-shell-${SHELL_MAJOR}"
GTK_SRC="${PRESET_DIR}/gtk-3.0"
if [ ! -d "$SHELL_SRC" ] || [ ! -d "$GTK_SRC" ]; then
  echo "missing prebuilt preset for accent '${ACCENT}' (${SHELL_SRC})" >&2
  exit 1
fi

# ---------------------------------------------------------------- render tweaks
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
if [ "$LAYOUT" = "source" ]; then
  python3 "${REPO_ROOT}/tools/theme/render.py" --accent "${ACCENT}" --dir "${REPO_ROOT}/src/tweaks" --out-dir "${TMP_DIR}/tweaks" >/dev/null
  python3 "${REPO_ROOT}/tools/theme/render.py" --accent "${ACCENT}" --in "${REPO_ROOT}/src/gtk-4.0/overrides.css" --out "${TMP_DIR}/gtk4.css" >/dev/null
  INDEX_SRC="${REPO_ROOT}/src/index.theme"
else
  TWEAK_DIR="${REPO_ROOT}/tweaks/${ACCENT}"
  GTK4_SRC="${REPO_ROOT}/gtk4/${ACCENT}/gtk.css"
  INDEX_SRC="${REPO_ROOT}/index.theme"
fi

append_css() {
  # Append a tweak file to a target stylesheet when it exists.
  file="$1"; target="$2"
  if [ -f "$file" ]; then cat "$file" >> "$target"; fi
}

# ---------------------------------------------------------------- install into ~/.themes
OLD_DIR="${HOME}/.local/share/themes/${THEME_NAME}"
if [ -d "$OLD_DIR" ]; then
  PARK="${REPO_ROOT}/deleted_files_folders"
  mkdir -p "$PARK"
  mv "$OLD_DIR" "${PARK}/${THEME_NAME}-local-share"
  echo "moved previous install from ${OLD_DIR} to ${PARK}/${THEME_NAME}-local-share"
fi

# Replace generated layers wholesale so stale assets from older versions never accumulate.
rm -rf "${THEME_DIR}/gnome-shell" "${THEME_DIR}/gtk-3.0" "${THEME_DIR}/gtk-4.0" \
       "${THEME_DIR}/gtk-2.0" "${THEME_DIR}/wallpapers" "${THEME_DIR}/extras"
mkdir -p "${THEME_DIR}/gtk-4.0" "${THEME_DIR}/gtk-2.0" "${THEME_DIR}/wallpapers" "${THEME_DIR}/extras"
cp "${INDEX_SRC}" "${THEME_DIR}/index.theme"
if [ -f "${REPO_ROOT}/src/thumbnail.png" ]; then
  cp "${REPO_ROOT}/src/thumbnail.png" "${THEME_DIR}/thumbnail.png"
elif [ -f "${REPO_ROOT}/thumbnail.png" ]; then
  cp "${REPO_ROOT}/thumbnail.png" "${THEME_DIR}/thumbnail.png"
fi
cp -r "${SHELL_SRC}" "${THEME_DIR}/gnome-shell"
cp -r "${GTK_SRC}" "${THEME_DIR}/gtk-3.0"

if [ "$LAYOUT" = "source" ]; then
  cp "${TMP_DIR}/gtk4.css" "${THEME_DIR}/gtk-4.0/gtk.css"
  TWEAK_DIR="${TMP_DIR}/tweaks"
else
  cp "${GTK4_SRC}" "${THEME_DIR}/gtk-4.0/gtk.css"
fi
cp "${THEME_DIR}/gtk-4.0/gtk.css" "${THEME_DIR}/gtk-4.0/gtk-dark.css"

# GTK2 fallback (rendered per accent so legacy apps follow the theme)
mkdir -p "${THEME_DIR}/gtk-2.0"
if [ "$LAYOUT" = "source" ]; then
  python3 "${REPO_ROOT}/tools/theme/render.py" --accent "${ACCENT}"     --in "${REPO_ROOT}/src/gtk-2.0/gtkrc" --out "${THEME_DIR}/gtk-2.0/gtkrc" >/dev/null
elif [ -f "${REPO_ROOT}/gtk2/${ACCENT}/gtkrc" ]; then
  cp "${REPO_ROOT}/gtk2/${ACCENT}/gtkrc" "${THEME_DIR}/gtk-2.0/gtkrc"
fi

# Wallpapers: only the selected set, never the whole suite
WALLPAPER_DIR="${REPO_ROOT}/wallpaper/dist"
[ "$LAYOUT" = "release" ] && WALLPAPER_DIR="${REPO_ROOT}/wallpapers"
if [ -d "$WALLPAPER_DIR" ]; then
  choose_wallpaper() {
    # Copy one wallpaper (dark or light) into the theme and echo its path.
    src="$1"; dest="$2"
    if [ -f "$src" ]; then cp "$src" "${THEME_DIR}/wallpapers/${dest}"; echo "${THEME_DIR}/wallpapers/${dest}"; fi
  }
  DARK_IMG="$(ls "${WALLPAPER_DIR}"/mt-verdant-canopy-*.jpg 2>/dev/null | head -n1 || true)"
  LIGHT_IMG="$(ls "${WALLPAPER_DIR}"/light/mt-verdant-canopy-dawn-*.jpg 2>/dev/null | head -n1 || true)"
  # Ship the compact suite (~1.5 MB) so the registration XMLs always resolve.
  mkdir -p "${THEME_DIR}/wallpapers/light"
  cp "${WALLPAPER_DIR}"/*.jpg "${THEME_DIR}/wallpapers/" 2>/dev/null || true
  cp "${WALLPAPER_DIR}"/light/*.jpg "${THEME_DIR}/wallpapers/light/" 2>/dev/null || true
  # always keep the registration XMLs so the theme appears in Settings
  for xml in "${WALLPAPER_DIR}"/*.xml*; do
    [ -f "$xml" ] && cp "$xml" "${THEME_DIR}/wallpapers/" 2>/dev/null || true
  done
  for xml in "${THEME_DIR}/wallpapers"/*.xml.in; do
    [ -f "$xml" ] || continue
    sed "s|@WALLPAPER_DIR@|${THEME_DIR}/wallpapers|g" "$xml" > "${xml%.in}"
  done
  if [ -f "${THEME_DIR}/wallpapers/gnome-background-properties.xml" ]; then
    mkdir -p "${HOME}/.local/share/gnome-background-properties"
    cp "${THEME_DIR}/wallpapers/gnome-background-properties.xml" "${HOME}/.local/share/gnome-background-properties/mt-verdant.xml"
  fi
fi

if [ -d "${REPO_ROOT}/extras" ]; then
  cp -r "${REPO_ROOT}/extras/"* "${THEME_DIR}/extras/" 2>/dev/null || true
fi

# ---------------------------------------------------------------- apply layers
SHELL_CSS="${THEME_DIR}/gnome-shell/gnome-shell.css"
GTK3_CSS="${THEME_DIR}/gtk-3.0/gtk.css"
GTK3_DARK="${THEME_DIR}/gtk-3.0/gtk-dark.css"
GTK4_CSS="${THEME_DIR}/gtk-4.0/gtk.css"
GTK4_DARK="${THEME_DIR}/gtk-4.0/gtk-dark.css"

append_css "${TWEAK_DIR}/shell/polish.css" "$SHELL_CSS"
case "${PANEL_STYLE}" in
  round-island) append_css "${TWEAK_DIR}/shell/tray-round.css" "$SHELL_CSS"; PANEL_RADIUS=16; echo "  + top bar: rounded floating island" ;;
  pill) append_css "${TWEAK_DIR}/shell/tray-pill.css" "$SHELL_CSS"; PANEL_RADIUS=999; echo "  + top bar: floating pill capsule" ;;
  bottom-round) append_css "${TWEAK_DIR}/shell/tray-bottom-round.css" "$SHELL_CSS"; PANEL_RADIUS=16; echo "  + top bar: bottom-rounded" ;;
  flat) PANEL_RADIUS=0; echo "  + top bar: classic edge-to-edge" ;;
esac

if [ "$WANT_BLUR" -eq 1 ] && [ "$WANT_OLED" -eq 0 ]; then
  append_css "${TWEAK_DIR}/shell/translucent.css" "$SHELL_CSS"
  echo "  + surface: translucent (blur needs Blur My Shell)"
else
  append_css "${TWEAK_DIR}/shell/noblur.css" "$SHELL_CSS"
  echo "  + surface: solid"
fi
append_css "${TWEAK_DIR}/shell/round.css" "$SHELL_CSS"
[ "$THEME_SIZE" = "compact" ] && append_css "${TWEAK_DIR}/shell/compact.css" "$SHELL_CSS"
[ "$WANT_OLED" -eq 1 ] && append_css "${TWEAK_DIR}/shell/black.css" "$SHELL_CSS"

for target in "$GTK3_CSS" "$GTK3_DARK" "$GTK4_CSS" "$GTK4_DARK"; do
  append_css "${TWEAK_DIR}/gtk/polish.css" "$target"
  append_css "${TWEAK_DIR}/gtk/round.css" "$target"
  [ "$THEME_SIZE" = "compact" ] && append_css "${TWEAK_DIR}/gtk/compact.css" "$target"
  [ "$WANT_OLED" -eq 1 ] && append_css "${TWEAK_DIR}/gtk/black.css" "$target"
  [ "$WANT_RIMLESS" -eq 1 ] && append_css "${TWEAK_DIR}/gtk/rimless.css" "$target"
  [ "$CONTROLS" = "macos" ] && append_css "${TWEAK_DIR}/gtk/macos.css" "$target"
  if [ "$WANT_BLUR" -eq 0 ]; then append_css "${TWEAK_DIR}/gtk/noblur.css" "$target"; fi
done

# ---------------------------------------------------------------- blur extension config
if have dconf && [ -d "${HOME}/.local/share/gnome-shell/extensions/blur-my-shell@aunetx" ]; then
  if [ "$WANT_BLUR" -eq 1 ] && [ "$WANT_OLED" -eq 0 ]; then
    dconf write /org/gnome/shell/extensions/blur-my-shell/panel/blur true 2>/dev/null || true
    dconf write /org/gnome/shell/extensions/blur-my-shell/panel/corner-radius "${PANEL_RADIUS}" 2>/dev/null || true
    dconf write /org/gnome/shell/extensions/blur-my-shell/panel/override-background false 2>/dev/null || true
  fi
else
  [ "$WANT_BLUR" -eq 1 ] && echo "  note: Blur My Shell not found — panels are translucent, not blurred."
fi

# ---------------------------------------------------------------- macOS window layout (opt-in)
if [ "$CONTROLS" = "macos" ] && have gsettings; then
  gsettings set org.gnome.desktop.wm.preferences button-layout 'close,minimize,maximize:' || true
  echo "  + window buttons moved left (revert: gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close')"
fi

# ---------------------------------------------------------------- wallpapers apply
if [ "$WANT_WALLPAPER" -eq 1 ] && [ "$WALLPAPER_CHOICE" != "none" ]; then
  if [ ! -d "$WALLPAPER_DIR" ]; then
    echo "wallpaper assets not found in ${WALLPAPER_DIR}" >&2
    exit 1
  fi
  DARK_CANOPY="$(ls "${WALLPAPER_DIR}"/mt-verdant-canopy-*.jpg 2>/dev/null | head -n1 || true)"
  LIGHT_CANOPY="$(ls "${WALLPAPER_DIR}"/light/mt-verdant-canopy-dawn-*.jpg 2>/dev/null | head -n1 || true)"
  case "${WALLPAPER_CHOICE}" in
    1|canopy) WP_PICK="$DARK_CANOPY" ;;
    2|aurora) WP_PICK="${WALLPAPER_DIR}/mt-verdant-aurora-3840x2160.jpg" ;;
    3|flora) WP_PICK="${WALLPAPER_DIR}/mt-verdant-flora-3840x2160.jpg" ;;
    4|river) WP_PICK="${WALLPAPER_DIR}/mt-verdant-river-3840x2160.jpg" ;;
    light-1|light-canopy-dawn) WP_PICK="$LIGHT_CANOPY" ;;
    light-2|light-celestial-rift) WP_PICK="${WALLPAPER_DIR}/light/mt-verdant-celestial-rift-3840x2160.jpg" ;;
    light-3|light-cosmic-dawn) WP_PICK="${WALLPAPER_DIR}/light/mt-verdant-cosmic-dawn-3840x2160.jpg" ;;
    light-4|light-botanical-horizon) WP_PICK="${WALLPAPER_DIR}/light/mt-verdant-botanical-horizon-3840x2160.jpg" ;;
    dynamic) WP_PICK="$DARK_CANOPY" ;;
    timed) WP_PICK="$DARK_CANOPY" ;;
    all) WP_PICK="$DARK_CANOPY" ;;
    *) WP_PICK="$DARK_CANOPY" ;;
  esac

  if [ "${WALLPAPER_CHOICE}" = "all" ]; then
    mkdir -p "${HOME}/Pictures/wallpapers-mt-verdant"
    cp "${WALLPAPER_DIR}"/*.jpg "${HOME}/Pictures/wallpapers-mt-verdant/" 2>/dev/null || true
    cp "${WALLPAPER_DIR}"/light/*.jpg "${HOME}/Pictures/wallpapers-mt-verdant/" 2>/dev/null || true
    echo "wallpaper suite copied to ~/Pictures/wallpapers-mt-verdant/"
  fi

  if [ -n "$WP_PICK" ] && [ -f "$WP_PICK" ]; then
    DEST="${HOME}/Pictures/mt-verdant-wallpaper$(printf '%s' "$WP_PICK" | sed 's/.*mt-verdant//')"
    mkdir -p "${HOME}/Pictures"
    cp "$WP_PICK" "$DEST"
    if [ "${WALLPAPER_CHOICE}" = "dynamic" ] && [ -n "$LIGHT_CANOPY" ] && [ -f "$LIGHT_CANOPY" ]; then
      LIGHT_DEST="${HOME}/Pictures/mt-verdant-wallpaper-dawn$(printf '%s' "$LIGHT_CANOPY" | sed 's/.*mt-verdant-canopy-dawn//')"
      cp "$LIGHT_CANOPY" "$LIGHT_DEST"
      gsettings set org.gnome.desktop.background picture-uri "file://${LIGHT_DEST}"
      gsettings set org.gnome.desktop.background picture-uri-dark "file://${DEST}"
      echo "wallpaper: dynamic (light: ${LIGHT_DEST}, dark: ${DEST})"
    elif [ "${WALLPAPER_CHOICE}" = "timed" ] && [ -f "${THEME_DIR}/wallpapers/mt-verdant-timed.xml" ]; then
      gsettings set org.gnome.desktop.background picture-uri "file://${THEME_DIR}/wallpapers/mt-verdant-timed.xml"
      gsettings set org.gnome.desktop.background picture-uri-dark "file://${DEST}"
      echo "wallpaper: timed XML (${THEME_DIR}/wallpapers/mt-verdant-timed.xml)"
    else
      gsettings set org.gnome.desktop.background picture-uri "file://${DEST}"
      gsettings set org.gnome.desktop.background picture-uri-dark "file://${DEST}"
      echo "wallpaper applied: ${DEST}"
    fi
  else
    echo "wallpaper '${WALLPAPER_CHOICE}' is not available in this build" >&2
    exit 1
  fi
fi

# ---------------------------------------------------------------- optional GTK4 override
if [ "$WANT_GTK4_OVERRIDE" -eq 1 ]; then
  CONF_DIR="${HOME}/.config/gtk-4.0"
  mkdir -p "${CONF_DIR}"
  [ -f "${CONF_DIR}/gtk.css" ] && [ ! -L "${CONF_DIR}/gtk.css" ] && cp "${CONF_DIR}/gtk.css" "${CONF_DIR}/gtk.css.pre-nocturne"
  [ -f "${CONF_DIR}/gtk-dark.css" ] && [ ! -L "${CONF_DIR}/gtk-dark.css" ] && cp "${CONF_DIR}/gtk-dark.css" "${CONF_DIR}/gtk-dark.css.pre-nocturne"
  if [ -L "${CONF_DIR}/gtk.css" ] && [ ! -f "${CONF_DIR}/gtk.css.pre-nocturne-link" ]; then
    readlink "${CONF_DIR}/gtk.css" > "${CONF_DIR}/gtk.css.pre-nocturne-link"
  fi
  if [ -L "${CONF_DIR}/gtk-dark.css" ] && [ ! -f "${CONF_DIR}/gtk-dark.css.pre-nocturne-link" ]; then
    readlink "${CONF_DIR}/gtk-dark.css" > "${CONF_DIR}/gtk-dark.css.pre-nocturne-link"
  fi
  ln -sf "${THEME_DIR}/gtk-4.0/gtk.css" "${CONF_DIR}/gtk.css"
  ln -sf "${THEME_DIR}/gtk-4.0/gtk-dark.css" "${CONF_DIR}/gtk-dark.css"
  echo "libadwaita best-effort override linked (opt-in). Revert with --uninstall."
else
  echo "  + GTK4/libadwaita override: skipped (opt-in with --gtk4-libadwaita)"
fi

# ---------------------------------------------------------------- manifest
{
  echo "${THEME_DIR}/index.theme"
  find "${THEME_DIR}" -type f 2>/dev/null
  echo "${HOME}/.local/share/gnome-background-properties/mt-verdant.xml"
  [ "$WANT_GTK4_OVERRIDE" -eq 1 ] && echo "${HOME}/.config/gtk-4.0/gtk.css"
  [ "$WANT_GTK4_OVERRIDE" -eq 1 ] && echo "${HOME}/.config/gtk-4.0/gtk-dark.css"
  [ "$WANT_GTK4_OVERRIDE" -eq 1 ] && [ -f "${HOME}/.config/gtk-4.0/gtk.css.pre-nocturne" ] && echo "${HOME}/.config/gtk-4.0/gtk.css.pre-nocturne"
  [ "$WANT_GTK4_OVERRIDE" -eq 1 ] && [ -f "${HOME}/.config/gtk-4.0/gtk-dark.css.pre-nocturne" ] && echo "${HOME}/.config/gtk-4.0/gtk-dark.css.pre-nocturne"
  [ "$WANT_GTK4_OVERRIDE" -eq 1 ] && [ -f "${HOME}/.config/gtk-4.0/gtk.css.pre-nocturne-link" ] && echo "${HOME}/.config/gtk-4.0/gtk.css.pre-nocturne-link"
  [ "$WANT_GTK4_OVERRIDE" -eq 1 ] && [ -f "${HOME}/.config/gtk-4.0/gtk-dark.css.pre-nocturne-link" ] && echo "${HOME}/.config/gtk-4.0/gtk-dark.css.pre-nocturne-link"
} | sort -u > "$MANIFEST"

# ---------------------------------------------------------------- activation
if have dconf; then
  dconf write /org/gnome/shell/extensions/user-theme/name "'${THEME_NAME}'" || true
fi
if have gsettings; then
  gsettings set org.gnome.desktop.interface gtk-theme "${THEME_NAME}" || true
fi
if have gnome-extensions && ! gnome-extensions list 2>/dev/null | grep -q '^user-theme@'; then
  echo "NOTE: User Themes extension not found/enabled — Shell styling needs it:"
  echo "  ${DEP_INSTALL}"
  echo "  then: gnome-extensions enable user-theme@gnome-shell-extensions.gcampax.github.com (re-login if new)"
fi

cat <<EOF

========================================================================
  MT Verdant Nocturne ${VERSION} installed
========================================================================
Theme Name:       ${THEME_NAME}
Installed To:     ${THEME_DIR}
Accent:           ${ACCENT}
Top Bar:          ${PANEL_STYLE}
Window Controls:  ${CONTROLS}
Density:          ${THEME_SIZE}
Surface:          $([ "$WANT_OLED" -eq 1 ] && echo "OLED black" || { [ "$WANT_BLUR" -eq 1 ] && echo "Translucent" || echo "Solid"; })

Companion icon & cursor pack:
  https://github.com/Mayanktaker/mt-verdant-icons

Uninstall (keeps a parked copy):
  $(basename "$0") --uninstall
EOF
