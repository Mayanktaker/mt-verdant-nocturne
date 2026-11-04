# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Deterministic 4K landscape and sculptural wallpaper suite.

import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageStat

ROOT = Path(__file__).resolve().parents[2]
TOKENS = json.loads((ROOT / "palette/tokens.json").read_text())
ART = TOKENS["art"]
W, H = 1920, 1080
SIZE = (3840, 2160)
DIST, PREVIEW = ROOT / "wallpaper/dist", ROOT / "wallpaper/preview"


def rgba(value, alpha=255, scale=1.0):
    # Convert a palette token to a scaled RGBA value.
    return tuple(max(0, min(255, round(int(value[i:i + 2], 16) * scale))) for i in (1, 3, 5)) + (alpha,)


def gradient(top, bottom):
    # Build a smooth vertical gradient at working resolution.
    a, b = np.array(rgba(top)[:3]), np.array(rgba(bottom)[:3])
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    return Image.fromarray(np.repeat(a * (1 - t) + b * t, W, axis=1).astype(np.uint8), "RGB").convert("RGBA")


def glow(image, x, y, radius, token, opacity):
    # Add a token-colored radial light at half resolution.
    yy, xx = np.mgrid[0:H:2, 0:W:2]
    falloff = np.clip(1 - np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / radius, 0, 1) ** 2
    layer = np.zeros((H // 2, W // 2, 4), dtype=np.uint8)
    layer[..., :3], layer[..., 3] = rgba(token)[:3], (falloff * opacity).astype(np.uint8)
    image.alpha_composite(Image.fromarray(layer, "RGBA").resize((W, H), Image.Resampling.BILINEAR))


def clouds(image, seed, token, ceiling=.68, opacity=38):
    # Add broad, broken cloud texture without flattening the night sky.
    rng=np.random.default_rng(seed)
    noise=Image.fromarray(rng.integers(0,256,(32,64),dtype=np.uint8)).resize((W,H),Image.Resampling.BICUBIC)
    values=np.asarray(noise,dtype=np.float32)/255
    yy=np.linspace(0,1,H)[:,None]
    alpha=(np.clip((values-.43)*2.2,0,1)*np.clip((ceiling-yy)*5,0,1)*opacity).astype(np.uint8)
    layer=np.zeros((H,W,4),dtype=np.uint8)
    layer[...,:3]=rgba(token)[:3]
    layer[...,3]=alpha
    image.alpha_composite(Image.fromarray(layer,"RGBA").filter(ImageFilter.GaussianBlur(7)))


def done(image, seed, noise=0.8):
    # Add film grain and broad tonal texture before enlarging to 4K.
    rng = np.random.default_rng(seed)
    pixels = np.asarray(image.convert("RGB"), dtype=np.float32)
    broad = rng.normal(0, 1, (54, 96)).astype(np.float32)
    broad = np.asarray(Image.fromarray(np.uint8(np.clip(broad * 36 + 128, 0, 255))).resize((W, H), Image.Resampling.BICUBIC), dtype=np.float32)
    pixels += rng.normal(0, noise * 0.45, (H, W, 1)) + ((broad - 128) * 0.035)[..., None]
    return Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8)).resize(SIZE, Image.Resampling.LANCZOS)


def stars(draw, rng, token, count, limit=.68):
    # Scatter sparse stars with natural size and brightness variation.
    for _ in range(count):
        x, y = rng.randrange(W), rng.randrange(int(H * limit))
        r = rng.choices([1, 2, 3], [8, 3, 1])[0]
        draw.ellipse((x-r, y-r, x+r, y+r), fill=rgba(token, rng.randint(55, 185)))


def treeline(draw, rng, ground, token, count, heights):
    # Draw uneven multi-tier pine silhouettes across a ridge.
    for _ in range(count):
        x, height = rng.randint(-30, W + 30), rng.randint(*heights)
        y, width = ground + rng.randint(-10, 18), height * rng.uniform(.34, .58)
        left, right = [(x, y-height)], [(x, y-height)]
        for tier in range(1, 8):
            fraction = tier / 7
            branch_width = width * fraction**.78 * rng.uniform(.88, 1.08)
            level = y-height+height*fraction
            left.append((x-branch_width, level-rng.uniform(0, height*.06)))
            right.append((x+branch_width*rng.uniform(.86, 1.08), level+rng.uniform(0, height*.025)))
        draw.polygon(left+right[::-1], fill=rgba(token))
        for tier in range(2, 8, 2):
            fraction=tier/8
            branch_width=width*fraction**.8
            level=y-height+height*fraction
            draw.line((x-branch_width,level,x+branch_width,level+rng.randint(1,5)),fill=rgba(token,scale=1.10),width=max(1,int(height*.018)))


