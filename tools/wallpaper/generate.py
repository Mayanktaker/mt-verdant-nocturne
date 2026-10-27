# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Procedural 4K wallpaper suite generator for MT Verdant Nocturne.
# Deterministic: pinned seeds, colors derived from palette/tokens.json.
# Generates 4 distinct 4K artworks: Canopy, Aurora, Flora, River.

import argparse
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())
COLOR = TOKENS["color"]
WIDTH, HEIGHT = 3840, 2160
FOLIAGE_TOP_LIMIT = 0.22


def hex_to_rgb(hex_color: str, alpha: int = 255) -> tuple:
    # Convert #RRGGBB plus alpha into an RGBA tuple.
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return (r, g, b, alpha)


def radial_glow(size: tuple, center: tuple, radius: float, rgb: tuple, max_alpha: int) -> Image.Image:
    # Soft additive radial light as an RGBA layer.
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2)
    falloff = np.clip(1.0 - dist / radius, 0.0, 1.0) ** 2.2
    alpha = (falloff * max_alpha).astype(np.uint8)
    layer = np.zeros((h, w, 4), dtype=np.uint8)
    layer[..., 0], layer[..., 1], layer[..., 2] = rgb
    layer[..., 3] = alpha
    return Image.fromarray(layer, "RGBA")


def vignette(intensity: int = 90) -> Image.Image:
    # Edge darkening to settle the composition and lift panel legibility.
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    dist = np.sqrt(((xx - WIDTH / 2) / (WIDTH / 2)) ** 2 + ((yy - HEIGHT / 2) / (HEIGHT / 2)) ** 2)
    alpha = (np.clip(dist - 0.55, 0.0, 1.0) * intensity).astype(np.uint8)
    layer = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    layer[..., 3] = alpha
    return Image.fromarray(layer, "RGBA")


