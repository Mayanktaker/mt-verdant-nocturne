# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Generates MT-Verdant-Icons suite: vector SVGs, multi-res PNGs, and theme metadata.
# High-definition botanical dark green palette with rich gradients and crisp contrast.

import os
import shutil
from pathlib import Path
import cairo
import gi
gi.require_version("Rsvg", "2.0")
gi.require_version("Adw", "1")
gi.require_version("Gio", "2.0")
from gi.repository import Rsvg, Adw, Gio

try:
    from symbolic_assets import EXTENDED_SYMBOLIC_ICONS
except ImportError:
    from tools.icons.symbolic_assets import EXTENDED_SYMBOLIC_ICONS

try:
    from app_assets import EXTENDED_APP_ICONS, EXTENDED_APP_ALIASES
except ImportError:
    from tools.icons.app_assets import EXTENDED_APP_ICONS, EXTENDED_APP_ALIASES

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "src" / "icons" / "MT-Verdant-Icons"

# =========================================================================
# High-Definition SVG Folder Template (Rich gradients, highlights, depth)
# =========================================================================

SVG_FOLDER_BASE = '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
  <!-- Back body gradient -->
  <linearGradient id="backGrad" x1="32" y1="10" x2="32" y2="56" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#193138"/>
    <stop offset="100%" stop-color="#102026"/>
  </linearGradient>
  <!-- Accent pill glow gradient -->
  <linearGradient id="pillGrad" x1="8" y1="11" x2="30" y2="11" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#8FB8A6"/>
    <stop offset="100%" stop-color="#3DD68C"/>
  </linearGradient>
  <!-- Front flap rich gradient -->
  <linearGradient id="flapGrad" x1="32" y1="20" x2="32" y2="58" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#24444D"/>
    <stop offset="40%" stop-color="#1B353D"/>
    <stop offset="100%" stop-color="#13262D"/>
  </linearGradient>
  <!-- Specular top edge highlight -->
  <linearGradient id="specularGrad" x1="8" y1="21" x2="56" y2="21" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#8FB8A6" stop-opacity="0.8"/>
    <stop offset="70%" stop-color="#3DD68C" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="#8FB8A6" stop-opacity="0.1"/>
  </linearGradient>
  <!-- Flap drop shadow filter -->
  <filter id="flapShadow" x="0" y="18" width="64" height="44" filterUnits="userSpaceOnUse">
    <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#000000" flood-opacity="0.45"/>
  </filter>
</defs>
<!-- Back folder tab & body -->
<rect x="6" y="9" width="26" height="11" rx="4" fill="url(#backGrad)" stroke="#2E555F" stroke-width="1"/>
<rect x="8.5" y="10.5" width="21" height="3" rx="1.5" fill="url(#pillGrad)"/>
<rect x="5.5" y="14.5" width="53" height="42" rx="6" fill="url(#backGrad)" stroke="#2E555F" stroke-width="1"/>
<!-- Front folder flap with shadow and curved geometry -->
<g filter="url(#flapShadow)">
  <path d="M 5.5 24.5 C 5.5 21 8 19 11.5 19 L 26.5 19 C 29 19 31.5 20.8 33 22.8 L 35.5 25.8 C 37 27.5 39 28 41.5 28 L 52.5 28 C 56 28 58.5 30.5 58.5 33.5 L 58.5 51.5 C 58.5 55 56 57.5 52.5 57.5 L 11.5 57.5 C 8 57.5 5.5 55 5.5 51.5 Z" fill="url(#flapGrad)" stroke="#2E555F" stroke-width="1"/>
  <!-- Specular highlight line along upper lip -->
  <path d="M 7 24.5 C 7 22.5 8.5 20.5 11.5 20.5 L 26.5 20.5 C 28.5 20.5 30.5 22 32 24 L 34.5 27 C 36 28.5 38 29.5 41.5 29.5 L 52.5 29.5 C 55 29.5 57 31 57 33.5" stroke="url(#specularGrad)" stroke-width="1.2" stroke-linecap="round"/>
</g>
'''

SVG_FOOTER = '''</svg>'''

# =========================================================================
# Vector Places Emblems (Crisp high-contrast icons for Nautilus & Desktop)
# =========================================================================

PLACES_EMBLEMS = {
    "folder": "",
    "folder-desktop": '''<!-- Desktop / Monitor emblem -->
<rect x="21" y="32" width="22" height="15" rx="2" stroke="#8FB8A6" stroke-width="2" fill="#13262D"/>
<rect x="23" y="34" width="18" height="11" fill="#193138"/>
<line x1="32" y1="47" x2="32" y2="52" stroke="#8FB8A6" stroke-width="2"/>
<line x1="26" y1="52" x2="38" y2="52" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
<circle cx="32" cy="39.5" r="2.5" fill="#3DD68C"/>''',

    "folder-home": '''<!-- Home emblem -->
<path d="M 32 30 L 20 40 L 23 40 L 23 51 L 29 51 L 29 44 L 35 44 L 35 51 L 41 51 L 41 40 L 44 40 Z" fill="#8FB8A6"/>
<polygon points="32,34 38,39 26,39" fill="#13262D"/>''',

    "folder-documents": '''<!-- Documents emblem -->
<rect x="23" y="31" width="18" height="20" rx="2.5" fill="#8FB8A6"/>
<rect x="26" y="35" width="12" height="2.2" rx="1.1" fill="#13262D"/>
<rect x="26" y="39.5" width="12" height="2.2" rx="1.1" fill="#13262D"/>
<rect x="26" y="44" width="7" height="2.2" rx="1.1" fill="#13262D"/>''',

    "folder-download": '''<!-- Download emblem -->
<path d="M 32 31 L 32 45 M 32 45 L 25 38 M 32 45 L 39 38" stroke="#8FB8A6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="22" y1="50" x2="42" y2="50" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round"/>''',

    "folder-music": '''<!-- Music emblem -->
<path d="M 26 47 A 3.5 3.5 0 1 1 26 40 A 3.5 3.5 0 0 1 26 47 Z" fill="#8FB8A6"/>
<path d="M 38 44 A 3.5 3.5 0 1 1 38 37 A 3.5 3.5 0 0 1 38 44 Z" fill="#8FB8A6"/>
<path d="M 29.5 41 L 29.5 32 L 41.5 29 L 41.5 38" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<polygon points="29.5,32 41.5,29 41.5,33 29.5,36" fill="#3DD68C"/>''',

    "folder-pictures": '''<!-- Pictures emblem -->
<rect x="21" y="32" width="22" height="18" rx="3" stroke="#8FB8A6" stroke-width="2" fill="#13262D"/>
<circle cx="27" cy="37.5" r="2.5" fill="#3DD68C"/>
<polygon points="23,48 28.5,41 33.5,46 37,42.5 41,48" fill="#8FB8A6"/>''',

    "folder-videos": '''<!-- Videos emblem -->
<rect x="20" y="32" width="24" height="18" rx="3" stroke="#8FB8A6" stroke-width="2" fill="#13262D"/>
<circle cx="32" cy="41" r="5" fill="#3DD68C"/>
<polygon points="30.5,38 35,41 30.5,44" fill="#13262D"/>''',

    "folder-templates": '''<!-- Templates / Drafting emblem -->
<rect x="22" y="32" width="20" height="18" rx="2" stroke="#8FB8A6" stroke-width="2" fill="none"/>
<line x1="22" y1="38" x2="42" y2="38" stroke="#8FB8A6" stroke-width="1.5"/>
<line x1="28" y1="32" x2="28" y2="50" stroke="#8FB8A6" stroke-width="1.5"/>
<polygon points="31,41 39,41 31,49" fill="#3DD68C"/>''',

    "folder-publicshare": '''<!-- Public share emblem -->
<circle cx="32" cy="36" r="3.5" fill="#8FB8A6"/>
<path d="M 24 49 C 24 44 27 42 32 42 C 37 42 40 44 40 49 Z" fill="#8FB8A6"/>
<circle cx="41" cy="37" r="2.5" fill="#3DD68C"/>
<circle cx="23" cy="37" r="2.5" fill="#3DD68C"/>''',

    "folder-remote": '''<!-- Network globe folder -->
<circle cx="32" cy="41" r="9" stroke="#8FB8A6" stroke-width="2" fill="#13262D"/>
<ellipse cx="32" cy="41" rx="4.5" ry="9" stroke="#8FB8A6" stroke-width="1.5" fill="none"/>
<line x1="23" y1="41" x2="41" y2="41" stroke="#3DD68C" stroke-width="1.8"/>''',

    "folder-projects": '''<!-- Code / Projects emblem -->
<polygon points="26,35 20,41 26,47" stroke="#3DD68C" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<polygon points="38,35 44,41 38,47" stroke="#3DD68C" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="34" y1="33" x2="30" y2="49" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>''',

    "folder-applications": '''<!-- Apps grid emblem -->
<rect x="23" y="32" width="6" height="6" rx="1.5" fill="#8FB8A6"/>
<rect x="35" y="32" width="6" height="6" rx="1.5" fill="#8FB8A6"/>
<rect x="23" y="42" width="6" height="6" rx="1.5" fill="#8FB8A6"/>
<rect x="35" y="42" width="6" height="6" rx="1.5" fill="#3DD68C"/>''',

    "folder-books": '''<!-- Bookshelf emblem -->
<rect x="22" y="32" width="4" height="18" rx="1" fill="#8FB8A6"/>
<rect x="28" y="30" width="4" height="20" rx="1" fill="#3DD68C"/>
<rect x="34" y="33" width="4" height="17" rx="1" fill="#8FB8A6"/>
<polygon points="32,35 38,45 26,45" fill="#8FB8A6"/>''',

    "folder-saved-search": '''<!-- Search emblem -->
<circle cx="29" cy="38" r="7" stroke="#8FB8A6" stroke-width="2.5" fill="none"/>
<line x1="34.5" y1="43.5" x2="43" y2="52" stroke="#3DD68C" stroke-width="3.5" stroke-linecap="round"/>''',

    "folder-github": '''<!-- Development emblem -->
<path d="M 26 35 L 20 41 L 26 47" stroke="#8FB8A6" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 38 35 L 44 41 L 38 47" stroke="#8FB8A6" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="34" y1="34" x2="30" y2="48" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round"/>''',

    "folder-open": '''<!-- Open folder flap -->
<path d="M 24 35 L 32 30 L 40 35" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round"/>
<rect x="23" y="37" width="18" height="12" rx="2" fill="#8FB8A6" fill-opacity="0.8"/>''',

    "folder-recent": '''<!-- Clock / Recent emblem -->
<circle cx="32" cy="41" r="9" stroke="#8FB8A6" stroke-width="2" fill="none"/>
<line x1="32" y1="36" x2="32" y2="41" stroke="#3DD68C" stroke-width="2" stroke-linecap="round"/>
<line x1="32" y1="41" x2="36" y2="41" stroke="#3DD68C" stroke-width="2" stroke-linecap="round"/>''',

    "folder-root": '''<!-- Root / Admin emblem -->
<path d="M 32 30 L 42 34 L 42 42 C 42 48 32 52 32 52 C 32 52 22 48 22 42 L 22 34 Z" fill="#8FB8A6"/>
<circle cx="32" cy="38" r="2.5" fill="#13262D"/>
<line x1="32" y1="40.5" x2="32" y2="46" stroke="#13262D" stroke-width="2"/>''',

    "folder-locked": '''<!-- Padlock emblem -->
<rect x="23" y="38" width="18" height="14" rx="2.5" fill="#8FB8A6"/>
<path d="M 27 38 L 27 34 C 27 31 29 29 32 29 C 35 29 37 31 37 34 L 37 38" stroke="#8FB8A6" stroke-width="2.5" fill="none"/>
<circle cx="32" cy="44" r="1.5" fill="#13262D"/>
<line x1="32" y1="45.5" x2="32" y2="49" stroke="#13262D" stroke-width="1.5"/>''',

    "folder-tar": '''<!-- Archive / Zipper emblem -->
<line x1="32" y1="30" x2="32" y2="52" stroke="#8FB8A6" stroke-width="3" stroke-dasharray="2 3"/>
<rect x="29" y="38" width="6" height="8" rx="1.5" fill="#3DD68C"/>''',

    "user-trash": '''<!-- Trash emblem -->
<path d="M 24 34 L 40 34 L 38 51 L 26 51 Z" stroke="#8FB8A6" stroke-width="2" fill="#13262D"/>
<line x1="21" y1="32" x2="43" y2="32" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<rect x="29" y="29" width="6" height="3" rx="1" fill="#3DD68C"/>
<line x1="28.5" y1="37" x2="28.5" y2="47" stroke="#8FB8A6" stroke-width="1.5"/>
<line x1="32" y1="37" x2="32" y2="47" stroke="#8FB8A6" stroke-width="1.5"/>
<line x1="35.5" y1="37" x2="35.5" y2="47" stroke="#8FB8A6" stroke-width="1.5"/>''',
}

