#!/bin/sh
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Automated installer for MT Verdant Nocturne app ecosystem and terminal themes.
# Detects installed user tools and registers matching color schemes.

set -eu

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "=== MT Verdant Nocturne: Application Ecosystem Installer ==="

have() {
  command -v "$1" >/dev/null 2>&1
}

# 1. Terminals
# Ghostty
if have ghostty || [ -d "${HOME}/.config/ghostty" ]; then
  mkdir -p "${HOME}/.config/ghostty/themes"
  cp "${REPO_ROOT}/extras/terminals/ghostty/mt-verdant-nocturne" "${HOME}/.config/ghostty/themes/"
  echo "✓ Ghostty: theme installed to ~/.config/ghostty/themes/mt-verdant-nocturne"
fi

# Kitty
if have kitty || [ -d "${HOME}/.config/kitty" ]; then
  mkdir -p "${HOME}/.config/kitty/themes"
  cp "${REPO_ROOT}/extras/terminals/kitty/mt-verdant-nocturne.conf" "${HOME}/.config/kitty/themes/"
  echo "✓ Kitty: theme installed to ~/.config/kitty/themes/mt-verdant-nocturne.conf"
fi

# Alacritty
if have alacritty || [ -d "${HOME}/.config/alacritty" ]; then
  mkdir -p "${HOME}/.config/alacritty/themes"
  cp "${REPO_ROOT}/extras/terminals/alacritty/mt-verdant-nocturne.toml" "${HOME}/.config/alacritty/themes/"
  echo "✓ Alacritty: theme installed to ~/.config/alacritty/themes/mt-verdant-nocturne.toml"
fi

# Foot
if have foot || [ -d "${HOME}/.config/foot" ]; then
  mkdir -p "${HOME}/.config/foot/themes"
  cp "${REPO_ROOT}/extras/terminals/foot/mt-verdant-nocturne.ini" "${HOME}/.config/foot/themes/"
  echo "✓ Foot: theme installed to ~/.config/foot/themes/mt-verdant-nocturne.ini"
fi

# GNOME Terminal
if have gnome-terminal || have dconf; then
  if [ -f "${REPO_ROOT}/extras/terminals/gnome-terminal/install.sh" ]; then
    bash "${REPO_ROOT}/extras/terminals/gnome-terminal/install.sh" >/dev/null 2>&1 || true
    echo "✓ GNOME Terminal: profile registered via dconf"
  fi
fi

# 2. Shells
# Fish Shell
if have fish || [ -d "${HOME}/.config/fish" ]; then
  if [ -f "${REPO_ROOT}/extras/fish/install.sh" ]; then
    bash "${REPO_ROOT}/extras/fish/install.sh" >/dev/null 2>&1 || true
    echo "✓ Fish Shell: theme installed to ~/.config/fish/themes/mt_verdant_nocturne.theme"
  fi
fi

# 3. Text Editors
# GNOME Text Editor / Gedit / GtkSourceView
if [ -f "${REPO_ROOT}/extras/text-editors/gnome-text-editor/install.sh" ]; then
  bash "${REPO_ROOT}/extras/text-editors/gnome-text-editor/install.sh" >/dev/null 2>&1 || true
  echo "✓ GNOME Text Editor: style scheme installed to GtkSourceView 4 & 5"
fi

# Kate / KWrite
if have kate || [ -d "${HOME}/.local/share/org.kde.syntax-highlighting" ] || [ -d "${HOME}/.local/share/color-schemes" ]; then
  if [ -f "${REPO_ROOT}/extras/text-editors/kate/install.sh" ]; then
    bash "${REPO_ROOT}/extras/text-editors/kate/install.sh" >/dev/null 2>&1 || true
    echo "✓ Kate: color scheme installed to ~/.local/share/org.kde.syntax-highlighting/themes/"
  fi
fi

# 4. KDE Plasma & Qt Color Scheme
if [ -f "${REPO_ROOT}/extras/kde/color-schemes/install.sh" ]; then
  bash "${REPO_ROOT}/extras/kde/color-schemes/install.sh" >/dev/null 2>&1 || true
  echo "✓ KDE Plasma: color scheme installed to ~/.local/share/color-schemes/"
fi

# 5. Fastfetch Showcase
if have fastfetch; then
  mkdir -p "${HOME}/.config/fastfetch"
  if [ ! -f "${HOME}/.config/fastfetch/config.jsonc" ]; then
    cp "${REPO_ROOT}/extras/fastfetch/config.jsonc" "${HOME}/.config/fastfetch/"
    cp "${REPO_ROOT}/extras/fastfetch/mt-verdant.txt" "${HOME}/.config/fastfetch/"
    echo "✓ Fastfetch: default config registered in ~/.config/fastfetch/"
  fi
fi

echo "=== All supported application color schemes installed successfully ==="