def add_grain(image: Image.Image, seed: int = 20261027) -> Image.Image:
    # Subtle film grain so flat gradients don't band.
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, 2.2, (HEIGHT, WIDTH, 1)).repeat(3, axis=2)
    data = np.clip(np.asarray(image, dtype=float) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(data, "RGB")


# =========================================================================
# Wallpaper 1: Botanical Canopy (Midnight Fern)
# =========================================================================

def draw_fern(draw: ImageDraw.ImageDraw, base: tuple, angle: float, length: float, curve: float, color: tuple, leaflets: int) -> None:
    # One arcing fern frond with tapering leaflets along its tangent.
    tip = (base[0] + length * math.sin(angle), base[1] - length * math.cos(angle))
    ctrl = (base[0] + length * 0.55 * math.sin(angle + curve), base[1] - length * 0.55 * math.cos(angle + curve))
    steps = 40
    prev = base
    for i in range(1, steps + 1):
        u = i / steps
        p = (
            (1 - u) ** 2 * base[0] + 2 * (1 - u) * u * ctrl[0] + u**2 * tip[0],
            (1 - u) ** 2 * base[1] + 2 * (1 - u) * u * ctrl[1] + u**2 * tip[1],
        )
        draw.line([prev, p], fill=color, width=max(2, int(6 * (1 - u)) + 2))
        prev = p
        if i % max(1, steps // leaflets) == 0 and p[1] > HEIGHT * FOLIAGE_TOP_LIMIT:
            tangent = math.atan2(p[0] - ctrl[0], ctrl[1] - p[1])
            size = length * 0.16 * (1 - u) + length * 0.02
            for side in (-1, 1):
                la = tangent + side * math.radians(52)
                end = (p[0] + size * math.sin(la), p[1] - size * math.cos(la))
                draw.polygon([p, (p[0] + size * 0.32 * math.sin(la + 1.2), p[1] - size * 0.32 * math.cos(la + 1.2)), end,
                              (p[0] + size * 0.32 * math.sin(la - 1.2), p[1] - size * 0.32 * math.cos(la - 1.2))], fill=color)


def draw_leaf(draw: ImageDraw.ImageDraw, base: tuple, angle: float, length: float, width: float, color: tuple, rib: tuple) -> None:
    # One simple pointed leaf built from mirrored quadratic edges plus a midrib.
    if base[1] < HEIGHT * FOLIAGE_TOP_LIMIT + length * 0.2:
        return
    tip = (base[0] + length * math.sin(angle), base[1] - length * math.cos(angle))
    nx, ny = math.cos(angle), math.sin(angle)
    left, right = [], []
    for i in range(13):
        u = i / 12
        w = width * math.sin(math.pi * min(1.0, u * 1.25)) ** 0.9
        px = base[0] * (1 - u) + tip[0] * u
        py = base[1] * (1 - u) + tip[1] * u
        left.append((px + nx * w, py + ny * w))
        right.append((px - nx * w, py - ny * w))
    draw.polygon(left + right[::-1], fill=color)
    draw.line([base, tip], fill=rib, width=3)


def draw_blossom(draw: ImageDraw.ImageDraw, center: tuple, size: float, petal: tuple, core: tuple) -> None:
    # Five-petal blossom with a soft core.
    for k in range(5):
        a = math.radians(72 * k + random.uniform(-8, 8))
        petal_tip = (center[0] + size * math.sin(a), center[1] - size * math.cos(a))
        side_a = (center[0] + size * 0.45 * math.sin(a + 1.5), center[1] - size * 0.45 * math.cos(a + 1.5))
        side_b = (center[0] + size * 0.45 * math.sin(a - 1.5), center[1] - size * 0.45 * math.cos(a - 1.5))
        draw.polygon([center, side_a, petal_tip, side_b], fill=petal)
    draw.ellipse([center[0] - size * 0.16, center[1] - size * 0.16, center[0] + size * 0.16, center[1] + size * 0.16], fill=core)


def generate_canopy(seed: int = 20261027) -> Image.Image:
    # Compose Wallpaper 1: Botanical Canopy.
    random.seed(seed)
    top = np.array(hex_to_rgb(COLOR["bg"]["base_darker"])[:3], dtype=float)
    bottom = np.array((13, 26, 24), dtype=float)
    t = np.linspace(0.0, 1.0, HEIGHT)[:, None, None]
    rows = top * (1 - t) + bottom * t
    canvas = Image.fromarray(np.repeat(rows, WIDTH, axis=1).astype(np.uint8), "RGB").convert("RGBA")

    # Moonlight glow
    canvas.alpha_composite(radial_glow((WIDTH, HEIGHT), (WIDTH * 0.78, HEIGHT * 0.14), WIDTH * 0.42, hex_to_rgb(COLOR["accent"]["base"])[:3], 26))

    # Foliage layers
    def f_layer(color: tuple, rib: tuple, blur: float, seed_offset: int) -> Image.Image:
        layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        rng = random.Random(seed + seed_offset)
        for base_x, base_y, angle, length in [
            (WIDTH * 0.02, HEIGHT * 1.02, 0.35, HEIGHT * 0.62), (WIDTH * 0.08, HEIGHT * 1.05, 0.55, HEIGHT * 0.5),
            (WIDTH * 0.97, HEIGHT * 1.03, -0.4, HEIGHT * 0.66), (WIDTH * 0.88, HEIGHT * 1.06, -0.6, HEIGHT * 0.52),
            (WIDTH * 0.30, HEIGHT * 1.08, 0.22, HEIGHT * 0.34), (WIDTH * 0.68, HEIGHT * 1.08, -0.25, HEIGHT * 0.36),
        ]:
            draw_fern(d, (base_x, base_y), angle + rng.uniform(-0.05, 0.05), length, rng.uniform(-0.16, 0.16), color, 16)
        for _ in range(22):
            bx = rng.uniform(0.0, WIDTH)
            by = rng.uniform(HEIGHT * 0.66, HEIGHT * 1.04)
            draw_leaf(d, (bx, by), rng.uniform(-0.9, 0.9), rng.uniform(120, 340), rng.uniform(34, 80), color, rib)
        return layer.filter(ImageFilter.GaussianBlur(blur))

    # Bokeh
    bokeh = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bokeh)
    brng = random.Random(seed + 7)
    for _ in range(46):
        cx, cy = brng.uniform(0, WIDTH), brng.uniform(HEIGHT * 0.28, HEIGHT)
        r = brng.uniform(18, 95)
        bd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=brng.choice([hex_to_rgb(COLOR["accent"]["base"], 26), hex_to_rgb("#49686A", 22)]))
    bokeh = bokeh.filter(ImageFilter.GaussianBlur(14))

    # Blossoms
    blossoms = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bld = ImageDraw.Draw(blossoms)
    blrng = random.Random(seed + 13)
    petal = hex_to_rgb(COLOR["status"]["petal_decorative"], 205)
    core = hex_to_rgb(COLOR["text"]["primary"], 120)
    for fx, fy in [(0.14, 0.80), (0.22, 0.92), (0.10, 0.65), (0.84, 0.78), (0.92, 0.88), (0.78, 0.93), (0.30, 0.86), (0.65, 0.90), (0.47, 0.95)]:
        jitter = (blrng.uniform(-0.02, 0.02), blrng.uniform(-0.03, 0.03))
        draw_blossom(bld, (WIDTH * (fx + jitter[0]), HEIGHT * (fy + jitter[1])), blrng.uniform(34, 62), petal, core)
    blossoms = blossoms.filter(ImageFilter.GaussianBlur(1.2))

    canvas.alpha_composite(f_layer(hex_to_rgb("#17262B", 235), hex_to_rgb("#1B2E33", 235), 7, 0))
    canvas.alpha_composite(bokeh)
    canvas.alpha_composite(f_layer(hex_to_rgb("#121E1B", 245), hex_to_rgb("#16241F", 245), 3, 1))
    canvas.alpha_composite(f_layer(hex_to_rgb("#0A1310", 255), hex_to_rgb("#0E1713", 255), 0, 2))
    canvas.alpha_composite(blossoms)
    canvas.alpha_composite(vignette(90))
    return add_grain(canvas.convert("RGB"), seed)


