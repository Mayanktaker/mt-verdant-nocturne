# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Generates MT-Verdant-Icons suite: vector SVGs, multi-res PNGs, and theme metadata.
# High-definition botanical dark green palette with rich gradients and crisp contrast.

import os
import shutil
from pathlib import Path
import cairo
import gi
gi.require_version("Rsvg", "2.0")
from gi.repository import Rsvg

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
<rect x="21" y="32" width="18" height="18" rx="2.5" fill="#8FB8A6"/>
<polygon points="39,36 45,32 45,50 39,46" fill="#8FB8A6"/>
<polygon points="27,36 34,41 27,46" fill="#13262D"/>''',

    "folder-remote": '''<!-- Network emblem -->
<circle cx="32" cy="41" r="9" stroke="#8FB8A6" stroke-width="2" fill="none"/>
<ellipse cx="32" cy="41" rx="4.5" ry="9" stroke="#8FB8A6" stroke-width="1.5" fill="none"/>
<line x1="23" y1="41" x2="41" y2="41" stroke="#3DD68C" stroke-width="1.5"/>''',

    "network-workgroup": '''<!-- Network workgroup emblem -->
<circle cx="32" cy="41" r="9" stroke="#8FB8A6" stroke-width="2" fill="none"/>
<ellipse cx="32" cy="41" rx="4.5" ry="9" stroke="#8FB8A6" stroke-width="1.5" fill="none"/>
<line x1="23" y1="41" x2="41" y2="41" stroke="#3DD68C" stroke-width="1.5"/>''',

    "network-server": '''<!-- Server rack emblem -->
<rect x="22" y="32" width="20" height="6" rx="2" fill="#13262D" stroke="#8FB8A6" stroke-width="1.5"/>
<rect x="22" y="41" width="20" height="6" rx="2" fill="#13262D" stroke="#8FB8A6" stroke-width="1.5"/>
<circle cx="25" cy="35" r="1" fill="#3DD68C"/>
<circle cx="25" cy="44" r="1" fill="#3DD68C"/>''',

    "folder-applications": '''<!-- Applications launcher grid emblem -->
<circle cx="26" cy="35" r="2.5" fill="#8FB8A6"/>
<circle cx="32" cy="35" r="2.5" fill="#8FB8A6"/>
<circle cx="38" cy="35" r="2.5" fill="#8FB8A6"/>
<circle cx="26" cy="41" r="2.5" fill="#8FB8A6"/>
<circle cx="32" cy="41" r="2.5" fill="#3DD68C"/>
<circle cx="38" cy="41" r="2.5" fill="#8FB8A6"/>
<circle cx="26" cy="47" r="2.5" fill="#8FB8A6"/>
<circle cx="32" cy="47" r="2.5" fill="#8FB8A6"/>
<circle cx="38" cy="47" r="2.5" fill="#8FB8A6"/>''',

    "folder-projects": '''<!-- Code brackets / Dev projects emblem -->
