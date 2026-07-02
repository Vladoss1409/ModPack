#!/usr/bin/env python3
"""Write Patchouli branch entries from side_lore.py."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from quest_content_v1 import POST_SIDE_BRANCHES, SIDE_BRANCHES  # noqa: E402
from side_lore import SIDE_BRANCH_LORE, side_patchouli_text  # noqa: E402

OUT = ROOT / "overrides" / "patchouli_books" / "expedition_journal" / "en_us" / "entries" / "branches"

NAMES = {
    "side_kitchen": "Полевая кухня",
    "side_storage": "Склад экспедиции",
    "side_bestiary": "Полевой бестиарий",
    "side_thermal": "Тепловой контур",
    "side_powah": "Резонанс Powah",
    "side_immersive": "Индустриальная ковка",
    "side_apotheosis": "Апофеоз",
    "side_silent_gear": "Ковка Silent Gear",
    "side_mekanism": "Промышленный узел",
    "side_enderio": "Проводник Ender IO",
    "side_flux": "Flux Networks",
    "side_arcane": "Арканум поля",
    "side_network": "Молекулярная сеть",
    "side_twilight": "Сумеречный рубеж",
    "side_draconic": "Драконья эволюция",
    "side_cataclysm": "Бездна Cataclysm",
    "side_relics": "Реликвии",
    "side_post_caves": "Печери розлому",
    "side_post_bossfarm": "Бос-фарм якоря",
    "side_post_epilogue": "Епілог модів",
}

SORT = {
    "side_kitchen": 2,
    "side_storage": 3,
    "side_bestiary": 4,
    "side_thermal": 1,
    "side_powah": 5,
    "side_immersive": 6,
    "side_apotheosis": 7,
    "side_silent_gear": 8,
    "side_mekanism": 9,
    "side_enderio": 10,
    "side_flux": 11,
    "side_arcane": 12,
    "side_network": 13,
    "side_twilight": 14,
    "side_draconic": 15,
    "side_cataclysm": 16,
    "side_relics": 17,
    "side_post_caves": 18,
    "side_post_bossfarm": 19,
    "side_post_epilogue": 20,
}


def write_branch_entry(fn: str, title: str, icon: str) -> None:
    if fn not in SIDE_BRANCH_LORE:
        return
    text = side_patchouli_text(fn)
    howto = (
        "$(bold)Как проходить$()$(br2)Квесты идут цепочкой после рубежа главного тира. "
        "Описания — от первого лица, как записи в блокноте экспедиции.$(br2)"
        "$(italic)«Сайд не обязателен для якоря — но даёт силу и удобство.»$()"
    )
    if fn.startswith("side_post_"):
        howto = (
            "$(bold)Після якоря$()$(br2)Ветка открывается после финала T5 и выбора пути в хабе «Після якоря». "
            "Описания — от первого лица.$(br2)"
            "$(italic)«Эпилог — для тех, кто хочет закрыть всё до конца.»$()"
        )
    entry = {
        "name": NAMES.get(fn, title),
        "icon": icon,
        "category": "patchouli:branches",
        "advancement": f"cooptech:journal/{fn}",
        "secret": True,
        "sortnum": SORT.get(fn, 99),
        "pages": [
            {"type": "patchouli:text", "text": text},
            {"type": "patchouli:text", "text": howto},
        ],
    }
    name_map = {
        "side_kitchen": "kitchen",
        "side_storage": "storage",
        "side_bestiary": "bestiary",
        "side_thermal": "thermal",
        "side_powah": "powah",
        "side_immersive": "immersive",
        "side_apotheosis": "apotheosis",
        "side_silent_gear": "silent_gear",
        "side_mekanism": "mekanism",
        "side_enderio": "enderio",
        "side_flux": "flux",
        "side_arcane": "arcane",
        "side_network": "network",
        "side_twilight": "twilight",
        "side_draconic": "draconic",
        "side_cataclysm": "cataclysm",
        "side_relics": "relics",
        "side_post_caves": "post_caves",
        "side_post_bossfarm": "post_bossfarm",
        "side_post_epilogue": "post_epilogue",
    }
    path = OUT / f"{name_map[fn]}.json"
    path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {path.name}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for fn, title, icon, *_ in SIDE_BRANCHES:
        write_branch_entry(fn, title, icon)
    for fn, title, icon, *_rest in POST_SIDE_BRANCHES:
        write_branch_entry(fn, title, icon)


if __name__ == "__main__":
    main()
