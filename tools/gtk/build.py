# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Build the MT Verdant Nocturne GTK3 theme: patch upstream Adwaita (gtk-3-24)
# base SASS variables with palette tokens, compile with sassc, ship dark-only.

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = REPO_ROOT / "src" / "gtk-3.0" / "upstream"
WORK = REPO_ROOT / "build" / "gtk-3.0-work"
OUT = REPO_ROOT / "build" / "theme" / "gtk-3.0"
HEADER = "/* MT Verdant Nocturne — © Mayanktaker Computers & Web Development | https://mayanktaker.com */\n"

# upstream base variable -> token dotted path (dark theme is our only variant)
VARIABLE_MAP = {
    "base_color": "bg.tile",
    "text_color": "text.primary",
    "caret_color": "accent.base",
    "bg_color": "bg.base",
    "fg_color": "text.primary",
    "selected_fg_color": "accent.text_on_accent",
    "selected_bg_color": "accent.base",
    "borders_color": "border.default",
    "alt_borders_color": "border.subtle",
    "warning_color": "status.warning",
    "error_color": "status.destructive",
    "success_color": "status.success",
    "destructive_color": "status.destructive",
    "osd_fg_color": "text.primary",
    "osd_text_color": "text.primary",
    "drop_target_color": "status.success",
}

# SASS expressions derived from tokens (kept translucent like upstream OSD)
EXPRESSION_MAP = {
    "osd_bg_color": "transparentize({bg.base_darker}, 0.1)",
    "osd_borders_color": "transparentize({border.default}, 0.3)",
}


def load_tokens() -> dict:
    # Flatten palette tokens into a dotted-path -> value dict.
    import json
    tokens = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())

    def flatten(node: dict, prefix: str = "") -> dict:
        flat = {}
        for key, value in node.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flat.update(flatten(value, path))
            else:
                flat[path] = value
        return flat
    return flatten(tokens["color"])


def patch_colors(tokens: dict) -> None:
    # Copy upstream SASS into the work dir and swap base variables for token values.
    if WORK.exists():
        shutil.rmtree(WORK)
    shutil.copytree(UPSTREAM, WORK)
    colors = WORK / "_colors.scss"
    css = colors.read_text()
    patched = 0
    for var, token_path in VARIABLE_MAP.items():
        pattern = re.compile(rf"(?m)^\${var}:\s*.*;$")
        if not pattern.search(css):
            print(f"variable ${var} not found in upstream _colors.scss", file=sys.stderr)
            sys.exit(2)
        css = pattern.sub(f"${var}: {tokens[token_path]};", css)
        patched += 1
    for var, template in EXPRESSION_MAP.items():
        expression = template
        for token_path, value in tokens.items():
            if isinstance(value, str):
                expression = expression.replace("{" + token_path + "}", value)
        pattern = re.compile(rf"(?m)^\${var}:\s*.*;$")
        if not pattern.search(css):
            print(f"variable ${var} not found in upstream _colors.scss", file=sys.stderr)
            sys.exit(2)
        css = pattern.sub(f"${var}: {expression};", css)
        patched += 1
    colors.write_text(css)
    print(f"patched {patched} base variables in _colors.scss")


def compile_sass(entry: str, output: Path) -> None:
    # Compile one SASS entry file with sassc into the theme output dir.
    result = subprocess.run(["sassc", str(WORK / entry), str(output)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"sassc failed for {entry}:\n{result.stderr}", file=sys.stderr)
        sys.exit(3)
    # prepend the project header after compilation
    css = HEADER + output.read_text()
    output.write_text(css)


def verify(output: Path) -> None:
    # Guard: theme families present, upstream default palettes fully gone.
    css = output.read_text().lower()
    checks = {
        "sage accent family": any(c in css for c in ("#8fb8a6", "#70a48d", "#aeccbf")),
        "charcoal-teal base family": any(c in css for c in ("#0f141b", "#16222a", "#121a21", "#18252d")),
        "no upstream blue #3584e4": "#3584e4" not in css,
        "no adwaita light bg #f6f5f4": "#f6f5f4" not in css,
        "no upstream osd grey #3a3a3a": "#3a3a3a" not in css,
    }
    for name, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if not all(checks.values()):
        sys.exit(4)


def main() -> int:
    # Patch, compile (gtk.css and gtk-dark.css are the same dark build), verify.
    tokens = load_tokens()
    patch_colors(tokens)
    OUT.mkdir(parents=True, exist_ok=True)
    compile_sass("gtk-contained-dark.scss", OUT / "gtk-dark.css")
    shutil.copy(OUT / "gtk-dark.css", OUT / "gtk.css")
    shutil.copytree(UPSTREAM / "assets", OUT / "assets", dirs_exist_ok=True)
    verify(OUT / "gtk-dark.css")
    print(f"GTK3 theme written to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
