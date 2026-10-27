# MT Verdant Nocturne

© Mayanktaker Computers & Web Development | https://mayanktaker.com

A dark GNOME theme suite — GNOME Shell, GTK3, GTK4 (best-effort) — in a quiet
charcoal-teal "Botanical Canopy" palette grown from a night-garden wallpaper,
plus a matching original wallpaper. Icon and cursor themes are planned follow-ups.

![wallpaper preview](wallpaper/preview/mt-verdant-nocturne-1920x1080.jpg)

## Requirements
- GNOME Shell **50.x or 51.x** (only versions actually tested are supported)
- GNOME's **User Themes** extension for the Shell theme
- Flatpak GTK3 apps additionally need the theme extension (see `docs/flatpak.md`)

## Install (user-level, no root)
```sh
git clone https://github.com/Mayanktaker/mt-verdant-nocturne.git
cd mt-verdant-nocturne
./tools/install.sh              # theme only
./tools/install.sh --wallpaper  # also set the wallpaper (opt-in)
```

## Build from source
```sh
python3 tools/dev/check_contrast.py     # WCAG gate
python3 tools/wallpaper/generate.py     # regenerate wallpaper renders
python3 tools/shell/build.py            # GNOME Shell theme
python3 tools/gtk/build.py              # GTK3 + GTK4 themes
```

## What's themed
| Layer | Status |
|---|---|
| GNOME Shell 50/51 | tested |
| GTK3 apps | tested |
| GTK4 / libadwaita | best-effort overrides, app-dependent |
| Flatpak GTK3 | via `org.gtk.Gtk3theme.MT-Verdant-Nocturne` |
| Icons / cursors | planned (not started) |

See `docs/compatibility.md` for the full version matrix and known limitations.

## License
- Code, CSS, build scripts: [GPL-3.0](LICENSES/GPL-3.0.txt)
- Wallpaper and artwork: [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt)
