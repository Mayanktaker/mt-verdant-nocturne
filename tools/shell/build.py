# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Build the MT Verdant Nocturne GNOME Shell theme per major Shell version:
# vendored upstream CSS is preferred (reproducible), host extraction is a fallback;
# colors are mapped through palette tokens for the chosen accent flavor.

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HEADER = "/* MT Verdant Nocturne — © Mayanktaker Computers & Web Development | https://mayanktaker.com */\n"

sys.path.insert(0, str(REPO_ROOT / "tools" / "theme"))
from palette import FLAVORS, flat_with_accent, load_tokens

TOKENS_RAW = load_tokens()


def host_shell_major() -> int:
    # Detect the running Shell major version.
    version = subprocess.run(["gnome-shell", "--version"], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"(\d+)\.", version).group(1))


def resolve_token(token_path: str, flat: dict) -> str:
    # Resolve a dotted token path (accent.* already bound to the chosen flavor).
    if token_path not in flat:
        print(f"unknown token path '{token_path}'", file=sys.stderr)
        sys.exit(2)
    return flat[token_path]


def vendored_path(major: int, filename: str) -> Path:
    # Path to a vendored upstream stylesheet for a Shell major.
    return REPO_ROOT / "src" / "shell" / f"upstream-{major}" / filename


def load_upstream_css(major: int) -> str:
    # Prefer vendored CSS (deterministic); fall back to the host gresource.
    vendored = vendored_path(major, "gnome-shell-dark.css")
    if vendored.exists():
        return vendored.read_text()
    if major == host_shell_major():
        from gi.repository import Gio
        res = Gio.Resource.load("/usr/share/gnome-shell/gnome-shell-theme.gresource")
        return res.lookup_data("/org/gnome/shell/theme/gnome-shell-dark.css", Gio.ResourceLookupFlags.NONE).get_data().decode()
    print(f"No vendored upstream CSS for Shell {major} — add src/shell/upstream-{major}/ first.", file=sys.stderr)
    sys.exit(2)


def load_high_contrast(major: int) -> str:
    # Prefer vendored high-contrast CSS; fall back to the host gresource.
    vendored = vendored_path(major, "gnome-shell-high-contrast.css")
    if vendored.exists():
        return vendored.read_text()
    if major == host_shell_major():
        from gi.repository import Gio
        res = Gio.Resource.load("/usr/share/gnome-shell/gnome-shell-theme.gresource")
        return res.lookup_data("/org/gnome/shell/theme/gnome-shell-high-contrast.css", Gio.ResourceLookupFlags.NONE).get_data().decode()
    print(f"No vendored high-contrast CSS for Shell {major}.", file=sys.stderr)
    sys.exit(2)


def normalize_hex(match_text: str) -> str:
    # Normalize a hex literal to lowercase 6-digit form for map lookups.
    h = match_text.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return f"#{h}"


def recolor(css: str, color_map: dict, flat: dict) -> tuple:
    # Apply pseudo-value, hex, and rgba-base replacements; return (css, usage_counts).
    usage = {}

    # 1. accent pseudo values (longest first: fg before plain)
    for pseudo in sorted(color_map["pseudo"], key=len, reverse=True):
        token_hex = resolve_token(color_map["pseudo"][pseudo], flat)
        usage[pseudo] = css.count(pseudo)
        css = css.replace(pseudo, token_hex)

    hex_map = {k.lower(): resolve_token(v, flat) for k, v in color_map["hex"].items()}

    # 2. plain hex literals
    def hex_sub(match):
        key = normalize_hex(match.group(0))
        mapped = hex_map.get(key)
        if mapped is None:
            return match.group(0)
        usage[key] = usage.get(key, 0) + 1
        return mapped

    css = re.sub(r"#[0-9a-fA-F]{3}\b|#[0-9a-fA-F]{6}\b", hex_sub, css)

    # 3. rgba() bases: map base color through the same table, preserve alpha
    base_overrides = {k: resolve_token(v, flat) for k, v in color_map.get("rgba_base_overrides", {}).items()}

    def rgba_sub(match):
        r, g, b, alpha = match.group(1), match.group(2), match.group(3), match.group(4)
        base = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
        target = base_overrides.get(f"{base}:a{alpha or 1}") or hex_map.get(base)
        if target is None:
            return match.group(0)
        key = f"rgba-base {base}"
        usage[key] = usage.get(key, 0) + 1
        tr, tg, tb = (int(target[i : i + 2], 16) for i in (1, 3, 5))
        return f"rgba({tr}, {tg}, {tb}, {alpha})" if alpha else f"rgb({tr}, {tg}, {tb})"

    css = re.sub(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)", rgba_sub, css)

    return css, usage


def build_major(major: int, accent: str, out_root: Path) -> None:
    # Build one Shell major and fail on map drift (mapped colors unused upstream).
    map_path = REPO_ROOT / "src" / "shell" / f"colormap-{major}.json"
    if not map_path.exists():
        print(f"No color map for GNOME Shell {major} — add src/shell/colormap-{major}.json first.", file=sys.stderr)
        sys.exit(2)
    color_map = json.loads(map_path.read_text())
    flat = flat_with_accent(TOKENS_RAW, accent)

    css, usage = recolor(load_upstream_css(major), color_map, flat)
    hc_css, _ = recolor(load_high_contrast(major), color_map, flat)

    out_dir = out_root / f"gnome-shell-{major}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "gnome-shell.css").write_text(HEADER + css)
    (out_dir / "gnome-shell-high-contrast.css").write_text(HEADER + f"/* Recolored with the {accent} accent at build time. */\n" + hc_css)

    unused = [k for k in usage if usage[k] == 0 and not k.startswith("rgba-base")]
    print(f"Shell {major}: wrote {out_dir / 'gnome-shell.css'} ({len(css)} bytes) | accent={accent} "
          f"pseudo={usage.get('-st-accent-color', 0)}, hex={sum(v for k, v in usage.items() if k.startswith('#'))}, "
          f"rgba={sum(v for k, v in usage.items() if k.startswith('rgba-base'))}")
    if unused:
        print(f"Shell {major} mapped colors not found upstream (map drift):", unused, file=sys.stderr)
        sys.exit(1)


def main() -> int:
    # Build requested majors: --all (every map), --major N, or the host default.
    parser = argparse.ArgumentParser(description="Build the MT Verdant Nocturne GNOME Shell theme")
    parser.add_argument("--major", type=int, help="Shell major to build")
    parser.add_argument("--all", action="store_true", help="build every mapped Shell major")
    parser.add_argument("--accent", default="sage", choices=FLAVORS)
    parser.add_argument("--out-dir", type=Path, default=REPO_ROOT / "build" / "theme")
    args = parser.parse_args()

    if args.all:
        majors = sorted(int(p.stem.split("-")[-1]) for p in (REPO_ROOT / "src" / "shell").glob("colormap-*.json"))
    elif args.major:
        majors = [args.major]
    else:
        majors = [host_shell_major()]
    for major in majors:
        build_major(major, args.accent, args.out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
