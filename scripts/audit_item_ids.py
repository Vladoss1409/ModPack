#!/usr/bin/env python3
"""Audit Patchouli + FTB Quests item IDs against installed mod jars."""
from __future__ import annotations

import json
import os
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "overrides"
MODS = Path(os.environ["MODPACK_MODS"]) if os.environ.get("MODPACK_MODS") else (
    Path(os.environ["APPDATA"]) / ".minecraft" / "versions" / "ModPack" / "mods"
)


def load_registry(mods_dir: Path) -> dict[str, str]:
    registry: dict[str, str] = {}

    def scan_jar(jar_path: Path, label: str) -> None:
        try:
            with zipfile.ZipFile(jar_path) as zf:
                for name in zf.namelist():
                    if name.startswith("META-INF/jarjar/") and name.endswith(".jar"):
                        import tempfile

                        nested = Path(tempfile.gettempdir()) / Path(name).name
                        nested.write_bytes(zf.read(name))
                        scan_jar(nested, label)
                        continue
                    for kind in ("item", "block"):
                        marker = f"/models/{kind}/"
                        if marker not in name or not name.endswith(".json"):
                            continue
                        parts = name.split("/")
                        if len(parts) < 4:
                            continue
                        ns = parts[1]
                        item = name.split(marker, 1)[1][:-5]
                        registry.setdefault(f"{ns}:{item}", label)
        except zipfile.BadZipFile:
            print(f"WARN: bad jar {jar_path.name}", file=sys.stderr)

    for sub in ("kubejs", "cooptech"):
        models = OVERRIDES / "kubejs" / "assets" / sub / "models" / "item"
        if models.is_dir():
            for path in models.glob("*.json"):
                registry[f"{sub}:{path.stem}"] = "kubejs"

    for jar in sorted(mods_dir.glob("*.jar")):
        scan_jar(jar, jar.name)

    return registry


def collect_refs() -> list[tuple[str, str, str]]:
    refs: list[tuple[str, str, str]] = []
    patchouli = OVERRIDES / "patchouli_books"
    if patchouli.is_dir():
        for path in patchouli.rglob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            rel = str(path.relative_to(OVERRIDES))
            icon = data.get("icon")
            if isinstance(icon, str) and ":" in icon and not icon.startswith("cooptech:"):
                refs.append((icon, rel, "icon"))
            for page in data.get("pages", []):
                if not isinstance(page, dict):
                    continue
                for key in ("item", "block"):
                    value = page.get(key)
                    if isinstance(value, str) and ":" in value:
                        refs.append((value, rel, f"page.{key}"))

    quests = OVERRIDES / "config" / "ftbquests" / "quests"
    id_re = re.compile(r'(?:item|id):\s*"([^"]+)"')
    if quests.is_dir():
        for path in quests.rglob("*.snbt"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            rel = str(path.relative_to(OVERRIDES))
            for match in id_re.finditer(text):
                value = match.group(1)
                if ":" not in value:
                    continue
                if value.startswith(("ftbquests:", "kubejs:quest_")):
                    continue
                refs.append((value, rel, "snbt"))

    return refs


def suggest(registry: dict[str, str], item_id: str) -> list[str]:
    if ":" not in item_id:
        return []
    ns, path = item_id.split(":", 1)
    norm = path.replace("_", "")
    out: list[str] = []
    for key in registry:
        if not key.startswith(f"{ns}:"):
            continue
        candidate = key.split(":", 1)[1]
        if path in candidate or norm in candidate.replace("_", ""):
            out.append(key)
            if len(out) >= 5:
                break
    return out


def main() -> int:
    if not MODS.is_dir():
        print(f"ERROR: mods dir not found: {MODS}")
        return 1

    registry = load_registry(MODS)
    refs = collect_refs()

    seen: dict[str, tuple[str, str]] = {}
    for item_id, file, ctx in refs:
        seen.setdefault(item_id, (file, ctx))

    invalid: list[tuple[str, str, str]] = []
    for item_id, (file, ctx) in sorted(seen.items()):
        ns = item_id.split(":", 1)[0]
        if ns == "minecraft":
            continue
        if item_id.startswith("cooptech:textures/"):
            continue
        if item_id not in registry:
            invalid.append((item_id, file, ctx))

    print(f"Registry items: {len(registry)}")
    print(f"Unique referenced IDs: {len(seen)}")
    print(f"INVALID: {len(invalid)}")
    for item_id, file, ctx in invalid:
        print(f"  {item_id}")
        print(f"    @ {file} ({ctx})")
        sug = suggest(registry, item_id)
        if sug:
            print(f"    maybe: {', '.join(sug)}")

    return 1 if invalid else 0


if __name__ == "__main__":
    sys.exit(main())
