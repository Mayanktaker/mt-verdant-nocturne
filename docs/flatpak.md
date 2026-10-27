# Flatpak compatibility

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Status: **built, installed, and mount-verified** on this host (freedesktop 26.08);
in-app visual pass consciously deferred.

## Verified
- Extension builds with `org.flatpak.Builder` (user-level, no root) and installs as
  `runtime/org.gtk.Gtk3theme.MT-Verdant-Nocturne/x86_64/3.22`.
- It **mounts inside every org.freedesktop.Platform 25.08/26.08 sandbox** at
  `/usr/share/runtime/share/themes/MT-Verdant-Nocturne/gtk-3.0/` with our
  `gtk.css`, `gtk-dark.css`, and `assets/` (verified via `flatpak run --command=ls`).
- Host side: the GTK3 theme itself resolves exact tokens in a live GTK probe.

## Key layout fact (modern runtimes)
The 25.08+ extension point mounts with `subdirectory-suffix gtk-3.0`, so the
extension payload root must be the **contents of `gtk-3.0/`** (the
`org.gtk.Gtk3theme.Adwaita-dark` pattern) — not a full theme tree (the pre-23.08
Yaru layout). Older runtimes that lack the suffix are not targeted.

## Deferred (accepted)
- In-app visual pass with a real GTK3 app (e.g. Firefox/GIMP flatpak) to confirm
  portal/XSettings propagation end-to-end. The SDK sandbox refuses display sockets
  (build runtime by design), so headless in-sandbox rendering isn't possible.
- Flathub submission: swap the manifest's `dir` source for the release tarball URL.

## Rules
- Theme name, extension suffix, and the host `gtk-theme` setting must all be exactly
  `MT-Verdant-Nocturne` for automatic matching.
- No broad host-filesystem overrides (`flatpak override --filesystem=~/.themes`) — the
  extension is the supported path; GTK4/libadwaita Flatpak apps stay best-effort.
