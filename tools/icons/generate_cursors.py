# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Generates MT-Verdant-Cursors suite: sleek aerodynamic botanical cursors.
# High-definition multi-resolution (24, 32, 48) Xcursor suite with smooth curves and sage glow.

import math
import os
import shutil
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "src" / "cursors" / "MT-Verdant-Cursors"

# Palette tokens from palette/tokens.json
COLOR_BODY = (15, 20, 27, 255)         # Obsidian deep charcoal #0F141B
COLOR_ACCENT = (143, 184, 166, 255)    # Botanical Sage #8FB8A6
COLOR_EMERALD = (61, 214, 140, 255)    # Aurora Emerald #3DD68C
COLOR_CORAL = (229, 115, 127, 255)     # Destructive Coral #E5737F
COLOR_SHADOW = (0, 0, 0, 130)

INDEX_THEME = """[Icon Theme]
Name=MT-Verdant-Cursors
Comment=Sleek aerodynamic botanical cursor suite for MT Verdant Nocturne
Inherits=Adwaita
"""

def img_to_premultiplied_bgra(img: Image.Image) -> bytes:
    # Convert RGBA Pillow image to premultiplied BGRA bytes for Xcursor binary format
    arr = np.array(img.convert("RGBA"), dtype=np.float32)
    alpha = arr[..., 3:4] / 255.0
    arr[..., :3] *= alpha
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return arr[..., [2, 1, 0, 3]].tobytes()

def make_xcursor(frames_with_hotspots: list) -> bytes:
    # frames_with_hotspots: list of tuples (Image, xhot, yhot, delay_ms)
    magic = 0x72756358
    header_size = 16
    version = 0x00010000
    ntoc = len(frames_with_hotspots)
    
    header = struct.pack("<IIII", magic, header_size, version, ntoc)
    toc_entries = []
    image_chunks = []
    cur_offset = header_size + ntoc * 12
    
    for img, xhot, yhot, delay in frames_with_hotspots:
        w, h = img.size
        toc_entries.append(struct.pack("<III", 0xfffd0002, w, cur_offset))
        img_hdr = struct.pack("<IIIIIIIII", 36, 0xfffd0002, w, 1, w, h, xhot, yhot, delay)
        bgra = img_to_premultiplied_bgra(img)
        chunk = img_hdr + bgra
        image_chunks.append(chunk)
        cur_offset += len(chunk)
        
    return header + b"".join(toc_entries) + b"".join(image_chunks)

def draw_aerodynamic_pointer(target_size: int, show_accent_dot: bool = False) -> tuple:
    # Draw a sleek aerodynamic curved cursor (Bibata / macOS inspired) with 4x supersampling
    scale = 4
    canvas_size = target_size * scale
    im = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    # Coordinates normalized to 128 canvas
    s = canvas_size / 128.0
    pts = [
        (16 * s, 16 * s),    # Tip
        (22 * s, 92 * s),    # Left barb
        (46 * s, 76 * s),    # Inner waist left
        (68 * s, 118 * s),   # Stem bottom left
        (82 * s, 110 * s),   # Stem bottom right
        (62 * s, 68 * s),    # Inner waist right
        (96 * s, 68 * s),    # Right barb
    ]
    
    # 1. Soft ambient drop shadow
    shadow = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    shadow_offset = 3 * s
    s_pts = [(x + shadow_offset, y + shadow_offset) for x, y in pts]
    sdraw.polygon(s_pts, fill=COLOR_SHADOW)
    shadow = shadow.filter(ImageFilter.GaussianBlur(5 * s))
    im = Image.alpha_composite(im, shadow)
    
    draw = ImageDraw.Draw(im)
    # 2. Outer glowing botanical border
    draw.polygon(pts, fill=COLOR_BODY)
    draw.line(pts + [pts[0]], fill=COLOR_EMERALD, width=int(round(4 * s)), joint="curve")
    
    # 3. Inner sage contour accent
    inner_contour = [(pts[0][0] + 5*s, pts[0][1] + 8*s), (pts[1][0] + 4*s, pts[1][1] - 10*s), (pts[2][0] + 2*s, pts[2][1] - 8*s)]
    draw.line(inner_contour, fill=COLOR_ACCENT, width=int(round(2.5 * s)))
    
    if show_accent_dot:
        dot_center = (pts[2][0] + 10 * s, pts[2][1] + 12 * s)
        draw.ellipse([(dot_center[0] - 6*s, dot_center[1] - 6*s), (dot_center[0] + 6*s, dot_center[1] + 6*s)], fill=COLOR_ACCENT)
        draw.ellipse([(dot_center[0] - 3*s, dot_center[1] - 3*s), (dot_center[0] + 3*s, dot_center[1] + 3*s)], fill=COLOR_EMERALD)
    
    # Downsample with Lanczos anti-aliasing
    final_img = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
    xhot = int(round(4 * (target_size / 32.0)))
    yhot = int(round(4 * (target_size / 32.0)))
    return final_img, xhot, yhot

