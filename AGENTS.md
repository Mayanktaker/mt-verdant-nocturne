# AGENTS.md — MT Verdant Nocturne

© Mayanktaker Computers & Web Development | https://mayanktaker.com

GNOME dark theme suite: Shell + GTK3 + GTK4 (best-effort) + Flatpak GTK3 extension.
Display name **MT Verdant Nocturne**, technical/theme-dir name `MT-Verdant-Nocturne`.

## Stack & toolchain (verify before assuming; update when versions change)
- Targets: GNOME Shell 50.x and 51.x (host dev machine: GNOME Shell 51.1, Wayland).
- Build: `sassc` (libsass 3.6.6), Python 3 + `numpy` 2.5.4 + `Pillow` 13.0.0.
- Repo: git 2.56, `gh` 2.102.1 authenticated as `Mayanktaker`.
- **Installation policy:** ALWAYS install user themes into the user's `~/.themes` (e.g. `/home/<user>/.themes`) ONLY — never `~/.local/share/themes` or system dirs. `tools/install.sh` implements and must keep this. Shell activation needs the **User Themes** extension (`user-theme@gnome-shell-extensions.gcampax.github.com`).
- **Installer behavior:** `tools/install.sh` detects distro (`/etc/os-release`) + GNOME Shell major (gate ≥50 with a matching colormap), checks missing packages/modules per distro (python3, gi, sassc, numpy, Pillow, User Themes extension) — only for parts it will actually build — prints the exact distro install command, and uses **sudo only for system package installs** via `--install-deps`; the theme install itself never needs root. Old installs under `~/.local/share/themes` are moved to `deleted_files_folders/`, never deleted.

## Single source of truth
- `palette/tokens.json` — every color in CSS/wallpaper/builds comes from here. No new magic values; add tokens instead.
- Shell theme is derived from upstream GNOME Shell CSS per major version, recolored via `src/shell/` maps (never hand-edit generated CSS).

## Commands
- Contrast gate: `python3 tools/dev/check_contrast.py` (must pass before commits).
- Wallpaper: `python3 tools/wallpaper/generate.py` → `wallpaper/dist/` (4K render is gitignored; preview JPG is committed).
- Shell theme build: `python3 tools/shell/build.py [--major N | --all]` (host major extracts from gresource; others use vendored `src/shell/upstream-<major>/`).
- GTK build: `python3 tools/gtk/build.py` → `build/theme/gtk-{3,4}.0/`.
- Install: `tools/install.sh [--wallpaper] [--gtk4-libadwaita] [--install-deps]` → installs into `~/.themes/MT-Verdant-Nocturne` (user-only; picks the Shell-major build; wallpaper always opt-in).
- Flatpak: `tools/flatpak/stage.sh` (stage extension payload), `tools/flatpak/local-fallback.sh` (user-level sandbox fallback; zero downloads).

## Layout
- `palette/` tokens · `src/` per-layer sources, shell color maps & vendored upstream CSS/SASS · `tools/` generators + installer
- `build/` generated output (gitignored) · `wallpaper/preview/` committed previews · `flatpak/` extension manifest + appdata · `docs/` focused docs

## Documentation pointers (do not duplicate content here)
- `docs/design.md` — Botanical Canopy direction, token table, wallpaper rules
- `docs/compatibility.md` — GNOME version matrix + test checklist
- `docs/flatpak.md` — Flatpak GTK3 theme extension plan & status
- `docs/workflow.md` — build/release workflow

## Conventions
- Every file starts with the © header comment above; every function/block gets ≤1-line comment.
- License: GPL-3.0 (code/CSS) + CC BY-SA 4.0 (artwork). See `LICENSES/`.
- Public repo `Mayanktaker/mt-verdant-nocturne`; commit at verified milestones, never force-push, secrets/license scan before push.