PLACES_ALIASES = {
    "user-desktop": "folder-desktop",
    "desktop": "folder-desktop",
    "user-home": "folder-home",
    "folder-downloads": "folder-download",
    "folder-development": "folder-projects",
    "folder-code": "folder-projects",
    "folder-apps": "folder-applications",
    "applications": "folder-applications",
    "folder-calibre": "folder-books",
    "folder-network": "network-workgroup",
    "network": "network-workgroup",
    "inode-directory": "folder",
    "folder_color": "folder",
    "user-trash-full": "user-trash",
    "folder-zip": "folder-tar",
    "folder-archive": "folder-tar",
}

# =========================================================================
# Symbolic Wireframe Icons (16x16 crisp vectors for Nautilus, Settings, Apps)
# =========================================================================

SYMBOLIC_ICONS = {
    # Fixes the white missing network icon in Nautilus
    "network-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 2 2 C 1.45 2 1 2.45 1 3 L 1 9 C 1 9.55 1.45 10 2 10 L 7 10 L 7 12 L 5 12 C 4.45 12 4 12.45 4 13 C 4 13.55 4.45 14 5 14 L 11 14 C 11.55 14 12 13.55 12 13 C 12 12.45 11.55 12 11 12 L 9 12 L 9 10 L 14 10 C 14.55 10 15 9.55 15 9 L 15 3 C 15 2.45 14.55 2 14 2 Z M 3 4 L 13 4 L 13 8 L 3 8 Z"/>
</svg>''',

    "network-workgroup-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 2 2 C 1.45 2 1 2.45 1 3 L 1 9 C 1 9.55 1.45 10 2 10 L 7 10 L 7 12 L 5 12 C 4.45 12 4 12.45 4 13 C 4 13.55 4.45 14 5 14 L 11 14 C 11.55 14 12 13.55 12 13 C 12 12.45 11.55 12 11 12 L 9 12 L 9 10 L 14 10 C 14.55 10 15 9.55 15 9 L 15 3 C 15 2.45 14.55 2 14 2 Z M 3 4 L 13 4 L 13 8 L 3 8 Z"/>
</svg>''',

    "network-server-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 3 2 C 1.9 2 1 2.9 1 4 L 1 7 C 1 8.1 1.9 9 3 9 L 13 9 C 14.1 9 15 8.1 15 7 L 15 4 C 15 2.9 14.1 2 13 2 Z M 3 3.5 L 13 3.5 C 13.3 3.5 13.5 3.7 13.5 4 L 13.5 7 C 13.5 7.3 13.3 7.5 13 7.5 L 3 7.5 C 2.7 7.5 2.5 7.3 2.5 7 L 2.5 4 C 2.5 3.7 2.7 3.5 3 3.5 Z M 4 5 L 6 5 L 6 6 L 4 6 Z M 12 5.5 C 12 5.8 11.8 6 11.5 6 C 11.2 6 11 5.8 11 5.5 C 11 5.2 11.2 5 11.5 5 C 11.8 5 12 5.2 12 5.5 Z M 3 9.5 C 1.9 9.5 1 10.4 1 11.5 L 1 14.5 C 1 15.6 1.9 16.5 3 16.5 L 13 16.5 C 14.1 16.5 15 15.6 15 14.5 L 15 11.5 C 15 10.4 14.1 9.5 13 9.5 Z M 3 11 L 13 11 C 13.3 11 13.5 11.2 13.5 11.5 L 13.5 14.5 C 13.5 14.8 13.3 15 13 15 L 3 15 C 2.7 15 2.5 14.8 2.5 14.5 L 2.5 11.5 C 2.5 11.2 2.7 11 3 11 Z M 4 12.5 L 6 12.5 L 6 13.5 L 4 13.5 Z M 12 13 C 12 13.3 11.8 13.5 11.5 13.5 C 11.2 13.5 11 13.3 11 13 C 11 12.7 11.2 12.5 11.5 12.5 C 11.8 12.5 12 12.7 12 13 Z"/>
</svg>''',

    "folder-remote-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 8 1 C 4.13 1 1 4.13 1 8 C 1 11.87 4.13 15 8 15 C 11.87 15 15 11.87 15 8 C 15 4.13 11.87 1 8 1 Z M 8 2.5 C 11.04 2.5 13.5 4.96 13.5 8 C 13.5 11.04 11.04 13.5 8 13.5 C 4.96 13.5 2.5 11.04 2.5 8 C 2.5 4.96 4.96 2.5 8 2.5 Z M 8 2.5 C 9.5 4 10.5 5.8 10.5 8 C 10.5 10.2 9.5 12 8 13.5 C 6.5 12 5.5 10.2 5.5 8 C 5.5 5.8 6.5 4 8 2.5 Z M 2.5 8 L 13.5 8 L 13.5 9.2 L 2.5 9.2 Z"/>
</svg>''',

    "user-home-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 8 2 L 2 7.5 L 3.5 7.5 L 3.5 13.5 L 6.5 13.5 L 6.5 9.5 L 9.5 9.5 L 9.5 13.5 L 12.5 13.5 L 12.5 7.5 L 14 7.5 Z"/>
</svg>''',

    "document-open-recent-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 8 1 C 4.13 1 1 4.13 1 8 C 1 11.87 4.13 15 8 15 C 11.87 15 15 11.87 15 8 C 15 4.13 11.87 1 8 1 Z M 8 2.5 C 11.04 2.5 13.5 4.96 13.5 8 C 13.5 11.04 11.04 13.5 8 13.5 C 4.96 13.5 2.5 11.04 2.5 8 C 2.5 4.96 4.96 2.5 8 2.5 Z M 7.2 4 L 8.8 4 L 8.8 7.5 L 11.5 9.2 L 10.7 10.5 L 7.2 8.3 Z"/>
</svg>''',

    "recent-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 8 1 C 4.13 1 1 4.13 1 8 C 1 11.87 4.13 15 8 15 C 11.87 15 15 11.87 15 8 C 15 4.13 11.87 1 8 1 Z M 8 2.5 C 11.04 2.5 13.5 4.96 13.5 8 C 13.5 11.04 11.04 13.5 8 13.5 C 4.96 13.5 2.5 11.04 2.5 8 C 2.5 4.96 4.96 2.5 8 2.5 Z M 7.2 4 L 8.8 4 L 8.8 7.5 L 11.5 9.2 L 10.7 10.5 L 7.2 8.3 Z"/>
</svg>''',

    "folder-recent-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 8 1 C 4.13 1 1 4.13 1 8 C 1 11.87 4.13 15 8 15 C 11.87 15 15 11.87 15 8 C 15 4.13 11.87 1 8 1 Z M 8 2.5 C 11.04 2.5 13.5 4.96 13.5 8 C 13.5 11.04 11.04 13.5 8 13.5 C 4.96 13.5 2.5 11.04 2.5 8 C 2.5 4.96 4.96 2.5 8 2.5 Z M 7.2 4 L 8.8 4 L 8.8 7.5 L 11.5 9.2 L 10.7 10.5 L 7.2 8.3 Z"/>
</svg>''',

    "starred-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polygon points="8,2 10,6.5 15,7 11.5,10.5 12.5,15 8,12.5 3.5,15 4.5,10.5 1,7 6,6.5" fill="currentColor"/>
</svg>''',

    "user-trash-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 3 4 L 13 4 L 11.5 14 L 4.5 14 Z M 5 2 L 11 2 L 12 3 L 4 3 Z"/>
</svg>''',

    "settings-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 7 1 L 9 1 L 9.3 2.7 C 9.8 2.9 10.3 3.2 10.7 3.6 L 12.3 2.9 L 13.7 4.3 L 13 5.9 C 13.4 6.3 13.7 6.8 13.9 7.3 L 15.6 7.6 L 15.6 9.6 L 13.9 9.9 C 13.7 10.4 13.4 10.9 13 11.3 L 13.7 12.9 L 12.3 14.3 L 10.7 13.6 C 10.3 14 9.8 14.3 9.3 14.5 L 9 16.2 L 7 16.2 L 6.7 14.5 C 6.2 14.3 5.7 14 5.3 13.6 L 3.7 14.3 L 2.3 12.9 L 3 11.3 C 2.6 10.9 2.3 10.4 2.1 9.9 L 0.4 9.6 L 0.4 7.6 L 2.1 7.3 C 2.3 6.8 2.6 6.3 3 5.9 L 2.3 4.3 L 3.7 2.9 L 5.3 3.6 C 5.7 3.2 6.2 2.9 6.7 2.7 Z M 8 5.5 A 2.5 2.5 0 1 0 8 10.5 A 2.5 2.5 0 1 0 8 5.5 Z"/>
</svg>''',

    "puzzle-piece-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 6 2 C 6 2.5 6.5 3 7 3 C 7.5 3 8 2.5 8 2 C 8 1.5 7.5 1 7 1 C 6.5 1 6 1.5 6 2 Z M 5 3 L 5 5 L 3 5 C 2.5 5 2 5.5 2 6 C 2 6.5 2.5 7 3 7 C 3.5 7 4 6.5 4 6 L 4 5 L 5 5 L 5 8 C 5 8.55 5.45 9 6 9 L 7 9 L 7 10 C 7 10.5 7.5 11 8 11 C 8.5 11 9 10.5 9 10 L 9 9 L 11 9 C 11.55 9 12 8.55 12 8 L 12 6 C 12 5.5 12.5 5 13 5 C 13.5 5 14 5.5 14 6 C 14 6.5 13.5 7 13 7 L 13 8 C 13 9.66 11.66 11 10 11 L 10 13 C 10 13.55 9.55 14 9 14 L 5 14 C 3.9 14 3 13.1 3 12 L 3 10 C 2.45 10 2 9.55 2 9 L 2 5 C 2 3.9 2.9 3 4 3 Z"/>
</svg>''',

    # Botanical Compound-Path Storage Drives Suite (prevents solid-fill bug in GTK)
    "drive-harddisk-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 4 1 L 12 1 C 13.65 1 15 2.35 15 4 L 15 12 C 15 13.65 13.65 15 12 15 L 4 15 C 2.35 15 1 13.65 1 12 L 1 4 C 1 2.35 2.35 1 4 1 Z M 4 2.5 L 12 2.5 C 12.83 2.5 13.5 3.17 13.5 4 L 13.5 12 C 13.5 12.83 12.83 13.5 12 13.5 L 4 13.5 C 3.17 13.5 2.5 12.83 2.5 12 L 2.5 4 C 2.5 3.17 3.17 2.5 4 2.5 Z M 8 3 C 10.49 3 12.5 5.01 12.5 7.5 C 12.5 9.99 10.49 12 8 12 C 5.51 12 3.5 9.99 3.5 7.5 C 3.5 5.01 5.51 3 8 3 Z M 8 6 C 7.17 6 6.5 6.67 6.5 7.5 C 6.5 8.33 7.17 9 8 9 C 8.83 9 9.5 8.33 9.5 7.5 C 9.5 6.67 8.83 6 8 6 Z M 4 12.5 L 12 12.5 L 12 13 L 4 13 Z"/>
</svg>''',

    "drive-harddisk-solidstate-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 4 1 L 12 1 C 13.65 1 15 2.35 15 4 L 15 12 C 15 13.65 13.65 15 12 15 L 4 15 C 2.35 15 1 13.65 1 12 L 1 4 C 1 2.35 2.35 1 4 1 Z M 4 2.5 L 12 2.5 C 12.83 2.5 13.5 3.17 13.5 4 L 13.5 12 C 13.5 12.83 12.83 13.5 12 13.5 L 4 13.5 C 3.17 13.5 2.5 12.83 2.5 12 L 2.5 4 C 2.5 3.17 3.17 2.5 4 2.5 Z M 5.5 4.5 L 10.5 4.5 C 11.05 4.5 11.5 4.95 11.5 5.5 L 11.5 9.5 C 11.5 10.05 11.05 10.5 10.5 10.5 L 5.5 10.5 C 4.95 10.5 4.5 10.05 4.5 9.5 L 4.5 5.5 C 4.5 4.95 4.95 4.5 5.5 4.5 Z M 6.5 6 L 9.5 6 L 9.5 9 L 6.5 9 Z M 6 3.5 L 7 3.5 L 7 4.5 L 6 4.5 Z M 9 3.5 L 10 3.5 L 10 4.5 L 9 4.5 Z M 6 10.5 L 7 10.5 L 7 11.5 L 6 11.5 Z M 9 10.5 L 10 10.5 L 10 11.5 L 9 11.5 Z M 4 12.5 L 12 12.5 L 12 13 L 4 13 Z"/>
</svg>''',

    "drive-harddisk-usb-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 6 0 L 10 0 L 10 2 L 12 2 C 13.65 2 15 3.35 15 5 L 15 13 C 15 14.65 13.65 16 12 16 L 4 16 C 2.35 16 1 14.65 1 13 L 1 5 C 1 3.35 2.35 2 4 2 L 6 2 Z M 7 1 L 7 2 L 9 2 L 9 1 Z M 4 3.5 C 3.17 3.5 2.5 4.17 2.5 5 L 2.5 13 C 2.5 13.83 3.17 14.5 4 14.5 L 12 14.5 C 12.83 14.5 13.5 13.83 13.5 13 L 13.5 5 C 13.5 4.17 12.83 3.5 12 3.5 Z M 8 4.5 C 5.79 4.5 4 6.29 4 8.5 C 4 10.71 5.79 12.5 8 12.5 C 10.21 12.5 12 10.71 12 8.5 C 12 6.29 10.21 4.5 8 4.5 Z M 8 6.5 C 9.1 6.5 10 7.4 10 8.5 C 10 9.6 9.1 10.5 8 10.5 C 6.9 10.5 6 9.6 6 8.5 C 6 7.4 6.9 6.5 8 6.5 Z"/>
</svg>''',

    "drive-harddisk-root-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 4 1 L 12 1 C 13.65 1 15 2.35 15 4 L 15 12 C 15 13.65 13.65 15 12 15 L 4 15 C 2.35 15 1 13.65 1 12 L 1 4 C 1 2.35 2.35 1 4 1 Z M 4 2.5 L 12 2.5 C 12.83 2.5 13.5 3.17 13.5 4 L 13.5 12 C 13.5 12.83 12.83 13.5 12 13.5 L 4 13.5 C 3.17 13.5 2.5 12.83 2.5 12 L 2.5 4 C 2.5 3.17 3.17 2.5 4 2.5 Z M 8 3 C 10.49 3 12.5 5.01 12.5 7.5 C 12.5 9.99 10.49 12 8 12 C 5.51 12 3.5 9.99 3.5 7.5 C 3.5 5.01 5.51 3 8 3 Z M 8 6 C 7.17 6 6.5 6.67 6.5 7.5 C 6.5 8.33 7.17 9 8 9 C 8.83 9 9.5 8.33 9.5 7.5 C 9.5 6.67 8.83 6 8 6 Z M 4 12.5 L 7 12.5 L 7 13 L 4 13 Z M 10.5 11.5 L 9 13.5 L 10 13.5 L 11.5 11.5 Z"/>
</svg>''',

    "drive-harddisk-system-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 4 1 L 12 1 C 13.65 1 15 2.35 15 4 L 15 12 C 15 13.65 13.65 15 12 15 L 4 15 C 2.35 15 1 13.65 1 12 L 1 4 C 1 2.35 2.35 1 4 1 Z M 4 2.5 L 12 2.5 C 12.83 2.5 13.5 3.17 13.5 4 L 13.5 12 C 13.5 12.83 12.83 13.5 12 13.5 L 4 13.5 C 3.17 13.5 2.5 12.83 2.5 12 L 2.5 4 C 2.5 3.17 3.17 2.5 4 2.5 Z M 8 3 C 10.49 3 12.5 5.01 12.5 7.5 C 12.5 9.99 10.49 12 8 12 C 5.51 12 3.5 9.99 3.5 7.5 C 3.5 5.01 5.51 3 8 3 Z M 8 6 C 7.17 6 6.5 6.67 6.5 7.5 C 6.5 8.33 7.17 9 8 9 C 8.83 9 9.5 8.33 9.5 7.5 C 9.5 6.67 8.83 6 8 6 Z M 4 12.5 L 7 12.5 L 7 13 L 4 13 Z M 10.5 11.5 L 9 13.5 L 10 13.5 L 11.5 11.5 Z"/>
</svg>''',

    "drive-harddisk-ieee1394-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 6 0 L 10 0 L 10 2 L 12 2 C 13.65 2 15 3.35 15 5 L 15 13 C 15 14.65 13.65 16 12 16 L 4 16 C 2.35 16 1 14.65 1 13 L 1 5 C 1 3.35 2.35 2 4 2 L 6 2 Z M 7 1 L 7 2 L 9 2 L 9 1 Z M 4 3.5 C 3.17 3.5 2.5 4.17 2.5 5 L 2.5 13 C 2.5 13.83 3.17 14.5 4 14.5 L 12 14.5 C 12.83 14.5 13.5 13.83 13.5 13 L 13.5 5 C 13.5 4.17 12.83 3.5 12 3.5 Z M 8 4.5 C 5.79 4.5 4 6.29 4 8.5 C 4 10.71 5.79 12.5 8 12.5 C 10.21 12.5 12 10.71 12 8.5 C 12 6.29 10.21 4.5 8 4.5 Z M 8 6.5 C 9.1 6.5 10 7.4 10 8.5 C 10 9.6 9.1 10.5 8 10.5 C 6.9 10.5 6 9.6 6 8.5 C 6 7.4 6.9 6.5 8 6.5 Z"/>
</svg>''',

    "drive-partition-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 4 1 L 12 1 C 13.65 1 15 2.35 15 4 L 15 12 C 15 13.65 13.65 15 12 15 L 4 15 C 2.35 15 1 13.65 1 12 L 1 4 C 1 2.35 2.35 1 4 1 Z M 4 2.5 L 7 2.5 L 7 13.5 L 4 13.5 C 3.17 13.5 2.5 12.83 2.5 12 L 2.5 4 C 2.5 3.17 3.17 2.5 4 2.5 Z M 9 2.5 L 12 2.5 C 12.83 2.5 13.5 3.17 13.5 4 L 13.5 12 C 13.5 12.83 12.83 13.5 12 13.5 L 9 13.5 Z M 4 4 L 5.5 4 L 5.5 5.5 L 4 5.5 Z M 10.5 4 L 12 4 L 12 5.5 L 10.5 5.5 Z M 4 10.5 L 5.5 10.5 L 5.5 12 L 4 12 Z M 10.5 10.5 L 12 10.5 L 12 12 L 10.5 12 Z"/>
</svg>''',

    "drive-multidisk-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 4 0 C 2.35 0 1 1.35 1 3 L 1 7 C 1 8.65 2.35 10 4 10 L 9 10 C 10.65 10 12 8.65 12 7 L 12 3 C 12 1.35 10.65 0 9 0 Z M 4 1.5 L 9 1.5 C 9.83 1.5 10.5 2.17 10.5 3 L 10.5 7 C 10.5 7.83 9.83 8.5 9 8.5 L 4 8.5 C 3.17 8.5 2.5 7.83 2.5 7 L 2.5 3 C 2.5 2.17 3.17 1.5 4 1.5 Z M 6.5 2.5 C 5.12 2.5 4 3.62 4 5 C 4 6.38 5.12 7.5 6.5 7.5 C 7.88 7.5 9 6.38 9 5 C 9 3.62 7.88 2.5 6.5 2.5 Z M 13 4.2 L 13 13 C 13 13.83 12.33 14.5 11.5 14.5 L 4 14.5 C 3.5 14.5 3 14.2 2.7 13.8 C 2.3 15.1 3.5 16 4.5 16 L 12 16 C 13.65 16 15 14.65 15 13 L 15 6 C 15 4.8 14.1 4.3 13 4.2 Z"/>
</svg>''',

    "drive-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 4 1 L 12 1 C 13.65 1 15 2.35 15 4 L 15 12 C 15 13.65 13.65 15 12 15 L 4 15 C 2.35 15 1 13.65 1 12 L 1 4 C 1 2.35 2.35 1 4 1 Z M 4 2.5 L 12 2.5 C 12.83 2.5 13.5 3.17 13.5 4 L 13.5 12 C 13.5 12.83 12.83 13.5 12 13.5 L 4 13.5 C 3.17 13.5 2.5 12.83 2.5 12 L 2.5 4 C 2.5 3.17 3.17 2.5 4 2.5 Z M 8 3 C 10.49 3 12.5 5.01 12.5 7.5 C 12.5 9.99 10.49 12 8 12 C 5.51 12 3.5 9.99 3.5 7.5 C 3.5 5.01 5.51 3 8 3 Z M 8 6 C 7.17 6 6.5 6.67 6.5 7.5 C 6.5 8.33 7.17 9 8 9 C 8.83 9 9.5 8.33 9.5 7.5 C 9.5 6.67 8.83 6 8 6 Z M 4 12.5 L 12 12.5 L 12 13 L 4 13 Z"/>
</svg>''',

    "drive-removable-media-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 5 0 L 11 0 L 11 4 L 5 4 Z M 6 1 L 7 1 L 7 2 L 6 2 Z M 9 1 L 10 1 L 10 2 L 9 2 Z M 4 5 C 2.35 5 1 6.35 1 8 L 1 13 C 1 14.65 2.35 16 4 16 L 12 16 C 13.65 16 15 14.65 15 13 L 15 8 C 15 6.35 13.65 5 12 5 Z M 4 6.5 L 12 6.5 C 12.83 6.5 13.5 7.17 13.5 8 L 13.5 13 C 13.5 13.83 12.83 14.5 12 14.5 L 4 14.5 C 3.17 14.5 2.5 13.83 2.5 13 L 2.5 8 C 2.5 7.17 3.17 6.5 4 6.5 Z M 8 9 C 7.17 9 6.5 9.67 6.5 10.5 C 6.5 11.33 7.17 12 8 12 C 8.83 12 9.5 11.33 9.5 10.5 C 9.5 9.67 8.83 9 8 9 Z"/>
</svg>''',

    "drive-removable-media-usb-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 5 0 L 11 0 L 11 4 L 5 4 Z M 6 1 L 7 1 L 7 2 L 6 2 Z M 9 1 L 10 1 L 10 2 L 9 2 Z M 4 5 C 2.35 5 1 6.35 1 8 L 1 13 C 1 14.65 2.35 16 4 16 L 12 16 C 13.65 16 15 14.65 15 13 L 15 8 C 15 6.35 13.65 5 12 5 Z M 4 6.5 L 12 6.5 C 12.83 6.5 13.5 7.17 13.5 8 L 13.5 13 C 13.5 13.83 12.83 14.5 12 14.5 L 4 14.5 C 3.17 14.5 2.5 13.83 2.5 13 L 2.5 8 C 2.5 7.17 3.17 6.5 4 6.5 Z M 8 9 C 7.17 9 6.5 9.67 6.5 10.5 C 6.5 11.33 7.17 12 8 12 C 8.83 12 9.5 11.33 9.5 10.5 C 9.5 9.67 8.83 9 8 9 Z"/>
</svg>''',

    "media-flash-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 5 1 C 3.35 1 2 2.35 2 4 L 2 13 C 2 14.65 3.35 16 5 16 L 11 16 C 12.65 16 14 14.65 14 13 L 14 4 C 14 3.73 13.89 3.48 13.7 3.29 L 11.7 1.29 C 11.52 1.11 11.27 1 11 1 Z M 5 2.5 L 10.5 2.5 L 12.5 4.5 L 12.5 13 C 12.5 13.83 11.83 14.5 11 14.5 L 5 14.5 C 4.17 14.5 3.5 13.83 3.5 13 L 3.5 4 C 3.5 3.17 4.17 2.5 5 2.5 Z M 5 4 L 6 4 L 6 7 L 5 7 Z M 7 4 L 8 4 L 8 7 L 7 7 Z M 9 4 L 10 4 L 10 7 L 9 7 Z M 11 5 L 11.5 5 L 11.5 7 L 11 7 Z"/>
</svg>''',

    "media-memory-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 5 1 C 3.35 1 2 2.35 2 4 L 2 13 C 2 14.65 3.35 16 5 16 L 11 16 C 12.65 16 14 14.65 14 13 L 14 4 C 14 3.73 13.89 3.48 13.7 3.29 L 11.7 1.29 C 11.52 1.11 11.27 1 11 1 Z M 5 2.5 L 10.5 2.5 L 12.5 4.5 L 12.5 13 C 12.5 13.83 11.83 14.5 11 14.5 L 5 14.5 C 4.17 14.5 3.5 13.83 3.5 13 L 3.5 4 C 3.5 3.17 4.17 2.5 5 2.5 Z M 5 4 L 6 4 L 6 7 L 5 7 Z M 7 4 L 8 4 L 8 7 L 7 7 Z M 9 4 L 10 4 L 10 7 L 9 7 Z M 11 5 L 11.5 5 L 11.5 7 L 11 7 Z"/>
</svg>''',

    "media-optical-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 8 1 C 4.13 1 1 4.13 1 8 C 1 11.87 4.13 15 8 15 C 11.87 15 15 11.87 15 8 C 15 4.13 11.87 1 8 1 Z M 8 2.5 C 11.04 2.5 13.5 4.96 13.5 8 C 13.5 11.04 11.04 13.5 8 13.5 C 4.96 13.5 2.5 11.04 2.5 8 C 2.5 4.96 4.96 2.5 8 2.5 Z M 8 5.5 C 6.62 5.5 5.5 6.62 5.5 8 C 5.5 9.38 6.62 10.5 8 10.5 C 9.38 10.5 10.5 9.38 10.5 8 C 10.5 6.62 9.38 5.5 8 5.5 Z M 8 7 C 7.45 7 7 7.45 7 8 C 7 8.55 7.45 9 8 9 C 8.55 9 9 8.55 9 8 C 9 7.45 8.55 7 8 7 Z"/>
</svg>''',

    "media-removable-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 5 0 L 11 0 L 11 4 L 5 4 Z M 6 1 L 7 1 L 7 2 L 6 2 Z M 9 1 L 10 1 L 10 2 L 9 2 Z M 4 5 C 2.35 5 1 6.35 1 8 L 1 13 C 1 14.65 2.35 16 4 16 L 12 16 C 13.65 16 15 14.65 15 13 L 15 8 C 15 6.35 13.65 5 12 5 Z M 4 6.5 L 12 6.5 C 12.83 6.5 13.5 7.17 13.5 8 L 13.5 13 C 13.5 13.83 12.83 14.5 12 14.5 L 4 14.5 C 3.17 14.5 2.5 13.83 2.5 13 L 2.5 8 C 2.5 7.17 3.17 6.5 4 6.5 Z M 8 9 C 7.17 9 6.5 9.67 6.5 10.5 C 6.5 11.33 7.17 12 8 12 C 8.83 12 9.5 11.33 9.5 10.5 C 9.5 9.67 8.83 9 8 9 Z"/>
</svg>''',

    "server-database-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" fill-rule="evenodd" d="M 8 1 C 4.69 1 2 2.12 2 3.5 C 2 4.88 4.69 6 8 6 C 11.31 6 14 4.88 14 3.5 C 14 2.12 11.31 1 8 1 Z M 8 2.2 C 10.5 2.2 12.5 3 12.5 3.5 C 12.5 4 10.5 4.8 8 4.8 C 5.5 4.8 3.5 4 3.5 3.5 C 3.5 3 5.5 2.2 8 2.2 Z M 2 5 L 2 8 C 2 9.38 4.69 10.5 8 10.5 C 11.31 10.5 14 9.38 14 8 L 14 5 C 13.6 5.8 11.5 6.8 8 6.8 C 4.5 6.8 2.4 5.8 2 5 Z M 2 9.5 L 2 12.5 C 2 13.88 4.69 15 8 15 C 11.31 15 14 13.88 14 12.5 L 14 9.5 C 13.6 10.3 11.5 11.3 8 11.3 C 4.5 11.3 2.4 10.3 2 9.5 Z"/>
</svg>''',

    # Fixes GNOME Settings Software Updates row (Left icon)
    "system-update-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 8 1 A 7 7 0 1 0 15 8 L 13.2 8 A 5.2 5.2 0 1 1 8 2.8 L 8 5 L 12 2.5 L 8 0 Z"/>
  <path fill="currentColor" d="M 8 6 L 8 10 L 6 8 L 5 9 L 8 12 L 11 9 L 10 8 L 8 10 Z"/>
</svg>''',

    "system-software-update-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 8 1 A 7 7 0 1 0 15 8 L 13.2 8 A 5.2 5.2 0 1 1 8 2.8 L 8 5 L 12 2.5 L 8 0 Z"/>
  <path fill="currentColor" d="M 8 6 L 8 10 L 6 8 L 5 9 L 8 12 L 11 9 L 10 8 L 8 10 Z"/>
</svg>''',

    "software-properties-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="3" width="12" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="8" cy="8" r="2.5" fill="currentColor"/>
</svg>''',

    # Fixes GNOME Settings Software Updates row (Right suffix icon) & Extension Manager
    "adw-external-link-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 5 2 C 3.34 2 2 3.34 2 5 L 2 11 C 2 12.66 3.34 14 5 14 L 11 14 C 12.66 14 14 12.66 14 11 L 14 8 L 12 8 L 12 11 C 12 11.55 11.55 12 11 12 L 5 12 C 4.45 12 4 11.55 4 11 L 4 5 C 4 4.45 4.45 4 5 4 L 8 4 L 8 2 Z M 10 2 L 10 4 L 12.59 4 L 7.29 9.29 L 8.71 10.71 L 14 5.41 L 14 8 L 16 8 L 16 2 Z"/>
</svg>''',

    "external-link-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 5 2 C 3.34 2 2 3.34 2 5 L 2 11 C 2 12.66 3.34 14 5 14 L 11 14 C 12.66 14 14 12.66 14 11 L 14 8 L 12 8 L 12 11 C 12 11.55 11.55 12 11 12 L 5 12 C 4.45 12 4 11.55 4 11 L 4 5 C 4 4.45 4.45 4 5 4 L 8 4 L 8 2 Z M 10 2 L 10 4 L 12.59 4 L 7.29 9.29 L 8.71 10.71 L 14 5.41 L 14 8 L 16 8 L 16 2 Z"/>
</svg>''',

    # Fixes Extension Manager right expander rows across all Libadwaita apps!
    "adw-expander-arrow-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M 4 6 L 8 10 L 12 6"/>
</svg>''',

    "expander-open-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M 4 6 L 8 10 L 12 6"/>
</svg>''',

    # Fixes Nautilus current folder search & search filters
    "nautilus-folder-search-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="10.5" y1="10.5" x2="14" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>''',

    "nautilus-search-filters-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <line x1="2" y1="4" x2="14" y2="4" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="5" cy="4" r="1.5" fill="currentColor"/>
  <line x1="2" y1="8" x2="14" y2="8" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="11" cy="8" r="1.5" fill="currentColor"/>
  <line x1="2" y1="12" x2="14" y2="12" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="7" cy="12" r="1.5" fill="currentColor"/>
</svg>''',

    # Fixes Sidebar toggle in Nautilus & Settings
    "sidebar-hide-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="2" width="12" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="6" y1="2" x2="6" y2="14" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="4.5,7 3,8.5 4.5,10" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
</svg>''',

    "sidebar-show-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="2" width="12" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="6" y1="2" x2="6" y2="14" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="3.5,7 5,8.5 3.5,10" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
</svg>''',

    # Fixes Extension Manager and app extras
    "donation-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 8 13.5 C 8 13.5 2 9.5 2 5.5 C 2 3.5 3.5 2 5.5 2 C 6.8 2 7.6 2.7 8 3.3 C 8.4 2.7 9.2 2 10.5 2 C 12.5 2 14 3.5 14 5.5 C 14 9.5 8 13.5 8 13.5 Z"/>
</svg>''',

    "star-outline-rounded-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polygon points="8,2.5 9.8,6.5 14.5,7 11,10.2 12,14.5 8,12.2 4,14.5 5,10.2 1.5,7 6.2,6.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
</svg>''',

    "star-filled-rounded-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polygon points="8,2.5 9.8,6.5 14.5,7 11,10.2 12,14.5 8,12.2 4,14.5 5,10.2 1.5,7 6.2,6.5" fill="currentColor"/>
</svg>''',

    "offline-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" d="M 4 10 C 2.5 10 1.5 8.8 1.5 7.5 C 1.5 6.2 2.5 5.2 3.8 5 C 4.2 3.3 5.8 2 7.5 2 C 9.5 2 11 3.4 11.3 5.2 C 12.3 5.5 13 6.4 13 7.5 M 1 1 L 15 15"/>
</svg>''',

    # Fixes Sound Input & Output Device Chooser row in Extension Manager
    "sound-output-device-chooser@kgshank.net": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 2 5 L 5 5 L 9 2 L 9 14 L 5 11 L 2 11 Z"/>
  <path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" d="M 11.5 5 C 12.5 6 13 7 13 8 C 13 9 12.5 10 11.5 11 M 13.5 3 C 15 4.5 15.5 6.2 15.5 8 C 15.5 9.8 15 11.5 13.5 13"/>
</svg>''',

    "sound-output-device-chooser": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 2 5 L 5 5 L 9 2 L 9 14 L 5 11 L 2 11 Z"/>
  <path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" d="M 11.5 5 C 12.5 6 13 7 13 8 C 13 9 12.5 10 11.5 11 M 13.5 3 C 15 4.5 15.5 6.2 15.5 8 C 15.5 9.8 15 11.5 13.5 13"/>
</svg>''',
}

# Merge extended symbolic icons (screenshot UI, Settings panels, navigation, globe)
SYMBOLIC_ICONS.update(EXTENDED_SYMBOLIC_ICONS)

# =========================================================================
# Application Icons (LibreOffice, Antigravity, Geary, Disks, Console, Apps)
# =========================================================================

APP_ICONS = {
    # 1. Nautilus / GNOME Files
    "org.gnome.Nautilus": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="cabGrad" x1="32" y1="6" x2="32" y2="58" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#24444D"/>
    <stop offset="50%" stop-color="#1A333A"/>
    <stop offset="100%" stop-color="#122329"/>
  </linearGradient>
  <linearGradient id="handleGrad" x1="24" y1="0" x2="40" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#8FB8A6"/>
    <stop offset="100%" stop-color="#3DD68C"/>
  </linearGradient>
</defs>
<rect x="12" y="6" width="40" height="52" rx="8" fill="url(#cabGrad)" stroke="#2E555F" stroke-width="1.5"/>
<rect x="13.5" y="7.5" width="37" height="5" rx="3" fill="#8FB8A6" fill-opacity="0.25"/>
<rect x="15" y="11" width="34" height="12" rx="3" fill="#14262C" stroke="#2E555F" stroke-width="1"/>
<rect x="26" y="15.5" width="12" height="3" rx="1.5" fill="url(#handleGrad)"/>
<rect x="15" y="25" width="34" height="12" rx="3" fill="#14262C" stroke="#2E555F" stroke-width="1"/>
<rect x="26" y="29.5" width="12" height="3" rx="1.5" fill="url(#handleGrad)"/>
<rect x="15" y="39" width="34" height="12" rx="3" fill="#14262C" stroke="#2E555F" stroke-width="1"/>
<rect x="26" y="43.5" width="12" height="3" rx="1.5" fill="url(#handleGrad)"/>
<circle cx="45" cy="17" r="1.5" fill="#3DD68C"/>
</svg>''',

    # 2. GNOME Terminal
    "utilities-terminal": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="6" y="8" width="52" height="48" rx="8" fill="#0B1317" stroke="#2C3E44" stroke-width="1.5"/>
<rect x="6" y="8" width="52" height="12" rx="8" fill="#16222A"/>
<circle cx="13" cy="14" r="2.5" fill="#E5737F"/>
<circle cx="20" cy="14" r="2.5" fill="#E5B580"/>
<circle cx="27" cy="14" r="2.5" fill="#3DD68C"/>
<path d="M 16 28 L 24 34 L 16 40" stroke="#8FB8A6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="28" y1="42" x2="42" y2="42" stroke="#3DD68C" stroke-width="3" stroke-linecap="round"/>
</svg>''',

    # 3. GNOME Settings
    "preferences-system": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="24" fill="#16222A" stroke="#2C3E44" stroke-width="1.5"/>
<circle cx="32" cy="32" r="15" fill="#1D3238" stroke="#8FB8A6" stroke-width="3"/>
<circle cx="32" cy="32" r="6" fill="#8FB8A6"/>
<rect x="30" y="10" width="4" height="8" rx="2" fill="#8FB8A6"/>
<rect x="30" y="46" width="4" height="8" rx="2" fill="#8FB8A6"/>
<rect x="10" y="30" width="8" height="4" rx="2" fill="#8FB8A6"/>
<rect x="46" y="30" width="8" height="4" rx="2" fill="#8FB8A6"/>
</svg>''',

    # 4. Text Editor
    "accessories-text-editor": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="12" y="8" width="38" height="48" rx="6" fill="#16222A" stroke="#2C3E44" stroke-width="1.5"/>
<rect x="12" y="8" width="38" height="10" rx="6" fill="#8FB8A6"/>
<line x1="18" y1="26" x2="42" y2="26" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<line x1="18" y1="33" x2="42" y2="33" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<line x1="18" y1="40" x2="34" y2="40" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<polygon points="42,44 48,38 48,50" fill="#3DD68C"/>
</svg>''',

    # 5. Calculator
    "org.gnome.Calculator": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="10" y="6" width="44" height="52" rx="8" fill="#16222A" stroke="#2C3E44" stroke-width="1.5"/>
<rect x="16" y="12" width="32" height="12" rx="3" fill="#1D3238" stroke="#8FB8A6" stroke-width="1"/>
<text x="44" y="21" font-family="sans-serif" font-size="10" fill="#3DD68C" text-anchor="end">42</text>
<circle cx="21" cy="32" r="3.5" fill="#1D3238"/>
<circle cx="32" cy="32" r="3.5" fill="#1D3238"/>
<circle cx="43" cy="32" r="3.5" fill="#8FB8A6"/>
<circle cx="21" cy="42" r="3.5" fill="#1D3238"/>
<circle cx="32" cy="42" r="3.5" fill="#1D3238"/>
<circle cx="43" cy="42" r="3.5" fill="#8FB8A6"/>
<circle cx="21" cy="51" r="3.5" fill="#1D3238"/>
<circle cx="32" cy="51" r="3.5" fill="#1D3238"/>
<circle cx="43" cy="51" r="3.5" fill="#3DD68C"/>
</svg>''',

    # 6. Google Antigravity IDE (Specialist requested icon)
    "antigravity": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="agGrad" x1="16" y1="46" x2="48" y2="14" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#3DD68C"/>
    <stop offset="50%" stop-color="#7FC8A0"/>
    <stop offset="100%" stop-color="#8FB8A6"/>
  </linearGradient>
</defs>
<rect x="6" y="6" width="52" height="52" rx="15" fill="#122329" stroke="#2E555F" stroke-width="2"/>
<circle cx="32" cy="32" r="23" fill="#182E36" fill-opacity="0.6"/>
<!-- Antigravity iconic smooth Gaussian bell arch -->
<path d="M 17 45 C 21 45 25 38 28.5 25 C 30 19 32 15 32 15 C 32 15 34 19 35.5 25 C 39 38 43 45 47 45 C 48.5 45 49 43.8 48 42.5 C 43 30 36.5 13 32 13 C 27.5 13 21 30 16 42.5 C 15 43.8 15.5 45 17 45 Z" fill="url(#agGrad)"/>
<circle cx="32" cy="22" r="3" fill="#3DD68C"/>
</svg>''',

    # 7. OpenChamber (AI Workspace)
    "openchamber": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="6" y="6" width="52" height="52" rx="14" fill="#122329" stroke="#2E555F" stroke-width="2"/>
<!-- Isometric 3D Chamber Cube in glowing emerald -->
<g transform="translate(32, 33) scale(0.38)">
  <path d="M 0 -48 L -41.5 -24 L 0 0 L 41.5 -24 Z" fill="none" stroke="#3DD68C" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 0 0 L -41.5 -24 L -41.5 24 L 0 48 Z" fill="#8FB8A6" fill-opacity="0.3" stroke="#8FB8A6" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 0 0 L 41.5 -24 L 41.5 24 L 0 48 Z" fill="#3DD68C" fill-opacity="0.45" stroke="#3DD68C" stroke-width="5" stroke-linejoin="round"/>
</g>
</svg>''',

    # 8. GNOME Geary Mail Client
    "org.gnome.Geary": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="12" width="48" height="40" rx="6" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<path d="M 10 14 L 32 32 L 54 14" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<polygon points="32,36 36,31 28,31" fill="#3DD68C"/>
<line x1="12" y1="48" x2="26" y2="34" stroke="#2E555F" stroke-width="1.8"/>
<line x1="52" y1="48" x2="38" y2="34" stroke="#2E555F" stroke-width="1.8"/>
</svg>''',

    # 9. GNOME Console (kgx)
    "org.gnome.Console": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="7" y="10" width="50" height="44" rx="8" fill="#0D1A1F" stroke="#2E555F" stroke-width="2"/>
<rect x="7" y="10" width="50" height="11" rx="8" fill="#172F37"/>
<circle cx="14" cy="15.5" r="2" fill="#E5737F"/>
<circle cx="20" cy="15.5" r="2" fill="#E5B580"/>
<circle cx="26" cy="15.5" r="2" fill="#3DD68C"/>
<path d="M 16 29 L 24 35 L 16 41" stroke="#3DD68C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="28" y1="41" x2="42" y2="41" stroke="#8FB8A6" stroke-width="3" stroke-linecap="round"/>
</svg>''',

    # 10. GNOME Disks / Disk Utility
    "org.gnome.DiskUtility": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="10" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
<circle cx="32" cy="32" r="18" fill="#1B353D" stroke="#8FB8A6" stroke-width="2"/>
<circle cx="32" cy="32" r="6" fill="#13262D" stroke="#3DD68C" stroke-width="2"/>
<circle cx="32" cy="32" r="2" fill="#3DD68C"/>
<path d="M 43 19 L 34 29" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="44" cy="18" r="2" fill="#8FB8A6"/>
</svg>''',

    # 11. LibreOffice Main / Start Center
    "libreoffice-startcenter": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
<rect x="18" y="14" width="28" height="36" rx="3" fill="#1E3B44" stroke="#8FB8A6" stroke-width="1.5"/>
<polygon points="38,14 46,22 38,22" fill="#3DD68C"/>
<circle cx="32" cy="35" r="6" fill="#3DD68C"/>
<circle cx="32" cy="35" r="3" fill="#13262D"/>
</svg>''',

    # 12. LibreOffice Writer
    "libreoffice-writer": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
<rect x="18" y="14" width="28" height="36" rx="3" fill="#1B353D" stroke="#8FB8A6" stroke-width="1.5"/>
<polygon points="38,14 46,22 38,22" fill="#7FC8A0"/>
<line x1="23" y1="24" x2="35" y2="24" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
<line x1="23" y1="30" x2="41" y2="30" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
<line x1="23" y1="36" x2="41" y2="36" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
<line x1="23" y1="42" x2="33" y2="42" stroke="#3DD68C" stroke-width="2" stroke-linecap="round"/>
</svg>''',

    # 13. LibreOffice Calc
    "libreoffice-calc": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
<rect x="18" y="14" width="28" height="36" rx="3" fill="#1B353D" stroke="#8FB8A6" stroke-width="1.5"/>
<polygon points="38,14 46,22 38,22" fill="#3DD68C"/>
<line x1="22" y1="26" x2="42" y2="26" stroke="#8FB8A6" stroke-width="1.5"/>
<line x1="22" y1="34" x2="42" y2="34" stroke="#8FB8A6" stroke-width="1.5"/>
<line x1="32" y1="20" x2="32" y2="44" stroke="#8FB8A6" stroke-width="1.5"/>
<rect x="24" y="37" width="5" height="5" fill="#3DD68C"/>
<rect x="34" y="29" width="6" height="3" fill="#7FC8A0"/>
</svg>''',

    # 14. LibreOffice Impress
    "libreoffice-impress": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
<rect x="18" y="14" width="28" height="36" rx="3" fill="#1B353D" stroke="#8FB8A6" stroke-width="1.5"/>
<polygon points="38,14 46,22 38,22" fill="#E5B580"/>
<circle cx="32" cy="33" r="8" fill="#13262D" stroke="#8FB8A6" stroke-width="1.5"/>
<path d="M 32 33 L 32 25 A 8 8 0 0 1 39 30 Z" fill="#E5B580"/>
<path d="M 32 33 L 39 30 A 8 8 0 0 1 32 41 Z" fill="#3DD68C"/>
</svg>''',

    # 15. LibreOffice Draw
    "libreoffice-draw": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
<rect x="18" y="14" width="28" height="36" rx="3" fill="#1B353D" stroke="#8FB8A6" stroke-width="1.5"/>
<polygon points="38,14 46,22 38,22" fill="#E5737F"/>
<path d="M 23 42 C 27 28 37 38 41 24" stroke="#3DD68C" stroke-width="2.5" fill="none" stroke-linecap="round"/>
<circle cx="23" cy="42" r="2.5" fill="#8FB8A6"/>
<circle cx="41" cy="24" r="2.5" fill="#8FB8A6"/>
</svg>''',

    # 16. LibreOffice Base
    "libreoffice-base": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
<rect x="18" y="14" width="28" height="36" rx="3" fill="#1B353D" stroke="#8FB8A6" stroke-width="1.5"/>
<polygon points="38,14 46,22 38,22" fill="#8FB8A6"/>
<ellipse cx="32" cy="28" rx="8" ry="3" fill="#13262D" stroke="#3DD68C" stroke-width="1.5"/>
<path d="M 24 28 L 24 34 C 24 36 27.5 37 32 37 C 36.5 37 40 36 40 34 L 40 28" fill="none" stroke="#3DD68C" stroke-width="1.5"/>
<path d="M 24 34 L 24 40 C 24 42 27.5 43 32 43 C 36.5 43 40 42 40 40 L 40 34" fill="none" stroke="#3DD68C" stroke-width="1.5"/>
</svg>''',

    # 17. LibreOffice Math
    "libreoffice-math": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
<rect x="18" y="14" width="28" height="36" rx="3" fill="#1B353D" stroke="#8FB8A6" stroke-width="1.5"/>
<polygon points="38,14 46,22 38,22" fill="#7FC8A0"/>
<path d="M 24 27 L 39 27 L 32 34 L 39 41 L 24 41" stroke="#3DD68C" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    # 18. Google Chrome
    "google-chrome": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="26" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<circle cx="32" cy="32" r="11" fill="#1D3238" stroke="#8FB8A6" stroke-width="3"/>
<circle cx="32" cy="32" r="5" fill="#3DD68C"/>
<path d="M 32 6 C 39.5 6 46.2 9.2 50.8 14.5 L 37.5 37.5" stroke="#E5737F" stroke-width="3" stroke-linecap="round"/>
<path d="M 50.8 14.5 C 55.2 19.5 58 26.2 58 33.5 L 26.5 33.5" stroke="#7FC8A0" stroke-width="3" stroke-linecap="round"/>
<path d="M 26.5 33.5 L 13.2 51.5 C 8.6 46.5 6 39.7 6 32" stroke="#E5B580" stroke-width="3" stroke-linecap="round"/>
</svg>''',

    # 19. Microsoft Edge
    "microsoft-edge": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="26" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<path d="M 32 10 C 22 10 14 18 14 28 C 14 36 20 42 27 42 C 34 42 40 37 40 32 C 40 28 37 25 33 25 C 29 25 27 28 27 30 C 27 32 29 34 31 34 C 33 34 34 33 34 32" stroke="#3DD68C" stroke-width="3.5" stroke-linecap="round" fill="none"/>
<path d="M 46 22 C 49 26 50 31 49 36 C 47 45 39 52 30 52 C 22 52 16 48 13 42" stroke="#8FB8A6" stroke-width="3" stroke-linecap="round" fill="none"/>
</svg>''',

    # 20. Brave Browser
    "brave-browser": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="14" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<polygon points="32,14 44,22 40,40 32,50 24,40 20,22" fill="#1B353D" stroke="#E5B580" stroke-width="2.5" stroke-linejoin="round"/>
<polygon points="32,24 38,30 36,40 32,44 28,40 26,30" fill="#3DD68C"/>
</svg>''',

    # 21. Claude Desktop (Anthropic)
    "claude-desktop": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="14" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<g transform="translate(32, 32)">
  <line x1="0" y1="-18" x2="0" y2="18" stroke="#E5B580" stroke-width="4" stroke-linecap="round"/>
  <line x1="-18" y1="0" x2="18" y2="0" stroke="#E5B580" stroke-width="4" stroke-linecap="round"/>
  <line x1="-12" y1="-12" x2="12" y2="12" stroke="#3DD68C" stroke-width="4" stroke-linecap="round"/>
  <line x1="12" y1="-12" x2="-12" y2="12" stroke="#3DD68C" stroke-width="4" stroke-linecap="round"/>
  <circle cx="0" cy="0" r="3.5" fill="#8FB8A6"/>
</g>
</svg>''',

    # 22. Telegram
    "org.telegram.desktop": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="26" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<circle cx="32" cy="32" r="24" fill="#1B353D"/>
<path d="M 16 31 L 46 19 L 41 45 L 30 37 L 24 43 L 26 35 Z" fill="#8FB8A6"/>
<path d="M 30 37 L 40 24 L 26 35 Z" fill="#3DD68C"/>
</svg>''',

    # 23. qBittorrent
    "org.qbittorrent.qBittorrent": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="26" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<path d="M 32 16 L 32 38 M 32 38 L 23 29 M 32 38 L 41 29" stroke="#3DD68C" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 20 44 C 24 48 40 48 44 44" stroke="#8FB8A6" stroke-width="3" stroke-linecap="round"/>
</svg>''',

    # 24. MPV Media Player
    "mpv": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="26" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<circle cx="32" cy="32" r="22" fill="#122329"/>
<polygon points="26,20 44,32 26,44" fill="#3DD68C"/>
</svg>''',

    # 25. Pavucontrol / Audio Volume Control
    "org.pulseaudio.pavucontrol": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<line x1="20" y1="16" x2="20" y2="48" stroke="#2E555F" stroke-width="3" stroke-linecap="round"/>
<line x1="32" y1="16" x2="32" y2="48" stroke="#2E555F" stroke-width="3" stroke-linecap="round"/>
<line x1="44" y1="16" x2="44" y2="48" stroke="#2E555F" stroke-width="3" stroke-linecap="round"/>
<circle cx="20" cy="26" r="4.5" fill="#3DD68C"/>
<circle cx="32" cy="40" r="4.5" fill="#8FB8A6"/>
<circle cx="44" cy="22" r="4.5" fill="#3DD68C"/>
</svg>''',

    # 26. Extension Manager
    "com.mattjakeman.ExtensionManager": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="14" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<path d="M 28 20 C 28 17.5 30 16 32 16 C 34 16 36 17.5 36 20 L 42 20 C 44 20 46 22 46 24 L 46 30 C 48.5 30 50 32 50 34 C 50 36 48.5 38 46 38 L 46 44 C 46 46 44 48 42 48 L 36 48 C 36 50.5 34 52 32 52 C 30 52 28 50.5 28 48 L 22 48 C 20 48 18 46 18 44 L 18 38 C 15.5 38 14 36 14 34 C 14 32 15.5 30 18 30 L 18 24 C 18 22 20 20 22 20 Z" fill="#1B353D" stroke="#3DD68C" stroke-width="2.5" stroke-linejoin="round"/>
<circle cx="32" cy="34" r="3.5" fill="#8FB8A6"/>
</svg>''',

    # 27. GNOME Software
    "org.gnome.Software": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="10" y="16" width="44" height="40" rx="8" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<path d="M 22 16 C 22 10 26 8 32 8 C 38 8 42 10 42 16" stroke="#8FB8A6" stroke-width="3" stroke-linecap="round" fill="none"/>
<polygon points="32,24 35,32 43,32 37,37 39,45 32,40 25,45 27,37 21,32 29,32" fill="#3DD68C"/>
</svg>''',

    # 28. GNOME System Monitor
    "org.gnome.SystemMonitor": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="10" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<line x1="8" y1="32" x2="56" y2="32" stroke="#2E555F" stroke-width="1.2" stroke-dasharray="2 2"/>
<line x1="32" y1="8" x2="32" y2="56" stroke="#2E555F" stroke-width="1.2" stroke-dasharray="2 2"/>
<polyline points="12,34 22,34 27,20 33,46 39,26 44,34 52,34" fill="none" stroke="#3DD68C" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    # 29. Btrfs Assistant
    "btrfs-assistant": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="10" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
<rect x="14" y="16" width="36" height="12" rx="3" fill="#1B353D" stroke="#8FB8A6" stroke-width="1.5"/>
<circle cx="43" cy="22" r="1.5" fill="#3DD68C"/>
<path d="M 22 28 L 22 44 L 32 44 M 22 36 L 42 36" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="32" cy="44" r="2.5" fill="#8FB8A6"/>
<circle cx="42" cy="36" r="2.5" fill="#8FB8A6"/>
</svg>''',

    # 30. btop
    "btop": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="6" y="8" width="52" height="48" rx="8" fill="#0D1A1F" stroke="#2E555F" stroke-width="2"/>
<polyline points="12,42 20,38 28,40 36,22 44,30 52,20" fill="none" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<polyline points="12,46 20,44 28,45 36,36 44,40 52,32" fill="none" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

    # 31. Alacritty
    "Alacritty": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="10" fill="#0D1A1F" stroke="#2E555F" stroke-width="2"/>
<polygon points="32,15 48,46 41,46 32,27 23,46 16,46" fill="#3DD68C"/>
<polygon points="26,38 38,38 32,26" fill="#0D1A1F"/>
</svg>''',

    # 32. Discord
    "discord": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="14" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<path d="M 44 20 C 41.5 18.8 38.8 18 36 17.5 C 35.6 18.2 35.1 19.2 34.8 20 C 31.8 19.6 28.8 19.6 25.8 20 C 25.5 19.2 25 18.2 24.6 17.5 C 21.8 18 19.1 18.8 16.6 20 C 12 26.8 10.8 33.5 11.4 40 C 14.5 42.3 17.4 43.7 20.3 44.6 C 21 43.6 21.6 42.6 22.2 41.5 C 21.1 41.1 20.1 40.5 19.2 39.8 C 19.5 39.6 19.7 39.4 20 39.2 C 25.5 41.8 31.5 41.8 37 39.2 C 37.3 39.4 37.5 39.6 37.8 39.8 C 36.9 40.5 35.9 41.1 34.8 41.5 C 35.4 42.6 36 43.6 36.7 44.6 C 39.6 43.7 42.5 42.3 45.6 40 C 46.3 32.5 44.5 25.8 44 20 Z M 23.5 35 A 3.5 3.5 0 1 1 23.5 28 A 3.5 3.5 0 0 1 23.5 35 Z M 37.5 35 A 3.5 3.5 0 1 1 37.5 28 A 3.5 3.5 0 0 1 37.5 35 Z" fill="#8FB8A6"/>
</svg>''',

    # 33. Spotify
    "spotify": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="26" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<circle cx="32" cy="32" r="23" fill="#0D1A1F"/>
<path d="M 19 24.5 C 27.5 22 37.5 23 45 27" stroke="#3DD68C" stroke-width="4" stroke-linecap="round"/>
<path d="M 21 32 C 28 30 36 31 43 35" stroke="#3DD68C" stroke-width="3.5" stroke-linecap="round"/>
<path d="M 23 39.5 C 28.5 38 34.5 39 40.5 42.5" stroke="#8FB8A6" stroke-width="3" stroke-linecap="round"/>
</svg>''',

    # 34. VS Code
    "code": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<path d="M 45 13 L 34 23 L 25 15 L 20 18 L 30 27 L 20 36 L 25 39 L 34 31 L 45 41 Z" fill="#8FB8A6"/>
<path d="M 45 13 L 34 23 L 45 33 Z" fill="#3DD68C"/>
</svg>''',
}

