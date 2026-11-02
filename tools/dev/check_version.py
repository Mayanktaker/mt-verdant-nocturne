# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Assert every user-visible version string matches the root VERSION file.

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    # Compare VERSION against README, tokens metadata and the release notes file.
    version = (REPO_ROOT / "VERSION").read_text().strip()
    problems = []

    tokens = json.loads((REPO_ROOT / "palette" / "tokens.json").read_text())
    if tokens.get("meta", {}).get("version") != version:
        problems.append(f"palette/tokens.json meta.version = {tokens.get('meta', {}).get('version')!r}, expected {version!r}")

    readme = (REPO_ROOT / "README.md").read_text()
    badge = re.search(r"release-v(\d+\.\d+\.\d+)", readme)
    if not badge or badge.group(1) != version:
        problems.append(f"README release badge = {badge.group(1) if badge else 'missing'}, expected {version}")

    notes = REPO_ROOT / "docs" / "release-notes" / f"v{version}.md"
    if not notes.exists():
        problems.append(f"missing release notes: {notes.relative_to(REPO_ROOT)}")

    if problems:
        print("version check failed:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(f"version check: {version} consistent across VERSION, tokens, README and release notes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