# =========================================================================
# Wallpaper 2: Verdant Aurora (Nordic Pines)
# =========================================================================

def draw_pine_tree(draw: ImageDraw.ImageDraw, x: float, y: float, height: float, width: float, color: tuple) -> None:
    # Draw a stylized layered pine tree silhouette.
    layers = 5
    for i in range(layers):
        u = i / layers
        ly_top = y - height * (1 - u * 0.8)
        ly_bot = y - height * (1 - (u + 0.28) * 0.8)
        w = width * (u + 0.3)
        draw.polygon([(x, ly_top), (x - w / 2, ly_bot), (x + w / 2, ly_bot)], fill=color)
    draw.rectangle([(x - width * 0.08, y - height * 0.15), (x + width * 0.08, y)], fill=color)


def generate_aurora(seed: int = 20261028) -> Image.Image:
    # Compose Wallpaper 2: Verdant Aurora.
    random.seed(seed)
    rng = random.Random(seed)

    sky_top = np.array(hex_to_rgb(COLOR["bg"]["oled"])[:3], dtype=float)
    sky_bot = np.array((10, 22, 26), dtype=float)
    t = np.linspace(0.0, 1.0, HEIGHT)[:, None, None]
    rows = sky_top * (1 - t) + sky_bot * t
    canvas = Image.fromarray(np.repeat(rows, WIDTH, axis=1).astype(np.uint8), "RGB").convert("RGBA")

    # Starfield
    stars = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stars)
    for _ in range(180):
        sx = rng.uniform(0, WIDTH)
        sy = rng.uniform(0, HEIGHT * 0.65)
        sr = rng.uniform(1.0, 2.8)
        alpha = int(rng.uniform(70, 240))
        sd.ellipse([(sx - sr, sy - sr), (sx + sr, sy + sr)], fill=(233, 241, 236, alpha))
    canvas.alpha_composite(stars)

    # Aurora borealis glowing wave ribbons
    aurora = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ad = ImageDraw.Draw(aurora)

    # Emerald ribbon 1
    points1 = []
    for x in range(0, WIDTH + 40, 40):
        wave = math.sin(x * 0.0016) * 160 + math.cos(x * 0.003) * 90 + math.sin(x * 0.0008) * 120
        points1.append((x, HEIGHT * 0.38 + wave))
    for p in points1:
        ad.line([(p[0], p[1] - 180), (p[0], p[1] + 120)], fill=(61, 214, 140, 42), width=48)
        ad.line([(p[0], p[1] - 80), (p[0], p[1] + 40)], fill=(143, 184, 166, 68), width=32)

    # Sage ribbon 2
    points2 = []
    for x in range(0, WIDTH + 40, 40):
        wave = math.cos(x * 0.0018 + 1.2) * 140 + math.sin(x * 0.0035) * 80
        points2.append((x, HEIGHT * 0.26 + wave))
    for p in points2:
        ad.line([(p[0], p[1] - 140), (p[0], p[1] + 80)], fill=(169, 205, 187, 36), width=40)

    aurora = aurora.filter(ImageFilter.GaussianBlur(32))
    canvas.alpha_composite(aurora)

    # Pine tree forest silhouettes
    ridge1 = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    rd1 = ImageDraw.Draw(ridge1)
    base1 = HEIGHT * 0.88
    for x in range(0, WIDTH + 30, 24):
        h = rng.uniform(HEIGHT * 0.14, HEIGHT * 0.22)
        draw_pine_tree(rd1, x + rng.uniform(-6, 6), base1, h, h * 0.32, (18, 34, 38, 160))
    canvas.alpha_composite(ridge1.filter(ImageFilter.GaussianBlur(4)))

    ridge2 = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    rd2 = ImageDraw.Draw(ridge2)
    base2 = HEIGHT * 0.94
    for x in range(0, WIDTH + 40, 36):
        h = rng.uniform(HEIGHT * 0.20, HEIGHT * 0.32)
        draw_pine_tree(rd2, x + rng.uniform(-10, 10), base2, h, h * 0.35, (12, 24, 28, 220))
    canvas.alpha_composite(ridge2.filter(ImageFilter.GaussianBlur(1.5)))

    ridge3 = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    rd3 = ImageDraw.Draw(ridge3)
    base3 = HEIGHT * 1.02
    for x in range(-20, WIDTH + 60, 60):
        h = rng.uniform(HEIGHT * 0.28, HEIGHT * 0.44)
        draw_pine_tree(rd3, x + rng.uniform(-15, 15), base3, h, h * 0.36, (5, 10, 12, 255))
    canvas.alpha_composite(ridge3)

    canvas.alpha_composite(vignette(80))
    return add_grain(canvas.convert("RGB"), seed)