# Merge extended core GNOME application icons (Calendar, Contacts, Weather, etc.)
APP_ICONS.update(EXTENDED_APP_ICONS)

APP_ALIASES = {
    # File manager
    "system-file-manager": "org.gnome.Nautilus",
    "nautilus": "org.gnome.Nautilus",
    "file-manager": "org.gnome.Nautilus",
    # Terminal
    "org.gnome.Terminal": "utilities-terminal",
    "kitty": "utilities-terminal",
    "alacritty": "Alacritty",
    "kgx": "org.gnome.Console",
    # Settings & Tools
    "org.gnome.Settings": "preferences-system",
    "org.gnome.tweaks": "preferences-system",
    "org.gnome.TextEditor": "accessories-text-editor",
    "text-editor": "accessories-text-editor",
    "accessories-calculator": "org.gnome.Calculator",
    "calculator": "org.gnome.Calculator",
    "gnome-disks": "org.gnome.DiskUtility",
    "gnome-disk-utility": "org.gnome.DiskUtility",
    "gnome-system-monitor": "org.gnome.SystemMonitor",
    "gnome-software": "org.gnome.Software",
    "extension-manager": "com.mattjakeman.ExtensionManager",
    "pavucontrol": "org.pulseaudio.pavucontrol",
    # Mail & Chat
    "geary": "org.gnome.Geary",
    "telegram": "org.telegram.desktop",
    "telegram-desktop": "org.telegram.desktop",
    "com.discordapp.Discord": "discord",
    "discord-canary": "discord",
    # Web & Dev
    "google-chrome-stable": "google-chrome",
    "chromium": "google-chrome",
    "edge": "microsoft-edge",
    "com.microsoft.Edge": "microsoft-edge",
    "openchamber-2.1.0-linux-x86_64": "openchamber",
    "com.anthropic.Claude": "claude-desktop",
    "qbittorrent": "org.qbittorrent.qBittorrent",
    "spotify-client": "spotify",
    "com.spotify.Client": "spotify",
    "visual-studio-code": "code",
    "com.visualstudio.code": "code",
    "vscode": "code",
    # LibreOffice suite
    "libreoffice-main": "libreoffice-startcenter",
    "libreoffice": "libreoffice-startcenter",
}

