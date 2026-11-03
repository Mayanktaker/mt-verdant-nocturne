# Compatibility matrix

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Policy: a GNOME version is listed only after it passed the checklist below on a
real session (host or disposable VM). "50+" never implies untested future releases.

| Layer | GNOME 50.x | GNOME 51.1 (host) | Notes |
|---|---|---|---|
| GNOME Shell CSS | **built** from vendored 50.6 upstream; live test pending | **verified live** on 51.1: loads without CSS parse errors, floating panel renders | upstream-extract + token map; all four accents built; high-contrast sheet recoloured |
| GTK3 apps | same build as 51 | **verified** with a live app and a headless widget probe (buttons, entries, switches, sliders, rows) | vendored gtk-3-24 SASS, per-accent build |
| GTK4 apps (plain) | same build as 51 | **verified live** in Shelly 3.1.10 (package grid, detail form, entries, checks, action buttons) + headless widget probe | full Adwaita dark base recoloured from tokens; every widget styled, no Adwaita blue left |
| libadwaita apps | n/a | **verified** in a libadwaita probe (preferences page, entry, switch, action buttons) | opt-in `--gtk4-libadwaita` colour contract only; libadwaita keeps its own widget CSS |
| Flatpak GTK3 | **built + mount-verified** | same | in-app visual pass deferred; details in docs/flatpak.md |
| Wallpaper | n/a | n/a | 8 procedural 4K JPEGs, adaptive pairs + timed cycle; apply is opt-in |
| Installer | n/a | verified from source **and** from the release archive in a sandboxed HOME | unknown values exit 2; uninstall restores GTK4 backups |

## Test checklist (per Shell major)
- [ ] Theme loads via User Themes extension without stylesheet parse errors (check `journalctl` / Looking Glass)
- [ ] Panel, calendar, quick settings, notifications, OSD readable; focus ring visible everywhere
- [ ] Overview, dash, app grid, search, window/workspace switcher correct
- [ ] Lock screen / unlock dialog session UI correct
- [ ] Dark style + high-contrast spot check; keyboard-only navigation
- [ ] Accent matrix: sage / emerald / moss / pine identical across Shell, GTK3 and GTK4
- [ ] Destructive button and selected-row contrast spot check
- [ ] GTK3 apps (e.g. a classic GTK3 app) + GTK4/libadwaita apps (Files, Settings) spot check
- [ ] Flatpak GTK3 app picks up the theme extension; result recorded in docs/flatpak.md

## Known limitations
- libadwaita apps replace the GTK theme with Adwaita by design, so the installed theme cannot style their widgets; the opt-in user CSS only supplies the colour contract.
- GTK4 sheet is generated from the host libgtk's Adwaita dark base, so a GTK major/minor that renames nodes can shift some exotic widget states until the next build.
- Shell CSS and wallpaper never affect the contents of Flatpak sandboxes.
- Blur requires the Blur My Shell extension; without it panels are translucent.
- GDM/login screen is intentionally not themed.