def water(draw, rng, top, bottom, tokens, count):
    # Draw tapered, horizon-aligned reflection streaks.
    for _ in range(count):
        y, x = rng.randint(top, bottom), rng.randrange(W)
        spread = .2 + .8 * (y-top) / max(1, bottom-top)
        length = rng.randint(5, 90) * spread
        draw.line((x, y, x+length, y+rng.uniform(-1, 1)), fill=rgba(rng.choice(tokens), rng.randint(20, 100)), width=1)


def lake(seed):
    # Blue-hour water and distant forest reflect the last warm horizon.
    p, rng = ART["dark"], random.Random(seed)
    image = gradient(p["sky_top"], p["sky_bottom"])
    glow(image, W*.5, H*.60, W*.36, p["glow_warm"], 50)
    glow(image, W*.5, H*.67, W*.3, p["glow_cool"], 40)
    clouds(image,seed+2,p["mist"],.59,28)
    draw = ImageDraw.Draw(image, "RGBA")
    stars(draw, rng, p["glow_cool"], 72, .52)
    horizon = int(H*.62)
    shore = [(0, horizon+22)]
    for x in range(0, W+30, 22):
        shore.append((x, int(horizon + math.sin(x*.006)*24 + math.cos(x*.002)*15)))
    shore += [(W, H), (0, H)]
    draw.polygon(shore, fill=rgba(p["water"]))
    treeline(draw, rng, horizon+17, p["foliage_near"], 160, (16, 50))
    water(draw, rng, horizon+25, H-10, [p["glow_cool"], p["mist"], p["glow_warm"]], 1050)
    draw.line((0, horizon+17, W, horizon+17), fill=rgba(p["glow_cool"], 100), width=2)
    return done(image, seed)


def aurora(seed):
    # Soft aurora ribbons cross a layered evergreen night scene.
    p, rng = ART["dark"], random.Random(seed)
    image = gradient(p["sky_top"], p["sky_bottom"])
    glow(image, W*.52, H*.28, W*.52, p["glow_cool"], 44)
    clouds(image,seed+3,p["glow_cool"],.66,26)
    draw = ImageDraw.Draw(image, "RGBA")
    stars(draw, rng, p["mist"], 190, .76)
    ribbons = Image.new("RGBA", (W, H))
    rd = ImageDraw.Draw(ribbons)
    for band, token in enumerate([p["glow_cool"], p["line"], p["mist"]]):
        pts = [(x, H*(.29+band*.085)+math.sin(x*.004+band)*45+math.cos(x*.009+band)*15) for x in range(-20, W+24, 8)]
        rd.line(pts, fill=rgba(token, 65), width=46-band*8, joint="curve")
        rd.line(pts, fill=rgba(token, 50), width=20-band*3, joint="curve")
    image.alpha_composite(ribbons.filter(ImageFilter.GaussianBlur(16)))
    draw = ImageDraw.Draw(image, "RGBA")
    for base, token, count, heights in [(.78,p["foliage_far"],100,(70,165)),(.91,p["foliage_mid"],85,(115,235)),(1.04,p["foliage_near"],70,(140,290))]:
        treeline(draw, rng, int(H*base), token, count, heights)
    draw.rectangle((0,H*.94,W,H), fill=rgba(p["foliage_near"]))
    return done(image, seed)