<path d="M 27 35 L 21 41 L 27 47" stroke="#8FB8A6" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 37 35 L 43 41 L 37 47" stroke="#8FB8A6" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="33" y1="34" x2="31" y2="48" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round"/>''',

    "folder-books": '''<!-- Book / Calibre library emblem -->
<path d="M 23 35 C 27 33 32 35 32 35 C 32 35 37 33 41 35 L 41 49 C 37 47 32 49 32 49 C 32 49 27 47 23 49 Z" fill="#8FB8A6" stroke="#13262D" stroke-width="1"/>
<line x1="32" y1="35" x2="32" y2="49" stroke="#3DD68C" stroke-width="2"/>''',

    "folder-publicshare": '''<!-- Public share emblem -->
<circle cx="27" cy="37" r="3.5" fill="#8FB8A6"/>
<circle cx="37" cy="37" r="3.5" fill="#8FB8A6"/>
<path d="M 21 49 C 21 44.5 24.5 43 27 43 C 29.5 43 33 44.5 33 49" fill="#8FB8A6"/>
<path d="M 31 49 C 31 44.5 34.5 43 37 43 C 39.5 43 43 44.5 43 49" fill="#3DD68C"/>''',

    "folder-templates": '''<!-- Templates emblem -->
<rect x="23" y="31" width="18" height="20" rx="2.5" stroke="#8FB8A6" stroke-width="2" stroke-dasharray="3 2" fill="none"/>
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
# Symbolic Wireframe Icons (16x16 crisp vectors for Nautilus Sidebar)
# =========================================================================

SYMBOLIC_ICONS = {
    # Fixes the white missing network icon!
    "network-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 2 2 C 1.45 2 1 2.45 1 3 L 1 9 C 1 9.55 1.45 10 2 10 L 7 10 L 7 12 L 5 12 C 4.45 12 4 12.45 4 13 C 4 13.55 4.45 14 5 14 L 11 14 C 11.55 14 12 13.55 12 13 C 12 12.45 11.55 12 11 12 L 9 12 L 9 10 L 14 10 C 14.55 10 15 9.55 15 9 L 15 3 C 15 2.45 14.55 2 14 2 Z M 3 4 L 13 4 L 13 8 L 3 8 Z"/>
</svg>''',

    "network-workgroup-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 2 2 C 1.45 2 1 2.45 1 3 L 1 9 C 1 9.55 1.45 10 2 10 L 7 10 L 7 12 L 5 12 C 4.45 12 4 12.45 4 13 C 4 13.55 4.45 14 5 14 L 11 14 C 11.55 14 12 13.55 12 13 C 12 12.45 11.55 12 11 12 L 9 12 L 9 10 L 14 10 C 14.55 10 15 9.55 15 9 L 15 3 C 15 2.45 14.55 2 14 2 Z M 3 4 L 13 4 L 13 8 L 3 8 Z"/>
</svg>''',

    "network-server-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="2" width="12" height="5" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <rect x="2" y="9" width="12" height="5" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="4.5" cy="4.5" r="0.75" fill="currentColor"/>
  <circle cx="4.5" cy="11.5" r="0.75" fill="currentColor"/>
</svg>''',

    "folder-remote-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <ellipse cx="8" cy="8" rx="2.5" ry="6" fill="none" stroke="currentColor" stroke-width="1"/>
  <line x1="2" y1="8" x2="14" y2="8" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    "user-home-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 8 2 L 2 7.5 L 3.5 7.5 L 3.5 13.5 L 6.5 13.5 L 6.5 9.5 L 9.5 9.5 L 9.5 13.5 L 12.5 13.5 L 12.5 7.5 L 14 7.5 Z"/>
</svg>''',

    "document-open-recent-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="8,4.5 8,8 10.5,9.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>''',

    "starred-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <polygon points="8,2 10,6.5 15,7 11.5,10.5 12.5,15 8,12.5 3.5,15 4.5,10.5 1,7 6,6.5" fill="currentColor"/>
</svg>''',

    "user-trash-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" d="M 3 4 L 13 4 L 11.5 14 L 4.5 14 Z M 5 2 L 11 2 L 12 3 L 4 3 Z"/>
</svg>''',

    "drive-harddisk-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="3" width="12" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="11.5" cy="10.5" r="1" fill="currentColor"/>
  <line x1="4" y1="10.5" x2="8" y2="10.5" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    # Fixes Extension Manager and Settings buttons!
    "settings-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 7 1 L 9 1 L 9.3 2.7 C 9.8 2.9 10.3 3.2 10.7 3.6 L 12.3 2.9 L 13.7 4.3 L 13 5.9 C 13.4 6.3 13.7 6.8 13.9 7.3 L 15.6 7.6 L 15.6 9.6 L 13.9 9.9 C 13.7 10.4 13.4 10.9 13 11.3 L 13.7 12.9 L 12.3 14.3 L 10.7 13.6 C 10.3 14 9.8 14.3 9.3 14.5 L 9 16.2 L 7 16.2 L 6.7 14.5 C 6.2 14.3 5.7 14 5.3 13.6 L 3.7 14.3 L 2.3 12.9 L 3 11.3 C 2.6 10.9 2.3 10.4 2.1 9.9 L 0.4 9.6 L 0.4 7.6 L 2.1 7.3 C 2.3 6.8 2.6 6.3 3 5.9 L 2.3 4.3 L 3.7 2.9 L 5.3 3.6 C 5.7 3.2 6.2 2.9 6.7 2.7 Z M 8 5.5 A 2.5 2.5 0 1 0 8 10.5 A 2.5 2.5 0 1 0 8 5.5 Z"/>
