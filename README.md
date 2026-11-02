# MT Verdant Nocturne

[![Release](https://img.shields.io/badge/release-v0.4.0-8fb8a6.svg?style=flat-square)](https://github.com/Mayanktaker/mt-verdant-nocturne/releases/tag/v0.4.0)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-3dd68c.svg?style=flat-square)](LICENSES/GPL-3.0.txt)
[![Showcase](https://img.shields.io/badge/Showcase-GitHub%20Pages-7fc8a0.svg?style=flat-square)](https://mayanktaker.github.io/mt-verdant-nocturne/)

© Mayanktaker Computers & Web Development | https://mayanktaker.com

A premium dark theme ecosystem for Linux desktops — GNOME Shell 50/51, GTK3, GTK4 (best-effort), and Flatpak — inspired by modern desktop aesthetics (Colloid, WhiteSur, TokyoNight, Catppuccin, Everforest). Featuring a quiet charcoal-teal "Botanical Canopy" palette, modular tweak flags, compact and standard sizing profiles, frosted glass and crisp no-blur modes, eight procedural 4K wallpapers (four night, four dawn, ~1.5 MB total), a matching companion icon and cursor pack, and presets across popular terminals and desktop apps.

🌐 **Live Showcase Website:** [https://mayanktaker.github.io/mt-verdant-nocturne/](https://mayanktaker.github.io/mt-verdant-nocturne/)

---

## Desktop Showcase & Design Variants (concept mockups)

| **Option A: Canopy Floating Glass** |
|:---:|
| ![Option A: Canopy Floating Glass](screenshots/option-a-floating-glass.png) |
| *Concept mockup, not a screenshot. Real GTK3/GTK4 renders ship in the release notes.* |

| **Option B: Obsidian Pro (Compact & OLED)** |
|:---:|
| ![Option B: Obsidian Pro](screenshots/option-b-obsidian-compact.png) |
| *Compact Sizing · OLED Deep Black · Rimless Crisp Corners · High-Density Headerbars* |

| **Option C: Nordic Evergreen (Organic Tactile)** |
|:---:|
| ![Option C: Nordic Evergreen](screenshots/option-c-nordic-organic.png) |
| *Standard Sizing · Solid Forest Surfaces · Warm Tactile Cards & Curved Window Accents* |

| **Multi-App Ecosystem & Terminals Showcase** |
|:---:|
| ![Multi-App Ecosystem](screenshots/showcase-terminals-apps.png) |
| *Ghostty · Kitty · GNOME Terminal · Fastfetch · Kate · GNOME Text Editor · Nautilus High-DPI Icons* |

---

## Verified Renders (real, not mockups)

These are headless renders of the built theme (sage accent) from the release gate: GTK3 on the left, GTK4/libadwaita with the opt-in override on the right.

| GTK3 widgets | GTK4 / libadwaita widgets |
|---|---|
| ![GTK3 real render](screenshots/real-gtk3-widgets.png) | ![GTK4 real render](screenshots/real-gtk4-widgets.png) |

Live GNOME Shell 51.1 (Wayland), captured after installing the release archive:

| Floating panel | Settings (libadwaita) |
|---|---|
| ![Live floating panel](screenshots/live-panel-51.png) | ![Live Settings](screenshots/live-settings-51.png) |

---

## Highlights & Features

- **Modular options**: `--panel round-island|pill|bottom-round|flat`, `--controls standard|macos`, `--accent sage|emerald|moss|pine`, `--size standard|compact`, `--oled`, `--rimless`, `--blur | --no-blur`. Legacy `--tweaks a,b,c` maps onto the same flags.
- **Sizing Density Profiles**:
  - `--size standard`: Balanced padding, generous touch targets, and comfortable typography.
  - `--size compact`: Reduced 38px headerbar height, tighter list items, and high-DPI space optimization for laptops and developers.
- **Blur & Compositing Profiles**:
  - `--blur`: Translucent panels. Real frosted blur requires the Blur My Shell extension; the installer configures it when present.
  - `--no-blur`: Opaque, high-contrast surfaces with zero compositor overhead.
- **Botanical Accent Flavors**:
  - `sage` (Default): Botanical Sage (`#8FB8A6`)
  - `emerald`: Aurora Emerald (`#3DD68C`)
  - `moss`: Earthy Moss (`#98B99A`)
  - `pine`: Nordic Pine (`#5E9E92`)
- **8 Procedural 4K Wallpapers (3840×2160)** — one art system, night and dawn:
  1. *Botanical Canopy* / *Botanical Canopy Dawn*
  2. *Verdant Aurora* / *Celestial Rift*
  3. *Zen Flora* / *Cosmic Dawn*
  4. *Obsidian River* / *Botanical Horizon*
  - GNOME adaptive pairs and a 24-hour timed cycle are registered automatically.
- **Companion Icon & Cursor Pack**:
  - `MT-Verdant-Icons` and `MT-Verdant-Cursors` now live in their own repository so they can be versioned and updated independently: [Mayanktaker/mt-verdant-icons](https://github.com/Mayanktaker/mt-verdant-icons).
  - The pack ships 100+ handcrafted application icons, botanical gradient folders, complete symbolic coverage, and matching obsidian pointers with sage glowing tips. Install it with:
    ```sh
    git clone https://github.com/Mayanktaker/mt-verdant-icons.git
    cd mt-verdant-icons && ./install.sh
    ```
- **Universal Application Support**: Ready-to-use color schemes for Kitty, Ghostty, Alacritty, Foot, GNOME Terminal, Fish Shell, Kate/KWrite, GNOME Text Editor, KDE Plasma, Fastfetch, GRUB bootloader, and Plymouth.

---

## 4K Wallpaper Gallery

| Night: Botanical Canopy | Night: Verdant Aurora |
|---|---|
| ![Canopy](wallpaper/preview/mt-verdant-canopy-1920x1080.jpg) | ![Aurora](wallpaper/preview/mt-verdant-aurora-1920x1080.jpg) |
| **Night: Zen Flora** | **Night: Obsidian River** |
| ![Flora](wallpaper/preview/mt-verdant-flora-1920x1080.jpg) | ![River](wallpaper/preview/mt-verdant-river-1920x1080.jpg) |
| **Dawn: Botanical Canopy Dawn** | **Dawn: Celestial Rift** |
| ![Canopy Dawn](wallpaper/preview/light/mt-verdant-canopy-dawn-1920x1080.jpg) | ![Celestial Rift](wallpaper/preview/light/mt-verdant-celestial-rift-1920x1080.jpg) |

---

## Installation & Setup Wizard (User-level, no root required)

User themes are installed exclusively into `~/.themes`. The companion icon and cursor packs install into `~/.icons` from their own repository.

### Interactive Setup Wizard (Recommended)
Simply run the installer without arguments to launch the friendly, step-by-step configuration wizard:

```sh
git clone https://github.com/Mayanktaker/mt-verdant-nocturne.git
cd mt-verdant-nocturne

# Run interactive wizard (prompts for tray style, controls, blur, density, accent, wallpapers):
./install.sh
```

### Direct CLI Installation (Human-Friendly Options)

```sh
# 1. Default Recommended: 16px Rounded Modern Island Tray Bar + Standard Clean Buttons:
./install.sh --panel round-island --controls standard

# 2. Floating Capsule Pill Bar + macOS Traffic Dots:
./install.sh --panel pill --controls macos

# 3. Connected Bottom-Rounded Top Bar (Screen-attached top edge, 16px curved bottom corners):
./install.sh --panel bottom-round

# 4. Classic Full-Width Edge-to-Edge Square Bar:
./install.sh --panel flat

# 5. Sizing and Blur Customization:
./install.sh --size compact --no-blur    # High density, crisp solid surfaces (laptops/low-GPU)
./install.sh --size standard --blur      # Balanced density, frosted glass translucency

# 6. Botanical Accent Colors (applied to Shell, GTK3 and GTK4 at build time):
./install.sh --accent sage               # Sage (#8FB8A6, default)
./install.sh --accent emerald            # Emerald (#3DD68C)
./install.sh --accent moss               # Moss (#98B99A)
./install.sh --accent pine               # Pine (#5E9E92)

# 7. Surfaces & window style:
./install.sh --oled --rimless            # Pure-black surfaces, borderless windows
./install.sh --no-blur                   # Solid surfaces

# 8. 4K Wallpapers:
./install.sh --wallpaper 1               # Dark Canopy (1-4)
./install.sh --wallpaper light-1         # Dawn Canopy (light-1..light-4)
./install.sh --wallpaper dynamic         # Dawn by day, Canopy by night
./install.sh --wallpaper timed           # 24-hour XML cycle
./install.sh --wallpaper all             # Copy all eight to ~/Pictures/wallpapers-mt-verdant

# 9. Scripting & Automation (Non-interactive mode):
./install.sh --non-interactive --panel round-island --controls standard --accent emerald

# 10. Remove the theme (keeps a parked copy, restores GTK4 backups):
./install.sh --uninstall
```

### Standalone Icon & Cursor Suite Installation (Any Linux Desktop)

If you only want the **MT-Verdant-Icons** and **MT-Verdant-Cursors** packs on any desktop environment (GNOME, KDE Plasma, XFCE, Cinnamon, Sway, Hyprland) without the full theme, install them from their own repository:

```sh
git clone https://github.com/Mayanktaker/mt-verdant-icons.git
cd mt-verdant-icons
./install.sh
```

---

## Supported App Ecosystem & Color Schemes

All application themes are bundled under `extras/` and use the single source of truth color tokens from `palette/tokens.json`.

### Quick Setup: One-Click App Theme Installer
To scan your system and install matching color schemes for all detected terminals, shells, and text editors (activation stays opt-in):
```sh
./tools/extras/install-all.sh
```

### Manual App Installation

- **Ghostty**:
  ```sh
  mkdir -p ~/.config/ghostty/themes
  cp extras/terminals/ghostty/mt-verdant-nocturne ~/.config/ghostty/themes/
  # In ~/.config/ghostty/config: theme = mt-verdant-nocturne
  ```
- **Kitty**:
  ```sh
  mkdir -p ~/.config/kitty/themes
  cp extras/terminals/kitty/mt-verdant-nocturne.conf ~/.config/kitty/themes/
  # In ~/.config/kitty/kitty.conf: include themes/mt-verdant-nocturne.conf
  ```
- **Alacritty**:
  ```sh
  mkdir -p ~/.config/alacritty/themes
  cp extras/terminals/alacritty/mt-verdant-nocturne.toml ~/.config/alacritty/themes/
  # In ~/.config/alacritty/alacritty.toml: import = ["~/.config/alacritty/themes/mt-verdant-nocturne.toml"]
  ```
- **Foot**:
  ```sh
  mkdir -p ~/.config/foot/themes
  cp extras/terminals/foot/mt-verdant-nocturne.ini ~/.config/foot/themes/
  # In ~/.config/foot/foot.ini: include = ~/.config/foot/themes/mt-verdant-nocturne.ini
  ```
- **GNOME Terminal**:
  ```sh
  # Automatically registers the "MT Verdant Nocturne" profile via dconf:
  bash extras/terminals/gnome-terminal/install.sh
  ```

### 2. Shells
- **Fish Shell**:
  ```sh
  bash extras/fish/install.sh
  fish_config theme choose "mt_verdant_nocturne"   # or: bash extras/fish/install.sh --apply
  ```

### 3. Text Editors & IDEs
- **GNOME Text Editor / Gedit / GtkSourceView 4 & 5**:
  ```sh
  bash extras/text-editors/gnome-text-editor/install.sh
  # Select "MT Verdant Nocturne" under Text Editor Preferences -> Appearance.
  ```
- **KDE Kate & KWrite**:
  ```sh
  bash extras/text-editors/kate/install.sh
  # Select "MT Verdant Nocturne" in Kate Settings -> Configure Kate -> Color Themes.
  ```
- **VS Code**: Complete editor syntax and workbench theme located in `extras/vscode/`.

### 4. KDE Plasma & Qt Apps
- **KDE Plasma Color Scheme**:
  ```sh
  bash extras/kde/color-schemes/install.sh
  # Apply "MT Verdant Nocturne" in System Settings -> Colors & Themes -> Color Scheme.
  ```

### 5. Fastfetch CLI Showcase
- Run the custom nocturnal ASCII tree and specs:
  ```sh
  fastfetch -c extras/fastfetch/config.jsonc
  ```

### 6. Boot & Login Screens
- **GRUB Bootloader**:
  ```sh
  # Installs 4K nocturnal boot theme with styled selector box (requires sudo):
  sudo bash extras/grub/mt-verdant-nocturne/install.sh
  ```
- **Plymouth Boot Splash**:
  ```sh
  sudo bash extras/plymouth/mt-verdant-nocturne/install.sh
  ```
- **SDDM Greeter**: Complete QML theme located in `extras/sddm/mt-verdant-nocturne/`.
- **GDM Greeter**: GNOME Display Manager CSS located in `extras/gdm/`.

---

## Build from Source

```sh
# Every gate the release runs
python3 tools/dev/check_contrast.py        # 103+ pairs incl. terminals and editor colors
python3 tools/dev/check_colors.py          # no color literals outside tokens
python3 tools/dev/check_selectors.py       # tweak selectors exist in Shell 50/51
python3 tools/dev/check_version.py

# Generate and verify the 8 wallpaper suite
python3 tools/wallpaper/generate.py --verify

# Build Shell (all mapped majors) and GTK3 for a chosen accent
python3 tools/shell/build.py --all --accent emerald
python3 tools/gtk/build.py --accent emerald

# Sandboxed install test (source tree or release tarball)
sh tools/dev/smoke-install.sh .

# Full release archive with per-accent presets + packaged-installer smoke test
sh tools/release.sh 0.4.0
```

---

## Layer & Component Matrix

| Layer | Status | Target Location |
|---|---|---|
| GNOME Shell 51.1 | Verified live (theme loads, floating panel, libadwaita app); quick settings/overview manual pass pending | `~/.themes/MT-Verdant-Nocturne/gnome-shell/` |
| GNOME Shell 50.x | Built from vendored 50 CSS; live session test pending | `~/.themes/MT-Verdant-Nocturne/gnome-shell/` |
| GTK3 Apps | Verified with a headless widget probe (standard, compact, macOS dots, rimless) | `~/.themes/MT-Verdant-Nocturne/gtk-3.0/` |
| GTK2 Legacy | Fallback `gtkrc` for older apps (GIMP 2.10, Audacity) | `~/.themes/MT-Verdant-Nocturne/gtk-2.0/` |
| GTK4 / Libadwaita | Opt-in best-effort override (`--gtk4-libadwaita`), probe-verified | `~/.config/gtk-4.0/gtk.css` |
| Flatpak GTK3 | Sandboxed apps via `org.gtk.Gtk3theme.MT-Verdant-Nocturne` | `flatpak/` |
| 4K Wallpapers | 8 procedural artworks (4 night + 4 dawn) | `${THEME_DIR}/wallpapers/` |
| Terminal Schemes | Kitty, Ghostty, Alacritty, Foot, GNOME Terminal | `extras/terminals/` |
| Shells | Fish syntax highlighting | `extras/fish/` |
| Text Editors | GtkSourceView 4/5, Kate/KWrite, VS Code | `extras/text-editors/`, `extras/vscode/` |
| KDE / Qt | Plasma Color Scheme | `extras/kde/color-schemes/` |
| Boot Screens | GRUB (4K) & Plymouth animated splash | `extras/grub/`, `extras/plymouth/` |
| Greeters | SDDM (QML) & GDM (CSS) | `extras/sddm/`, `extras/gdm/` |

---

## Troubleshooting

- **Icons not refreshing in Nautilus or Dash?**
  Rebuild the user icon cache in the icon pack repository:
  ```sh
  cd mt-verdant-icons
  ./install.sh
  ```
  Installing the pack again refreshes `~/.icons/MT-Verdant-Icons` and its cache.
- **Shell styles not reloading on Wayland?**
  Toggle the User Themes extension via Extensions app or log out and back in to reload GNOME Shell CSS.

---

## License

- Code, CSS, and build scripts: [GPL-3.0](LICENSES/GPL-3.0.txt)
- Wallpapers and artwork: [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt)
- Icons and cursors are licensed in the [mt-verdant-icons](https://github.com/Mayanktaker/mt-verdant-icons) repository.