def mountains(seed):
    # Jagged alpine ridges are lit by cold moonlight beneath sparse stars.
    p, rng = ART["dark"], random.Random(seed)
    image = gradient(p["sky_top"], p["sky_bottom"])
    glow(image, W*.78, H*.20, W*.25, p["glow_cool"], 24)
    clouds(image,seed+5,p["mist"],.72,22)
    draw = ImageDraw.Draw(image, "RGBA")
    stars(draw, rng, p["mist"], 340, .72)
    peaks = [(0,.74),(.08,.54),(.16,.66),(.24,.36),(.31,.57),(.43,.30),(.52,.62),(.61,.42),(.70,.66),(.82,.34),(.91,.56),(1,.41)]
    points = [(int(x*W),int(y*H)) for x,y in peaks] + [(W,H),(0,H)]
    draw.polygon(points, fill=rgba(p["foliage_mid"], scale=.82))
    for i in range(1, len(peaks)-1):
        x,y = int(peaks[i][0]*W),int(peaks[i][1]*H)
        left,right = int(peaks[i-1][0]*W),int(peaks[i+1][0]*W)
        draw.polygon([(x,y),(x-(x-left)*.34,int(y+H*.2)),(x+(right-x)*.10,int(y+H*.12))], fill=rgba(p["mist"], 105))
        for _ in range(17):
            sx,sy = rng.randint(max(0,x-85),min(W,x+85)),rng.randint(y,min(H,y+155))
            draw.line((sx,sy,sx+rng.randint(5,34),sy+rng.randint(0,4)), fill=rgba(p["glow_cool"],rng.randint(18,65)))
    treeline(draw, rng, int(H*.97), p["foliage_near"], 250, (65,175))
    return done(image, seed)


def river(seed):
    # A winding mineral channel catches fine sage light between dark rocks.
    p, rng = ART["dark"], random.Random(seed)
    image = gradient(p["sky_bottom"], p["foliage_near"])
    glow(image, W*.52, H*.63, W*.45, p["glow_cool"], 28)
    draw = ImageDraw.Draw(image, "RGBA")
    for layer in range(8):
        y0, pts = int(H*(.39+layer*.08)), [(0,H)]
        for x in range(0,W+12,12):
            y=y0+math.sin(x*(.004+layer*.0002)+layer)*(36+layer*4)+math.cos(x*.0015)*42
            pts.append((x,int(y)))
        pts.append((W,H))
        draw.polygon(pts, fill=rgba(p["foliage_near"],scale=.78+layer*.04))
    left,right=[],[]
    for y in range(H+20,int(H*.38),-7):
        x=W*.52+math.sin(y*.006)*W*.1+math.cos(y*.002)*W*.04
        width=38+(H-y)*.25
        left.append((x-width,y)); right.append((x+width,y))
    draw.polygon(left+right[::-1], fill=rgba(p["water"],235))
    for _ in range(1600):
        y=rng.randint(int(H*.4),H)
        x=int(W*.52+math.sin(y*.006)*W*.1+math.cos(y*.002)*W*.04+rng.gauss(0,40+(y-H*.4)*.16))
        draw.line((x,y,x+rng.randint(4,36),y), fill=rgba(rng.choice([p["line"],p["glow_cool"],p["mist"]]),rng.randint(16,100)), width=1)
    for _ in range(700):
        x,y,r=rng.randrange(W),rng.randrange(int(H*.38),H),rng.randint(1,4)
        draw.ellipse((x,y,x+r*3,y+r), fill=rgba(p["mist"],rng.randint(20,85),rng.uniform(.75,1.1)))
    return done(image, seed, 1.1)


def leaf(cx,cy,length,width,angle,steps=54):
    # Shape a long folded leaf from opposing tapered curves.
    ux,uy,nx,ny=math.sin(angle),-math.cos(angle),math.cos(angle),math.sin(angle)
    a,b=[],[]
    for i in range(steps+1):
        t=i/steps; w=math.sin(math.pi*t)**.82*width; bend=math.sin(math.pi*t)*length*.1
        x,y=cx+ux*length*t+nx*bend,cy+uy*length*t+ny*bend
        a.append((x+nx*w,y+ny*w)); b.append((x-nx*w,y-ny*w))
    return a+b[::-1]


