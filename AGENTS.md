# AGENTS.md — MT Verdant Nocturne

© Mayanktaker Computers & Web Development | https://mayanktaker.com

GNOME dark theme suite: Shell + GTK3 + GTK4 (best-effort) + Flatpak GTK3 extension.
Display name **MT Verdant Nocturne**, technical/theme-dir name `MT-Verdant-Nocturne`.

## Stack & toolchain (verify before assuming; update when versions change)
- Targets: GNOME Shell 50.x and 51.x (host dev machine: GNOME Shell 51.1, Wayland).
- Build: `sassc` (libsass 3.6.6), Python 3 + `numpy` 2.5.4 + `Pillow` 13.0.0.
- Repo: git 2.56, `gh` 2.102.1 authenticated as `Mayanktaker`.
- User-level install only: `~/.local/share/themes/MT-Verdant-Nocturne/`; Shell theme needs the **User Themes** extension (`user-theme@gnome-shell-extensions.gcampax.github.com`).

## Single source of truth
- `palette/tokens.json` — every color in CSS/wallpaper/builds comes from here. No new magic values; add tokens instead.
- Shell theme is derived from upstream GNOME Shell CSS per major version, recolored via `src/shell/` maps (never hand-edit generated CSS).

## Commands
- Contrast gate: `python3 tools/dev/check_contrast.py` (must pass before commits).
- Wallpaper: `python3 tools/wallpaper/generate.py` → `wallpaper/dist/` (4K render is gitignored; preview JPG is committed).
- Shell theme build: `python3 tools/shell/build.py` (extracts upstream CSS → recolors → writes `build/theme/gnome-shell/`).
- GTK build: `python3 tools/gtk/build.py` → `build/theme/gtk-{3,4}.0/`.
- Install: `tools/install.sh` (user-level; no root). Wallpaper apply is always opt-in via `--wallpaper`.

## Layout
- `palette/` tokens · `src/` per-layer sources & color maps · `tools/` generators + installer
- `build/` generated output (gitignored) · `wallpaper/preview/` committed previews · `docs/` focused docs

## Documentation pointers (do not duplicate content here)
- `docs/design.md` — Botanical Canopy direction, token table, wallpaper rules
- `docs/compatibility.md` — GNOME version matrix + test checklist
- `docs/flatpak.md` — Flatpak GTK3 theme extension plan & status
- `docs/workflow.md` — build/release workflow

## Conventions
- Every file starts with the © header comment above; every function/block gets ≤1-line comment.
- License: GPL-3.0 (code/CSS) + CC BY-SA 4.0 (artwork). See `LICENSES/`.
- Public repo `Mayanktaker/mt-verdant-nocturne`; commit at verified milestones, never force-push, secrets/license scan before push.
