# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Build the MT Verdant Nocturne GTK4 theme: full Adwaita dark base, recoloured
# through src/gtk-4.0/recolor.json, plus the curated token layer.

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = REPO_ROOT / "src" / "gtk-4.0"
OVERRIDES = SOURCE_DIR / "overrides.css"
RECOLOR = SOURCE_DIR / "recolor.json"
DEFAULT_OUT = REPO_ROOT / "build" / "theme" / "gtk-4.0"
HEADER = "/* MT Verdant Nocturne — © Mayanktaker Computers & Web Development | https://mayanktaker.com */\n"
BASE_RESOURCE = "/org/gtk/libgtk/theme/Default/Default-dark.css"
ASSET_PREFIX = "resource:///org/gtk/libgtk/theme/Default/"

sys.path.insert(0, str(REPO_ROOT / "tools" / "theme"))
from palette import FLAVORS, flatten, load_tokens, render_template, resolve_accent


def read_base() -> str:
    # Read GTK's own compiled Adwaita dark stylesheet from its gresource.
    import gi

    gi.require_version("Gtk", "4.0")
    from gi.repository import Gio, Gtk  # noqa: F401  (import registers GTK's resources)

    try:
        data = Gio.resources_lookup_data(BASE_RESOURCE, 0)
    except Exception as error:  # noqa: BLE001 - surfaced as a build failure
        raise SystemExit(f"cannot read {BASE_RESOURCE} from libgtk: {error}") from error
    return data.get_data().decode("utf-8")


def token_colors(tokens: dict, accent: str) -> dict:
    # Resolve the literal -> token mapping into literal -> hex colour.
    flat = flatten(tokens["color"])
    for key, value in resolve_accent(tokens, accent).items():
        flat[f"accent.{key}"] = value
    mapping = json.loads(RECOLOR.read_text())["hex"]
    resolved = {}
    for literal, path in mapping.items():
        if path not in flat:
            raise SystemExit(f"recolor.json references unknown token: {path}")
        resolved[literal.lower()] = flat[path]
    return resolved


def recolor(css: str, mapping: dict) -> tuple[str, int]:
    # Swap Adwaita's identity colours for palette tokens, keeping alpha values.
    count = 0
    triplets = {}
    for literal, replacement in mapping.items():
        triplets[tuple(int(literal[i : i + 2], 16) for i in (1, 3, 5))] = replacement

    def swap_hex(match) -> str:
        nonlocal count
        literal = match.group(0).lower()
        if literal in mapping:
            count += 1
            return mapping[literal]
        return match.group(0)

    def swap_rgba(match) -> str:
        nonlocal count
        rgb = tuple(int(part) for part in match.group(1).split(","))
        if rgb in triplets:
            count += 1
            top = triplets[rgb].lstrip("#")
            parts = [str(int(top[i : i + 2], 16)) for i in (0, 2, 4)]
            return f"rgba({', '.join(parts)}, {match.group(2)})"
        return match.group(0)

    css = re.sub(r"#[0-9a-fA-F]{6}\b", swap_hex, css)
    css = re.sub(r"rgba\(\s*(\d{1,3},\s*\d{1,3},\s*\d{1,3})\s*,\s*([^)]+)\)", swap_rgba, css)
    return css, count


def rebase_assets(css: str) -> str:
    # Point relative asset URLs at GTK's own gresource so no assets need shipping.
    return re.sub(r'url\("assets/([^"]+)"\)', lambda m: f'url("{ASSET_PREFIX}assets/{m.group(1)}")', css)


def color_definitions(rendered_overrides: str) -> str:
    # Extract the @define-color block (the libadwaita-facing colour contract).
    return "\n".join(line for line in rendered_overrides.splitlines() if line.startswith("@define-color"))


def verify(css: str, tokens: dict, accent: str, replaced: int) -> None:
    # Guard: no Adwaita identity colours survive, palette colours are present.
    palette = resolve_accent(tokens, accent)
    leftovers = [
        literal
        for literal in ("#15539e", "#3584e4", "#b2161d", "#26a269", "#f57900", "#629fea")
        if literal in css.lower()
    ]
    checks = {
        "accent identity recoloured": replaced > 40,
        "no Adwaita accent left": not leftovers,
        "sage accent baked": palette["base"].lower() in css.lower(),
        "destructive baked": tokens["color"]["status"]["destructive"].lower() in css.lower(),
        "total view surface baked": tokens["color"]["bg"]["tile"].lower() in css.lower(),
        "asset urls rebased": 'url("assets/' not in css,
    }
    for name, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if leftovers:
        print(f"  leftover literals: {', '.join(leftovers)}", file=sys.stderr)
    if not all(checks.values()):
        raise SystemExit(4)


def main() -> int:
    # Render, recolour, inline the base and write the theme files.
    parser = argparse.ArgumentParser(description="Build the MT Verdant Nocturne GTK4 theme")
    parser.add_argument("--accent", default="sage", choices=FLAVORS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--base", type=Path, help="use a saved Adwaita stylesheet instead of libgtk")
    args = parser.parse_args()

    tokens = load_tokens()
    base = args.base.read_text() if args.base else read_base()
    mapping = token_colors(tokens, args.accent)
    base, replaced = recolor(base, mapping)
    base = rebase_assets(base)

    overrides = render_template(OVERRIDES.read_text(), tokens, args.accent)
    css = f"{HEADER}/* ---- Upstream Adwaita dark base (recoloured) ---- */\n{base}\n{overrides}"
    verify(css, tokens, args.accent, replaced)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "gtk-dark.css").write_text(css)
    (out_dir / "gtk.css").write_text(css)

    # Opt-in user CSS for libadwaita apps: colour contract only, never the base.
    user_css = (
        f"{HEADER}/* libadwaita colour contract — palette/tokens.json is the source of truth */\n"
        f"{color_definitions(overrides)}\n"
    )
    (out_dir / "user.css").write_text(user_css)

    print(f"GTK4 theme written to {out_dir} (accent: {args.accent}, {replaced} colours recoloured)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