def draw_pointer_hand(target_size: int) -> tuple:
    # Modern sleek pointer hand (index extended, organic curve)
    scale = 4
    canvas_size = target_size * scale
    s = canvas_size / 128.0
    im = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    # Shadow
    shadow = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([(36*s + 2*s, 16*s + 3*s), (54*s + 2*s, 72*s + 3*s)], radius=9*s, fill=COLOR_SHADOW)
    sdraw.rounded_rectangle([(24*s + 2*s, 50*s + 3*s), (88*s + 2*s, 108*s + 3*s)], radius=16*s, fill=COLOR_SHADOW)
    shadow = shadow.filter(ImageFilter.GaussianBlur(5 * s))
    im = Image.alpha_composite(im, shadow)
    
    draw = ImageDraw.Draw(im)
    # Palm body
    draw.rounded_rectangle([(24*s, 50*s), (88*s, 108*s)], radius=16*s, fill=COLOR_BODY, outline=COLOR_EMERALD, width=int(round(4*s)))
    # Index finger
    draw.rounded_rectangle([(36*s, 16*s), (54*s, 76*s)], radius=9*s, fill=COLOR_BODY, outline=COLOR_EMERALD, width=int(round(4*s)))
    # Accent ring on index knuckle
    draw.line([(38*s, 44*s), (52*s, 44*s)], fill=COLOR_ACCENT, width=int(round(3*s)))
    
    final_img = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
    xhot = int(round(11 * (target_size / 32.0)))
    yhot = int(round(4 * (target_size / 32.0)))
    return final_img, xhot, yhot

def draw_ibeam_text(target_size: int) -> tuple:
    # Sleek modern text insertion cursor (I-beam with sage caps)
    scale = 4
    canvas_size = target_size * scale
    s = canvas_size / 128.0
    im = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(im)
    cx = 64 * s
    # Top bar
    draw.line([(cx - 24*s, 24*s), (cx + 24*s, 24*s)], fill=COLOR_EMERALD, width=int(round(5*s)))
    # Bottom bar
    draw.line([(cx - 24*s, 104*s), (cx + 24*s, 104*s)], fill=COLOR_EMERALD, width=int(round(5*s)))
    # Central stem
    draw.line([(cx, 24*s), (cx, 104*s)], fill=COLOR_BODY, width=int(round(7*s)))
    draw.line([(cx, 26*s), (cx, 102*s)], fill=COLOR_ACCENT, width=int(round(3*s)))
    
    final_img = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
    return final_img, target_size // 2, target_size // 2

def draw_crosshair(target_size: int) -> tuple:
    # Sleek precision reticle
    scale = 4
    canvas_size = target_size * scale
    s = canvas_size / 128.0
    im = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(im)
    cx, cy = 64 * s, 64 * s
    gap = 10 * s
    length = 36 * s
    
    # Outer dark lines
    for p1, p2 in [((cx, cy - gap), (cx, cy - length)), ((cx, cy + gap), (cx, cy + length)),
                   ((cx - gap, cy), (cx - length, cy)), ((cx + gap, cy), (cx + length, cy))]:
        draw.line([p1, p2], fill=COLOR_EMERALD, width=int(round(4*s)))
        draw.line([p1, p2], fill=COLOR_BODY, width=int(round(2*s)))
        
    draw.ellipse([(cx - 2*s, cy - 2*s), (cx + 2*s, cy + 2*s)], fill=COLOR_EMERALD)
    
    final_img = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
    return final_img, target_size // 2, target_size // 2

