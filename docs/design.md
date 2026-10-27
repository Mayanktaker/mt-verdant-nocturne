# Design — Botanical Canopy direction

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Single source of truth for colors: `palette/tokens.json` (do not hardcode hex values elsewhere).

## Principles
- **Dark-first, quiet surfaces:** charcoal-teal bases a step darker than Adwaita, never pure black; menus and dialogs stay opaque for readability.
- **Leaf-sage accent:** sage is the only action/focus/selection color; blossom-pink is decorative (wallpaper, branding) and never an action color.
- **Familiar GNOME shape:** upstream layout, radius, and spacing are kept; only the palette is re-voiced.
- **Contrast is a gate:** `tools/dev/check_contrast.py` must pass (WCAG ≥4.5 body text, ≥7 preferred) before any milestone commit.
- **System fonts**, no custom typography in the theme itself.

## Tokens (v0.1.0)
| Token | Value | Use |
|---|---|---|
| bg.base | #0F141B | panel, dialogs, cards |
| bg.base_darker | #0B0F14 | overview backdrop, OSD base |
| bg.tile | #16222A | quick-settings tiles, list rows |
| bg.surface / hover / active | #1D3238 / #2A4148 / #35525A | raised surfaces and states |
| accent.base / strong / dim | #8FB8A6 / #A9CDBB / #52736F | focus, selected, sliders, links |
| text.primary / secondary / disabled | #E9F1EC / #A7B8B1 / #76877F | foreground tiers |
| status destructive/success/warning | #E5737F / #7FC8A0 / #E5B580 | semantic states |
| status.petal_decorative | #C9A3B0 | artwork only |
| border.default / subtle | #2C3E44 / #223237 | separators, edges |

All text/accent pairs verified ≥4.5:1 on their backgrounds (most ≥7:1).

## Wallpaper rules
- One original procedural artwork (`tools/wallpaper/generate.py`, seed 20261027) — night-garden foliage in theme tones with restrained pale-pink blossoms.
- Composition keeps the top fifth clean for the shell panel; vignette settles the edges.
- The 4K render lives in `wallpaper/dist/` (gitignored; shipped in releases); the committed artifact is the 1920×1080 preview JPG.
- Applying the wallpaper is always an explicit opt-in (`tools/install.sh --wallpaper`); the user's current background is never touched silently.