# Merge extended application aliases for full desktop compatibility
APP_ALIASES.update(EXTENDED_APP_ALIASES)

# =========================================================================
# MIME Type Document Icons (Clean botanical file-type suite for Nautilus)
# =========================================================================

MIME_DOC_BASE = '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="docGrad" x1="32" y1="8" x2="32" y2="56" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#1B353D"/>
    <stop offset="100%" stop-color="#122329"/>
  </linearGradient>
</defs>
<rect x="14" y="8" width="36" height="48" rx="6" fill="url(#docGrad)" stroke="#2E555F" stroke-width="1.5"/>
<polygon points="36,8 50,22 36,22" fill="#2E555F"/>
<polygon points="36,8 50,22 36,22" fill="#8FB8A6" fill-opacity="0.3"/>
'''

MIME_ICONS = {
    "text-plain": MIME_DOC_BASE + '''
<line x1="22" y1="28" x2="42" y2="28" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
<line x1="22" y1="34" x2="42" y2="34" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
<line x1="22" y1="40" x2="34" y2="40" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
''' + SVG_FOOTER,

    "text-x-python": MIME_DOC_BASE + '''
<path d="M 28 26 C 28 24 30 23 32 23 L 36 23 C 38 23 39 24 39 26 L 39 30 L 33 30 C 31 30 30 31 30 33 L 30 36 L 28 36 C 26 36 25 35 25 33 L 25 29 C 25 27 26 26 28 26 Z" fill="#3DD68C"/>
<path d="M 36 42 C 36 44 34 45 32 45 L 28 45 C 26 45 25 44 25 42 L 25 38 L 31 38 C 33 38 34 37 34 35 L 34 32 L 36 32 C 38 32 39 33 39 35 L 39 39 C 39 41 38 42 36 42 Z" fill="#8FB8A6"/>
<circle cx="30" cy="26" r="0.8" fill="#122329"/>
<circle cx="34" cy="42" r="0.8" fill="#122329"/>
''' + SVG_FOOTER,

    "application-x-zerosize": MIME_DOC_BASE + '''
