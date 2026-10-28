# Design — Botanical Canopy direction

© Mayanktaker Computers & Web Development | https://mayanktaker.com

Single source of truth for colors: `palette/tokens.json` (do not hardcode hex values elsewhere).

## Principles
- **Dark-first, quiet surfaces:** charcoal-teal bases a step darker than Adwaita, never pure black; menus and dialogs stay opaque for readability.
- **Leaf-sage accent:** sage is the only action/focus/selection color; blossom-pink is decorative (wallpaper, branding) and never an action color.
- **Familiar GNOME shape:** upstream layout, radius, and spacing are kept; only the palette is re-voiced.
- **Contrast is a gate:** `tools/dev/check_contrast.py` must pass (WCAG ≥4.5 body text, ≥7 preferred) before any milestone commit.
- **System fonts**, no custom typography in the theme itself.

## Tokens (v0.2.0)
| Token | Value | Use |
|---|---|---|
| bg.base | #0F141B | panel, dialogs, cards |
| bg.base_darker | #0B0F14 | overview backdrop, OSD base |
| bg.oled | #050807 | true pitch-black OLED background (`--tweaks black`) |
| bg.tile | #16222A | quick-settings tiles, list rows |
| bg.surface / hover / active | #1D3238 / #2A4148 / #35525A | raised surfaces and states |
| accent.base / strong / dim | #8FB8A6 / #A9CDBB / #52736F | focus, selected, sliders, links (default Sage) |
| accent_flavors.emerald | #3DD68C | vibrant Aurora Emerald accent (`--accent emerald`) |
| accent_flavors.moss | #98B99A | earthy Everforest Moss accent (`--accent moss`) |
| accent_flavors.pine | #5E9E92 | Nordic Cypress Pine accent (`--accent pine`) |
| window_controls close/min/max | #E5737F / #E5B580 / #7FC8A0 | macOS/Colloid traffic light buttons (`--tweaks macos`) |
| text.primary / secondary / disabled | #E9F1EC / #A7B8B1 / #76877F | foreground tiers |
| status destructive/success/warning | #E5737F / #7FC8A0 / #E5B580 | semantic states |
| status.petal_decorative | #C9A3B0 | artwork only |
| border.default / subtle | #2C3E44 / #223237 | separators, edges |

All text/accent pairs verified ≥4.5:1 on their backgrounds (most ≥7:1).

## Modular Tweaks System
Inspired by top-tier Linux desktop themes (Colloid, WhiteSur, TokyoNight GTK, Catppuccin, Everforest):
- **Option A: Canopy Floating Glass (Default showcase)**: Floating rounded pill top bar (`--tweaks float`), frosted translucent backdrop (`--tweaks translucent`), circular window controls (`--tweaks macos`), modern quick settings polish.
- **Option B: Obsidian Pro & Compact**: True pitch-black surfaces (`--tweaks black`), high density compact headerbars (`--tweaks compact`), rimless borderless windows (`--tweaks rimless`), vibrant emerald highlights.
- **Option C: Nordic Evergreen & Organic**: Soft modern curves (`--tweaks round`), solid forest panel, native Adwaita inset buttons, warm earthy moss tones.

## 4K Wallpaper Suite Rules
Four original dark procedural artworks generated via `tools/wallpaper/generate.py`:
1. **Botanical Canopy (Midnight Fern)**: Night-garden foliage in theme tones with restrained pale-pink blossoms and quiet moonlight.
2. **Verdant Aurora (Nordic Pines)**: Silhouetted pine forest under a glowing emerald and sage aurora borealis gradient with distant stars.
3. **Zen Flora (Geometric Contour)**: Bauhaus/Material-inspired organic geometric leaf contour curves on deep obsidian teal.
4. **Obsidian River (Mineral Flow)**: Fluid topographic elevation isolines with glowing sage mineral veins over dark riverbed bedrock.

### 4K Light Suite (Ethereal Dawn & Luminous Sage)
Four high-resolution dawn & luminous atmospheric artworks (`wallpaper/dist/light/`):
1. **Botanical Canopy Dawn (Morning Mist)**: Sunbeams filtering through lush morning garden foliage and sage leaves with delicate pale blossom buds.
2. **Luminous Sage Celestial Rift**: Flowing ethereal cyan & sage cosmic dust rift with delicate starfield and soft atmospheric depth.
3. **Cosmic Dawn (Stellar Amber & Emerald Cloud)**: Glowing golden-amber rimmed stellar cloud with undulating sage and emerald stardust ridges.
4. **Celestial Botanical Horizon (Aurora Dawn)**: Delicate botanical foreground silhouettes transitioning into soft dawn rose and radiant sage aurora curtains.

- All dark and light wallpapers render at 3840×2160 and copy into `${THEME_DIR}/wallpapers/` on install.
- 1920×1080 preview JPGs reside in `wallpaper/preview/` and `wallpaper/preview/light/`.
- Dynamic Day/Night switching:
  - **Adaptive pairing** (`--wallpaper dynamic`): Pairs Canopy Dawn for GNOME Light style (`picture-uri`) and Midnight Fern for GNOME Dark style (`picture-uri-dark`).
  - **24-hour timed cycle** (`--wallpaper timed`): Continuous clock-based cross-fade via `mt-verdant-timed.xml`.
  - Registered natively into GNOME Settings Backgrounds via `~/.local/share/gnome-background-properties/mt-verdant.xml`.
- Applying wallpaper is opt-in via `./tools/install.sh --wallpaper [1-4|light-1..4|dynamic|timed|all]`.

## Icon Suite (MT-Verdant-Icons)
- **Design language**: High-definition vector icons adhering to the Botanical Canopy dark-green identity (obsidian teal bases `#122329` to `#24444D`, sage `#8FB8A6` and emerald `#3DD68C` accents).
- **Core application coverage**: Provides full dark-green vector designs for all essential GNOME and desktop apps (Calendar, Contacts, Characters, Connections, Weather, Clocks, Snapshot, Loupe, Showtime, Decibels, Papers, Maps, Music, Scanner, Logs, Disk Usage, Fonts, Tour, Help, Extensions, Printers, and Vim).
- **Symbolic UI & Wireframes**: Complete 16×16 symbolic coverage across `symbolic/*` and `scalable/*` contexts for empty states (`globe-centered-symbolic`), Libadwaita split navigation (`view-sidebar-start/end-symbolic`), interactive screenshot & screencast overlay utilities, and all 25+ GNOME Settings panels.
- **Cache & Distribution**: Automatically generated via `tools/icons/generate_icons.py` into scalable vector SVGs and multi-size PNGs (32, 48, 64, 128), and compiled with `gtk-update-icon-cache` upon installation into `~/.icons/MT-Verdant-Icons`.
