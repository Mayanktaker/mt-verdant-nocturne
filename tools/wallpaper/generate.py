# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Unified procedural wallpaper suite for MT Verdant Nocturne.
# One art system, eight compositions: four night pieces and four dawn pieces.
# Deterministic seeds, colors from palette/tokens.json (art.dark / art.light).

import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageStat

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())
ART = TOKENS["art"]
WIDTH, HEIGHT = 3840, 2160
PREVIEW = (1920, 1080)
DIST = REPO_ROOT / "wallpaper" / "dist"
PREVIEW_DIR = REPO_ROOT / "wallpaper" / "preview"


def rgba(hex_color: str, alpha: int = 255) -> tuple:
    # Convert #RRGGBB plus alpha into an RGBA tuple.
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return (r, g, b, alpha)


def gradient(top: str, bottom: str, bias: float = 1.0) -> Image.Image:
    # Full-frame vertical gradient with a gamma bias for more sky at the top.
    top_rgb = np.array(rgba(top)[:3], dtype=float)
    bottom_rgb = np.array(rgba(bottom)[:3], dtype=float)
    t = np.linspace(0.0, 1.0, HEIGHT)[:, None, None] ** bias
    rows = top_rgb * (1 - t) + bottom_rgb * t
    return Image.fromarray(np.repeat(rows, WIDTH, axis=1).astype(np.uint8), "RGB").convert("RGBA")


def glow(center: tuple, radius: float, color: str, max_alpha: int, power: float = 2.2) -> Image.Image:
    # Soft additive radial light.
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    dist = np.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2)
    falloff = np.clip(1.0 - dist / radius, 0.0, 1.0) ** power
    layer = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    layer[..., 0], layer[..., 1], layer[..., 2] = rgba(color)[:3]
    layer[..., 3] = (falloff * max_alpha).astype(np.uint8)
    return Image.fromarray(layer, "RGBA")


