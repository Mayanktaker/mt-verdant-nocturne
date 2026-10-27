#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# User-scoped local Flatpak fallback: exposes the GTK3 theme to sandboxed apps
# without a configured remote (documented "unmaintained extension" layout).
# Prefer the packaged org.gtk.Gtk3theme.MT-Verdant-Nocturne extension when available.

set -eu

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
THEME_NAME="MT-Verdant-Nocturne"
ARCH="$(flatpak --default-arch)"
XDG_DATA_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}"
EXT_DIR="${XDG_DATA_HOME}/flatpak/extension/org.gtk.Gtk3theme.${THEME_NAME}/${ARCH}/3.22"

[ -f "${REPO_ROOT}/build/theme/gtk-3.0/gtk-dark.css" ] || python3 "${REPO_ROOT}/tools/gtk/build.py"

mkdir -p "${EXT_DIR}"
cp -r "${REPO_ROOT}/build/theme/gtk-3.0/." "${EXT_DIR}/"
echo "local Flatpak theme fallback installed at ${EXT_DIR}"
echo "remove with: rm -rf \"${XDG_DATA_HOME}/flatpak/extension/org.gtk.Gtk3theme.${THEME_NAME}\""
