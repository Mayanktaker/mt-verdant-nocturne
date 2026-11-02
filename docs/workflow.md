# Workflow — build & release

© Mayanktaker Computers & Web Development | https://mayanktaker.com

## Milestone flow
1. `python3 tools/dev/check_contrast.py` — every text/surface, UI-edge, terminal and editor pair must pass.
2. `python3 tools/dev/check_colors.py` — no color literal outside `palette/tokens.json`.
3. `python3 tools/dev/check_selectors.py` — every Shell tweak selector must exist in the vendored 50/51 CSS.
4. `python3 tools/dev/check_version.py` — VERSION, tokens meta, README badge and release notes agree.
5. Build the changed layer:
   - `python3 tools/shell/build.py --all --accent <flavor>`
   - `python3 tools/gtk/build.py --accent <flavor>`
   - `python3 tools/wallpaper/generate.py --verify`
6. `sh tools/dev/smoke-install.sh .` — sandboxed install, accent/panel/controls/wallpaper assertions, OLED + rimless, strict CLI rejection, uninstall.
7. Verify on the host session (Wayland: re-login or toggle User Themes off/on to reload CSS).
8. Commit a small, coherent change; push verified milestones only.
9. Update `docs/compatibility.md` and tick the plan step when a milestone completes.

## Release flow
- Bump `VERSION`, `palette/tokens.json:meta.version`, the README badge and add `docs/release-notes/v<version>.md`.
- Run `sh tools/release.sh <version>`. It:
  - runs every gate and regenerates the 8-wallpaper suite;
  - builds Shell + GTK3 presets for **all four accents** under `presets/<accent>/`;
  - pre-renders tokenized tweaks and GTK4 overrides per accent (the release installer needs no sassc);
  - assembles the archive, then extracts it into a temp `HOME` and installs it, asserting that emerald reaches Shell, GTK3 and GTK4.
- Tag `vX.Y`, push, `gh release create` with the tarball.
- Release notes are written for end users: what looks different, what got smoother, what was fixed — no internal identifiers.

## Repo rules
- Public repo: `github.com/Mayanktaker/mt-verdant-nocturne` (main branch).
- No force-push, no history rewrites after push; license/secrets check before every push.
- Never hard-delete user installs; park to `deleted_files_folders/`.

## Ownership of state
- `palette/tokens.json` owns colors, accents, geometry and the wallpaper palettes.
- `src/tweaks/**` are templates; never put hex literals in them (`{{dotted.token}}` only).
- `tools/theme/render.py` renders templates for the selected accent at build/install time.
- `src/shell/upstream-<major>/` is vendored upstream CSS; regenerate it from the matching gresource, never hand-edit.