def soft_blur(layer: Image.Image, radius: float) -> Image.Image:
    # Blur at half resolution to keep 4K generation fast.
    if radius <= 0:
        return layer
    small = layer.resize((WIDTH // 2, HEIGHT // 2), Image.Resampling.BILINEAR)
    small = small.filter(ImageFilter.GaussianBlur(radius / 2))
    return small.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)


def vignette(intensity: int = 70, color: str = "#000000", power: float = 1.0) -> Image.Image:
    # Edge shading (or lift) to settle the composition.
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    dist = np.sqrt(((xx - WIDTH / 2) / (WIDTH / 2)) ** 2 + ((yy - HEIGHT / 2) / (HEIGHT / 2)) ** 2)
    alpha = (np.clip(dist - 0.5, 0.0, 1.0) ** power * intensity).astype(np.uint8)
    layer = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    layer[..., 0], layer[..., 1], layer[..., 2] = rgba(color)[:3]
    layer[..., 3] = alpha
    return Image.fromarray(layer, "RGBA")


def grain(image: Image.Image, seed: int, amount: float = 0.7) -> Image.Image:
    # Subtle deterministic grain prevents 8-bit banding in the gradients.
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, amount, (HEIGHT, WIDTH, 1)).repeat(3, axis=2)
    data = np.clip(np.asarray(image.convert("RGB"), dtype=float) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(data, "RGB")


def draw_fern(draw, base, angle, length, curve, color, leaflets) -> None:
    # One arcing fern frond with tapering leaflets along its tangent.
    tip = (base[0] + length * math.sin(angle), base[1] - length * math.cos(angle))
    ctrl = (base[0] + length * 0.55 * math.sin(angle + curve), base[1] - length * 0.55 * math.cos(angle + curve))
    prev = base
    for i in range(1, 41):
        u = i / 40
        p = (
            (1 - u) ** 2 * base[0] + 2 * (1 - u) * u * ctrl[0] + u**2 * tip[0],
            (1 - u) ** 2 * base[1] + 2 * (1 - u) * u * ctrl[1] + u**2 * tip[1],
        )
        draw.line([prev, p], fill=color, width=max(2, int(6 * (1 - u)) + 2))
        prev = p
        if i % max(1, 40 // leaflets) == 0 and p[1] > HEIGHT * 0.18:
            tangent = math.atan2(p[0] - ctrl[0], ctrl[1] - p[1])
            size = length * 0.16 * (1 - u) + length * 0.02
            for side in (-1, 1):
                la = tangent + side * math.radians(52)
                end = (p[0] + size * math.sin(la), p[1] - size * math.cos(la))
                draw.polygon([
                    p,
                    (p[0] + size * 0.32 * math.sin(la + 1.2), p[1] - size * 0.32 * math.cos(la + 1.2)),
                    end,
                    (p[0] + size * 0.32 * math.sin(la - 1.2), p[1] - size * 0.32 * math.cos(la - 1.2)),
                ], fill=color)


def draw_leaf(draw, base, angle, length, width, color, rib) -> None:
    # Pointed leaf built from mirrored quadratic edges plus a midrib.
    tip = (base[0] + length * math.sin(angle), base[1] - length * math.cos(angle))
    nx, ny = math.cos(angle), math.sin(angle)
    left, right = [], []
    for i in range(15):
        u = i / 14
        w = width * math.sin(math.pi * min(1.0, u * 1.25)) ** 0.9
        px = base[0] * (1 - u) + tip[0] * u
        py = base[1] * (1 - u) + tip[1] * u
        left.append((px + nx * w, py + ny * w))
        right.append((px - nx * w, py - ny * w))
    draw.polygon(left + right[::-1], fill=color)
    draw.line([base, tip], fill=rib, width=2)


def draw_rounded_petal(draw, center, size, petal, core) -> None:
    # Five rounded petals (no star polygons) with a soft core.
    for k in range(5):
        a = math.radians(72 * k + 18)
        cx = center[0] + size * 0.55 * math.sin(a)
        cy = center[1] - size * 0.55 * math.cos(a)
        r = size * 0.42
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=petal)
    draw.ellipse([center[0] - size * 0.22, center[1] - size * 0.22,
                  center[0] + size * 0.22, center[1] + size * 0.22], fill=core)


def draw_pine(draw, x, y, height, width, color) -> None:
    # Layered pine silhouette.
    for i in range(5):
        u = i / 5
        top = y - height * (1 - u * 0.8)
        bot = y - height * (1 - (u + 0.3) * 0.8)
        w = width * (u + 0.3)
        draw.polygon([(x, top), (x - w / 2, bot), (x + w / 2, bot)], fill=color)


def bokeh(rng, colors, count, region, radius, alpha) -> Image.Image:
    # Soft out-of-focus discs used across every composition.
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for _ in range(count):
        cx = rng.uniform(0, WIDTH)
        cy = rng.uniform(HEIGHT * region[0], HEIGHT * region[1])
        r = rng.uniform(*radius)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgba(rng.choice(colors), rng.randint(alpha[0], alpha[1])))
    return soft_blur(layer, 14)


def fern_layer(pal, seed, color, rib, count, blur) -> Image.Image:
    # Framing fern/leaf layer anchored below the horizon.
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    rng = random.Random(seed)
    for base_x, base_y, angle, length in [
        (WIDTH * 0.02, HEIGHT * 1.02, 0.35, HEIGHT * 0.62), (WIDTH * 0.08, HEIGHT * 1.05, 0.55, HEIGHT * 0.5),
        (WIDTH * 0.97, HEIGHT * 1.03, -0.4, HEIGHT * 0.66), (WIDTH * 0.88, HEIGHT * 1.06, -0.6, HEIGHT * 0.52),
        (WIDTH * 0.30, HEIGHT * 1.08, 0.22, HEIGHT * 0.34), (WIDTH * 0.68, HEIGHT * 1.08, -0.25, HEIGHT * 0.36),
    ]:
        draw_fern(draw, (base_x, base_y), angle + rng.uniform(-0.05, 0.05), length, rng.uniform(-0.16, 0.16), color, 16)
    for _ in range(count):
        bx = rng.uniform(0.0, WIDTH)
        by = rng.uniform(HEIGHT * 0.64, HEIGHT * 1.04)
        draw_leaf(draw, (bx, by), rng.uniform(-0.9, 0.9), rng.uniform(120, 340), rng.uniform(34, 80), color, rib)
    return soft_blur(layer, blur)