<line x1="22" y1="32" x2="42" y2="32" stroke="#2E555F" stroke-width="1.5" stroke-dasharray="2 3"/>
''' + SVG_FOOTER,

    "image-x-generic": MIME_DOC_BASE + '''
<rect x="20" y="26" width="24" height="18" rx="2" fill="#16222A" stroke="#8FB8A6" stroke-width="1.5"/>
<circle cx="26" cy="31" r="2" fill="#3DD68C"/>
<polygon points="23,43 28,37 33,41 36,38 41,43" fill="#8FB8A6"/>
''' + SVG_FOOTER,

    "application-pdf": MIME_DOC_BASE + '''
<rect x="20" y="26" width="24" height="14" rx="3" fill="#E5737F"/>
<text x="32" y="36.5" font-family="sans-serif" font-weight="bold" font-size="8" fill="#FFFFFF" text-anchor="middle">PDF</text>
<line x1="22" y1="46" x2="42" y2="46" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
''' + SVG_FOOTER,
}

# =========================================================================
# Hardware Storage Devices Suite (64x64 Color SVGs with botanical styling)
# =========================================================================

DEVICE_ICONS = {
    "drive-harddisk": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="6" width="48" height="52" rx="8" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
  <rect x="12" y="10" width="40" height="44" rx="5" fill="#1B353D" stroke="#24444D" stroke-width="1"/>
  <circle cx="32" cy="30" r="17" fill="#13262D" stroke="#8FB8A6" stroke-width="2"/>
  <circle cx="32" cy="30" r="6" fill="#1B353D" stroke="#3DD68C" stroke-width="2"/>
  <circle cx="32" cy="30" r="2" fill="#3DD68C"/>
  <path d="M 44 19 L 34 28" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="44" cy="18" r="2.5" fill="#8FB8A6"/>
  <circle cx="14" cy="12" r="1.5" fill="#2E555F"/>
  <circle cx="50" cy="12" r="1.5" fill="#2E555F"/>
  <circle cx="14" cy="52" r="1.5" fill="#2E555F"/>
  <circle cx="50" cy="52" r="1.5" fill="#2E555F"/>
  <rect x="20" y="47" width="24" height="4" rx="2" fill="#24444D"/>
  <circle cx="40" cy="49" r="1" fill="#3DD68C"/>
</svg>''',

    "drive-harddisk-solidstate": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="6" width="48" height="52" rx="8" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
  <rect x="12" y="10" width="40" height="44" rx="5" fill="#1B353D" stroke="#24444D" stroke-width="1"/>
  <rect x="22" y="18" width="20" height="20" rx="3" fill="#13262D" stroke="#3DD68C" stroke-width="2"/>
  <rect x="27" y="23" width="10" height="10" rx="1.5" fill="#24444D"/>
  <line x1="26" y1="14" x2="26" y2="18" stroke="#8FB8A6" stroke-width="1.5"/>
  <line x1="32" y1="14" x2="32" y2="18" stroke="#8FB8A6" stroke-width="1.5"/>
  <line x1="38" y1="14" x2="38" y2="18" stroke="#8FB8A6" stroke-width="1.5"/>
  <line x1="26" y1="38" x2="26" y2="42" stroke="#8FB8A6" stroke-width="1.5"/>
  <line x1="32" y1="38" x2="32" y2="42" stroke="#8FB8A6" stroke-width="1.5"/>
  <line x1="38" y1="38" x2="38" y2="42" stroke="#8FB8A6" stroke-width="1.5"/>
  <rect x="18" y="46" width="28" height="5" rx="1" fill="#24444D" stroke="#8FB8A6" stroke-width="1"/>
  <line x1="22" y1="46" x2="22" y2="51" stroke="#3DD68C" stroke-width="1.5"/>
  <line x1="26" y1="46" x2="26" y2="51" stroke="#3DD68C" stroke-width="1.5"/>
  <line x1="30" y1="46" x2="30" y2="51" stroke="#3DD68C" stroke-width="1.5"/>
