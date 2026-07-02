#!/usr/bin/env python3
"""Restore side chapter layout from dist snapshot and patch unlock IDs to T0–T5."""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from quest_content_v1 import SIDE_BRANCHES  # noqa: E402
from quests_build_sides import GROUP_MAIN, SIDE_MENU_ORDER, SIDE_UNLOCKS, main_qid  # noqa: E402

DIST = ROOT / "dist" / "MyModPack-0.1.0-server" / "config" / "ftbquests" / "quests" / "chapters"
OUT = ROOT / "overrides" / "config" / "ftbquests" / "quests" / "chapters"
T5_FINALE = "5225A0000000001A"

POST_MENU_ORDER = {
    "side_post_caves": 62,
    "side_post_bossfarm": 63,
    "side_post_epilogue": 64,
}


def build_unlock_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for fn, _title, _ic, _grp, old_unlock, _ord_i, _prefix, _quests, _layout in SIDE_BRANCHES:
        if fn not in SIDE_UNLOCKS:
            continue
        tier, _gate, main_q, _main_title = SIDE_UNLOCKS[fn]
        mapping[old_unlock] = main_qid(tier, main_q)
    return mapping


def patch_sidebar_order(path: Path) -> None:
    stem = path.stem
    order = SIDE_MENU_ORDER.get(stem) or POST_MENU_ORDER.get(stem)
    if order is None:
        return
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'\tgroup: "[^"]+"', f'\tgroup: "{GROUP_MAIN}"', text, count=1)
    text = re.sub(r"\torder_index: \d+", f"\torder_index: {order}", text, count=1)
    path.write_text(text, encoding="utf-8")


def patch_side_file(path: Path, unlock_map: dict[str, str]) -> int:
    text = path.read_text(encoding="utf-8")
    count = 0
    for old, new in unlock_map.items():
        needle = f'dependencies: ["{old}"]'
        if needle in text:
            text = text.replace(needle, f'dependencies: ["{new}"]')
            count += 1
    text = re.sub(r'filename: "([^"]+)\.snbt"', r'filename: "\1"', text)
    if path.name.startswith("side_post_"):
        text = re.sub(
            rf'dependencies: \["{T5_FINALE}", "A90000000000000[234]"\]',
            f'dependencies: ["{T5_FINALE}"]',
            text,
        )
    path.write_text(text, encoding="utf-8")
    patch_sidebar_order(path)
    return count


def main() -> int:
    if not DIST.is_dir():
        print(f"ERROR: dist snapshot missing: {DIST}")
        return 1

    unlock_map = build_unlock_map()
    for src in sorted(DIST.glob("side_*.snbt")):
        dst = OUT / src.name
        shutil.copy2(src, dst)
        n = patch_side_file(dst, unlock_map)
        print(f"  restored {src.name} ({n} unlock patch(es))")

    hub = OUT / "main_post_anchor.snbt"
    if hub.is_file():
        hub.unlink()
        print("  removed main_post_anchor.snbt")

    return 0


if __name__ == "__main__":
    sys.exit(main())