# =========================================================================
# Wallpaper 3: Zen Flora (Geometric Leaf Contour)
# =========================================================================

def generate_flora(seed: int = 20261029) -> Image.Image:
    # Compose Wallpaper 3: Zen Flora (Bauhaus / Minimal Architectural Leaf).
    top = np.array(hex_to_rgb(COLOR["bg"]["base_darker"])[:3], dtype=float)
    bottom = np.array(hex_to_rgb(COLOR["bg"]["tile"])[:3], dtype=float)
    t = np.linspace(0.0, 1.0, HEIGHT)[:, None, None]
    rows = top * (1 - t) + bottom * t
    canvas = Image.fromarray(np.repeat(rows, WIDTH, axis=1).astype(np.uint8), "RGB").convert("RGBA")

    # Ambient organic halo
    canvas.alpha_composite(radial_glow((WIDTH, HEIGHT), (WIDTH * 0.65, HEIGHT * 0.55), WIDTH * 0.45, hex_to_rgb(COLOR["accent"]["base"])[:3], 35))

    shapes = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shapes)

    cx, cy = WIDTH * 0.58, HEIGHT * 0.62
    num_leaves = 6
    for i in range(num_leaves):
        scale = 1.0 - i * 0.12
        angle = math.radians(-32 + i * 14)
        length = HEIGHT * 0.75 * scale
        width = WIDTH * 0.22 * scale

        tip = (cx + length * math.sin(angle), cy - length * math.cos(angle))
        left_ctrl = (cx + width * math.cos(angle) + length * 0.4 * math.sin(angle), cy + width * math.sin(angle) - length * 0.4 * math.cos(angle))
        right_ctrl = (cx - width * math.cos(angle) + length * 0.4 * math.sin(angle), cy - width * math.sin(angle) - length * 0.4 * math.cos(angle))

        poly = [(cx, cy)]
        for step in range(25):
            u = step / 24
            px = (1 - u) ** 2 * cx + 2 * (1 - u) * u * left_ctrl[0] + u**2 * tip[0]
            py = (1 - u) ** 2 * cy + 2 * (1 - u) * u * left_ctrl[1] + u**2 * tip[1]
            poly.append((px, py))
        for step in range(25, -1, -1):
            u = step / 24
            px = (1 - u) ** 2 * cx + 2 * (1 - u) * u * right_ctrl[0] + u**2 * tip[0]
            py = (1 - u) ** 2 * cy + 2 * (1 - u) * u * right_ctrl[1] + u**2 * tip[1]
            poly.append((px, py))

        fill_alpha = 14 + i * 8
        sd.polygon(poly, fill=(29, 50, 56, fill_alpha))
        stroke_col = hex_to_rgb(COLOR["accent"]["base"], 140 - i * 16)
        sd.line(poly, fill=stroke_col, width=max(2, 6 - i))
        sd.line([(cx, cy), tip], fill=hex_to_rgb(COLOR["accent"]["strong"], 160 - i * 20), width=3)

    canvas.alpha_composite(shapes)
    canvas.alpha_composite(vignette(95))
    return add_grain(canvas.convert("RGB"), seed)


