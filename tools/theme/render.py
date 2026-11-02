#!/usr/bin/env python3
# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Render token placeholders ({{dotted.path}}) in CSS tweaks for a chosen accent flavor.

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from palette import FLAVORS, load_tokens, render_file

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    # Parse CLI and render either a single file or a whole directory tree.
    parser = argparse.ArgumentParser(description="Render MT Verdant Nocturne CSS tweaks")
    parser.add_argument("--accent", default="sage", choices=FLAVORS)
    parser.add_argument("--in", dest="source", type=Path, help="single template file")
    parser.add_argument("--out", dest="target", type=Path, help="single output file")
    parser.add_argument("--dir", type=Path, help="template directory (all *.css)")
    parser.add_argument("--out-dir", type=Path, help="output directory")
    args = parser.parse_args()

    tokens = load_tokens()
    if args.source:
        if not args.target:
            parser.error("--in requires --out")
        render_file(args.source, args.target, tokens, args.accent)
        print(f"rendered {args.target}")
        return 0
    if args.dir:
        if not args.out_dir:
            parser.error("--dir requires --out-dir")
        count = 0
        for source in sorted(args.dir.rglob("*.css")):
            target = args.out_dir / source.relative_to(args.dir)
            render_file(source, target, tokens, args.accent)
            count += 1
        print(f"rendered {count} files into {args.out_dir}")
        return 0
    parser.error("nothing to render: pass --in/--out or --dir/--out-dir")
    return 2


if __name__ == "__main__":
    sys.exit(main())