</svg>''',

    # Fixes Extension Manager 'Use Extensions' row!
    "puzzle-piece-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path fill="currentColor" class="ColorScheme-Text" d="M 6 2 C 6 2.5 6.5 3 7 3 C 7.5 3 8 2.5 8 2 C 8 1.5 7.5 1 7 1 C 6.5 1 6 1.5 6 2 Z M 5 3 L 5 5 L 3 5 C 2.5 5 2 5.5 2 6 C 2 6.5 2.5 7 3 7 C 3.5 7 4 6.5 4 6 L 4 5 L 5 5 L 5 8 C 5 8.55 5.45 9 6 9 L 7 9 L 7 10 C 7 10.5 7.5 11 8 11 C 8.5 11 9 10.5 9 10 L 9 9 L 11 9 C 11.55 9 12 8.55 12 8 L 12 6 C 12 5.5 12.5 5 13 5 C 13.5 5 14 5.5 14 6 C 14 6.5 13.5 7 13 7 L 13 8 C 13 9.66 11.66 11 10 11 L 10 13 C 10 13.55 9.55 14 9 14 L 5 14 C 3.9 14 3 13.1 3 12 L 3 10 C 2.45 10 2 9.55 2 9 L 2 5 C 2 3.9 2.9 3 4 3 Z"/>
</svg>''',

    # Fixes Nautilus Recent sidebar row!
    "recent-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="8,4.5 8,8 10.5,9.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>''',

    "folder-recent-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="8,4.5 8,8 10.5,9.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>''',

    # Fixes Nautilus partitions & drive rows!
    "drive-harddisk-root-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="3" width="12" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="11.5" cy="10.5" r="1" fill="currentColor"/>
  <line x1="4" y1="10.5" x2="8" y2="10.5" stroke="currentColor" stroke-width="1.2"/>
  <line x1="7" y1="4.5" x2="5" y2="8.5" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    "drive-partition-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="2" y="3" width="12" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="8" y1="3" x2="8" y2="13" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 1"/>
  <circle cx="5" cy="10.5" r="0.8" fill="currentColor"/>
  <circle cx="11" cy="10.5" r="0.8" fill="currentColor"/>
</svg>''',

    "drive-removable-media-usb-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <rect x="5" y="6" width="6" height="8" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <rect x="6" y="2" width="4" height="4" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="8" cy="10" r="1" fill="currentColor"/>
</svg>''',

    "media-memory-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path d="M 4 2 L 10 2 L 12 4 L 12 14 L 4 14 Z" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="6" y1="4" x2="6" y2="6" stroke="currentColor" stroke-width="1.2"/>
  <line x1="8" y1="4" x2="8" y2="6" stroke="currentColor" stroke-width="1.2"/>
  <line x1="10" y1="5" x2="10" y2="6" stroke="currentColor" stroke-width="1.2"/>
</svg>''',

    "server-database-symbolic": '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <ellipse cx="8" cy="4" rx="5" ry="2" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <path d="M 3 4 L 3 8 C 3 9.1 5.2 10 8 10 C 10.8 10 13 9.1 13 8 L 13 4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <path d="M 3 8 L 3 12 C 3 13.1 5.2 14 8 14 C 10.8 14 13 13.1 13 12 L 13 8" fill="none" stroke="currentColor" stroke-width="1.5"/>
</svg>''',
}

# =========================================================================
# Application Icons (GNOME Files/Nautilus, Terminal, Settings, Editor, Calc)
# =========================================================================