# =========================================================================
# Wallpaper 4: Obsidian River (Topographic Mineral Flow)
# =========================================================================

def generate_river(seed: int = 20261030) -> Image.Image:
    # Compose Wallpaper 4: Obsidian River (Topographic flow).
    random.seed(seed)
    top = np.array(hex_to_rgb(COLOR["bg"]["oled"])[:3], dtype=float)
    bottom = np.array((14, 25, 28), dtype=float)
    t = np.linspace(0.0, 1.0, HEIGHT)[:, None, None]
    rows = top * (1 - t) + bottom * t
    canvas = Image.fromarray(np.repeat(rows, WIDTH, axis=1).astype(np.uint8), "RGB").convert("RGBA")

    canvas.alpha_composite(radial_glow((WIDTH, HEIGHT), (WIDTH * 0.45, HEIGHT * 0.65), WIDTH * 0.5, (45, 82, 88), 38))

    contours = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cd = ImageDraw.Draw(contours)

    num_isolines = 28
    glow_indices = {6, 14, 21}
    for idx in range(num_isolines):
        base_y = HEIGHT * 0.15 + (idx / num_isolines) * (HEIGHT * 0.9)
        phase = idx * 0.32
        freq = 0.0012 + (idx % 3) * 0.0003
        amp = 90 + math.sin(idx * 0.4) * 50

        points = []
        for x in range(0, WIDTH + 30, 20):
            y = base_y + math.sin(x * freq + phase) * amp + math.cos(x * 0.0006) * 40
            points.append((x, y))

        is_glow = idx in glow_indices
        color = hex_to_rgb(COLOR["accent"]["base"], 180) if is_glow else hex_to_rgb(COLOR["border"]["default"], 85)
        width = 4 if is_glow else 2
        cd.line(points, fill=color, width=width)

    glow_pass = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gpd = ImageDraw.Draw(glow_pass)
    for idx in glow_indices:
        base_y = HEIGHT * 0.15 + (idx / num_isolines) * (HEIGHT * 0.9)
        phase = idx * 0.32
        freq = 0.0012 + (idx % 3) * 0.0003
        amp = 90 + math.sin(idx * 0.4) * 50
        pts = [(x, base_y + math.sin(x * freq + phase) * amp + math.cos(x * 0.0006) * 40) for x in range(0, WIDTH + 30, 20)]
        gpd.line(pts, fill=hex_to_rgb(COLOR["accent"]["base"], 90), width=16)
    glow_pass = glow_pass.filter(ImageFilter.GaussianBlur(12))

    canvas.alpha_composite(glow_pass)
    canvas.alpha_composite(contours)
    canvas.alpha_composite(vignette(85))
    return add_grain(canvas.convert("RGB"), seed)


