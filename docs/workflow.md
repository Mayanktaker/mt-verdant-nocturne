# Workflow — build & release

© Mayanktaker Computers & Web Development | https://mayanktaker.com

## Milestone flow
1. `python3 tools/dev/check_contrast.py` — must pass.
2. Build the layer being changed (`tools/shell/build.py`, `tools/gtk/build.py`, `tools/wallpaper/generate.py`).
3. Verify on the host session (Wayland: re-login or toggle User Themes off/on to reload CSS).
4. Commit a small, coherent change; push verified milestones only.
5. Update `docs/compatibility.md` and tick the plan step when a milestone completes.

## Release flow
- Tag `vX.Y`; attach the built theme tarball + 4K wallpaper PNG from `wallpaper/dist/`.
- Release notes are written for end users: what looks different, what got smoother, what was fixed — no internal identifiers.

## Repo rules
- Public repo: `github.com/Mayanktaker/mt-verdant-nocturne` (main branch).
- No force-push, no history rewrites after push; license/secrets check before every push.
