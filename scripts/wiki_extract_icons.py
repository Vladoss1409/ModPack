#!/usr/bin/env python3
"""Extract item/block icon textures referenced in wiki articles.

Articles use inline markers: {{icon namespace/texture_stem}}

This script scans markdown, finds all references, pulls matching PNGs from mod
jars (item texture first, then block), saves to wiki/public/textures/icons/ and
updates wiki/src/data/icons.json.
"""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS = ROOT / "mods"
CONTENT = ROOT / "wiki" / "src" / "content"
OUT = ROOT / "wiki" / "public" / "textures" / "icons"
MANIFEST = ROOT / "wiki" / "src" / "data" / "icons.json"
REFS_FILE = ROOT / "wiki" / "src" / "data" / "icon_refs.json"

ICON_RE = re.compile(r"\{\{icon\s+([a-z0-9_./-]+)\}\}", re.I)

# wiki namespace -> jar asset namespaces to try (order matters)
NS_ALIASES: dict[str, list[str]] = {
    "ae2": ["ae2", "appliedenergistics2"],
    "mekanism": ["mekanism"],
    "thermal": ["thermal"],
    "enderio": ["enderio"],
    "powah": ["powah"],
    "draconicevolution": ["draconicevolution"],
    "immersiveengineering": ["immersiveengineering"],
    "appliedenergistics2": ["ae2", "appliedenergistics2"],
    "twilightforest": ["twilightforest"],
    "aether": ["aether"],
    "farmersdelight": ["farmersdelight"],
    "sophisticatedbackpacks": ["sophisticatedbackpacks"],
    "sophisticatedstorage": ["sophisticatedstorage"],
    "projecte": ["projecte"],
    "fluxnetworks": ["fluxnetworks"],
    "irons_spellbooks": ["irons_spellbooks"],
    "cataclysm": ["cataclysm"],
    "apotheosis": ["apotheosis"],
}


def collect_refs() -> set[str]:
    refs: set[str] = set()
    if REFS_FILE.is_file():
        refs.update(json.loads(REFS_FILE.read_text(encoding="utf-8")))
    for md in CONTENT.rglob("*.md"):
        refs.update(ICON_RE.findall(md.read_text(encoding="utf-8")))
    return refs


def jar_index() -> list[tuple[Path, list[str]]]:
    out: list[tuple[Path, list[str]]] = []
    for jar in sorted(MODS.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as zf:
                out.append((jar, zf.namelist()))
        except zipfile.BadZipFile:
            continue
    return out


def namespaces_for(ref: str) -> tuple[str, str, list[str]]:
    if "/" not in ref:
        raise ValueError(f"bad icon ref (need ns/stem): {ref}")
    ns, stem = ref.split("/", 1)
    return ns, stem, NS_ALIASES.get(ns, [ns])


def find_texture(names: list[str], asset_ns: str, stem: str) -> str | None:
    stem_low = stem.lower()
    norm = {n.replace("\\", "/").lower(): n for n in names if n.lower().endswith(".png")}

    exact_paths = [
        f"assets/{asset_ns}/textures/item/{stem}.png",
        f"assets/{asset_ns}/textures/items/{stem}.png",
        f"assets/{asset_ns}/textures/block/{stem}.png",
        f"assets/{asset_ns}/textures/blocks/{stem}.png",
        f"assets/{asset_ns}/textures/block/models/{stem}.png",
    ]
    for face in ("front_active", "front", "top", "side", "back"):
        exact_paths.append(f"assets/{asset_ns}/textures/block/{stem}/{face}.png")
    for p in exact_paths:
        if p.lower() in norm:
            return norm[p.lower()]

    # fuzzy: exact stem filename under item/block texture trees
    for n in names:
        nl = n.replace("\\", "/").lower()
        if not nl.endswith(".png"):
            continue
        if "/textures/item" not in nl and "/textures/block" not in nl:
            if "/textures/items" not in nl and "/textures/blocks" not in nl:
                continue
        if Path(nl).stem.lower() == stem_low:
            return n
        # block folder name match: .../block/enrichment_chamber/front.png
        parts = Path(nl).parts
        for i, part in enumerate(parts):
            if part == "block" and i + 1 < len(parts) and parts[i + 1].lower() == stem_low:
                return n
    return None


def extract_ref(ref: str, jars: list[tuple[Path, list[str]]]) -> bool:
    ns, stem, asset_namespaces = namespaces_for(ref)
    out_file = OUT / ns / f"{stem.replace('/', '_')}.png"
    if out_file.is_file() and out_file.stat().st_size > 50:
        return True
    for jar, names in jars:
        for asset_ns in asset_namespaces:
            hit = find_texture(names, asset_ns, stem)
            if not hit:
                continue
            try:
                with zipfile.ZipFile(jar) as zf:
                    data = zf.read(hit)
            except (KeyError, zipfile.BadZipFile):
                continue
            if len(data) < 50:
                continue
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_bytes(data)
            return True
    return False


def main() -> int:
    refs = sorted(collect_refs())
    if not refs:
        print("No {{icon ns/stem}} references found in wiki content.")
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text("{}\n", encoding="utf-8")
        return 0

    jars = jar_index()
    manifest: dict[str, str] = {}
    ok = miss = 0
    missing: list[str] = []

    for ref in refs:
        ns, stem, _ = namespaces_for(ref)
        out_rel = f"textures/icons/{ns}/{stem.replace('/', '_')}.png"
        if extract_ref(ref, jars):
            manifest[ref] = out_rel
            print(f"OK  {ref}")
            ok += 1
        else:
            print(f"MISS {ref}")
            miss += 1
            missing.append(ref)

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nIcons: {ok} ok, {miss} missing -> {OUT}")
    if missing:
        print("Missing:", ", ".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