def scene_canopy(pal, seed) -> Image.Image:
    # Botanical frame: dawn or moonlight glow behind layered ferns and blossoms.
    rng = random.Random(seed)
    canvas = gradient(pal["sky_top"], pal["sky_bottom"], 1.15)
    canvas.alpha_composite(glow((WIDTH * 0.74, HEIGHT * 0.2), WIDTH * 0.46, pal["glow_cool"], 46 if is_dark(pal) else 92))
    canvas.alpha_composite(glow((WIDTH * 0.2, HEIGHT * 0.72), WIDTH * 0.3, pal["mist"], 34 if is_dark(pal) else 60))
    canvas.alpha_composite(glow((WIDTH * 0.5, HEIGHT * 0.58), WIDTH * 0.8, pal["mist"], 22 if is_dark(pal) else 46))
    canvas.alpha_composite(bokeh(rng, [pal["glow_cool"]], 30, (0.28, 0.95), (14, 60), (10, 24)))

    # Hanging canopy: large leaves descending from the top corners frame the panel area.
    hanging_far = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    hf = ImageDraw.Draw(hanging_far)
    hrng = random.Random(seed + 21)
    for bx, angle, length, width in [
        (0.02, math.pi + 0.18, 780, 150), (0.10, math.pi - 0.12, 620, 120),
        (0.98, math.pi - 0.20, 820, 160), (0.90, math.pi + 0.14, 640, 125),
    ]:
        draw_leaf(hf, (WIDTH * bx, -40), angle + hrng.uniform(-0.06, 0.06), length, width,
                  rgba(pal["foliage_far"], 210), rgba(pal["line"], 70))
    canvas.alpha_composite(soft_blur(hanging_far, 7))

    hanging_near = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    hn = ImageDraw.Draw(hanging_near)
    for bx, angle, length, width in [
        (0.04, math.pi + 0.10, 520, 95), (0.96, math.pi - 0.12, 560, 100),
    ]:
        draw_leaf(hn, (WIDTH * bx, -30), angle, length, width,
                  rgba(pal["foliage_near"], 235), rgba(pal["line"], 60))
    canvas.alpha_composite(soft_blur(hanging_near, 2))

    canvas.alpha_composite(fern_layer(pal, seed + 1, rgba(pal["foliage_far"], 235), rgba(pal["line"], 55), 22, 8))
    canvas.alpha_composite(bokeh(rng, [pal["glow_cool"]], 18, (0.45, 1.0), (20, 60), (8, 18)))
    canvas.alpha_composite(fern_layer(pal, seed + 2, rgba(pal["foliage_mid"], 245), rgba(pal["line"], 55), 26, 3))
    canvas.alpha_composite(fern_layer(pal, seed + 3, rgba(pal["foliage_near"], 255), rgba(pal["line"], 55), 18, 0))
    blossoms = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blossoms)
    brng = random.Random(seed + 9)
    for fx, fy in [(0.14, 0.80), (0.22, 0.92), (0.10, 0.65), (0.84, 0.78), (0.92, 0.88), (0.78, 0.93), (0.30, 0.86), (0.65, 0.90)]:
        draw_rounded_petal(bd, (WIDTH * (fx + brng.uniform(-0.02, 0.02)), HEIGHT * (fy + brng.uniform(-0.03, 0.03))),
                           brng.uniform(30, 58), rgba(pal["glow_warm"], 200), rgba(pal["glow_cool"], 120))
    canvas.alpha_composite(soft_blur(blossoms, 1.5))
    canvas.alpha_composite(vignette(72 if is_dark(pal) else 42, pal["foliage_near"] if is_dark(pal) else pal["mist"]))
    return grain(canvas, seed)


