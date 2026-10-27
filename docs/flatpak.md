# Flatpak compatibility

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Status: **planned** — implemented in a later milestone of this plan.

## Approach
- Package the GTK3 theme as a Flatpak theme extension on the `org.gtk.Gtk3theme`
  extension point: ID `org.gtk.Gtk3theme.MT-Verdant-Nocturne`, with branches
  matching supported GNOME/Freedesktop runtime ABIs.
- Flatpak auto-installs the extension when the host `gtk-theme` setting equals
  `MT-Verdant-Nocturne` (`active-gtk-theme` conditional), so names must match exactly.
- A user-scoped local fallback (`~/.local/share/flatpak/extension/...`) covers
  development and machines without a configured remote.
- No broad host-filesystem overrides (`flatpak override --filesystem=~/.themes`)
  in documented setup: they weaken the sandbox and are not needed with the extension.

## Verification plan
- Real GTK3 Flatpak apps on each supported runtime branch.
- Wayland: theme propagates via the Settings portal; X11: via XSettings (`gsd-xsettings`).
- Record any apps/runtimes that ignore host theme settings.
- GTK4/libadwaita Flatpak apps are tested separately and labeled best-effort.

References: docs.flatpak.org — desktop-integration (theming), extensions (`org.gtk.Gtk3theme`).