</svg>''',

    "drive-harddisk-usb": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="8" width="44" height="50" rx="9" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
  <rect x="14" y="12" width="36" height="42" rx="6" fill="#1B353D" stroke="#24444D" stroke-width="1"/>
  <line x1="12" y1="20" x2="12" y2="46" stroke="#3DD68C" stroke-width="3" stroke-linecap="round"/>
  <line x1="52" y1="20" x2="52" y2="46" stroke="#3DD68C" stroke-width="3" stroke-linecap="round"/>
  <circle cx="32" cy="28" r="8" fill="#13262D" stroke="#8FB8A6" stroke-width="1.5"/>
  <rect x="28" y="3" width="8" height="6" rx="1" fill="#2E555F" stroke="#8FB8A6" stroke-width="1"/>
  <line x1="30" y1="5" x2="30" y2="7" stroke="#3DD68C" stroke-width="1"/>
  <line x1="34" y1="5" x2="34" y2="7" stroke="#3DD68C" stroke-width="1"/>
  <circle cx="32" cy="46" r="2" fill="#3DD68C"/>
</svg>''',

    "drive-harddisk-root": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="6" width="48" height="52" rx="8" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
  <rect x="12" y="10" width="40" height="44" rx="5" fill="#1B353D" stroke="#24444D" stroke-width="1"/>
  <circle cx="32" cy="30" r="17" fill="#13262D" stroke="#8FB8A6" stroke-width="2"/>
  <circle cx="32" cy="30" r="6" fill="#1B353D" stroke="#3DD68C" stroke-width="2"/>
  <circle cx="32" cy="30" r="2" fill="#3DD68C"/>
  <path d="M 44 19 L 34 28" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="44" cy="18" r="2.5" fill="#8FB8A6"/>
  <circle cx="46" cy="46" r="10" fill="#13262D" stroke="#3DD68C" stroke-width="2"/>
  <line x1="49" y1="40" x2="43" y2="52" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