def draw_move(target_size: int) -> tuple:
    # 4-way aerodynamic arrows meeting at center
    scale = 4
    canvas_size = target_size * scale
    s = canvas_size / 128.0
    im = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(im)
    cx, cy = 64 * s, 64 * s
    
    # Center dot
    draw.ellipse([(cx - 8*s, cy - 8*s), (cx + 8*s, cy + 8*s)], fill=COLOR_EMERALD)
    draw.ellipse([(cx - 5*s, cy - 5*s), (cx + 5*s, cy + 5*s)], fill=COLOR_BODY)
    
    # 4 arrows
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        dx, dy = math.cos(rad), math.sin(rad)
        tip = (cx + dx * 46*s, cy + dy * 46*s)
        base = (cx + dx * 16*s, cy + dy * 16*s)
        draw.line([base, tip], fill=COLOR_EMERALD, width=int(round(4*s)))
        
        # Barb wings
        perp_x, perp_y = -dy, dx
        w1 = (tip[0] - dx*12*s + perp_x*8*s, tip[1] - dy*12*s + perp_y*8*s)
        w2 = (tip[0] - dx*12*s - perp_x*8*s, tip[1] - dy*12*s - perp_y*8*s)
        draw.polygon([tip, w1, w2], fill=COLOR_EMERALD)
        
    final_img = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
    return final_img, target_size // 2, target_size // 2

def draw_resize_col(target_size: int) -> tuple:
    # Horizontal bidirectional arrows
    scale = 4
    canvas_size = target_size * scale
    s = canvas_size / 128.0
    im = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    cy = 64 * s
    
    # Central bar
    draw.line([(24*s, cy), (104*s, cy)], fill=COLOR_EMERALD, width=int(round(4*s)))
    # Left arrow
    draw.polygon([(18*s, cy), (32*s, cy - 10*s), (32*s, cy + 10*s)], fill=COLOR_EMERALD)
    # Right arrow
    draw.polygon([(110*s, cy), (96*s, cy - 10*s), (96*s, cy + 10*s)], fill=COLOR_EMERALD)
    # Split bar in center
    draw.line([(64*s, cy - 18*s), (64*s, cy + 18*s)], fill=COLOR_BODY, width=int(round(5*s)))
    draw.line([(64*s, cy - 16*s), (64*s, cy + 16*s)], fill=COLOR_ACCENT, width=int(round(2*s)))
    
    final_img = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
    return final_img, target_size // 2, target_size // 2

def draw_resize_row(target_size: int) -> tuple:
    # Vertical bidirectional arrows
    img, xhot, yhot = draw_resize_col(target_size)
    return img.rotate(90), xhot, yhot

def draw_resize_nesw(target_size: int) -> tuple:
    # Diagonal resize
    img, xhot, yhot = draw_resize_col(target_size)
    return img.rotate(45), xhot, yhot

def draw_resize_nwse(target_size: int) -> tuple:
    # Diagonal resize
    img, xhot, yhot = draw_resize_col(target_size)
    return img.rotate(-45), xhot, yhot

def draw_not_allowed(target_size: int) -> tuple:
    # Forbidden circular sign with diagonal bar in coral red
    scale = 4
    canvas_size = target_size * scale
    s = canvas_size / 128.0
    im = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    cx, cy = 64 * s, 64 * s
    r = 38 * s
    
    # Outer ring
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=COLOR_BODY, outline=COLOR_CORAL, width=int(round(8*s)))
    # Diagonal slash
    draw.line([(cx - r*0.65, cy - r*0.65), (cx + r*0.65, cy + r*0.65)], fill=COLOR_CORAL, width=int(round(8*s)))
    
    final_img = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
    return final_img, target_size // 2, target_size // 2

def draw_spinner_frame(target_size: int, frame_idx: int, num_frames: int = 8, with_pointer: bool = False) -> tuple:
    # Rotating emerald spinner ring
    scale = 4
    canvas_size = target_size * scale
    s = canvas_size / 128.0
    im = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    if with_pointer:
        # Base pointer
        ptr, px, py = draw_aerodynamic_pointer(target_size, show_accent_dot=False)
        im = ptr.resize((canvas_size, canvas_size), Image.Resampling.NEAREST)
        # Spinner located at bottom-right
        scx, scy = 88 * s, 88 * s
        sr = 22 * s
    else:
        scx, scy = 64 * s, 64 * s
        sr = 36 * s
        
    draw = ImageDraw.Draw(im)
    base_angle = (360.0 / num_frames) * frame_idx
    
    for i in range(num_frames):
        a = math.radians(base_angle + i * (360.0 / num_frames))
        ax = scx + math.cos(a) * sr
        ay = scy + math.sin(a) * sr
        dot_r = (2.0 + 3.5 * (i / num_frames)) * s
        alpha = int(60 + 195 * (i / num_frames))
        col = (61, 214, 140, alpha)
        draw.ellipse([(ax - dot_r, ay - dot_r), (ax + dot_r, ay + dot_r)], fill=col)
        
    final_img = im.resize((target_size, target_size), Image.Resampling.LANCZOS)
    xhot = int(round(4 * (target_size / 32.0))) if with_pointer else target_size // 2
    yhot = int(round(4 * (target_size / 32.0))) if with_pointer else target_size // 2
    return final_img, xhot, yhot

