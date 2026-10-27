# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Build the MT Verdant Nocturne GNOME Shell theme: extract upstream CSS per
# major Shell version, recolor via src/shell/colormap-<major>.json + palette tokens.

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())
BUILD_DIR = REPO_ROOT / "build" / "theme" / "gnome-shell"
HEADER = "/* MT Verdant Nocturne — © Mayanktaker Computers & Web Development | https://mayanktaker.com */\n"


def detect_shell_major() -> int:
    # Detect the running Shell major to pick the matching color map.
    import subprocess
    version = subprocess.run(["gnome-shell", "--version"], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"(\d+)\.", version).group(1))


def resolve_token(token_path: str) -> str:
    # Resolve a dotted token path inside the color tree.
    node = TOKENS["color"]
    for part in token_path.split("."):
        node = node[part]
    return node


def load_upstream_css(major: int) -> str:
    # Extract the upstream dark stylesheet from the host gresource.
    from gi.repository import Gio
    gresource = f"/usr/share/gnome-shell/gnome-shell-theme.gresource"
    resource_path = "/org/gnome/shell/theme/gnome-shell-dark.css"
    data = Gio.Resource.load(gresource).lookup_data(resource_path, Gio.ResourceLookupFlags.NONE).get_data()
    return data.decode()


def normalize_hex(match_text: str) -> str:
    # Normalize a hex literal to lowercase 6-digit form for map lookups.
    h = match_text.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return f"#{h}"


def recolor(css: str, color_map: dict) -> tuple:
    # Apply pseudo-value, hex, and rgba-base replacements; return (css, usage_counts).
    usage = {}

    # 1. accent pseudo values (longest first: fg before plain)
    for pseudo in sorted(color_map["pseudo"], key=len, reverse=True):
        token_hex = resolve_token(color_map["pseudo"][pseudo])
        usage[pseudo] = css.count(pseudo)
        css = css.replace(pseudo, token_hex)

    hex_map = {k.lower(): resolve_token(v) for k, v in color_map["hex"].items()}

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
    base_overrides = {k: resolve_token(v) for k, v in color_map.get("rgba_base_overrides", {}).items()}

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


def copy_high_contrast() -> None:
    # Keep upstream high-contrast stylesheet as a safe fallback for a11y mode.
    from gi.repository import Gio
    data = Gio.Resource.load("/usr/share/gnome-shell/gnome-shell-theme.gresource")
    hc = data.lookup_data("/org/gnome/shell/theme/gnome-shell-high-contrast.css", Gio.ResourceLookupFlags.NONE).get_data()
    (BUILD_DIR / "gnome-shell-high-contrast.css").write_text(HEADER + hc.decode())


def main() -> int:
    # Build, report coverage, and fail if any mapped color went unused (map drift).
    major = detect_shell_major()
    map_path = REPO_ROOT / "src" / f"shell/colormap-{major}.json"
    if not map_path.exists():
        print(f"No color map for GNOME Shell {major} yet — add src/shell/colormap-{major}.json first.", file=sys.stderr)
        return 2
    color_map = json.loads(map_path.read_text())
    css, usage = recolor(load_upstream_css(major), color_map)

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    (BUILD_DIR / "gnome-shell.css").write_text(HEADER + css)
    copy_high_contrast()

    unused = [k for k in usage if usage[k] == 0 and not k.startswith("rgba-base")]
    total_colors = len(re.findall(r"#[0-9a-fA-F]{3}\b|#[0-9a-fA-F]{6}\b|rgba?\(", css))
    print(f"Shell {major}: wrote {BUILD_DIR / 'gnome-shell.css'} ({len(css)} bytes)")
    print(f"replacements: pseudo={usage.get('-st-accent-color', 0)}+fg{usage.get('-st-accent-fg-color', 0)}, "
          f"hex={sum(v for k, v in usage.items() if k.startswith('#'))}, "
          f"rgba={sum(v for k, v in usage.items() if k.startswith('rgba-base'))}")
    print(f"color instances remaining in output: {total_colors}")
    if unused:
        print("mapped colors not found upstream (map drift):", unused, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