</svg>''',

    "drive-partition": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="6" width="48" height="52" rx="8" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
  <rect x="12" y="10" width="18" height="44" rx="4" fill="#1B353D" stroke="#24444D" stroke-width="1"/>
  <rect x="34" y="10" width="18" height="44" rx="4" fill="#1B353D" stroke="#24444D" stroke-width="1"/>
  <circle cx="21" cy="20" r="4" fill="#3DD68C"/>
  <circle cx="43" cy="20" r="4" fill="#8FB8A6"/>
  <rect x="16" y="30" width="10" height="18" rx="2" fill="#13262D"/>
  <rect x="38" y="30" width="10" height="18" rx="2" fill="#13262D"/>
</svg>''',

    "drive-multidisk": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="6" width="44" height="22" rx="5" fill="#13262D" stroke="#2E555F" stroke-width="1.5"/>
  <rect x="14" y="10" width="36" height="14" rx="3" fill="#1B353D"/>
  <circle cx="20" cy="17" r="3" fill="#3DD68C"/>
  <rect x="28" y="15" width="18" height="4" rx="2" fill="#2E555F"/>
  <rect x="10" y="34" width="44" height="22" rx="5" fill="#13262D" stroke="#2E555F" stroke-width="1.5"/>
  <rect x="14" y="38" width="36" height="14" rx="3" fill="#1B353D"/>
  <circle cx="20" cy="45" r="3" fill="#3DD68C"/>
  <rect x="28" y="43" width="18" height="4" rx="2" fill="#2E555F"/>
</svg>''',

    "drive-removable-media": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="22" y="6" width="20" height="16" rx="2" fill="#2E555F" stroke="#8FB8A6" stroke-width="1.5"/>
  <rect x="27" y="10" width="4" height="5" fill="#13262D"/>
  <rect x="33" y="10" width="4" height="5" fill="#13262D"/>
  <rect x="16" y="20" width="32" height="38" rx="8" fill="#13262D" stroke="#2E555F" stroke-width="2"/>
  <rect x="20" y="24" width="24" height="30" rx="5" fill="#1B353D"/>
  <circle cx="32" cy="38" r="5" fill="#3DD68C"/>
  <circle cx="32" cy="38" r="2" fill="#13262D"/>
</svg>'''
}

DEVICE_ALIASES = {
    "drive": "drive-harddisk",
    "drive-harddisk-system": "drive-harddisk-root",
    "drive-removable-media-usb": "drive-removable-media",
    "media-flash": "drive-removable-media",
    "media-optical": "drive-harddisk",
}

INDEX_THEME = """[Icon Theme]
Name=MT-Verdant-Icons
Comment=Botanical Canopy high-definition dark green icon suite for MT Verdant Nocturne
Inherits=Adwaita,breeze-dark,hicolor
Directories=scalable/places,scalable/apps,scalable/status,scalable/devices,scalable/actions,scalable/categories,scalable/ui,scalable/mimetypes,symbolic/actions,symbolic/apps,symbolic/categories,symbolic/devices,symbolic/emblems,symbolic/emotes,symbolic/mimetypes,symbolic/places,symbolic/status,symbolic/ui,symbolic/legacy,32x32/places,32x32/apps,32x32/devices,32x32/mimetypes,48x48/places,48x48/apps,48x48/devices,48x48/mimetypes,64x64/places,64x64/apps,64x64/devices,64x64/mimetypes,128x128/places,128x128/apps,128x128/devices,128x128/mimetypes

[scalable/places]
Size=64
MinSize=16
MaxSize=512
Context=Places
Type=Scalable

[scalable/apps]
Size=64
MinSize=16
MaxSize=512
Context=Applications
Type=Scalable

[scalable/status]
Size=16
MinSize=16
MaxSize=512
Context=Status
Type=Scalable

[scalable/devices]
Size=64
MinSize=16
MaxSize=512
Context=Devices
Type=Scalable

[scalable/actions]
Size=16
MinSize=16
MaxSize=512
Context=Actions
Type=Scalable

[scalable/categories]
Size=16
MinSize=16
MaxSize=512
Context=Categories
Type=Scalable

[scalable/ui]
Size=16
MinSize=8
MaxSize=512
Context=UI
Type=Scalable

[scalable/mimetypes]
Size=64
MinSize=16
MaxSize=512
Context=MimeTypes
Type=Scalable

[symbolic/actions]
Size=16
MinSize=8
MaxSize=512
Context=Actions
Type=Scalable

[symbolic/apps]
Size=16
MinSize=8
MaxSize=512
Context=Applications
Type=Scalable

[symbolic/categories]
Size=16
MinSize=8
MaxSize=512
Context=Categories
Type=Scalable

[symbolic/devices]
Size=16
MinSize=8
MaxSize=512
Context=Devices
Type=Scalable

[symbolic/emblems]
Size=16
MinSize=8
MaxSize=512
Context=Emblems
Type=Scalable

[symbolic/emotes]
Size=16
MinSize=8
MaxSize=512
Context=Emotes
Type=Scalable

[symbolic/mimetypes]
Size=16
MinSize=8
MaxSize=512
Context=MimeTypes
Type=Scalable

[symbolic/places]
Size=16
MinSize=8
MaxSize=512
Context=Places
Type=Scalable

[symbolic/status]
Size=16
MinSize=8
MaxSize=512
Context=Status
Type=Scalable

[symbolic/ui]
Size=16
MinSize=8
MaxSize=512
Context=UI
Type=Scalable

[symbolic/legacy]
Size=16
MinSize=8
MaxSize=512
Context=Legacy
Type=Scalable

[32x32/places]
Size=32
Context=Places
Type=Fixed

[32x32/apps]
Size=32
Context=Applications
Type=Fixed

[32x32/devices]
Size=32
Context=Devices
Type=Fixed

[32x32/mimetypes]
Size=32
Context=MimeTypes
Type=Fixed

[48x48/places]
Size=48
Context=Places
Type=Fixed

[48x48/apps]
Size=48
Context=Applications
Type=Fixed

[48x48/devices]
Size=48
Context=Devices
Type=Fixed

[48x48/mimetypes]
Size=48
Context=MimeTypes
Type=Fixed

[64x64/places]
Size=64
Context=Places
Type=Fixed

[64x64/apps]
Size=64
Context=Applications
Type=Fixed

[64x64/devices]
Size=64
Context=Devices
Type=Fixed

[64x64/mimetypes]
Size=64
Context=MimeTypes
Type=Fixed

[128x128/places]
Size=128
Context=Places
Type=Fixed

[128x128/apps]
Size=128
Context=Applications
Type=Fixed

[128x128/devices]
Size=128
Context=Devices
Type=Fixed

[128x128/mimetypes]
Size=128
Context=MimeTypes
Type=Fixed
"""

