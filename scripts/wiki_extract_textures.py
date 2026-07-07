#!/usr/bin/env python3
"""Extract block textures from mod jars for the wiki 3D viewer."""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS = ROOT / "mods"
OUT = ROOT / "wiki" / "public" / "textures" / "blocks"
MANIFEST = ROOT / "wiki" / "src" / "data" / "texture_manifest.json"

# modid -> list of (output_stem, jar_path_suffix or stem for fuzzy)
TEXTURE_ALIASES: dict[str, list[tuple[str, str]]] = {
    "powah": [
        ("reactor_core", "textures/model/tile/reactor_block_nitro.png"),
    ],
    "draconicevolution": [
        ("crafting_injector", "textures/block/crafting/injector_top.png"),
        ("energy_io", "textures/block/energy_transfuser.png"),
    ],
    "immersiveengineering": [
        ("rs_engineering", "textures/block/metal_decoration/rs_engineering.png"),
    ],
    "next_ae": [
        ("massive_crafter_core", "textures/block/massive_crafter/core.png"),
        ("massive_crafter_frame", "textures/block/massive_crafter/frame.png"),
        ("massive_crafter_wall", "textures/block/massive_crafter/wall.png"),
        ("massive_crafter_glass", "textures/block/massive_crafter/glass.png"),
        ("massive_crafter_pattern", "textures/block/massive_crafter/template_provider.png"),
        ("massive_crafter_speed", "textures/block/massive_crafter/accelerator.png"),
    ],
}

TEXTURES: dict[str, list[str]] = {
    "powah": ["uraninite_block", "reactor_core"],
    "draconicevolution": [
        "draconium_block",
        "awakened_draconium_block",
        "crafting_core",
        "crafting_injector",
        "energy_io",
        "reactor_core",
        "energy_core",
        "reactor_stabilizer",
    ],
    "mekanism": [
        "digital_miner",
        "structural_glass",
        "steel_casing",
        "industrial_alarm",
    ],
    "appliedenergistics2": [
        "controller",
        "drive",
        "chest",
        "energy_acceptor",
        "quartz_glass",
    ],
    "immersiveengineering": [
        "cokebrick",
        "blastbrick",
        "blastbrick_reinforced",
        "coke_oven",
        "blast_furnace",
        "metal_press",
        "light_engineering",
        "heavy_engineering",
        "rs_engineering",
        "sheetmetal_steel",
    ],
    "next_ae": [
        "massive_crafter_core",
        "massive_crafter_frame",
        "massive_crafter_wall",
        "massive_crafter_glass",
        "massive_crafter_pattern",
        "massive_crafter_speed",
    ],
}


def find_jar(modid: str) -> Path | None:
    if not MODS.is_dir():
        return None
    for jar in MODS.glob("*.jar"):
        low = jar.name.lower()
        if modid.replace("_", "") in low.replace("_", "").replace("-", ""):
            return jar
        if modid == "appliedenergistics2" and "appliedenergistics2" in low:
            return jar
        if modid == "next_ae" and "next_ae" in low:
            return jar
    return None


def extract_by_suffix(jar: Path, modid: str, stem: str, suffix: str) -> bool:
    out_dir = OUT / modid
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{stem}.png"
    suffix = suffix.replace("\\", "/").lower()
    try:
        with zipfile.ZipFile(jar) as zf:
            for name in zf.namelist():
                n = name.replace("\\", "/").lower()
                if n.endswith(suffix):
                    out_file.write_bytes(zf.read(name))
                    return True
    except zipfile.BadZipFile:
        return False
    return False


def extract_texture(jar: Path, modid: str, stem: str) -> bool:
    out_dir = OUT / modid
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{stem}.png"
    if out_file.is_file() and out_file.stat().st_size > 100:
        return True

    patterns = [
        re.compile(rf"assets/{re.escape(modid)}/textures/block/{re.escape(stem)}\.png$", re.I),
        re.compile(rf"assets/{re.escape(modid)}/textures/blocks/{re.escape(stem)}\.png$", re.I),
    ]
    # AE2 sometimes uses ae2 namespace
    if modid == "appliedenergistics2":
        patterns.append(re.compile(rf"assets/ae2/textures/block/{re.escape(stem)}\.png$", re.I))

    try:
        with zipfile.ZipFile(jar) as zf:
            for name in zf.namelist():
                for pat in patterns:
                    if pat.search(name.replace("\\", "/")):
                        out_file.write_bytes(zf.read(name))
                        return True
            # fuzzy: stem contained in path
            stem_low = stem.lower()
            for name in zf.namelist():
                n = name.replace("\\", "/").lower()
                if not n.endswith(".png"):
                    continue
                if "/textures/block" not in n and "/textures/blocks" not in n:
                    continue
                if stem_low in Path(n).stem.lower():
                    out_file.write_bytes(zf.read(name))
                    print(f"  fuzzy match: {stem} <- {name}")
                    return True
    except zipfile.BadZipFile:
        return False
    return False


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, str] = {}
    ok = 0
    miss = 0

    for modid, stems in TEXTURES.items():
        jar = find_jar(modid)
        if not jar:
            print(f"[SKIP] no jar for {modid}")
            miss += len(stems)
            continue
        print(f"[JAR] {modid} <- {jar.name}")
        for stem in stems:
            if extract_texture(jar, modid, stem):
                manifest[f"{modid}/{stem}"] = f"textures/blocks/{modid}/{stem}.png"
                print(f"  OK  {stem}")
                ok += 1
            else:
                print(f"  MISS {stem}")
                miss += 1
        for stem, suffix in TEXTURE_ALIASES.get(modid, []):
            if (OUT / modid / f"{stem}.png").is_file():
                continue
            if extract_by_suffix(jar, modid, stem, suffix):
                manifest[f"{modid}/{stem}"] = f"textures/blocks/{modid}/{stem}.png"
                print(f"  OK  {stem} (alias)")
                ok += 1
            else:
                print(f"  MISS alias {stem}")
                miss += 1

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nExtracted {ok}, missing {miss} -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
