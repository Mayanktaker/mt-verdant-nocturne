# Design — Botanical Canopy direction

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Single source of truth for colors: `palette/tokens.json` (do not hardcode hex values elsewhere).

## Principles
- **Dark-first, quiet surfaces:** charcoal-teal bases a step darker than Adwaita, never pure black; menus and dialogs stay opaque for readability.
- **Leaf-sage accent:** sage is the only action/focus/selection color; blossom-pink is decorative (wallpaper, branding) and never an action color.
- **Familiar GNOME shape:** upstream layout and spacing are kept; radii come from the `geometry` token scale so Shell, GTK3 and GTK4 agree.
- **Contrast is a gate:** `tools/dev/check_contrast.py` checks every emitted text/surface pair, UI edges, terminal ANSI colors and editor syntax colors (WCAG ≥4.5 body text, ≥3:1 UI components, ≥7 preferred).
- **System fonts**, no custom typography in the theme itself.

## Tokens (v0.4.0)
| Token | Value | Use |
|---|---|---|
| bg.base | #0F141B | panel, dialogs, cards |
| bg.base_darker | #0B0F14 | overview backdrop, OSD base |
| bg.oled | #050807 | true pitch-black OLED background (`--tweaks black`) |
| bg.tile | #16222A | quick-settings tiles, list rows |
| bg.surface / hover / active | #1D3238 / #2A4148 / #2E444B | raised surfaces and states |
| accent.base / strong / dim | #8FB8A6 / #A9CDBB / #6A8F88 | focus, selected, sliders, links (default Sage) |
| accent_flavors.emerald | #3DD68C | vibrant Aurora Emerald accent (`--accent emerald`) |
| accent_flavors.moss | #98B99A | earthy Everforest Moss accent (`--accent moss`) |
| accent_flavors.pine | #5E9E92 | Nordic Cypress Pine accent (`--accent pine`) |
| window_controls close/min/max | #E5737F / #E5B580 / #7FC8A0 | macOS/Colloid traffic light buttons (`--tweaks macos`) |
| text.primary / secondary / disabled | #E9F1EC / #A7B8B1 / #6C7C75 | foreground tiers |
| status destructive/success/warning | #E5737F / #7FC8A0 / #E5B580 | semantic states |
| status.petal_decorative | #C9A3B0 | artwork only |
| border.default / subtle / oled | #2C3E44 / #223237 / #1A2624 | separators, edges |
| window_controls glyph / hovers | #141C22 / #F28591 / #F0C38F / #8ED9AD | traffic-light dots |
| geometry.radius | control 8 · tile 12 · popover 16 · dock 24 · dialog 22 · pill 999 | one radius scale across layers |
| art.dark / art.light | palette blocks | procedural wallpaper palettes |

Every text pair is verified ≥4.5:1 on every surface it is drawn on; disabled text targets ≥3:1 and UI edges ≥3:1. Terminals and the editor theme are checked by the same gate.

## Modular Tweaks System
Flags map onto one implementation, and unknown values fail loudly:
- **Canopy Floating Glass (default)**: `--panel round-island`, `--blur` (translucent; real blur when Blur My Shell is present), `--controls macos`, quick-settings polish.
- **Obsidian Pro**: `--oled` (pitch-black surfaces), `--size compact`, `--rimless` (borderless windows), `--accent emerald`.
- **Nordic Evergreen**: `--panel bottom-round` or `--panel round-island`, `--no-blur`, `--accent moss` or `pine`.
- Legacy `--tweaks float,translucent,black,rimless,compact,macos,round,noblur` maps onto the flags above.

## 4K Wallpaper Suite Rules
Eight procedural artworks from one shared renderer (`tools/wallpaper/generate.py`), four night and four dawn. Dark pieces target 28–50/255 mean luminance so they read on normal panels; all outputs are 3840×2160 JPEG with 1920×1080 previews. No photographic sources.

Night:
1. **Botanical Canopy (Midnight Fern)**: Night-garden foliage in theme tones with restrained pale-pink blossoms and quiet moonlight.
2. **Verdant Aurora (Nordic Pines)**: Silhouetted pine forest under a glowing emerald and sage aurora borealis gradient with distant stars.
3. **Zen Flora (Geometric Contour)**: Bauhaus/Material-inspired organic geometric leaf contour curves on deep obsidian teal.
4. **Obsidian River (Mineral Flow)**: Fluid topographic elevation isolines with glowing sage mineral veins over dark riverbed bedrock.

### Dawn Suite (`wallpaper/dist/light/`)
The same four compositions re-voiced with the `art.light` palette, so both suites share one style:
1. **Botanical Canopy Dawn (Morning Mist)**: The canopy frame in warm morning light.
2. **Celestial Rift (Sage Sky)**: Aurora ribbons over pale pine ridges.
3. **Cosmic Dawn (Stellar Amber)**: Architectural leaf contours on a dawn gradient.
4. **Botanical Horizon (Aurora Dawn)**: Topographic flow in muted sage.

- The compact suite (~1.5 MB total) ships with the theme so GNOME Settings entries always resolve; only the selected image is applied to the desktop.
- 1920×1080 preview JPGs reside in `wallpaper/preview/` and `wallpaper/preview/light/`.
- Dynamic Day/Night switching:
  - **Adaptive pairing** (`--wallpaper dynamic`): Pairs Canopy Dawn for GNOME Light style (`picture-uri`) and Midnight Fern for GNOME Dark style (`picture-uri-dark`).
  - **24-hour timed cycle** (`--wallpaper timed`): Continuous clock-based cross-fade via `mt-verdant-timed.xml`.
  - Registered natively into GNOME Settings Backgrounds via `~/.local/share/gnome-background-properties/mt-verdant.xml`.
- Applying wallpaper is opt-in via `./install.sh --wallpaper [1-4|light-1..4|dynamic|timed|all]`; unknown values exit with an error.

## Icon & Cursor Suite
The `MT-Verdant-Icons` and `MT-Verdant-Cursors` packs are maintained in a separate public repository:
[Mayanktaker/mt-verdant-icons](https://github.com/Mayanktaker/mt-verdant-icons). They follow the same
Botanical Canopy palette (obsidian `#122329`–`#24444D`, sage `#8FB8A6`, emerald `#3DD68C`) but own
their palette file and build pipeline so they can be released independently.
