#!/usr/bin/env python3
"""Undo accidental journal_page_00_ prefix corruption from fix_item_ids."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [ROOT / "overrides", ROOT / "scripts"]


def fix_text(text: str) -> str:
    text = text.replace("kubejs:journal_page_", "kubejs:journal_page_")
    text = text.replace("'kubejs:journal_page_' +", "'kubejs:journal_page_' +")
    return text


def main() -> None:
    changed = 0
    for base in TARGETS:
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".json", ".snbt", ".py", ".js"}:
                continue
            if "quests_backup_original" in path.parts or "archive" in path.parts:
                continue
            original = path.read_text(encoding="utf-8")
            updated = fix_text(original)
            if updated != original:
                path.write_text(updated, encoding="utf-8", newline="\n")
                changed += 1
    print(f"Reverted journal page IDs in {changed} files")


if __name__ == "__main__":
    main()
