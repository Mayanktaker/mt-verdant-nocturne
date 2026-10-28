# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Processes, enhances, and renders the 4K Light Suite wallpapers and 1080p previews.

import json
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "wallpaper" / "raw_light"
DIST_LIGHT_DIR = REPO_ROOT / "wallpaper" / "dist" / "light"
PREVIEW_LIGHT_DIR = REPO_ROOT / "wallpaper" / "preview" / "light"
WIDTH, HEIGHT = 3840, 2160
PREVIEW_W, PREVIEW_H = 1920, 1080

WALLPAPERS = [
    {
        "id": "1",
        "raw": "1-canopy-dawn.jpg",
        "title": "Botanical Canopy Dawn (Morning Mist)",
        "file": "mt-verdant-canopy-dawn-3840x2160.png",
        "preview": "mt-verdant-canopy-dawn-1920x1080.jpg",
    },
    {
        "id": "2",
        "raw": "2-celestial-rift.jpg",
        "title": "Luminous Sage Celestial Rift",
        "file": "mt-verdant-celestial-rift-3840x2160.png",
        "preview": "mt-verdant-celestial-rift-1920x1080.jpg",
    },
    {
        "id": "3",
        "raw": "3-cosmic-dawn.jpg",
        "title": "Cosmic Dawn (Stellar Amber & Emerald Cloud)",
        "file": "mt-verdant-cosmic-dawn-3840x2160.png",
        "preview": "mt-verdant-cosmic-dawn-1920x1080.jpg",
    },
    {
        "id": "4",
        "raw": "4-botanical-horizon.jpg",
        "title": "Celestial Botanical Horizon (Aurora Dawn)",
        "file": "mt-verdant-botanical-horizon-3840x2160.png",
        "preview": "mt-verdant-botanical-horizon-1920x1080.jpg",
    },
]


def add_subtle_grain(image: Image.Image, seed: int = 20261028) -> Image.Image:
    # Adds subtle noise to prevent 4K gradient banding.
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, 1.4, (HEIGHT, WIDTH, 1)).repeat(3, axis=2)
    data = np.clip(np.asarray(image, dtype=float) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(data, "RGB")


def extract_dominant_colors(image: Image.Image, count: int = 8) -> List[str]:
    # Samples top dominant hex colors from resized image.
    thumb = image.resize((150, 150), Image.Resampling.BILINEAR)
    colors = thumb.getcolors(maxcolors=22500)
    sorted_colors = sorted(colors, key=lambda c: c[0], reverse=True)
    hex_list = []
    for _, rgb in sorted_colors:
        h = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        if h not in hex_list:
            hex_list.append(h)
        if len(hex_list) >= count:
            break
    return hex_list


def process_wallpaper(entry: Dict[str, str]) -> Dict[str, object]:
    # Upscales raw image to 4K UHD, sharpens, adds grain, and generates preview.
    raw_path = RAW_DIR / entry["raw"]
    img = Image.open(raw_path).convert("RGB")

    # High quality upscale to 4K
    img_4k = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    img_4k = img_4k.filter(ImageFilter.UnsharpMask(radius=1.5, percent=115, threshold=3))
    img_4k = add_subtle_grain(img_4k, seed=int(entry["id"]) * 1000 + 42)

    # Save 4K PNG
    out_png = DIST_LIGHT_DIR / entry["file"]
    img_4k.save(out_png, format="PNG", optimize=True)

    # Save 1080p preview JPG
    preview_img = img_4k.resize((PREVIEW_W, PREVIEW_H), Image.Resampling.LANCZOS)
    out_preview = PREVIEW_LIGHT_DIR / entry["preview"]
    preview_img.save(out_preview, format="JPEG", quality=92, optimize=True)

    dominants = extract_dominant_colors(preview_img)
    return {
        "title": entry["title"],
        "file": entry["file"],
        "preview": entry["preview"],
        "dominant": dominants,
    }


def main() -> None:
    # Builds all light suite wallpapers and writes palette summary.
    DIST_LIGHT_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_LIGHT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {}
    for item in WALLPAPERS:
        print(f"Processing 4K: {item['title']}...")
        summary[item["id"]] = process_wallpaper(item)

    summary_file = DIST_LIGHT_DIR / "palette-summary.json"
    summary_file.write_text(json.dumps(summary, indent=2) + "\n")

    # Generate dynamic day/night cycle and GNOME properties XML
    try:
        from tools.wallpaper.generate_dynamic import main as generate_dynamic_xml
    except ModuleNotFoundError:
        import sys
        sys.path.insert(0, str(REPO_ROOT))
        from tools.wallpaper.generate_dynamic import main as generate_dynamic_xml
    generate_dynamic_xml()

    print(f"Done! Light suite generated at: {DIST_LIGHT_DIR}")


if __name__ == "__main__":
    main()
