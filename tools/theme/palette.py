# © Mayanktaker Computers & Web Development | https://mayanktaker.com
# Shared palette loading, accent resolution and token rendering for MT Verdant Nocturne.

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS_PATH = REPO_ROOT / "palette" / "tokens.json"
FLAVORS = ("sage", "emerald", "moss", "pine")


def load_tokens(path: Path = TOKENS_PATH) -> dict:
    # Load the single source of truth.
    return json.loads(Path(path).read_text())


def flatten(node, prefix: str = "") -> dict:
    # Flatten nested dicts into dotted paths; lists are ignored.
    flat = {}
    for key, value in node.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten(value, path))
        elif not isinstance(value, list):
            flat[path] = value
    return flat


def resolve_accent(tokens: dict, flavor: str = "sage") -> dict:
    # Return the chosen accent family, rejecting unknown flavors.
    if flavor not in FLAVORS:
        raise ValueError(f"unknown accent flavor '{flavor}' (choose one of: {', '.join(FLAVORS)})")
    data = tokens["color"]["accent_flavors"][flavor]
    return {
        "base": data["base"],
        "strong": data["strong"],
        "dim": data["dim"],
        "text_on_accent": data["text_on"],
    }


def flat_with_accent(tokens: dict, flavor: str = "sage") -> dict:
    # Flatten color/art/geometry and bind accent.* to the chosen flavor.
    flat = flatten(tokens["color"])
    flat.update(flatten(tokens["art"], "art"))
    flat.update(flatten(tokens["geometry"], "geometry"))
    accent = resolve_accent(tokens, flavor)
    for key, value in accent.items():
        flat[f"accent.{key}"] = value
    return flat


def hex_to_rgb(hex_color: str) -> str:
    # Convert #RRGGBB into a CSS "r, g, b" triplet.
    value = hex_color.lstrip("#")
    return ", ".join(str(int(value[i : i + 2], 16)) for i in (0, 2, 4))


def render_template(text: str, tokens: dict, flavor: str = "sage") -> str:
    # Replace {{dotted.path}} and {{dotted.path.rgb}} placeholders with token values.
    flat = flat_with_accent(tokens, flavor)

    def substitute(match) -> str:
        path = match.group(1)
        if path not in flat:
            raise KeyError(f"unknown token placeholder: {path}")
        value = flat[path]
        if match.group(2):
            if not isinstance(value, str) or not value.startswith("#"):
                raise TypeError(f"token {path} is not a hex color")
            return hex_to_rgb(value)
        return str(value)

    return re.sub(r"\{\{\s*([A-Za-z0-9_.]+?)(\.rgb)?\s*\}\}", substitute, text)


def render_file(source: Path, target: Path, tokens: dict, flavor: str = "sage") -> None:
    # Render one template file, creating parent directories.
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_template(Path(source).read_text(), tokens, flavor))
