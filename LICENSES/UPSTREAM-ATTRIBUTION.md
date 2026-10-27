# Upstream attribution

© Mayanktaker Computers & Web Development | https://mayanktaker.com

MT Verdant Nocturne derives from GNOME upstream theme code:

- **GNOME Shell stylesheet** — derived at build time from the installed
  `gnome-shell-theme.gresource` (upstream `gnome-shell` project, GPLv2+),
  recolored through our token maps. Not committed verbatim; regenerated per host.
- **GTK3 theme SASS** — `src/gtk-3.0/upstream/` vendors the upstream Adwaita
  theme from the gtk `gtk-3-24` branch (LGPL-2.1+). Our build patches its base
  color variables only; derived markup is untouched.
- **GTK4 overrides** — original CSS in `src/gtk-4.0/overrides.css` (GPL-3.0),
  using GTK4's documented `@define-color` names.

Project modifications and original files are GPL-3.0 (code/CSS) and
CC BY-SA 4.0 (artwork); see `LICENSES/`.
