# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Procedural "botanical night-garden" wallpaper generator for MT Verdant Nocturne.
# Deterministic: pinned SEED, colors derived from palette/tokens.json.

import json
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())
COLOR = TOKENS["color"]
SEED = 20261027  # pinned so renders are reproducible
WIDTH, HEIGHT = 3840, 2160
FOLIAGE_TOP_LIMIT = 0.22  # keep the top fifth clean for the shell panel


def hex_to_rgb(hex_color: str, alpha: int = 255) -> tuple:
    # Convert #RRGGBB plus alpha into an RGBA tuple.
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return (r, g, b, alpha)


def gradient_background() -> Image.Image:
    # Vertical charcoal-teal gradient: darkest at top, faint green at the bottom.
    top = np.array(hex_to_rgb(COLOR["bg"]["base_darker"])[:3], dtype=float)
    bottom = np.array((13, 26, 24), dtype=float)  # deep garden floor green
    t = np.linspace(0.0, 1.0, HEIGHT)[:, None, None]
    rows = top * (1 - t) + bottom * t
    return Image.fromarray(np.repeat(rows, WIDTH, axis=1).astype(np.uint8), "RGB").convert("RGBA")


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


def draw_fern(draw: ImageDraw.ImageDraw, base: tuple, angle: float, length: float, curve: float, color: tuple, leaflets: int) -> None:
    # One arcing fern frond: curved stem with tapering leaflets along its tangent.
    tip = (base[0] + length * math.sin(angle), base[1] - length * math.cos(angle))
    ctrl = (base[0] + length * 0.55 * math.sin(angle + curve), base[1] - length * 0.55 * math.cos(angle + curve))
    steps = 40
    prev = base
    for i in range(1, steps + 1):
        u = i / steps
        # quadratic bezier point and tangent
        p = (
            (1 - u) ** 2 * base[0] + 2 * (1 - u) * u * ctrl[0] + u**2 * tip[0],
            (1 - u) ** 2 * base[1] + 2 * (1 - u) * u * ctrl[1] + u**2 * tip[1],
        )
        draw.line([prev, p], fill=color, width=max(2, int(6 * (1 - u)) + 2))
        prev = p
        if i % max(1, steps // leaflets) == 0 and p[1] > HEIGHT * FOLIAGE_TOP_LIMIT:
            tangent = math.atan2(p[0] - ctrl[0], ctrl[1] - p[1])  # rough direction along stem
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
    nx, ny = math.cos(angle), math.sin(angle)  # unit normal to leaf axis
    left, right = [], []
    for i in range(13):
        u = i / 12
        # width profile: slim at both ends, widest at 40%
        w = width * math.sin(math.pi * min(1.0, u * 1.25)) ** 0.9
        px = base[0] * (1 - u) + tip[0] * u
        py = base[1] * (1 - u) + tip[1] * u
        left.append((px + nx * w, py + ny * w))
        right.append((px - nx * w, py - ny * w))
    draw.polygon(left + right[::-1], fill=color)
    draw.line([base, tip], fill=rib, width=3)


def draw_blossom(draw: ImageDraw.ImageDraw, center: tuple, size: float, petal: tuple, core: tuple) -> None:
    # Five-petal blossom with a soft core; the theme's single decorative accent.
    for k in range(5):
        a = math.radians(72 * k + random.uniform(-8, 8))
        petal_tip = (center[0] + size * math.sin(a), center[1] - size * math.cos(a))
        side_a = (center[0] + size * 0.45 * math.sin(a + 1.5), center[1] - size * 0.45 * math.cos(a + 1.5))
        side_b = (center[0] + size * 0.45 * math.sin(a - 1.5), center[1] - size * 0.45 * math.cos(a - 1.5))
        draw.polygon([center, side_a, petal_tip, side_b], fill=petal)
    draw.ellipse([center[0] - size * 0.16, center[1] - size * 0.16, center[0] + size * 0.16, center[1] + size * 0.16], fill=core)


def foliage_layer(color: tuple, rib: tuple, blur: float) -> Image.Image:
    # One depth layer of ferns and leaves over transparency.
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rng = random.Random(SEED)
    # ferns arching from the bottom corners and lower edges
    for base_x, base_y, angle, length in [
        (WIDTH * 0.02, HEIGHT * 1.02, 0.35, HEIGHT * 0.62), (WIDTH * 0.08, HEIGHT * 1.05, 0.55, HEIGHT * 0.5),
        (WIDTH * 0.97, HEIGHT * 1.03, -0.4, HEIGHT * 0.66), (WIDTH * 0.88, HEIGHT * 1.06, -0.6, HEIGHT * 0.52),
        (WIDTH * 0.30, HEIGHT * 1.08, 0.22, HEIGHT * 0.34), (WIDTH * 0.68, HEIGHT * 1.08, -0.25, HEIGHT * 0.36),
    ]:
        draw_fern(d, (base_x, base_y), angle + rng.uniform(-0.05, 0.05), length, rng.uniform(-0.16, 0.16), color, 16)
    # scattered simple leaves
    for _ in range(22):
        bx = rng.uniform(0.0, WIDTH)
        by = rng.uniform(HEIGHT * 0.66, HEIGHT * 1.04)
        draw_leaf(d, (bx, by), rng.uniform(-0.9, 0.9), rng.uniform(120, 340), rng.uniform(34, 80), color, rib)
    return layer.filter(ImageFilter.GaussianBlur(blur))


def bokeh_layer() -> Image.Image:
    # Scattered soft sage/teal light dots for depth.
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rng = random.Random(SEED + 7)
    sage = hex_to_rgb(COLOR["accent"]["base"], 26)
    teal = hex_to_rgb("#49686A", 22)
    for _ in range(46):
        cx, cy = rng.uniform(0, WIDTH), rng.uniform(HEIGHT * 0.28, HEIGHT)
        r = rng.uniform(18, 95)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rng.choice([sage, teal]))
    return layer.filter(ImageFilter.GaussianBlur(14))


