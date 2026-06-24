#!/usr/bin/env python3
"""Fix FTB Quests SNBT for CoopTech: BOM, subtitles, item format, disable JEI on quests."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTS = ROOT / 'overrides' / 'config' / 'ftbquests' / 'quests'

CHAPTER_SUBTITLE = re.compile(
    r'^(\t)subtitle: "([^"]*)"\r?\n(\1title: )',
    re.MULTILINE,
)

ITEM_COMPOUND = re.compile(
    r'item: \{ count: 1, id: "([^"]+)" \}',
)

ICON_SHORT = re.compile(
    r'icon: \{ id: "([^"]+)" \}',
)

QUEST_ID = re.compile(r'^(\t\t\tid: "A\d+"\r?\n)', re.MULTILINE)

CHAPTER_LOCKING = (
    '\tprogression_mode: "linear"\n'
    '\thide_quest_until_deps_complete: false\n'
    '\thide_quest_details_until_startable: true\n'
)

QUEST_TEXTURE_ICONS = {
    'cooptech:textures/quests/gate.png': 'kubejs:quest_gate',
    'cooptech:textures/quests/side_lock.png': 'kubejs:quest_side_lock',
    'cooptech:textures/quests/lock.png': 'kubejs:quest_lock',
    'cooptech:textures/quests/pool.png': 'kubejs:quest_pool',
    'cooptech:textures/quests/finale.png': 'kubejs:quest_finale',
    'cooptech:textures/quests/chapter_start.png': 'kubejs:quest_chapter_start',
    'cooptech:textures/quests/wave.png': 'kubejs:quest_wave',
}


def strip_bom(text: str) -> str:
    if text.startswith('\ufeff'):
        return text[1:]
    return text


def fix_chapter_subtitle(text: str) -> str:
    return CHAPTER_SUBTITLE.sub(r'\1subtitle: [\n\1\t"\2"\n\1]\n\3', text)


def flatten_item_stacks(text: str) -> str:
    return ITEM_COMPOUND.sub(r'item: "\1"', text)


def normalize_icons(text: str) -> str:
    return ICON_SHORT.sub(r'icon: { count: 1, id: "\1" }', text)


def fix_quest_texture_icons(text: str) -> str:
    for old, new in QUEST_TEXTURE_ICONS.items():
        text = text.replace(f'id: "{old}"', f'id: "{new}"')
    text = text.replace('id: "jei:jei"', 'id: "minecraft:book"')
    text = text.replace('id: "kubejs:relic_vault"', 'id: "kubejs:reliquary_field"')
    return text


def add_chapter_defaults(text: str) -> str:
    if 'default_quest_disable_jei:' in text:
        if 'default_hide_dependency_lines:' not in text:
            text = re.sub(
                r'(default_quest_disable_jei: true\r?\n)',
                r'\1\tdefault_hide_dependency_lines: false\n',
                text,
                count=1,
            )
        return text
    return re.sub(
        r'^\{\r?\n',
        '{\n\tdefault_quest_disable_jei: true\n\tdefault_hide_dependency_lines: false\n',
        text,
        count=1,
    )


def add_chapter_locking(text: str) -> str:
    if 'progression_mode:' in text:
        return text
    if 'default_hide_dependency_lines:' in text:
        return re.sub(
            r'(default_hide_dependency_lines: false\r?\n)',
            r'\1' + CHAPTER_LOCKING,
            text,
            count=1,
        )
    if 'default_quest_disable_jei:' in text:
        return re.sub(
            r'(default_quest_disable_jei: true\r?\n)',
            r'\1' + CHAPTER_LOCKING,
            text,
            count=1,
        )
    return text


def normalize_chapter_locking(text: str, chapter_name: str) -> str:
    """Main chapters: tree visible. Side chapters keep hide_quest_until_deps_complete."""
    if not chapter_name.startswith('side_'):
        text = text.replace('hide_quest_until_deps_complete: true', 'hide_quest_until_deps_complete: false')
    text = text.replace('default_hide_dependency_lines: true', 'default_hide_dependency_lines: false')
    if 'progression_mode:' not in text:
        text = add_chapter_locking(text)
    return text


def dedupe_disable_jei(text: str) -> str:
    return re.sub(r'(\t\t\tdisable_jei: true\n)(?:\t\t\tdisable_jei: true\n)+', r'\1', text)


def add_quest_disable_jei(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        block = match.group(0)
        if 'disable_jei:' in block:
            return block
        return block.replace(
            match.group(1),
            match.group(1) + '\t\t\tdisable_jei: true\n',
            1,
        )

    return QUEST_ID.sub(repl, text)


def strip_per_quest_line_hiding(text: str) -> str:
    """Per-quest hide_dependency_lines: true suppresses arrows entirely — remove."""
    return re.sub(r'\t\t\thide_dependency_lines: true\n', '', text)


def process(path: Path) -> None:
    raw = path.read_bytes()
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    text = raw.decode('utf-8')
    text = strip_bom(text)

    if path.parent.name == 'chapters' and path.name.endswith('.snbt'):
        text = fix_chapter_subtitle(text)
        text = add_chapter_defaults(text)
        text = add_chapter_locking(text)
        text = normalize_chapter_locking(text, path.name.replace('.snbt', ''))
        text = fix_quest_texture_icons(text)
        text = flatten_item_stacks(text)
        text = normalize_icons(text)
        text = add_quest_disable_jei(text)
        text = dedupe_disable_jei(text)
        text = strip_per_quest_line_hiding(text)

    path.write_text(text, encoding='utf-8', newline='\n')


def main() -> None:
    for snbt in sorted(QUESTS.rglob('*.snbt')):
        process(snbt)
        print(f'fixed: {snbt.relative_to(ROOT)}')
    print('Done.')


if __name__ == '__main__':
    main()
