# Flatpak compatibility

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Status: **packaged** — extension manifest + appdata + staging ready; building the
distributable extension and live-app verification are the remaining work.

## What's in place
- Manifest `flatpak/org.gtk.Gtk3theme.MT-Verdant-Nocturne.json`: `org.gtk.Gtk3theme`
  extension point, branch `3.22`, runtime `org.freedesktop.Platform` 26.08,
  theme installed at `/usr/share/runtime/share/themes/MT-Verdant-Nocturne/` (Yaru-style layout).
- Appdata for Flathub discovery; staging via `tools/flatpak/stage.sh` (runs the GTK build first).
- **Local fallback** `tools/flatpak/local-fallback.sh`: installs the documented
  user-scoped unmaintained-extension layout with zero downloads — use it when no
  remote/extension is available. Removal command printed by the script.

## Remaining
1. Build with flatpak-builder (`org.flatpak.Builder` from Flathub works user-level):
   `flatpak run org.flatpak.Builder --force-clean --user --install-deps-from=flathub --install flatpak/build flatpak/org.gtk.Gtk3theme.MT-Verdant-Nocturne.json`
2. Verify with a real GTK3 Flatpak app (auto-install via `active-gtk-theme`,
   mount at `/usr/share/themes/MT-Verdant-Nocturne/` inside the sandbox,
   Wayland Settings-portal and X11 XSettings propagation).
3. Record results here; Flathub submission needs the release tarball URL as the manifest source.

## Rules
- Theme name, extension suffix, and the host `gtk-theme` setting must all be exactly
  `MT-Verdant-Nocturne` for automatic matching.
- No broad host-filesystem overrides (`flatpak override --filesystem=~/.themes`) — the
  extension is the supported path; GTK4/libadwaita Flatpak apps stay best-effort.
