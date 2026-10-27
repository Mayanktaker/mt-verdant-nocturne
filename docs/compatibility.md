# Compatibility matrix

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Policy: a GNOME version is listed only after it passed the checklist below on a
real session (host or disposable VM). "50+" never implies untested future releases.

| Layer | GNOME 50.x | GNOME 51.1 (host) | Notes |
|---|---|---|---|
| GNOME Shell CSS | pending test | pending test | built from upstream per-major CSS |
| GTK3 apps | pending test | pending test | |
| GTK4 / libadwaita | best-effort | best-effort | app-dependent; see limitations |
| Flatpak GTK3 | pending test | pending test | via theme extension |
| Wallpaper | n/a | n/a | version-independent |

## Test checklist (per Shell major)
- [ ] Theme loads via User Themes extension without stylesheet parse errors (check `journalctl` / Looking Glass)
- [ ] Panel, calendar, quick settings, notifications, OSD readable; focus ring visible everywhere
- [ ] Overview, dash, app grid, search, window/workspace switcher correct
- [ ] Lock screen / unlock dialog session UI correct
- [ ] Dark style + high-contrast spot check; keyboard-only navigation
- [ ] GTK3 apps (e.g. a classic GTK3 app) + GTK4/libadwaita apps (Files, Settings) spot check
- [ ] Flatpak GTK3 app picks up the theme extension; result recorded in docs/flatpak.md

## Known limitations
- libadwaita apps limit third-party styling; GTK4 overrides are conservative and app-dependent.
- Shell CSS and wallpaper never affect the contents of Flatpak sandboxes.
- GDM/login screen is intentionally not themed.