def scene_aurora(pal, seed) -> Image.Image:
    # Ribbon aurora over layered pine ridges, with soft dust instead of star glyphs.
    rng = random.Random(seed)
    canvas = gradient(pal["sky_top"], pal["water"], 1.15)
    dust = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dust)
    for _ in range(180):
        sx = rng.uniform(0, WIDTH)
        sy = rng.uniform(0, HEIGHT * 0.62)
        sr = rng.uniform(0.8, 2.4)
        dd.ellipse([(sx - sr, sy - sr), (sx + sr, sy + sr)], fill=rgba(pal["glow_cool"], rng.randint(40, 150)))
    canvas.alpha_composite(soft_blur(dust, 1.2))

    ribbons = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ribbons)
    for index, (base_y, amp, color, alpha, width) in enumerate([
        (0.34, 150, pal["glow_cool"], 40, 56),
        (0.25, 120, pal["glow_warm"], 30, 42),
        (0.42, 90, pal["line"], 26, 34),
    ]):
        for x in range(0, WIDTH + 40, 32):
            wave = math.sin(x * 0.0015 + index) * amp + math.cos(x * 0.003 + index * 0.8) * amp * 0.6
            y = HEIGHT * base_y + wave
            rd.line([(x, y - 140), (x, y + 90)], fill=rgba(color, alpha), width=width)
    canvas.alpha_composite(soft_blur(ribbons, 34))

    for base_frac, hmin, hmax, step, color, blur in [
        (0.88, 0.14, 0.22, 24, rgba(pal["foliage_far"], 180), 4),
        (0.94, 0.20, 0.32, 36, rgba(pal["foliage_mid"], 220), 2),
        (1.02, 0.28, 0.44, 60, rgba(pal["foliage_near"], 255), 0),
    ]:
        ridge = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        rid = ImageDraw.Draw(ridge)
        for x in range(-20, WIDTH + 60, step):
            height = rng.uniform(HEIGHT * hmin, HEIGHT * hmax)
            draw_pine(rid, x + rng.uniform(-10, 10), HEIGHT * base_frac, height, height * 0.34, color)
        canvas.alpha_composite(soft_blur(ridge, blur))

    # Seal the bottom edge so gaps between the nearest tree crowns do not show through.
    ground = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ImageDraw.Draw(ground).rectangle([(0, HEIGHT * 0.985), (WIDTH, HEIGHT)], fill=rgba(pal["foliage_near"], 255))
    canvas.alpha_composite(ground)

    canvas.alpha_composite(glow((WIDTH * 0.5, HEIGHT * 0.72), WIDTH * 0.5, pal["mist"], 24 if is_dark(pal) else 70))
    canvas.alpha_composite(vignette(64 if is_dark(pal) else 30, pal["foliage_near"] if is_dark(pal) else pal["mist"]))
    return grain(canvas, seed)


def scene_flora(pal, seed) -> Image.Image:
    # Minimal architectural leaf: layered translucent contours and one halo.
    canvas = gradient(pal["sky_top"], pal["sky_bottom"], 1.2)
    canvas.alpha_composite(glow((WIDTH * 0.62, HEIGHT * 0.55), WIDTH * 0.46, pal["glow_cool"], 40 if is_dark(pal) else 80))
    canvas.alpha_composite(bokeh(random.Random(seed + 4), [pal["mist"], pal["glow_cool"]], 30, (0.2, 0.9), (30, 120), (12, 30)))

    shapes = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shapes)
    cx, cy = WIDTH * 0.55, HEIGHT * 0.80
    for i in range(6):
        scale = 1.0 - i * 0.12
        angle = math.radians(-32 + i * 14)
        length = HEIGHT * 0.58 * scale
        width = WIDTH * 0.20 * scale
        tip = (cx + length * math.sin(angle), cy - length * math.cos(angle))
        left_ctrl = (cx + width * math.cos(angle) + length * 0.4 * math.sin(angle),
                     cy + width * math.sin(angle) - length * 0.4 * math.cos(angle))
        right_ctrl = (cx - width * math.cos(angle) + length * 0.4 * math.sin(angle),
                      cy - width * math.sin(angle) - length * 0.4 * math.cos(angle))
        poly = [(cx, cy)]
        for step in range(25):
            u = step / 24
            poly.append(((1 - u) ** 2 * cx + 2 * (1 - u) * u * left_ctrl[0] + u**2 * tip[0],
                         (1 - u) ** 2 * cy + 2 * (1 - u) * u * left_ctrl[1] + u**2 * tip[1]))
        for step in range(25, -1, -1):
            u = step / 24
            poly.append(((1 - u) ** 2 * cx + 2 * (1 - u) * u * right_ctrl[0] + u**2 * tip[0],
                         (1 - u) ** 2 * cy + 2 * (1 - u) * u * right_ctrl[1] + u**2 * tip[1]))
        sd.polygon(poly, fill=rgba(pal["foliage_far"], 24 + i * 10))
        sd.line(poly, fill=rgba(pal["line"], 170 - i * 18), width=max(2, 6 - i))
        sd.line([(cx, cy), tip], fill=rgba(pal["glow_cool"], 170 - i * 20), width=3)

    canvas.alpha_composite(soft_blur(shapes, 0.6))
    canvas.alpha_composite(vignette(66 if is_dark(pal) else 28, pal["foliage_near"] if is_dark(pal) else pal["mist"]))
    return grain(canvas, seed)


