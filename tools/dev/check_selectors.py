# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Assert every selector used by the Shell tweaks exists in the vendored upstream CSS.
# #panelBox is an actor added in JS, so it cannot be verified from CSS and is allowed.

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ACTOR_ALLOWLIST = {"#panelBox"}
TOKEN_RE = re.compile(r"[.#][A-Za-z][A-Za-z0-9_-]*")


def selectors_from(css: str) -> set:
    # Extract class/id tokens from selector blocks (properties are ignored).
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    tokens = set()
    for block in re.findall(r"([^{}]+)\{", css):
        for selector in block.split(","):
            tokens |= set(TOKEN_RE.findall(selector))
    return tokens


def main() -> int:
    # Compare tweak selectors against every vendored Shell major.
    tweak_tokens = set()
    for path in (REPO_ROOT / "src" / "tweaks" / "shell").glob("*.css"):
        tweak_tokens |= selectors_from(path.read_text())

    majors = sorted(p.name.split("-")[-1] for p in (REPO_ROOT / "src" / "shell").glob("upstream-*"))
    if not majors:
        print("no vendored upstream Shell CSS found", file=sys.stderr)
        return 1

    failed = False
    for major in majors:
        upstream = (REPO_ROOT / "src" / "shell" / f"upstream-{major}" / "gnome-shell-dark.css").read_text()
        known = selectors_from(upstream) | ACTOR_ALLOWLIST
        missing = sorted(t for t in tweak_tokens if t not in known)
        if missing:
            failed = True
            print(f"Shell {major}: selectors missing upstream: {', '.join(missing)}", file=sys.stderr)
        else:
            print(f"Shell {major}: all {len(tweak_tokens)} tweak selectors resolve")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
