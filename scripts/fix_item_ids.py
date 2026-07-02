#!/usr/bin/env python3
"""Apply known-bad item ID fixes across overrides and generator scripts."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Old registry id -> correct id for installed mod versions.
REPLACEMENTS: dict[str, str] = {
    "mekanism:basic_factory": "mekanism:basic_smelting_factory",
    "mekanism:heat_generator": "mekanismgenerators:heat_generator",
    "appliedenergistics2:controller": "ae2:controller",
    "immersiveengineering:cokeoven": "immersiveengineering:coke_oven",
    "draconicevolution:draconic_core": "draconicevolution:awakened_core",
    "draconicevolution:crafting_injector": "draconicevolution:wyvern_crafting_injector",
    "draconicevolution:chaotic_shard": "draconicevolution:chaos_shard",
    "enderio:wireless_antenna": "enderio:vibrant_capacitor_bank",
    "enderio:soul_vial": "enderio:empty_soul_vial",
    '"kubejs:journal_page"': '"kubejs:journal_page_00"',
    "ae2wtlib:wireless_terminal": "ae2wtlib:wireless_universal_terminal",
    "alexsmobs:grizzly_bear_fur": "alexsmobs:bear_fur",
    "apotheosis:mythic_gem": "apotheosis:mythic_material",
    "cataclysm:iron_sword": "cataclysm:black_steel_sword",
    "mowziesmobs:wroughtnaut_helmet": "mowziesmobs:wrought_helmet",
    "relics:horseshoe": "relics:lucky_horseshoe",
    "relics:midnight_roast": "relics:midnight_robe",
    "silentgear:rough_pickaxe": "silentgear:pickaxe",
    "thermal:copper_ingot": "minecraft:copper_ingot",
    "thermal:redstone_furnace": "thermal:machine_furnace",
    "thermal:sawmill": "thermal:machine_sawmill",
    "thermal:upgrade_augment_1": "thermal:slot_seal",
    "thermal:upgrade_augment_3": "thermal:flux_capacitor",
}

TARGET_DIRS = [
    ROOT / "overrides",
    ROOT / "scripts",
]


def replace_in_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS.items():
        if old.startswith('"'):
            text = text.replace(old, new)
        else:
            text = re.sub(rf"(?<![a-z0-9_]){re.escape(old)}(?![a-z0-9_])", new, text)
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return 1
    return 0


def main() -> None:
    changed = 0
    for base in TARGET_DIRS:
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".json", ".snbt", ".py", ".js"}:
                continue
            if "quests_backup_original" in path.parts or "archive" in path.parts:
                continue
            changed += replace_in_file(path)
    print(f"Updated {changed} files")


if __name__ == "__main__":
    main()