def scene_river(pal, seed) -> Image.Image:
    # Topographic mineral flow with three lifted isolines.
    canvas = gradient(pal["sky_top"], pal["sky_bottom"], 1.25)
    canvas.alpha_composite(glow((WIDTH * 0.45, HEIGHT * 0.65), WIDTH * 0.5, pal["mist"], 42 if is_dark(pal) else 80))
    canvas.alpha_composite(bokeh(random.Random(seed + 5), [pal["glow_cool"]], 18, (0.4, 0.9), (40, 140), (10, 24)))

    contours = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cd = ImageDraw.Draw(contours)
    count = 28
    glow_indices = {6, 14, 21}
    for idx in range(count):
        base_y = HEIGHT * 0.15 + (idx / count) * (HEIGHT * 0.9)
        phase = idx * 0.32
        freq = 0.0012 + (idx % 3) * 0.0003
        amp = 90 + math.sin(idx * 0.4) * 50
        points = [(x, base_y + math.sin(x * freq + phase) * amp + math.cos(x * 0.0006) * 40)
                  for x in range(0, WIDTH + 30, 20)]
        if idx in glow_indices:
            cd.line(points, fill=rgba(pal["line"], 190), width=4)
        else:
            cd.line(points, fill=rgba(pal["glow_cool"], 70), width=2)

    glow_pass = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_pass)
    for idx in glow_indices:
        base_y = HEIGHT * 0.15 + (idx / count) * (HEIGHT * 0.9)
        phase = idx * 0.32
        freq = 0.0012 + (idx % 3) * 0.0003
        amp = 90 + math.sin(idx * 0.4) * 50
        pts = [(x, base_y + math.sin(x * freq + phase) * amp + math.cos(x * 0.0006) * 40)
               for x in range(0, WIDTH + 30, 20)]
        gd.line(pts, fill=rgba(pal["line"], 100), width=16)

    canvas.alpha_composite(soft_blur(glow_pass, 14))
    canvas.alpha_composite(contours)
    canvas.alpha_composite(vignette(60 if is_dark(pal) else 26, pal["foliage_near"] if is_dark(pal) else pal["mist"]))
    return grain(canvas, seed)


def is_dark(pal: dict) -> bool:
    # The dark palette has a near-black sky top.
    return int(pal["sky_top"][1:3], 16) < 64


COMPOSITIONS = {
    "1": ("mt-verdant-canopy", "Botanical Canopy (Midnight Fern)", scene_canopy, ART["dark"]),
    "2": ("mt-verdant-aurora", "Verdant Aurora (Nordic Pines)", scene_aurora, ART["dark"]),
    "3": ("mt-verdant-flora", "Zen Flora (Geometric Contour)", scene_flora, ART["dark"]),
    "4": ("mt-verdant-river", "Obsidian River (Mineral Flow)", scene_river, ART["dark"]),
    "light-1": ("mt-verdant-canopy-dawn", "Botanical Canopy Dawn (Morning Mist)", scene_canopy, ART["light"]),
    "light-2": ("mt-verdant-celestial-rift", "Celestial Rift (Sage Sky)", scene_aurora, ART["light"]),
    "light-3": ("mt-verdant-cosmic-dawn", "Cosmic Dawn (Stellar Amber)", scene_flora, ART["light"]),
    "light-4": ("mt-verdant-botanical-horizon", "Botanical Horizon (Aurora Dawn)", scene_river, ART["light"]),
}


