# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Fail when a tweak/override contains a color literal that is not a palette token.

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())


def token_colors(node) -> set:
    # Collect every hex value declared anywhere in the token tree.
    found = set()
    if isinstance(node, dict):
        for value in node.values():
            found |= token_colors(value)
    elif isinstance(node, list):
        for value in node:
            found |= token_colors(value)
    elif isinstance(node, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", node):
        found.add(node.lower())
    return found


def main() -> int:
    # Templates must contain no literals at all: colors come through {{token}} placeholders.
    offenders = []
    sources = list((REPO_ROOT / "src" / "tweaks").rglob("*.css")) + [REPO_ROOT / "src" / "gtk-4.0" / "overrides.css", REPO_ROOT / "src" / "gtk-2.0" / "gtkrc"]
    for path in sources:
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if re.search(r"#[0-9a-fA-F]{3,8}", line):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{number}: hex literal")
            if re.search(r"rgba?\(\s*\d", line):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{number}: raw rgb()/rgba() literal")
            if re.search(r"\{\{geometry\.(radius|space)\.[a-z]+\}\}(?!px|em|%)", line):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{number}: geometric token without unit")

    if offenders:
        print("color literals in templates (use {{dotted.token}} placeholders):", file=sys.stderr)
        for item in offenders:
            print(f"  {item}", file=sys.stderr)
        return 1
    print(f"color check: {len(sources)} template files use tokens only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