def light_landscape(seed, warm=False, upscale=True):
    # Sunrise over quiet layered hills, rendered as tactile paper-cut forms.
    p,rng=ART["light"],random.Random(seed)
    image=gradient(p["sky_top"],p["sky_bottom"])
    glow(image,W*.52,H*.47,W*.27,p["glow_warm"],48)
    glow(image,W*.52,H*.69,W*.30,p["glow_cool"],34)
    draw=ImageDraw.Draw(image,"RGBA")
    if warm:
        draw.ellipse((W*.485,H*.39,W*.535,H*.48),fill=rgba(p["glow_warm"],160))
    for i,(base,token,amp) in enumerate([(.61,p["foliage_far"],34),(.70,p["foliage_mid"],40),(.81,p["foliage_near"],32)]):
        pts=[(0,H)] + [(x,int(H*base+math.sin(x*(.003+i*.001)+i)*amp+math.cos(x*.006)*amp*.25)) for x in range(-10,W+12,12)] + [(W,H)]
        draw.polygon(pts,fill=rgba(token,225))
    top=int(H*.79)
    draw.rectangle((0,top,W,H),fill=rgba(p["water"],135))
    water(draw,rng,top,H,[p["glow_cool"],p["mist"],p["glow_warm"]],650)
    return done(image,seed,.65) if upscale else image


def sculpture(seed, mode):
    # Independent light artwork built from translucent folded botanical ribbons.
    p=ART["light"]
    image=gradient(p["sky_top"],p["mist"])
    glow(image,W*.72,H*.46,W*.56,p["glow_cool"],24)
    art=Image.new("RGBA",(W,H)); draw=ImageDraw.Draw(art,"RGBA")
    if mode==0:
        specs=[(1.12,.48,-.55),(1.06,.40,-.32),(1.02,.32,-.12),(.94,.25,.16),(.84,.18,.34),(.72,.13,.51)]
        origin=(W*.73,H*1.05)
    else:
        specs=[(1.18,.37,.64),(1.08,.31,.43),(1,.26,.22),(.91,.21,.03),(.82,.16,-.19),(.72,.11,-.38),(.61,.08,-.58)]
        origin=(W*.40,H*1.10)
    shadows=Image.new("RGBA",(W,H)); shade=ImageDraw.Draw(shadows)
    colors=[p["foliage_far"],p["water"],p["mist"],p["glow_cool"],p["glow_warm"],p["foliage_mid"]]
    for i,(length,width,angle) in enumerate(specs):
        cx,cy=origin[0]+math.sin(i*.65)*W*.10,origin[1]+i*8
        pts=leaf(cx,cy,H*length,W*width,angle)
        shade.polygon([(x+9,y+13) for x,y in pts],fill=rgba(TOKENS["color"]["shadow"],32))
        token=colors[i%len(colors)]
        alpha=145 if token==p["glow_warm"] else 230-i*9
        draw.polygon(pts,fill=rgba(token,alpha))
        draw.line(pts[:55],fill=rgba(p["mist"],110),width=2)
        draw.line(pts[54:],fill=rgba(p["foliage_mid"],75),width=2)
        draw.line((cx,cy,cx+math.sin(angle)*H*length,cy-math.cos(angle)*H*length),fill=rgba(p["glow_cool"],85),width=2)
    image.alpha_composite(shadows.filter(ImageFilter.GaussianBlur(18)))
    image.alpha_composite(art.filter(ImageFilter.GaussianBlur(.5)))
    return done(image,seed,.55)


def horizon(seed):
    # Broad misty water and soft low ridges, with reeds only at the edges.
    p,rng=ART["light"],random.Random(seed)
    image=gradient(p["sky_top"],p["water"])
    glow(image,W*.29,H*.45,W*.34,p["glow_cool"],35)
    draw=ImageDraw.Draw(image,"RGBA")
    for layer,(base,token,amp) in enumerate([(.54,p["foliage_far"],25),(.63,p["foliage_mid"],28),(.71,p["foliage_near"],18)]):
        pts=[(0,H)] + [(x,int(H*base+math.sin(x*(.003+layer*.001)+1.5)*amp+math.cos(x*.004)*amp*.24)) for x in range(-12,W+16,12)] + [(W,H)]
        draw.polygon(pts,fill=rgba(token,205-layer*20))
    water_top=int(H*.73)
    draw.rectangle((0,water_top,W,H),fill=rgba(p["water"],145))
    water(draw,rng,water_top,H,[p["glow_cool"],p["mist"]],760)
    for edge,direction in [(0,1),(W,-1)]:
        for _ in range(38):
            x=edge+direction*rng.randint(0,135); y=rng.randint(int(H*.73),H)
            draw.line((x,y,x+direction*rng.randint(8,55),y-rng.randint(35,150)),fill=rgba(p["foliage_mid"],rng.randint(75,160)),width=rng.choice([1,2,3]))
    return done(image,seed+1,.6)


