# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# WCAG contrast validation for MT Verdant Nocturne tokens (single source: palette/tokens.json).

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())


def resolve(token_path: str) -> str:
    # Look up a dotted token path inside the color token tree.
    node = TOKENS["color"]
    for part in token_path.split("."):
        node = node[part]
    return node


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


def main() -> int:
    # Validate every declared pair against the token thresholds; exit non-zero on failure.
    minimums = TOKENS["wcag_minimums"]
    failures = []
    for fg_token, bg_token in minimums["pairs"]:
        ratio = contrast_ratio(resolve(fg_token), resolve(bg_token))
        needed = minimums["body_text"]
        ok = ratio >= needed
        preferred = ratio >= minimums["preferred_text"]
        label = "PASS+" if preferred else ("PASS" if ok else "FAIL")
        print(f"{label}  {fg_token} on {bg_token}: {ratio:.2f}:1 (min {needed})")
        if not ok:
            failures.append((fg_token, bg_token, ratio))
    if failures:
        print("\nContrast failures:", failures, file=sys.stderr)
        return 1
    print("\nAll token pairs meet WCAG minimums.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