def blossoms_layer() -> Image.Image:
    # Restrained pale-pink blossoms riding on the near foliage layer.
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rng = random.Random(SEED + 13)
    petal = hex_to_rgb(COLOR["status"]["petal_decorative"], 205)
    core = hex_to_rgb(COLOR["text"]["primary"], 120)
    spots = [(0.14, 0.80), (0.22, 0.92), (0.10, 0.65), (0.84, 0.78), (0.92, 0.88), (0.78, 0.93), (0.30, 0.86), (0.65, 0.90), (0.47, 0.95)]
    for fx, fy in spots:
        jitter = (rng.uniform(-0.02, 0.02), rng.uniform(-0.03, 0.03))
        draw_blossom(d, (WIDTH * (fx + jitter[0]), HEIGHT * (fy + jitter[1])), rng.uniform(34, 62), petal, core)
    return layer.filter(ImageFilter.GaussianBlur(1.2))


def vignette() -> Image.Image:
    # Edge darkening to settle the composition and lift panel legibility.
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    dist = np.sqrt(((xx - WIDTH / 2) / (WIDTH / 2)) ** 2 + ((yy - HEIGHT / 2) / (HEIGHT / 2)) ** 2)
    alpha = (np.clip(dist - 0.55, 0.0, 1.0) * 90).astype(np.uint8)
    layer = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    layer[..., 3] = alpha
    return Image.fromarray(layer, "RGBA")


def add_grain(image: Image.Image) -> Image.Image:
    # Subtle film grain so flat gradients don't band.
    rng = np.random.default_rng(SEED)
    noise = rng.normal(0.0, 2.2, (HEIGHT, WIDTH, 1)).repeat(3, axis=2)
    data = np.clip(np.asarray(image, dtype=float) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(data, "RGB")


def dominant_palette(image: Image.Image, count: int = 8) -> list:
    # Report dominant colors so docs can show the sampled render palette.
    small = image.convert("RGB").resize((160, 90))
    quantized = small.quantize(colors=count, method=Image.Quantize.MEDIANCUT).convert("RGB")
    counts = sorted(quantized.getcolors(160 * 90) or [], reverse=True)
    return [f"#{r:02x}{g:02x}{b:02x}" for _, (r, g, b) in counts]


def main() -> None:
    # Compose the wallpaper and write the 4K render, preview, and palette summary.
    random.seed(SEED)
    canvas = gradient_background()
    # moonlight from the upper right, very quiet
    canvas.alpha_composite(radial_glow((WIDTH, HEIGHT), (WIDTH * 0.78, HEIGHT * 0.14), WIDTH * 0.42, hex_to_rgb(COLOR["accent"]["base"])[:3], 26))
    # three foliage depth layers: hazy far, mid, sharp near
    canvas.alpha_composite(foliage_layer(hex_to_rgb("#17262B", 235), hex_to_rgb("#1B2E33", 235), 7))
    canvas.alpha_composite(bokeh_layer())
    canvas.alpha_composite(foliage_layer(hex_to_rgb("#121E1B", 245), hex_to_rgb("#16241F", 245), 3))
    canvas.alpha_composite(foliage_layer(hex_to_rgb("#0A1310", 255), hex_to_rgb("#0E1713", 255), 0))
    canvas.alpha_composite(blossoms_layer())
    canvas.alpha_composite(vignette())
    final = add_grain(canvas.convert("RGB"))

    dist = REPO_ROOT / "wallpaper" / "dist"
    preview = REPO_ROOT / "wallpaper" / "preview"
    dist.mkdir(parents=True, exist_ok=True)
    preview.mkdir(parents=True, exist_ok=True)
    final.save(dist / "mt-verdant-nocturne-3840x2160.png", optimize=True)
    final.resize((1920, 1080), Image.LANCZOS).save(preview / "mt-verdant-nocturne-1920x1080.jpg", quality=88, optimize=True)
    summary = {"seed": SEED, "size": [WIDTH, HEIGHT], "dominant": dominant_palette(final)}
    (dist / "palette-summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
