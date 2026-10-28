# AGENTS.md — MT Verdant Nocturne

© Mayanktaker Computers & Web Development | https://mayanktaker.com

GNOME dark theme suite: Shell + GTK3 + GTK4 (best-effort) + Flatpak GTK3 extension.
Display name **MT Verdant Nocturne**, technical/theme-dir name `MT-Verdant-Nocturne`.

## Stack & toolchain (verify before assuming; update when versions change)
- Targets: GNOME Shell 50.x and 51.x (host dev machine: GNOME Shell 51.1, Wayland).
- Build: `sassc` (libsass 3.6.6), Python 3 + `numpy` 2.5.4 + `Pillow` 13.0.0.
- Repo: git 2.56, `gh` 2.102.1 authenticated as `Mayanktaker`.
- **Installation policy:** ALWAYS install user themes into the user's `~/.themes` (e.g. `/home/<user>/.themes`) ONLY, and user icon/cursor packs into the user's `~/.icons` (e.g. `/home/<user>/.icons`) ONLY — never `~/.local/share/themes`, `~/.local/share/icons`, or system dirs. `tools/install.sh` implements and must keep this. Shell activation needs the **User Themes** extension (`user-theme@gnome-shell-extensions.gcampax.github.com`).
- **Installer behavior:** `tools/install.sh` detects distro (`/etc/os-release`) + GNOME Shell major (gate ≥50 with a matching colormap), checks missing packages/modules per distro (python3, gi, sassc, numpy, Pillow, User Themes extension) — only for parts it will actually build — prints the exact distro install command, and uses **sudo only for system package installs** via `--install-deps`; the theme install itself never needs root. Old installs under `~/.local/share/themes` are moved to `deleted_files_folders/`, never deleted.

## Single source of truth
- `palette/tokens.json` — every color in CSS/wallpaper/builds comes from here. No new magic values; add tokens instead.
- Shell theme is derived from upstream GNOME Shell CSS per major version, recolored via `src/shell/` maps (never hand-edit generated CSS).

## Commands
- Contrast gate: `python3 tools/dev/check_contrast.py` (must pass before commits).
- Wallpaper suite: `python3 tools/wallpaper/generate.py [--which 1|2|3|4|all]` (dark) and `python3 tools/wallpaper/process_light.py` (light) → generates 4K renders into `wallpaper/dist/` and `wallpaper/dist/light/` + preview JPGs in `wallpaper/preview/`.
- Icons & Cursors build: `python3 tools/icons/generate_icons.py && python3 tools/icons/generate_cursors.py` → builds `src/icons/` and `src/cursors/`.
- Shell theme build: `python3 tools/shell/build.py [--major N | --all]` (host major extracts from gresource; others use vendored `src/shell/upstream-<major>/`).
- GTK build: `python3 tools/gtk/build.py` → `build/theme/gtk-{3,4}.0/`.
- Install: `./install.sh` (interactive CLI wizard) or `tools/install.sh [--panel round-island|pill|bottom-round|flat] [--controls standard|macos] [--accent <flavor>] [--size standard|compact] [--blur|--no-blur] [--wallpaper [1-4|light-1..4|dynamic|timed|all]] [--icons] [--gtk4-libadwaita] [--install-deps]` → installs theme into `~/.themes/MT-Verdant-Nocturne` and icons/cursors into `~/.icons/` (user-only; copies 4K wallpapers into `${THEME_DIR}/wallpapers/` and extras into `${THEME_DIR}/extras/`).
- App extras install: `tools/extras/install-all.sh` (scans & installs for all detected apps) or individual scripts under `extras/`.

## Layout
- `palette/` tokens (v0.2.0 w/ flavors & OLED) · `src/` per-layer sources (shell, gtk, tweaks, icons, cursors) · `extras/` (terminals, fish, text-editors, kde, grub, sddm, gdm, plymouth, fastfetch, firefox, vscode) · `tools/` generators + installer
- `build/` generated output (gitignored) · `wallpaper/preview/` committed previews · `flatpak/` extension manifest + appdata · `docs/` focused docs

## Documentation pointers (do not duplicate content here)
- `docs/design.md` — Botanical Canopy direction, token table, wallpaper rules
- `docs/compatibility.md` — GNOME version matrix + test checklist
- `docs/flatpak.md` — Flatpak GTK3 theme extension plan & status
- `docs/workflow.md` — build/release workflow
- `docs/index.html` — GitHub Pages interactive showcase site
- `docs/release-notes/` — user-facing changelog and release notes

## Conventions
- Every file starts with the © header comment above; every function/block gets ≤1-line comment.
- License: GPL-3.0 (code/CSS) + CC BY-SA 4.0 (artwork). See `LICENSES/`.
- Public repo `Mayanktaker/mt-verdant-nocturne`; commit at verified milestones, never force-push, secrets/license scan before push.
