#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Sandboxed install smoke test: works on a git checkout or a release tarball.

set -eu

TARGET="${1:-.}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

if [ -f "$TARGET" ]; then
  mkdir -p "$WORK/pkg"
  tar -xf "$TARGET" -C "$WORK/pkg"
  ROOT="$(find "$WORK/pkg" -maxdepth 2 -name install.sh -printf '%h\n' | head -n1)"
else
  ROOT="$(cd "$TARGET" && pwd)"
fi
[ -n "$ROOT" ] && [ -f "$ROOT/install.sh" ] || { echo "no installer found in $TARGET" >&2; exit 1; }

BIN="$WORK/bin"
mkdir -p "$BIN"
printf '#!/bin/sh\necho "GNOME Shell 51.1"\n' > "$BIN/gnome-shell"
printf '#!/bin/sh\necho "dconf $*" >> "%s/dconf.log"\n' "$WORK" > "$BIN/dconf"
printf '#!/bin/sh\necho "gsettings $*" >> "%s/gsettings.log"\n' "$WORK" > "$BIN/gsettings"
printf '#!/bin/sh\nexit 0\n' > "$BIN/gnome-extensions"
chmod +x "$BIN"/*

HOME_DIR="$WORK/home"
mkdir -p "$HOME_DIR"
HOME="$HOME_DIR" PATH="$BIN:$PATH" sh "$ROOT/install.sh" --non-interactive \
  --accent emerald --panel pill --controls macos --wallpaper light-1 > "$WORK/install.log" 2>&1 || {
    cat "$WORK/install.log" >&2
    exit 1
  }

THEME="$HOME_DIR/.themes/MT-Verdant-Nocturne"
fail() { echo "FAIL: $1" >&2; exit 1; }
[ -s "$THEME/gnome-shell/gnome-shell.css" ] || fail "shell CSS missing"
[ -s "$THEME/gtk-3.0/gtk.css" ] || fail "GTK3 CSS missing"
[ -s "$THEME/gtk-4.0/gtk.css" ] || fail "GTK4 CSS missing"
[ -s "$THEME/index.theme" ] || fail "index.theme missing"
[ -f "$THEME/.mt-verdant-manifest" ] || fail "install manifest missing"

grep -qi "#3dd68c" "$THEME/gnome-shell/gnome-shell.css" || fail "accent not baked into Shell"
grep -qi "#3dd68c" "$THEME/gtk-3.0/gtk.css" || fail "accent not baked into GTK3"
grep -qi "#3dd68c" "$THEME/gtk-4.0/gtk.css" || fail "accent not baked into GTK4"
if grep -qi "8fb8a6" "$THEME/gnome-shell/gnome-shell.css"; then fail "sage accent leaked into emerald Shell"; fi
grep -q "border-radius: 999px" "$THEME/gnome-shell/gnome-shell.css" || fail "pill panel not applied"
grep -q "headerbar windowcontrols button.close" "$THEME/gtk-3.0/gtk.css" || fail "macOS controls not applied"
grep -q "canopy-dawn" "$WORK/gsettings.log" || fail "light wallpaper not applied"

# OLED + rimless legacy tweaks must produce real output.
HOME2="$WORK/home2"; mkdir -p "$HOME2"
HOME="$HOME2" PATH="$BIN:$PATH" sh "$ROOT/install.sh" --non-interactive --tweaks black,rimless > "$WORK/install2.log" 2>&1 || {
  cat "$WORK/install2.log" >&2
  exit 1
}
grep -q "#050807" "$HOME2/.themes/MT-Verdant-Nocturne/gtk-3.0/gtk.css" || fail "OLED tweak not applied"
grep -q "window.solid-csd" "$HOME2/.themes/MT-Verdant-Nocturne/gtk-3.0/gtk.css" || fail "rimless tweak not applied"

# Unknown values must fail loudly, not fall back.
if HOME="$HOME2" PATH="$BIN:$PATH" sh "$ROOT/install.sh" --non-interactive --wallpaper wat >/dev/null 2>&1; then
  fail "unknown wallpaper value was accepted"
fi

# Uninstall parks the theme instead of deleting it.
HOME="$HOME_DIR" PATH="$BIN:$PATH" sh "$ROOT/install.sh" --uninstall >/dev/null 2>&1 || fail "uninstall failed"
[ ! -d "$THEME" ] || fail "theme directory still present after uninstall"
find "$ROOT/deleted_files_folders" -maxdepth 1 -name 'MT-Verdant-Nocturne-uninstalled-*' | grep -q . || fail "uninstall did not park the theme"

echo "smoke install: PASS ($ROOT)"