def build_cursor_theme() -> None:
    # Build complete MT-Verdant-Cursors theme directory
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
        
    out_cursors = OUT_DIR / "cursors"
    out_cursors.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.theme").write_text(INDEX_THEME)
    
    sizes = [24, 32, 48]
    
    # 1. Base cursor shapes map
    generators = {
        "default": lambda sz: draw_aerodynamic_pointer(sz, False),
        "pointer": lambda sz: draw_pointer_hand(sz),
        "text": lambda sz: draw_ibeam_text(sz),
        "crosshair": lambda sz: draw_crosshair(sz),
        "move": lambda sz: draw_move(sz),
        "col-resize": lambda sz: draw_resize_col(sz),
        "row-resize": lambda sz: draw_resize_row(sz),
        "nesw-resize": lambda sz: draw_resize_nesw(sz),
        "nwse-resize": lambda sz: draw_resize_nwse(sz),
        "not-allowed": lambda sz: draw_not_allowed(sz),
    }
    
    # Render static cursors
    for name, gen_fn in generators.items():
        frames = []
        for sz in sizes:
            img, xh, yh = gen_fn(sz)
            frames.append((img, xh, yh, 0))
        raw_bytes = make_xcursor(frames)
        (out_cursors / name).write_bytes(raw_bytes)
        print(f"  + generated cursor: {name}")
        
    # Render animated progress and wait cursors (8 frames @ 60ms delay)
    for name, with_ptr in [("wait", False), ("progress", True)]:
        frames = []
        for f in range(8):
            for sz in sizes:
                img, xh, yh = draw_spinner_frame(sz, f, num_frames=8, with_pointer=with_ptr)
                frames.append((img, xh, yh, 60))
        raw_bytes = make_xcursor(frames)
        (out_cursors / name).write_bytes(raw_bytes)
        print(f"  + generated animated cursor: {name}")
        
    # Symlink aliases
    aliases = {
        "default": [
            "arrow", "top_left_arrow", "left_ptr", "right_ptr", "center_ptr",
        ],
        "pointer": [
            "hand1", "hand2", "pointing_hand", "e29285e634086352946a0e7090d73106",
            "9d800788f1b08800ae810202380a0822",
        ],
        "text": [
            "xterm", "ibeam",
        ],
        "wait": [
            "watch", "0426c80cad02078e4301040052da300e",
        ],
        "progress": [
            "left_ptr_watch", "3ecb610c1bf2410f44200f48c40d3599",
            "08e8e1c95fe2fc01f976f1e063a24ccd", "00000000000000020006000e7e9ffc3f",
        ],
        "crosshair": [
            "cross", "tcross",
        ],
        "move": [
            "fleur", "all-scroll", "4498f0e0c1937ffe01fd06f973665830",
            "9081237383d90e509aa00f00170e968f",
        ],
        "not-allowed": [
            "circle", "crossed_circle", "03b6e0fcb3499374a867c041f52298f0",
        ],
        "col-resize": [
            "ew-resize", "split_h", "size_hor", "h_double_arrow",
            "028006030e0e7ebffb7f7070c0600140", "e-resize", "w-resize",
        ],
        "row-resize": [
            "ns-resize", "split_v", "size_ver", "v_double_arrow",
            "00008160000006810000408080010102", "n-resize", "s-resize",
        ],
        "nesw-resize": [
            "size_bdiag", "50585d5204e6e9a0397017c60f1e0878",
            "fcf1c3c7cd4491d801f1e1c78f100822", "ne-resize", "sw-resize",
        ],
        "nwse-resize": [
            "size_fdiag", "38c9d0d4e788665001f357607e443022",
            "c7088f0f3e6c8088236ef8e1e3e70000", "nw-resize", "se-resize",
        ],
    }
    
    for target, symlinks in aliases.items():
        for link_name in symlinks:
            dst = out_cursors / link_name
            if not dst.exists():
                dst.symlink_to(target)
                
    print(f"Generated {len(aliases)} cursor categories with symlinks into {OUT_DIR}")

if __name__ == "__main__":
    build_cursor_theme()
