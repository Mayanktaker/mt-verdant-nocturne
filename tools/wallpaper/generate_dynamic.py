# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Generates GNOME timed day/night transition XML and background properties
# for the unified JPEG wallpaper suite.

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())
DIST_DIR = REPO_ROOT / "wallpaper" / "dist"
BG = TOKENS["color"]["bg"]["base"]
FG = TOKENS["color"]["text"]["primary"]

DARK = [
    ("mt-verdant-canopy", "MT Verdant — Stillwater at Blue Hour"),
    ("mt-verdant-aurora", "MT Verdant — Verdant Aurora"),
    ("mt-verdant-flora", "MT Verdant — Moonlit Alpine Range"),
    ("mt-verdant-river", "MT Verdant — Mineral River"),
]
LIGHT = [
    ("mt-verdant-canopy-dawn", "MT Verdant — Sculpted Canopy"),
    ("mt-verdant-celestial-rift", "MT Verdant — Paper-Cut Sunrise"),
    ("mt-verdant-cosmic-dawn", "MT Verdant — Folded Celadon"),
    ("mt-verdant-botanical-horizon", "MT Verdant — Mist on the Water"),
]


def timed_xml(base: str) -> str:
    # 24-hour cross-fade between the dawn and night canopy renders.
    dawn = f"{base}/light/mt-verdant-canopy-dawn-3840x2160.jpg"
    night = f"{base}/mt-verdant-canopy-3840x2160.jpg"
    return f"""<?xml version="1.0"?>
<!DOCTYPE background SYSTEM "file:///usr/share/gnome-background-properties/gnome-wp-list.dtd">
<!-- © Mayanktaker Computers & Web Development | https://mayanktaker.com -->
<background>
  <starttime><year>2026</year><month>01</month><day>01</day><hour>07</hour><minute>00</minute><second>00</second></starttime>
  <static><duration>39600.0</duration><file>{dawn}</file></static>
  <transition type="overlay"><duration>3600.0</duration><from>{dawn}</from><to>{night}</to></transition>
  <static><duration>39600.0</duration><file>{night}</file></static>
  <transition type="overlay"><duration>3600.0</duration><from>{night}</from><to>{dawn}</to></transition>
</background>
"""


def properties_xml(base: str) -> str:
    # GNOME Settings entries: four adaptive pairs, the timed cycle, and each artwork.
    entries = []
    for (dark, dark_name), (light, light_name) in zip(DARK, LIGHT):
        entries.append(f"""  <wallpaper deleted="false">
    <name>{light_name.replace(' (', ' / ').replace(')', '')}</name>
    <filename>{base}/light/{light}-3840x2160.jpg</filename>
    <filename-dark>{base}/{dark}-3840x2160.jpg</filename-dark>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>{BG}</pcolor>
    <scolor>{BG}</scolor>
  </wallpaper>""")
    entries.append(f"""  <wallpaper deleted="false">
    <name>MT Verdant — Stillwater (24-Hour Timed Cycle)</name>
    <filename>{base}/mt-verdant-timed.xml</filename>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>{BG}</pcolor>
    <scolor>{BG}</scolor>
  </wallpaper>""")
    for name, title in DARK:
        entries.append(f"""  <wallpaper deleted="false">
    <name>{title}</name>
    <filename>{base}/{name}-3840x2160.jpg</filename>
    <options>zoom</options>
    <pcolor>{BG}</pcolor>
    <scolor>{BG}</scolor>
  </wallpaper>""")
    for name, title in LIGHT:
        entries.append(f"""  <wallpaper deleted="false">
    <name>{title}</name>
    <filename>{base}/light/{name}-3840x2160.jpg</filename>
    <options>zoom</options>
    <pcolor>{BG}</pcolor>
    <scolor>{BG}</scolor>
  </wallpaper>""")
    return f"""<?xml version="1.0"?>
<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">
<!-- © Mayanktaker Computers & Web Development | https://mayanktaker.com -->
<!-- foreground reference: {FG} -->
<wallpapers>
{chr(10).join(entries)}
</wallpapers>
"""


def main() -> None:
    # Write both placeholder templates and development copies.
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    for suffix, base in ((".xml.in", "@WALLPAPER_DIR@"), (".xml", str(DIST_DIR.resolve()))):
        (DIST_DIR / f"mt-verdant-timed{suffix}").write_text(timed_xml(base))
        (DIST_DIR / f"gnome-background-properties{suffix}").write_text(properties_xml(base))
    print(f"wallpaper XML written to {DIST_DIR}")


if __name__ == "__main__":
    main()
