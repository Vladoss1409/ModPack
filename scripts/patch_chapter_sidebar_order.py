#!/usr/bin/env python3
"""Patch side chapter group/order for interleaved T0+sides…T5 sidebar."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from quests_build_sides import GROUP_MAIN, SIDE_MENU_ORDER  # noqa: E402

CHAPTERS = ROOT / "overrides" / "config" / "ftbquests" / "quests" / "chapters"
BACKUP = ROOT / "overrides" / "config" / "ftbquests" / "quests_backup_original" / "chapters"

POST_MENU_ORDER = {
    "side_post_caves": 62,
    "side_post_bossfarm": 63,
    "side_post_epilogue": 64,
}


def patch_chapter_meta(path: Path, group: str, order_index: int) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'\tgroup: "[^"]+"', f'\tgroup: "{group}"', text, count=1)
    text = re.sub(r"\torder_index: \d+", f"\torder_index: {order_index}", text, count=1)
    path.write_text(text, encoding="utf-8")


def remove_welcome() -> None:
    welcome = CHAPTERS / "main_00_welcome.snbt"
    if not welcome.is_file():
        return
    BACKUP.mkdir(parents=True, exist_ok=True)
    dest = BACKUP / "main_00_welcome.snbt"
    if not dest.is_file():
        welcome.replace(dest)
        print("  archived main_00_welcome.snbt")
    else:
        welcome.unlink()
        print("  removed main_00_welcome.snbt")


def main() -> int:
    remove_welcome()

    patched = 0
    for name, order in {**SIDE_MENU_ORDER, **POST_MENU_ORDER}.items():
        path = CHAPTERS / f"{name}.snbt"
        if not path.is_file():
            print(f"  skip missing {name}.snbt")
            continue
        patch_chapter_meta(path, GROUP_MAIN, order)
        patched += 1
        print(f"  {name}: group=Прохождение order={order}")

    print(f"Patched {patched} side/post chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