def render_svg_to_png(svg_text: str, out_path: Path, size: int) -> None:
    # Rasterize an SVG string into a pixel-perfect PNG at specified dimensions.
    handle = Rsvg.Handle.new_from_data(svg_text.encode("utf-8"))
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surf)
    ctx.scale(size / 64.0, size / 64.0)
    handle.render_cairo(ctx)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    surf.write_to_png(str(out_path))

def build_places() -> None:
    # Build places icons (folders, special directories).
    scalable_dir = OUT_DIR / "scalable" / "places"
    scalable_dir.mkdir(parents=True, exist_ok=True)

    for name, emblem in PLACES_EMBLEMS.items():
        svg_content = SVG_FOLDER_BASE + emblem + "\n" + SVG_FOOTER
        (scalable_dir / f"{name}.svg").write_text(svg_content)
        for size in [32, 48, 64, 128]:
            png_file = OUT_DIR / f"{size}x{size}" / "places" / f"{name}.png"
            render_svg_to_png(svg_content, png_file, size)

    for alias, target in PLACES_ALIASES.items():
        dst_svg = scalable_dir / f"{alias}.svg"
        if dst_svg.exists() or dst_svg.is_symlink():
            dst_svg.unlink()
        dst_svg.symlink_to(f"{target}.svg")
        for size in [32, 48, 64, 128]:
            size_dir = OUT_DIR / f"{size}x{size}" / "places"
            dst_png = size_dir / f"{alias}.png"
            if dst_png.exists() or dst_png.is_symlink():
                dst_png.unlink()
            dst_png.symlink_to(f"{target}.png")

def build_apps() -> None:
    # Build application icons.
    scalable_dir = OUT_DIR / "scalable" / "apps"
    scalable_dir.mkdir(parents=True, exist_ok=True)

    for name, svg_content in APP_ICONS.items():
        (scalable_dir / f"{name}.svg").write_text(svg_content)
        for size in [32, 48, 64, 128]:
            png_file = OUT_DIR / f"{size}x{size}" / "apps" / f"{name}.png"
            render_svg_to_png(svg_content, png_file, size)

    for alias, target in APP_ALIASES.items():
        dst_svg = scalable_dir / f"{alias}.svg"
        if dst_svg.exists() or dst_svg.is_symlink():
            dst_svg.unlink()
        dst_svg.symlink_to(f"{target}.svg")
        for size in [32, 48, 64, 128]:
            size_dir = OUT_DIR / f"{size}x{size}" / "apps"
            dst_png = size_dir / f"{alias}.png"
            if dst_png.exists() or dst_png.is_symlink():
                dst_png.unlink()
            dst_png.symlink_to(f"{target}.png")

def build_symbolic() -> None:
    # Build symbolic wireframe icons for sidebar navigation, settings, devices, and UI actions.
    contexts = ["status", "places", "devices", "actions", "categories", "apps", "ui"]
    scalable_dirs = {ctx: OUT_DIR / "scalable" / ctx for ctx in contexts}
    symbolic_dirs = {ctx: OUT_DIR / "symbolic" / ctx for ctx in contexts}

    for d in list(scalable_dirs.values()) + list(symbolic_dirs.values()):
        d.mkdir(parents=True, exist_ok=True)

    def write_icon(target_contexts: list[str], icon_name: str, svg_content: str) -> None:
        filename = f"{icon_name}.svg" if not icon_name.endswith(".svg") else icon_name
        for ctx in target_contexts:
            if ctx in scalable_dirs:
                (scalable_dirs[ctx] / filename).write_text(svg_content)
            if ctx in symbolic_dirs:
                (symbolic_dirs[ctx] / filename).write_text(svg_content)

    # 1. Write core and extended symbolic SVGs
    for name, svg_content in SYMBOLIC_ICONS.items():
        ctx_list = ["status", "actions"]

        # Applications and Settings panels
        if "Settings" in name or name.endswith("-app-symbolic"):
            ctx_list.extend(["apps", "categories"])

        # Places / storage / navigation
        if any(k in name for k in ["folder", "network", "home", "trash", "recent", "globe", "map"]):
            ctx_list.append("places")

        # UI & Sidebar navigation
        if any(k in name for k in ["sidebar", "split", "find", "menu", "pan-", "go-", "window-", "screenshot", "camera", "screencast", "record"]):
            ctx_list.append("ui")

        # Hardware devices
        if any(k in name for k in ["drive", "media", "server", "camera", "display", "mouse", "keyboard"]):
            ctx_list.append("devices")

        # Categories
        if any(k in name for k in ["setting", "puzzle", "system", "preference"]):
            ctx_list.append("categories")

        write_icon(list(set(ctx_list)), name, svg_content)

    # Storage symbolic aliases
    storage_sym_aliases = {
        "drive-symbolic": "drive-harddisk-symbolic",
        "drive-harddisk-system-symbolic": "drive-harddisk-root-symbolic",
        "drive-harddisk-ieee1394-symbolic": "drive-harddisk-usb-symbolic",
        "drive-removable-media-usb-symbolic": "drive-removable-media-symbolic",
        "media-memory-symbolic": "media-flash-symbolic",
        "media-removable-symbolic": "drive-removable-media-symbolic",
        "media-optical-cd-symbolic": "media-optical-symbolic",
        "media-optical-dvd-symbolic": "media-optical-symbolic",
        "media-optical-bd-symbolic": "media-optical-symbolic",
    }
    for alias, target in storage_sym_aliases.items():
        if target in SYMBOLIC_ICONS:
            write_icon(["status", "actions", "devices"], alias, SYMBOLIC_ICONS[target])

    # 2. Extract and bundle GNOME Shell internal symbolic icons
    gs_res_path = Path("/usr/share/gnome-shell/gnome-shell-icons.gresource")
    if gs_res_path.exists():
        try:
            res = Gio.Resource.load(str(gs_res_path))
            Gio.resources_register(res)
            for subpath, ctx_targets in [
                ("/org/gnome/shell/icons/scalable/actions", ["actions", "status", "ui"]),
                ("/org/gnome/shell/icons/scalable/status", ["status", "actions", "ui"]),
            ]:
                try:
                    for icon in Gio.resources_enumerate_children(subpath, Gio.ResourceLookupFlags.NONE):
                        try:
                            data = Gio.resources_lookup_data(f"{subpath}/{icon}", Gio.ResourceLookupFlags.NONE)
                            svg_text = data.get_data().decode("utf-8")
                            write_icon(ctx_targets, icon, svg_text)
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception as e:
            print(f"Notice: GNOME Shell icons resource lookup skipped ({e})")

    # 3. Extract and bundle all Libadwaita internal symbolic icons
    try:
        Adw.init()
        adw_icons = Gio.resources_enumerate_children("/org/gnome/Adwaita/icons/scalable/actions", Gio.ResourceLookupFlags.NONE)
        for icon in adw_icons:
            try:
                data = Gio.resources_lookup_data(f"/org/gnome/Adwaita/icons/scalable/actions/{icon}", Gio.ResourceLookupFlags.NONE)
                svg_text = data.get_data().decode("utf-8")
                write_icon(["actions", "status", "ui"], icon, svg_text)
            except Exception:
                pass
    except Exception as e:
        print(f"Notice: Adw resource lookup skipped ({e})")

    # 4. Integrate Blur my Shell extension icons if present
    bms_dir = Path.home() / ".local" / "share" / "gnome-shell" / "extensions" / "blur-my-shell@aunetx" / "icons" / "hicolor" / "scalable" / "actions"
    if bms_dir.exists():
        for bms_svg in bms_dir.glob("*.svg"):
            write_icon(["actions", "status", "ui"], bms_svg.name, bms_svg.read_text())

    # 5. Integrate Tiling Shell extension icons if present
    ts_dir = Path.home() / ".local" / "share" / "gnome-shell" / "extensions" / "tilingshell@ferrarodomenico.com" / "icons"
    if ts_dir.exists():
        for ts_svg in ts_dir.glob("*.svg"):
            write_icon(["actions", "status", "ui"], ts_svg.name, ts_svg.read_text())

def build_devices() -> None:
    # Build hardware storage devices icons (HDD, SSD, USB external, Partition).
    scalable_dir = OUT_DIR / "scalable" / "devices"
    scalable_dir.mkdir(parents=True, exist_ok=True)

    for name, svg_content in DEVICE_ICONS.items():
        (scalable_dir / f"{name}.svg").write_text(svg_content)
        for size in [32, 48, 64, 128]:
            png_file = OUT_DIR / f"{size}x{size}" / "devices" / f"{name}.png"
            render_svg_to_png(svg_content, png_file, size)

    # Link device aliases
    for alias, target in DEVICE_ALIASES.items():
        svg_alias = scalable_dir / f"{alias}.svg"
        if svg_alias.exists() or svg_alias.is_symlink():
            svg_alias.unlink()
        svg_alias.symlink_to(f"{target}.svg")

        for size in [32, 48, 64, 128]:
            size_dir = OUT_DIR / f"{size}x{size}" / "devices"
            dst_png = size_dir / f"{alias}.png"
            if dst_png.exists() or dst_png.is_symlink():
                dst_png.unlink()
            dst_png.symlink_to(f"{target}.png")

def build_mimetypes() -> None:
    # Build MIME type document icons.
    scalable_dir = OUT_DIR / "scalable" / "mimetypes"
    scalable_dir.mkdir(parents=True, exist_ok=True)

    for name, svg_content in MIME_ICONS.items():
        (scalable_dir / f"{name}.svg").write_text(svg_content)
        for size in [32, 48, 64, 128]:
            png_file = OUT_DIR / f"{size}x{size}" / "mimetypes" / f"{name}.png"
            render_svg_to_png(svg_content, png_file, size)

def main() -> None:
    # Clean and assemble full MT-Verdant-Icons suite.
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.theme").write_text(INDEX_THEME)

    print("Building Places Icons...")
    build_places()

    print("Building App Icons (LibreOffice, Antigravity, Geary, Disks, Console)...")
    build_apps()

    print("Building Devices Icons (HDD, SSD, USB External, Partition, Media)...")
    build_devices()

    print("Building Symbolic Icons (Fixing Blur my Shell, Settings, Storage Drives)...")
    build_symbolic()

    print("Building MIME Type Icons...")
    build_mimetypes()

    print(f"\nMT-Verdant-Icons suite successfully assembled in {OUT_DIR}")

if __name__ == "__main__":
    main()
