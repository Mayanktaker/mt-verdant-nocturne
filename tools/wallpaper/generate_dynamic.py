# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Generates GNOME timed day/night transition XML and GNOME background properties.

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DIST_DIR = REPO_ROOT / "wallpaper" / "dist"
DIST_LIGHT_DIR = DIST_DIR / "light"


def build_timed_xml(wallpaper_base_dir: str) -> str:
    # 24-hour timed transition XML between morning mist dawn and midnight fern.
    dawn_path = f"{wallpaper_base_dir}/light/mt-verdant-canopy-dawn-3840x2160.png"
    night_path = f"{wallpaper_base_dir}/mt-verdant-canopy-3840x2160.png"

    return f"""<?xml version="1.0"?>
<!DOCTYPE background SYSTEM "file:///usr/share/gnome-background-properties/gnome-wp-list.dtd">
<!-- © Mayanktaker Computers & Web Development | https://mayanktaker.com -->
<!-- MT Verdant Nocturne 24-Hour Botanical Canopy Day/Night Cycle -->
<background>
  <starttime>
    <year>2026</year>
    <month>01</month>
    <day>01</day>
    <hour>07</hour>
    <minute>00</minute>
    <second>00</second>
  </starttime>
  <!-- Daytime: Botanical Canopy Dawn (7:00 AM - 6:00 PM, 11 hours) -->
  <static>
    <duration>39600.0</duration>
    <file>{dawn_path}</file>
  </static>
  <!-- Dusk transition into Midnight Fern (6:00 PM - 7:00 PM, 1 hour) -->
  <transition type="overlay">
    <duration>3600.0</duration>
    <from>{dawn_path}</from>
    <to>{night_path}</to>
  </transition>
  <!-- Nighttime: Botanical Canopy Midnight (7:00 PM - 6:00 AM, 11 hours) -->
  <static>
    <duration>39600.0</duration>
    <file>{night_path}</file>
  </static>
  <!-- Dawn transition into Morning Mist (6:00 AM - 7:00 AM, 1 hour) -->
  <transition type="overlay">
    <duration>3600.0</duration>
    <from>{night_path}</from>
    <to>{dawn_path}</to>
  </transition>
</background>
"""


def build_gnome_properties_xml(wallpaper_base_dir: str) -> str:
    # GNOME Settings background properties listing adaptive pairs and timed cycle.
    w_dir = wallpaper_base_dir
    return f"""<?xml version="1.0"?>
<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">
<!-- © Mayanktaker Computers & Web Development | https://mayanktaker.com -->
<wallpapers>
  <!-- Adaptive Light/Dark Pairs (GNOME 42+ automatic switch) -->
  <wallpaper deleted="false">
    <name>MT Verdant Canopy (Adaptive Day/Night)</name>
    <filename>{w_dir}/light/mt-verdant-canopy-dawn-3840x2160.png</filename>
    <filename-dark>{w_dir}/mt-verdant-canopy-3840x2160.png</filename-dark>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
  <wallpaper deleted="false">
    <name>MT Verdant Celestial Rift (Adaptive Light/Dark)</name>
    <filename>{w_dir}/light/mt-verdant-celestial-rift-3840x2160.png</filename>
    <filename-dark>{w_dir}/mt-verdant-aurora-3840x2160.png</filename-dark>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
  <wallpaper deleted="false">
    <name>MT Verdant Cosmic Dawn (Adaptive Light/Dark)</name>
    <filename>{w_dir}/light/mt-verdant-cosmic-dawn-3840x2160.png</filename>
    <filename-dark>{w_dir}/mt-verdant-flora-3840x2160.png</filename-dark>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
  <wallpaper deleted="false">
    <name>MT Verdant Botanical Horizon (Adaptive Light/Dark)</name>
    <filename>{w_dir}/light/mt-verdant-botanical-horizon-3840x2160.png</filename>
    <filename-dark>{w_dir}/mt-verdant-river-3840x2160.png</filename-dark>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>

  <!-- 24-Hour Timed Day/Night Cross-Fade -->
  <wallpaper deleted="false">
    <name>MT Verdant Canopy (24-Hour Timed Cycle)</name>
    <filename>{w_dir}/mt-verdant-timed.xml</filename>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>

  <!-- Individual Dark Artworks -->
  <wallpaper deleted="false">
    <name>MT Verdant Canopy (Midnight Fern)</name>
    <filename>{w_dir}/mt-verdant-canopy-3840x2160.png</filename>
    <options>zoom</options>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
  <wallpaper deleted="false">
    <name>MT Verdant Aurora (Nordic Pines)</name>
    <filename>{w_dir}/mt-verdant-aurora-3840x2160.png</filename>
    <options>zoom</options>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
  <wallpaper deleted="false">
    <name>MT Verdant Flora (Zen Contour)</name>
    <filename>{w_dir}/mt-verdant-flora-3840x2160.png</filename>
    <options>zoom</options>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
  <wallpaper deleted="false">
    <name>MT Verdant River (Obsidian Flow)</name>
    <filename>{w_dir}/mt-verdant-river-3840x2160.png</filename>
    <options>zoom</options>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>

  <!-- Individual Light Artworks -->
  <wallpaper deleted="false">
    <name>MT Verdant Canopy Dawn (Morning Mist)</name>
    <filename>{w_dir}/light/mt-verdant-canopy-dawn-3840x2160.png</filename>
    <options>zoom</options>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
  <wallpaper deleted="false">
    <name>MT Verdant Celestial Rift (Sage Cyan)</name>
    <filename>{w_dir}/light/mt-verdant-celestial-rift-3840x2160.png</filename>
    <options>zoom</options>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
  <wallpaper deleted="false">
    <name>MT Verdant Cosmic Dawn (Stellar Amber)</name>
    <filename>{w_dir}/light/mt-verdant-cosmic-dawn-3840x2160.png</filename>
    <options>zoom</options>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
  <wallpaper deleted="false">
    <name>MT Verdant Botanical Horizon (Aurora Dawn)</name>
    <filename>{w_dir}/light/mt-verdant-botanical-horizon-3840x2160.png</filename>
    <options>zoom</options>
    <pcolor>#0F141B</pcolor>
    <scolor>#0F141B</scolor>
  </wallpaper>
</wallpapers>
"""


def main() -> None:
    # Writes template XML files in dist directory with replaceable tokens.
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    template_base = "@WALLPAPER_DIR@"

    timed_xml = build_timed_xml(template_base)
    (DIST_DIR / "mt-verdant-timed.xml.in").write_text(timed_xml)

    properties_xml = build_gnome_properties_xml(template_base)
    (DIST_DIR / "gnome-background-properties.xml.in").write_text(properties_xml)

    # Also write a local development version pointing to current repo's wallpaper/dist
    local_base = str(DIST_DIR.resolve())
    (DIST_DIR / "mt-verdant-timed.xml").write_text(build_timed_xml(local_base))
    (DIST_DIR / "gnome-background-properties.xml").write_text(build_gnome_properties_xml(local_base))
    print(f"Dynamic wallpaper XML templates generated in: {DIST_DIR}")


if __name__ == "__main__":
    main()