# =========================================================================
# CLI and Output orchestration
# =========================================================================

WALLPAPER_META = {
    "1": ("mt-verdant-canopy", "Botanical Canopy (Midnight Fern)", generate_canopy),
    "2": ("mt-verdant-aurora", "Verdant Aurora (Nordic Pines)", generate_aurora),
    "3": ("mt-verdant-flora", "Zen Flora (Geometric Contour)", generate_flora),
    "4": ("mt-verdant-river", "Obsidian River (Mineral Flow)", generate_river),
}


def dominant_palette(image: Image.Image, count: int = 8) -> list:
    # Report dominant colors so docs can show the sampled render palette.
    small = image.convert("RGB").resize((160, 90))
    quantized = small.quantize(colors=count, method=Image.Quantize.MEDIANCUT).convert("RGB")
    counts = sorted(quantized.getcolors(160 * 90) or [], reverse=True)
    return [f"#{r:02x}{g:02x}{b:02x}" for _, (r, g, b) in counts]


def main() -> None:
    # Generate requested wallpapers (1-4 or all).
    parser = argparse.ArgumentParser(description="Generate 4K procedural wallpapers for MT Verdant Nocturne")
    parser.add_argument("--which", default="all", choices=["1", "2", "3", "4", "all"], help="Which wallpaper to generate")
    args = parser.parse_args()

    dist = REPO_ROOT / "wallpaper" / "dist"
    preview = REPO_ROOT / "wallpaper" / "preview"
    dist.mkdir(parents=True, exist_ok=True)
    preview.mkdir(parents=True, exist_ok=True)

    targets = list(WALLPAPER_META.keys()) if args.which == "all" else [args.which]
    summaries = {}

    for key in targets:
        name_prefix, title, generator_fn = WALLPAPER_META[key]
        print(f"Generating Wallpaper {key}: {title} (4K 3840x2160)...")
        img = generator_fn()

        png_path = dist / f"{name_prefix}-3840x2160.png"
        img.save(png_path, optimize=True)

        jpg_path = preview / f"{name_prefix}-1920x1080.jpg"
        img.resize((1920, 1080), Image.LANCZOS).save(jpg_path, quality=88, optimize=True)

        if key == "1":
            compat_png = dist / "mt-verdant-nocturne-3840x2160.png"
            compat_jpg = preview / "mt-verdant-nocturne-1920x1080.jpg"
            img.save(compat_png, optimize=True)
            img.resize((1920, 1080), Image.LANCZOS).save(compat_jpg, quality=88, optimize=True)

        summaries[key] = {
            "title": title,
            "file": f"{name_prefix}-3840x2160.png",
            "preview": f"{name_prefix}-1920x1080.jpg",
            "dominant": dominant_palette(img),
        }
        print(f"  ✓ Saved 4K: {png_path.name}")
        print(f"  ✓ Saved Preview: {jpg_path.name}")

    summary_file = dist / "palette-summary.json"
    summary_file.write_text(json.dumps(summaries, indent=2))
    print(f"\nAll wallpapers generated successfully. Summary at {summary_file}")


if __name__ == "__main__":
    main()
