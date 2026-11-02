# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# WCAG contrast validation for every foreground/background pair the theme emits.
# Covers text tiers on all surfaces, accent families, UI state edges, terminal ANSI
# palettes and editor syntax colors. Exits non-zero on any failure.

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())


def flatten(node, prefix="") -> dict:
    # Flatten nested dicts into dotted paths.
    flat = {}
    for key, value in node.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten(value, path))
        elif not isinstance(value, list):
            flat[path] = value
    return flat


COLOR = flatten(TOKENS["color"])
MIN = TOKENS["wcag_minimums"]


def srgb_to_linear(channel: int) -> float:
    # Convert an 8-bit sRGB channel to linear light.
    c = channel / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    # WCAG relative luminance of a #RRGGBB color.
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * srgb_to_linear(r) + 0.7152 * srgb_to_linear(g) + 0.0722 * srgb_to_linear(b)


def contrast_ratio(fg: str, bg: str) -> float:
    # WCAG contrast ratio between two #RRGGBB colors.
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


FAILURES = []
RESULTS = []


def check(label: str, fg: str, bg: str, minimum: float) -> None:
    # Record one contrast result and remember failures.
    ratio = contrast_ratio(fg, bg)
    ok = ratio >= minimum
    RESULTS.append((ok, label, fg, bg, ratio, minimum))
    if not ok:
        FAILURES.append((label, fg, bg, ratio, minimum))


def token(path: str) -> str:
    # Resolve a dotted token path.
    if path not in COLOR:
        raise KeyError(f"unknown token {path}")
    return COLOR[path]


def check_tokens() -> None:
    # Every text tier on every declared surface.
    surfaces = MIN["surfaces"]
    for tier in MIN["text_tiers"]:
        for surface in surfaces:
            check(f"{tier} on {surface}", token(tier), token(surface), MIN["body_text"])

    # Disabled text is exempt from WCAG AA but must stay visible and clearly muted.
    for surface in ("bg.base", "bg.tile", "bg.raised", "bg.surface"):
        check(f"text.disabled on {surface}", token("text.disabled"), token(surface), MIN["disabled_text"])

    # Accent families: text usage on reading surfaces, UI edges (3:1) everywhere.
    text_surfaces = ("bg.base", "bg.tile", "bg.raised")
    for flavor, data in TOKENS["color"]["accent_flavors"].items():
        for surface in text_surfaces:
            check(f"accent {flavor}.base on {surface}", data["base"], token(surface), MIN["body_text"])
        for surface in surfaces:
            check(f"accent {flavor}.base edge on {surface}", data["base"], token(surface), MIN["ui_component"])
        check(f"accent {flavor}.dim on bg.base", data["dim"], token("bg.base"), MIN["body_text"])
        check(f"accent {flavor}.dim on bg.tile", data["dim"], token("bg.tile"), MIN["body_text"])
        check(f"text on accent {flavor}", data["text_on"], data["base"], MIN["body_text"])

    # Status colors used as text and as destructive-button backgrounds.
    for status in ("status.destructive", "status.success", "status.warning"):
        check(f"{status} on bg.base", token(status), token("bg.base"), MIN["body_text"])
        check(f"{status} on bg.tile", token(status), token("bg.tile"), MIN["body_text"])
    check("accent.text_on_accent on destructive", token("accent.text_on_accent"), token("status.destructive"), MIN["body_text"])
    check("accent.text_on_accent on status.success", token("accent.text_on_accent"), token("status.success"), MIN["body_text"])


def parse_kitty() -> None:
    # Validate the canonical ANSI palette against the terminal background.
    path = REPO_ROOT / "extras" / "terminals" / "kitty" / "mt-verdant-nocturne.conf"
    if not path.exists():
        return
    values = {}
    for line in path.read_text().splitlines():
        match = re.match(r"^(color\d+|background|foreground|selection_background|selection_foreground|cursor)\s+(#[0-9a-fA-F]{6})", line.strip())
        if match:
            values[match.group(1)] = match.group(2)
    bg = values.get("background")
    if not bg:
        return
    for index in list(range(1, 8)) + list(range(9, 16)):
        key = f"color{index}"
        if key in values:
            check(f"terminal {key} on background", values[key], bg, MIN["body_text"])
    for key in ("color0", "color8"):
        if key in values:
            check(f"terminal {key} visible on background", values[key], bg, 1.1)
    if "selection_background" in values and "selection_foreground" in values:
        check("terminal selection", values["selection_foreground"], values["selection_background"], MIN["body_text"])


def parse_vscode() -> None:
    # Validate editor foreground and comment color against the editor background.
    path = REPO_ROOT / "extras" / "vscode" / "themes" / "mt-verdant-nocturne-color-theme.json"
    if not path.exists():
        return
    data = json.loads(path.read_text())
    colors = data.get("colors", {})
    bg = colors.get("editor.background")
    fg = colors.get("editor.foreground")
    if bg and fg:
        check("vscode editor foreground", fg, bg, MIN["body_text"])
    for entry in data.get("tokenColors", []):
        scope = entry.get("scope")
        if isinstance(scope, list) and "comment" in scope and bg:
            color = entry.get("settings", {}).get("foreground")
            if color:
                check("vscode comments", color, bg, MIN["body_text"])


def main() -> int:
    # Run every check and print one line per pair.
    check_tokens()
    parse_kitty()
    parse_vscode()

    for ok, label, fg, bg, ratio, minimum in RESULTS:
        label_text = "PASS" if ok else "FAIL"
        print(f"{label_text}  {label}: {fg} on {bg} = {ratio:.2f}:1 (min {minimum})")

    print(f"\n{len(RESULTS)} pairs checked, {len(FAILURES)} failure(s).")
    if FAILURES:
        for label, fg, bg, ratio, minimum in FAILURES:
            print(f"  FAIL {label}: {ratio:.2f} < {minimum}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