APP_ICONS = {
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

    "utilities-terminal": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="6" y="8" width="52" height="48" rx="8" fill="#0B1317" stroke="#2C3E44" stroke-width="1.5"/>
<rect x="6" y="8" width="52" height="12" rx="8" fill="#16222A"/>
<circle cx="13" cy="14" r="2.5" fill="#E5737F"/>
<circle cx="20" cy="14" r="2.5" fill="#E5B580"/>
<circle cx="27" cy="14" r="2.5" fill="#3DD68C"/>
<path d="M 16 28 L 24 34 L 16 40" stroke="#8FB8A6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="28" y1="42" x2="42" y2="42" stroke="#3DD68C" stroke-width="3" stroke-linecap="round"/>
</svg>''',

    "preferences-system": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="24" fill="#16222A" stroke="#2C3E44" stroke-width="1.5"/>
<circle cx="32" cy="32" r="15" fill="#1D3238" stroke="#8FB8A6" stroke-width="3"/>
<circle cx="32" cy="32" r="6" fill="#8FB8A6"/>
<rect x="30" y="10" width="4" height="8" rx="2" fill="#8FB8A6"/>
<rect x="30" y="46" width="4" height="8" rx="2" fill="#8FB8A6"/>
<rect x="10" y="30" width="8" height="4" rx="2" fill="#8FB8A6"/>
<rect x="46" y="30" width="8" height="4" rx="2" fill="#8FB8A6"/>
</svg>''',

    "accessories-text-editor": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="12" y="8" width="38" height="48" rx="6" fill="#16222A" stroke="#2C3E44" stroke-width="1.5"/>
<rect x="12" y="8" width="38" height="10" rx="6" fill="#8FB8A6"/>
<line x1="18" y1="26" x2="42" y2="26" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<line x1="18" y1="33" x2="42" y2="33" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<line x1="18" y1="40" x2="34" y2="40" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<polygon points="42,44 48,38 48,50" fill="#3DD68C"/>
</svg>''',

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

    # 6. Google Chrome
    "google-chrome": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="26" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<circle cx="32" cy="32" r="11" fill="#1D3238" stroke="#8FB8A6" stroke-width="3"/>
<circle cx="32" cy="32" r="5" fill="#3DD68C"/>
<path d="M 32 6 C 39.5 6 46.2 9.2 50.8 14.5 L 37.5 37.5" stroke="#E5737F" stroke-width="3" stroke-linecap="round"/>
<path d="M 50.8 14.5 C 55.2 19.5 58 26.2 58 33.5 L 26.5 33.5" stroke="#7FC8A0" stroke-width="3" stroke-linecap="round"/>
<path d="M 26.5 33.5 L 13.2 51.5 C 8.6 46.5 6 39.7 6 32" stroke="#E5B580" stroke-width="3" stroke-linecap="round"/>
</svg>''',

    # 7. Discord
    "discord": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="14" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<path d="M 44 20 C 41.5 18.8 38.8 18 36 17.5 C 35.6 18.2 35.1 19.2 34.8 20 C 31.8 19.6 28.8 19.6 25.8 20 C 25.5 19.2 25 18.2 24.6 17.5 C 21.8 18 19.1 18.8 16.6 20 C 12 26.8 10.8 33.5 11.4 40 C 14.5 42.3 17.4 43.7 20.3 44.6 C 21 43.6 21.6 42.6 22.2 41.5 C 21.1 41.1 20.1 40.5 19.2 39.8 C 19.5 39.6 19.7 39.4 20 39.2 C 25.5 41.8 31.5 41.8 37 39.2 C 37.3 39.4 37.5 39.6 37.8 39.8 C 36.9 40.5 35.9 41.1 34.8 41.5 C 35.4 42.6 36 43.6 36.7 44.6 C 39.6 43.7 42.5 42.3 45.6 40 C 46.3 32.5 44.5 25.8 44 20 Z M 23.5 35 A 3.5 3.5 0 1 1 23.5 28 A 3.5 3.5 0 0 1 23.5 35 Z M 37.5 35 A 3.5 3.5 0 1 1 37.5 28 A 3.5 3.5 0 0 1 37.5 35 Z" fill="#8FB8A6"/>
</svg>''',

    # 8. Spotify
    "spotify": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="32" cy="32" r="26" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<circle cx="32" cy="32" r="23" fill="#0D1A1F"/>
<path d="M 19 24.5 C 27.5 22 37.5 23 45 27" stroke="#3DD68C" stroke-width="4" stroke-linecap="round"/>
<path d="M 21 32 C 28 30 36 31 43 35" stroke="#3DD68C" stroke-width="3.5" stroke-linecap="round"/>
<path d="M 23 39.5 C 28.5 38 34.5 39 40.5 42.5" stroke="#8FB8A6" stroke-width="3" stroke-linecap="round"/>
</svg>''',

    # 9. VS Code
    "code": '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="8" y="8" width="48" height="48" rx="12" fill="#14262C" stroke="#2E555F" stroke-width="2"/>
<path d="M 45 13 L 34 23 L 25 15 L 20 18 L 30 27 L 20 36 L 25 39 L 34 31 L 45 41 Z" fill="#8FB8A6"/>
<path d="M 45 13 L 34 23 L 45 33 Z" fill="#3DD68C"/>
</svg>''',
}

APP_ALIASES = {
    "system-file-manager": "org.gnome.Nautilus",
    "nautilus": "org.gnome.Nautilus",
    "file-manager": "org.gnome.Nautilus",
    "org.gnome.Terminal": "utilities-terminal",
    "org.gnome.Settings": "preferences-system",
    "org.gnome.TextEditor": "accessories-text-editor",
    "text-editor": "accessories-text-editor",
    "accessories-calculator": "org.gnome.Calculator",
    "calculator": "org.gnome.Calculator",
    "google-chrome-stable": "google-chrome",
    "chromium": "google-chrome",
    "com.discordapp.Discord": "discord",
    "discord-canary": "discord",
    "spotify-client": "spotify",
    "com.spotify.Client": "spotify",
    "visual-studio-code": "code",
    "com.visualstudio.code": "code",
    "vscode": "code",
}

# =========================================================================
# MIME Type Document Icons (Clean botanical file-type suite for Nautilus)
# =========================================================================

MIME_DOC_BASE = '''<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="docGrad" x1="32" y1="8" x2="32" y2="56" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#1A2B33"/>
    <stop offset="100%" stop-color="#101D22"/>
  </linearGradient>
</defs>
<path d="M 14 10 C 14 7.5 16 6 18.5 6 L 39 6 L 50 17 L 50 54 C 50 56.5 48 58 45.5 58 L 18.5 58 C 16 58 14 56.5 14 54 Z" fill="url(#docGrad)" stroke="#2C4852" stroke-width="1.5"/>
<path d="M 39 6 L 39 17 L 50 17 Z" fill="#243C45"/>
'''

MIME_ICONS = {
    "text-x-generic": MIME_DOC_BASE + '''
<line x1="22" y1="26" x2="42" y2="26" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<line x1="22" y1="33" x2="42" y2="33" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<line x1="22" y1="40" x2="34" y2="40" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<line x1="22" y1="47" x2="38" y2="47" stroke="#3DD68C" stroke-width="2" stroke-linecap="round"/>
''' + SVG_FOOTER,

    "text-x-script": MIME_DOC_BASE + '''
<path d="M 22 28 L 28 34 L 22 40" stroke="#3DD68C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<line x1="31" y1="40" x2="41" y2="40" stroke="#8FB8A6" stroke-width="2.5" stroke-linecap="round"/>
<line x1="22" y1="47" x2="36" y2="47" stroke="#2C4852" stroke-width="2" stroke-linecap="round"/>
''' + SVG_FOOTER,

    "application-x-executable": MIME_DOC_BASE + '''
<polygon points="28,26 40,34 28,42" fill="#3DD68C"/>
<line x1="22" y1="48" x2="42" y2="48" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
''' + SVG_FOOTER,

    "application-x-archive": MIME_DOC_BASE + '''
<line x1="32" y1="22" x2="32" y2="48" stroke="#8FB8A6" stroke-width="3" stroke-dasharray="2 3"/>
<rect x="29" y="32" width="6" height="8" rx="1.5" fill="#3DD68C"/>
''' + SVG_FOOTER,

    "audio-x-generic": MIME_DOC_BASE + '''
<circle cx="26" cy="42" r="3.5" fill="#8FB8A6"/>
<circle cx="38" cy="38" r="3.5" fill="#8FB8A6"/>
<path d="M 29.5 42 L 29.5 28 L 41.5 25 L 41.5 38" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
<polygon points="29.5,28 41.5,25 41.5,29 29.5,32" fill="#3DD68C"/>
''' + SVG_FOOTER,

    "video-x-generic": MIME_DOC_BASE + '''
<rect x="22" y="28" width="16" height="14" rx="2" fill="#8FB8A6"/>
<polygon points="38,31 44,27 44,43 38,39" fill="#8FB8A6"/>
<polygon points="27,31 33,35 27,39" fill="#101D22"/>
''' + SVG_FOOTER,

    "image-x-generic": MIME_DOC_BASE + '''
<rect x="21" y="27" width="22" height="18" rx="2" stroke="#8FB8A6" stroke-width="1.5" fill="#13262D"/>
<circle cx="26" cy="32" r="2" fill="#3DD68C"/>
<polygon points="23,43 28,37 33,41 36,38 41,43" fill="#8FB8A6"/>
''' + SVG_FOOTER,

    "application-pdf": MIME_DOC_BASE + '''
<rect x="20" y="26" width="24" height="14" rx="3" fill="#E5737F"/>
<text x="32" y="36.5" font-family="sans-serif" font-weight="bold" font-size="8" fill="#FFFFFF" text-anchor="middle">PDF</text>
<line x1="22" y1="46" x2="42" y2="46" stroke="#8FB8A6" stroke-width="2" stroke-linecap="round"/>
''' + SVG_FOOTER,
}

INDEX_THEME = """[Icon Theme]
Name=MT-Verdant-Icons
Comment=Botanical Canopy high-definition dark green icon suite for MT Verdant Nocturne
Inherits=Papirus-Dark,Adwaita,hicolor
Directories=scalable/places,scalable/apps,scalable/status,scalable/devices,scalable/actions,scalable/categories,scalable/mimetypes,32x32/places,32x32/apps,32x32/mimetypes,48x48/places,48x48/apps,48x48/mimetypes,64x64/places,64x64/apps,64x64/mimetypes,128x128/places,128x128/apps,128x128/mimetypes

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
Size=16
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

[scalable/mimetypes]
Size=64
MinSize=16
MaxSize=512
Context=MimeTypes
Type=Scalable

[32x32/places]
Size=32
Context=Places
Type=Fixed

[32x32/apps]
Size=32
Context=Applications
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
        (scalable_dir / f"{alias}.svg").symlink_to(f"{target}.svg")
        for size in [32, 48, 64, 128]:
            size_dir = OUT_DIR / f"{size}x{size}" / "apps"
            (size_dir / f"{alias}.png").symlink_to(f"{target}.png")

def build_symbolic() -> None:
    # Build symbolic wireframe icons for sidebar navigation, settings, and devices.
    status_dir = OUT_DIR / "scalable" / "status"
    places_dir = OUT_DIR / "scalable" / "places"
    devices_dir = OUT_DIR / "scalable" / "devices"
    actions_dir = OUT_DIR / "scalable" / "actions"
    categories_dir = OUT_DIR / "scalable" / "categories"
    
    for d in [status_dir, places_dir, devices_dir, actions_dir, categories_dir]:
        d.mkdir(parents=True, exist_ok=True)

    for name, svg_content in SYMBOLIC_ICONS.items():
        (status_dir / f"{name}.svg").write_text(svg_content)
        
        # Symlink to places
        if "folder" in name or "network" in name or "home" in name or "trash" in name or "recent" in name:
            p_dst = places_dir / f"{name}.svg"
            if not p_dst.exists():
                p_dst.symlink_to(f"../status/{name}.svg")
                
        # Symlink to devices
        if "drive" in name or "media" in name or "server" in name:
            d_dst = devices_dir / f"{name}.svg"
            if not d_dst.exists():
                d_dst.symlink_to(f"../status/{name}.svg")
                
        # Symlink to actions & categories
        if "setting" in name or "puzzle" in name or "system" in name:
            a_dst = actions_dir / f"{name}.svg"
            if not a_dst.exists():
                a_dst.symlink_to(f"../status/{name}.svg")
            c_dst = categories_dir / f"{name}.svg"
            if not c_dst.exists():
                c_dst.symlink_to(f"../status/{name}.svg")

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

    print("Building App Icons (Nautilus, Terminal, Settings)...")
    build_apps()

    print("Building Symbolic Icons (Fixing Network & Sidebar)...")
    build_symbolic()

    print("Building MIME Type Icons...")
    build_mimetypes()

    print(f"\nMT-Verdant-Icons suite successfully assembled in {OUT_DIR}")

if __name__ == "__main__":
    main()
