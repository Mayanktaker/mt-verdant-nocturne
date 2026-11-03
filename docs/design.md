# Design — Botanical Canopy direction

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Single source of truth for colors: `palette/tokens.json` (do not hardcode hex values elsewhere).

## Principles
- **Dark-first, quiet surfaces:** charcoal-teal bases a step darker than Adwaita, never pure black; menus and dialogs stay opaque for readability.
- **Leaf-sage accent:** sage is the only action/focus/selection color; blossom-pink is decorative (wallpaper, branding) and never an action color.
- **Familiar GNOME shape:** upstream layout and spacing are kept; radii come from the `geometry` token scale so Shell, GTK3 and GTK4 agree.
- **No Shell drop shadows:** outer `box-shadow` is removed from every Shell surface (popups, OSD, dash, panel, banners, dialogs); Blur My Shell supplies depth when installed. Shell spreads blur far wider than GTK, so even an 8px shadow read as a grey halo on light wallpapers. Inset focus rings stay.
- **Contrast is a gate:** `tools/dev/check_contrast.py` checks every emitted text/surface pair, UI edges, terminal ANSI colors and editor syntax colors (WCAG ≥4.5 body text, ≥3:1 UI components, ≥7 preferred).
- **System fonts**, no custom typography in the theme itself.

## Tokens (v0.5.1)
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
| geometry.radius | button 6 · control 8 · tile 12 · popover 16 · dock 24 · dialog 22 · pill 999 | one radius scale across layers |
| art.dark / art.light | palette blocks | procedural wallpaper palettes |

Every text pair is verified ≥4.5:1 on every surface it is drawn on; disabled text targets ≥3:1 and UI edges ≥3:1. Terminals and the editor theme are checked by the same gate.

## Modular Tweaks System
Flags map onto one implementation, and unknown values fail loudly:
- **Canopy Floating Glass (default)**: `--panel round-island`, `--blur` (translucent; real blur when Blur My Shell is present), `--controls macos`, quick-settings polish.
- **Obsidian Pro**: `--oled` (pitch-black surfaces), `--size compact`, `--rimless` (borderless windows), `--accent emerald`.
- **Nordic Evergreen**: `--panel bottom-round` or `--panel round-island`, `--no-blur`, `--accent moss` or `pine`.
- Legacy `--tweaks float,translucent,black,rimless,compact,macos,round,noblur` maps onto the flags above.

## GTK4 layer
A GTK4 theme *replaces* the widget stylesheet instead of extending Adwaita, so a colour-only `gtk-4.0/gtk.css` leaves plain GTK4 apps (Shelly, distro tools, anything not on libadwaita) with unstyled check buttons, list cards and action buttons. The build therefore inlines GTK's own Adwaita dark sheet as the base, recolours its identity colours through `src/gtk-4.0/recolor.json`, rebases its asset URLs onto GTK's gresource, and then appends the curated token layer in `src/gtk-4.0/overrides.css`:

- **Surfaces:** window, headerbar, sidebar, view, cards and popovers from the `bg.*` tokens.
- **Buttons:** 6px radius, raised fill, flat/hover/active states, solid Sage suggested and coral destructive actions with the dark label the rest of the suite uses.
- **Inputs:** recessed `bg.base_darker` fill, `border.default` edge, 8px radius, accent border plus inner ring on focus, dim placeholder, muted disabled.
- **Checks and radios:** 16px indicator with a visible edge, Sage fill and dark glyph when checked, 4px (check) and pill (radio) radius.
- **Lists, tabs, sliders, switches, selects, tooltips, scrollbars:** recoloured from the same tokens so no Adwaita blue or grey leaks through.

Surface variants live in `src/tweaks/gtk4/` (`black.css` for OLED, `rimless.css`, `compact.css`, `macos.css`), written against GTK4 node names; the installer appends them after the curated sheet instead of reusing the GTK3 tweak files.

`tools/gtk4/build.py` also emits `gtk-4.0/user.css`, the opt-in `~/.config/gtk-4.0/gtk.css` contract for libadwaita apps. It carries the `@define-color` names only, never the base sheet, so libadwaita keeps its own widget CSS and only takes our palette.

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