def dominant_palette(image: Image.Image, count: int = 8) -> list:
    # Report dominant colors so docs can show the sampled render palette.
    small = image.convert("RGB").resize((160, 90))
    quantized = small.quantize(colors=count, method=Image.Quantize.MEDIANCUT).convert("RGB")
    counts = sorted(quantized.getcolors(160 * 90) or [], reverse=True)
    return [f"#{r:02x}{g:02x}{b:02x}" for _, (r, g, b) in counts]


def expected_paths() -> list:
    # Every output file, with its suite.
    paths = []
    for key, (prefix, _title, _fn, pal) in COMPOSITIONS.items():
        folder = DIST / "light" if not is_dark(pal) else DIST
        paths.append((key, folder / f"{prefix}-3840x2160.jpg"))
    return paths


def verify() -> int:
    # Check existence, dimensions, uniqueness and luminance targets.
    problems = []
    hashes = {}
    for key, path in expected_paths():
        if not path.exists():
            problems.append(f"missing {path.relative_to(REPO_ROOT)}")
            continue
        image = Image.open(path).convert("RGB")
        if image.size != (WIDTH, HEIGHT):
            problems.append(f"{path.name}: {image.size[0]}x{image.size[1]}, expected {WIDTH}x{HEIGHT}")
        digest = hashlib.md5(path.read_bytes()).hexdigest()
        if digest in hashes:
            problems.append(f"{path.name} duplicates {hashes[digest]}")
        hashes[digest] = path.name
        mean = ImageStat.Stat(image.convert("L")).mean[0]
        if is_dark(COMPOSITIONS[key][3]):
            if not 28 <= mean <= 50:
                problems.append(f"{path.name}: dark mean luminance {mean:.1f} outside 28-50")
        elif mean < 150:
            problems.append(f"{path.name}: light mean luminance {mean:.1f} below 150")
        print(f"  {path.name}: {mean:.1f} mean luminance")
    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1
    print(f"verify: {len(hashes)} unique wallpapers, luminance and dimensions within target")
    return 0


def main() -> int:
    # Generate requested wallpapers or verify the existing suite.
    parser = argparse.ArgumentParser(description="Generate the MT Verdant Nocturne wallpaper suite")
    parser.add_argument("--which", default="all", choices=[*COMPOSITIONS.keys(), "all"])
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    if args.verify:
        return verify()

    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "light").mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    (PREVIEW_DIR / "light").mkdir(parents=True, exist_ok=True)

    keys = list(COMPOSITIONS) if args.which == "all" else [args.which]
    summaries = {}
    seed_base = 20261102
    for index, key in enumerate(keys):
        prefix, title, scene, pal = COMPOSITIONS[key]
        dark = is_dark(pal)
        print(f"Generating {title} ({'night' if dark else 'dawn'}, 4K)...")
        seed = seed_base + list(COMPOSITIONS).index(key) * 17
        image = scene(pal, seed)
        folder = DIST if dark else DIST / "light"
        preview_folder = PREVIEW_DIR if dark else PREVIEW_DIR / "light"
        target = folder / f"{prefix}-3840x2160.jpg"
        image.convert("RGB").save(target, "JPEG", quality=82, optimize=True, progressive=True)
        preview = preview_folder / f"{prefix}-1920x1080.jpg"
        image.resize(PREVIEW, Image.Resampling.LANCZOS).convert("RGB").save(preview, "JPEG", quality=86, optimize=True, progressive=True)
        summaries[key] = {
            "title": title,
            "suite": "dark" if dark else "light",
            "file": str(target.relative_to(REPO_ROOT)),
            "preview": str(preview.relative_to(REPO_ROOT)),
            "dominant": dominant_palette(image),
        }
        print(f"  saved {target.name} + preview")

    summary_path = DIST / "palette-summary.json"
    existing = {}
    if args.which != "all" and summary_path.exists():
        try:
            existing = json.loads(summary_path.read_text())
        except json.JSONDecodeError:
            existing = {}
    existing.update(summaries)
    summary_path.write_text(json.dumps(existing, indent=2))
    from generate_dynamic import main as write_xml
    write_xml()
    print(f"wallpaper summary: {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