SCENES={
    "1":("mt-verdant-canopy","Stillwater at Blue Hour",lake,ART["dark"]),
    "2":("mt-verdant-aurora","Verdant Aurora",aurora,ART["dark"]),
    "3":("mt-verdant-flora","Moonlit Alpine Range",mountains,ART["dark"]),
    "4":("mt-verdant-river","Mineral River",river,ART["dark"]),
    "light-1":("mt-verdant-canopy-dawn","Sculpted Canopy",lambda seed:sculpture(seed,0),ART["light"]),
    "light-2":("mt-verdant-celestial-rift","Paper-Cut Sunrise",lambda seed:light_landscape(seed,True),ART["light"]),
    "light-3":("mt-verdant-cosmic-dawn","Folded Celadon",lambda seed:sculpture(seed,1),ART["light"]),
    "light-4":("mt-verdant-botanical-horizon","Mist on the Water",horizon,ART["light"]),
}


def dark(palette):
    # Identify dark suites from their source sky token.
    return int(palette["sky_top"][1:3],16)<64


def verify():
    # Verify image dimensions, uniqueness and luminance by suite.
    failures,seen=[],set()
    for key,(prefix,_title,_scene,palette) in SCENES.items():
        path=(DIST/"light" if not dark(palette) else DIST)/f"{prefix}-3840x2160.jpg"
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}"); continue
        image=Image.open(path).convert("RGB"); digest=hashlib.sha256(path.read_bytes()).hexdigest()
        mean=ImageStat.Stat(image.convert("L")).mean[0]
        if image.size!=SIZE: failures.append(f"{path.name}: dimensions {image.size}, expected {SIZE}")
        if digest in seen: failures.append(f"{path.name}: duplicate image")
        seen.add(digest)
        if dark(palette) and not 18<=mean<=105: failures.append(f"{path.name}: dark luminance {mean:.1f} outside 18-105")
        if not dark(palette) and mean<135: failures.append(f"{path.name}: light luminance {mean:.1f} below 135")
        print(f"  {path.name}: {image.width}x{image.height}, luminance {mean:.1f}")
    for failure in failures: print(f"FAIL {failure}",file=sys.stderr)
    if failures: return 1
    print(f"verify: {len(seen)} unique 4K wallpapers pass"); return 0


def main():
    # Generate selected original artwork or verify the suite.
    parser=argparse.ArgumentParser(description="Generate MT Verdant Nocturne wallpapers")
    parser.add_argument("--which",default="all",choices=[*SCENES,"all"])
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    if args.verify: return verify()
    for folder in [DIST,DIST/"light",PREVIEW,PREVIEW/"light"]: folder.mkdir(parents=True,exist_ok=True)
    keys=list(SCENES) if args.which=="all" else [args.which]
    summary_path=DIST/"palette-summary.json"
    try: summary=json.loads(summary_path.read_text()) if args.which!="all" and summary_path.exists() else {}
    except json.JSONDecodeError: summary={}
    for key in keys:
        prefix,title,scene,palette=SCENES[key]
        image=scene(20261103+list(SCENES).index(key)*29)
        folder,preview_folder=(DIST/"light",PREVIEW/"light") if not dark(palette) else (DIST,PREVIEW)
        target=folder/f"{prefix}-3840x2160.jpg"
        image.save(target,"JPEG",quality=93,optimize=True,progressive=True,subsampling=0)
        small=image.resize((1920,1080),Image.Resampling.LANCZOS)
        preview=preview_folder/f"{prefix}-1920x1080.jpg"
        small.save(preview,"JPEG",quality=90,optimize=True,progressive=True)
        summary[key]={"title":title,"suite":"dark" if dark(palette) else "light","file":str(target.relative_to(ROOT)),"preview":str(preview.relative_to(ROOT))}
        print(f"Generated {title}: {target.relative_to(ROOT)}")
    summary_path.write_text(json.dumps(summary,indent=2)+"\n")
    from generate_dynamic import main as write_xml
    write_xml()
    return 0


if __name__=="__main__":
    sys.exit(main())
