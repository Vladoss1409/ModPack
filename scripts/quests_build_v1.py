#!/usr/bin/env python3
"""Build CoopTech FTB Quest chapters v1 (quest-only, journal-focused)."""
from __future__ import annotations

import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

from quest_content_v1 import (
    MAIN_CHAPTERS,
    SIDE_BRANCHES,
    CH1,
    CH1_PREFIX,
    PROLOGUE_FINALE,
    Q,
    qid,
    tid,
    rid,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
QUESTS = ROOT / 'overrides' / 'config' / 'ftbquests' / 'quests'
CHAPTERS = QUESTS / 'chapters'
BACKUP = ROOT / 'overrides' / 'config' / 'ftbquests' / 'quests_backup_original' / 'chapters'

GROUP_INTRO = 'B100000000000001'
GROUP_MAIN = 'B100000000000002'
GROUP_TECH = 'B100000000000003'
GROUP_MAGIC = 'B100000000000004'
GROUP_OTHER = 'B100000000000005'


def chapter_id(prefix: str) -> str:
    """FTB chapter object id — must not equal any quest id in the same prefix."""
    return f'{prefix}000000000000'


def tab(n: int) -> str:
    return '\t' * n


def snbt_str(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')


def desc_lines(lines: list[str], indent: int = 3) -> str:
    p = tab(indent)
    return '\n'.join(f'{p}"{snbt_str(line)}"' for line in lines)


def icon(item: str) -> str:
    return f'{{ count: 1, id: "{item}" }}'


def task_check(tid: str, title: str) -> str:
    return f'{{ id: "{tid}", title: "{snbt_str(title)}", type: "checkmark" }}'


def task_advancement(tid: str, title: str, adv: str, criterion: str = 'unlock') -> str:
    return (
        f'{{ advancement: "{adv}", criterion: "{criterion}", '
        f'id: "{tid}", title: "{snbt_str(title)}", type: "advancement" }}'
    )


def task_item(tid: str, title: str, item_id: str, count: int = 1) -> str:
    if count == 1:
        return f'{{ id: "{tid}", item: "{item_id}", title: "{snbt_str(title)}", type: "item" }}'
    return (
        f'{{ count: {count}, id: "{tid}", item: "{item_id}", '
        f'title: "{snbt_str(title)}", type: "item" }}'
    )


def reward_item(rid: str, item_id: str, count: int = 1) -> str:
    if count == 1:
        return f'{{ id: "{rid}", item: "{item_id}", type: "item" }}'
    return f'{{ count: {count}, id: "{rid}", item: "{item_id}", type: "item" }}'


def reward_xp(rid: str, xp: int) -> str:
    return f'{{ id: "{rid}", type: "xp", xp: {xp} }}'


def quest_block(
    qid: str,
    title: str,
    x: float,
    y: float,
    tasks: list[str],
    *,
    deps: list[str] | None = None,
    desc: list[str] | None = None,
    subtitle: str = '',
    shape: str = 'circle',
    size: float | None = None,
    icon_id: str = 'minecraft:paper',
    rewards: list[str] | None = None,
    hide_until_visible: bool = False,
    hide_dep_lines: bool = False,
    tags: list[str] | None = None,
    min_deps: int | None = None,
) -> str:
    lines = [f'{tab(2)}{{']
    if desc:
        lines.append(f'{tab(3)}description: [')
        lines.append(desc_lines(desc, 3))
        lines.append(f'{tab(3)}]')
    if deps:
        dep_str = ', '.join(f'"{d}"' for d in deps)
        lines.append(f'{tab(3)}dependencies: [{dep_str}]')
    if min_deps is not None:
        lines.append(f'{tab(3)}min_required_dependencies: {min_deps}')
    if hide_until_visible:
        lines.append(f'{tab(3)}hide_quest_until_deps_visible: true')
    if hide_dep_lines:
        lines.append(f'{tab(3)}hide_dependency_lines: true')
    lines.append(f'{tab(3)}icon: {icon(icon_id)}')
    lines.append(f'{tab(3)}id: "{qid}"')
    if rewards:
        lines.append(f'{tab(3)}rewards: [')
        lines.append('\n'.join(f'{tab(4)}{r}' for r in rewards))
        lines.append(f'{tab(3)}]')
    lines.append(f'{tab(3)}shape: "{shape}"')
    if size is not None:
        lines.append(f'{tab(3)}size: {size}d')
    elif shape == 'circle':
        lines.append(f'{tab(3)}size: 1.0d')
    if subtitle:
        lines.append(f'{tab(3)}subtitle: "{snbt_str(subtitle)}"')
    if tags:
        tag_str = ', '.join(f'"{t}"' for t in tags)
        lines.append(f'{tab(3)}tags: [{tag_str}]')
    lines.append(f'{tab(3)}tasks: [')
    if len(tasks) == 1:
        lines.append(f'{tab(4)}{tasks[0]}')
    else:
        lines.append('\n'.join(f'{tab(4)}{t}' for t in tasks))
    lines.append(f'{tab(3)}]')
    lines.append(f'{tab(3)}title: "{snbt_str(title)}"')
    lines.append(f'{tab(3)}x: {x}d')
    lines.append(f'{tab(3)}y: {y}d')
    lines.append(f'{tab(2)}}}')
    return '\n'.join(lines)


def chapter_header(
    filename: str,
    chapter_id: str,
    chapter_title: str,
    icon_id: str,
    group: str,
    order: int,
    *,
    side: bool = False,
    default_shape: str = 'circle',
    hide_lines: bool = False,
) -> str:
    hide_complete = 'true' if side else 'false'
    hide_lines_str = 'true' if hide_lines else 'false'
    return f'''{{
{tab(1)}default_quest_disable_jei: true
{tab(1)}default_hide_dependency_lines: {hide_lines_str}
{tab(1)}progression_mode: "linear"
{tab(1)}hide_quest_until_deps_complete: {hide_complete}
{tab(1)}hide_quest_details_until_startable: true
{tab(1)}default_quest_shape: "{default_shape}"
{tab(1)}filename: "{filename}"
{tab(1)}group: "{group}"
{tab(1)}icon: {icon(icon_id)}
{tab(1)}id: "{chapter_id}"
{tab(1)}order_index: {order}
{tab(1)}quest_links: [ ]
{tab(1)}quests: ['''


def chapter_footer(chapter_title: str, subtitle: str | None = None) -> str:
    lines = [f'{tab(1)}]']
    if subtitle:
        lines.append(f'{tab(1)}subtitle: [')
        lines.append(f'{tab(2)}"{snbt_str(subtitle)}"')
        lines.append(f'{tab(1)}]')
    lines.append(f'{tab(1)}title: "{snbt_str(chapter_title)}"')
    lines.append('}')
    return '\n'.join(lines)


def write_chapter(filename: str, body: str) -> None:
    CHAPTERS.mkdir(parents=True, exist_ok=True)
    path = CHAPTERS / filename
    path.write_text(body + '\n', encoding='utf-8')
    print(f'  wrote {filename}')


def build_welcome() -> None:
    cid = chapter_id('A001')
    qs = []
    qs.append(
        quest_block(
            'A001000000000001',
            'Сигнал якоря',
            0,
            0,
            [task_check('T001000000000001', 'Начать путь экспедиции')],
            desc=[
                '§l[ Журнал «Якорь» ]§r',
                '',
                '§bCoopTech§r — кооперативная экспедиция. Прогресс ведёт §dКодекс поручений§r (Gr).',
                '§bЛор и подсказки§r — в §dЖурнале экспедиции§r и §eСтраницах журнала§r (ПКМ).',
                '',
                'NPC нет — только записи, квесты и мир.',
            ],
            shape='gear',
            size=1.4,
            icon_id='minecraft:writable_book',
            rewards=[
                reward_item('R001000000000001', 'kubejs:expedition_journal'),
                reward_item('R001000000000002', 'kubejs:journal_page_00'),
                reward_xp('R001000000000003', 25),
            ],
        )
    )
    branches = [
        ('A001000000000002', 'Кодекс и журнал', -3, 2, 'minecraft:book', 'branch_explore',
         [task_advancement('T001000000000002', 'Прочитать страницу §8#0§r', 'cooptech:journal/page_00_read')]),
        ('A001000000000003', 'Кооп-клятва', 0, 2, 'minecraft:shield', 'branch_coop',
         [task_item('T001000000000003', 'Щит экспедиции', 'minecraft:shield', 1)]),
        ('A001000000000004', 'Лагерь у спавна', 3, 2, 'minecraft:campfire', 'branch_craft',
         [task_item('T001000000000004', 'Костёр лагеря', 'minecraft:campfire', 1)]),
    ]
    for qid_, title, x, y, ic, tag, tasks in branches:
        qs.append(
            quest_block(
                qid_,
                title,
                x,
                y,
                tasks,
                deps=['A001000000000001'],
                desc=[f'§d{title}§r — выполните задание для отметки в кодексе.'],
                icon_id=ic,
                tags=[tag],
            )
        )
    qs.append(
        quest_block(
            'A001000000000005',
            'Первая запись',
            -1.5,
            4,
            [task_advancement('T001000000000005', 'ПКМ по Странице журнала §8#0§r', 'cooptech:journal/page_00_read')],
            deps=['A001000000000002'],
            desc=[
                '§bЗадание:§r §eПКМ§r по §dСтранице журнала §8#0§r — приказ из хроники в чат.',
                '§7Тот же текст — в §dЖурнале экспедиции§r → «Хроника».',
            ],
            icon_id='kubejs:journal_page_00',
            shape='diamond',
        )
    )
    qs.append(
        quest_block(
            'A001000000000006',
            'Закрепить цель',
            1.5,
            4,
            [task_item('T001000000000006', 'Подзорная труба', 'minecraft:spyglass', 1)],
            deps=['A001000000000003'],
            icon_id='minecraft:spyglass',
        )
    )
    qs.append(
        quest_block(
            'A001000000000007',
            'Полевой штаб',
            0,
            6,
            [task_item('T001000000000007', 'Лодестон', 'minecraft:lodestone', 1)],
            deps=['A001000000000004', 'A001000000000005'],
            min_deps=2,
            desc=['Найдите костёр, палатки и сундук. Лагерь построен у спавна.'],
            icon_id='minecraft:lodestone',
            shape='diamond',
        )
    )
    qs.append(
        quest_block(
            'A001000000000008',
            'Вступление завершено',
            0,
            8,
            [task_item('T001000000000008', 'Факел экспедиции', 'minecraft:torch', 16)],
            deps=['A001000000000006', 'A001000000000007'],
            min_deps=2,
            desc=['Вступление закрыто — откройте §eГайды§r, затем §eГлаву 1§r.'],
            icon_id='kubejs:quest_gate',
            shape='gear',
            size=1.2,
            rewards=[reward_xp('R001000000000008', 50)],
        )
    )
    body = chapter_header(
        'main_00_welcome', cid, 'Добро пожаловать!', 'minecraft:writable_book', GROUP_INTRO, 0,
    )
    body += '\n' + ',\n'.join(qs) + '\n' + chapter_footer('Добро пожаловать!', '~15 мин')
    write_chapter('main_00_welcome.snbt', body)


def build_guides() -> None:
    cid = chapter_id('A002')
    intro = quest_block(
        'A002000000000001',
        'Путеводитель',
        0,
        0,
        [task_item('T002000000000001', 'Карта маршрута', 'minecraft:map', 1)],
        desc=[
            '§l[ Справка экспедиции ]§r',
            'Краткие правила: §eJEI§r, §eFTB Teams§r, §eJourneyMap§r, §ePatchouli§r.',
            'Подробности — в следующих узлах и в журнале.',
        ],
        shape='gear',
        size=1.3,
        icon_id='minecraft:map',
    )
    guides = [
        ('A002000000000002', 'JEI / REI', -4, 2, 'minecraft:book', 'Скрафтите деревянную кирку.',
         [task_item('T002000000000002', 'Деревянная кирка', 'minecraft:wooden_pickaxe', 1)]),
        ('A002000000000003', 'FTB Teams', -2, 2, 'minecraft:shield', '/ftbteams party create — затем щит.',
         [task_item('T002000000000003', 'Щит гильдии', 'minecraft:shield', 1)]),
        ('A002000000000004', 'Книга квестов', 0, 2, 'ftbquests:book', 'Клавиша Gr — Кодекс поручений.',
         [task_item('T002000000000004', 'Книга квестов', 'ftbquests:book', 1)]),
        ('A002000000000005', 'Журнал', 2, 2, 'kubejs:expedition_journal', 'ПКМ — Patchouli.',
         [task_item('T002000000000005', 'Журнал экспедиции', 'kubejs:expedition_journal', 1)]),
        ('A002000000000006', 'JourneyMap', 4, 2, 'minecraft:filled_map', 'Waypoints для разломов.',
         [task_item('T002000000000006', 'Карта', 'minecraft:filled_map', 1)]),
        ('A002000000000007', 'Кооп-маяк', -3, 4, 'kubejs:resonance_beacon', 'ПКМ у костра лагеря.',
         [task_item('T002000000000007', 'Кооп-маяк', 'kubejs:resonance_beacon', 1)]),
        ('A002000000000008', 'Реликварии', -1, 4, 'kubejs:reliquary_field', 'ПКМ — полевые сундуки.',
         [task_item('T002000000000008', 'Реликварий поля', 'kubejs:reliquary_field', 1)]),
        ('A002000000000009', 'Vein mining', 1, 4, 'minecraft:iron_shovel', 'Зажмите клавишу копания.',
         [task_item('T002000000000009', 'Железная лопата', 'minecraft:iron_shovel', 1)]),
        ('A002000000000010', 'Справка готова', 0, 6, 'minecraft:experience_bottle', 'В Главу 1!',
         [task_item('T002000000000010', 'Пузырёк опыта', 'minecraft:experience_bottle', 1)]),
    ]
    qs = [intro]
    for i, (qid_, title, x, y, ic, hint, tasks) in enumerate(guides):
        deps = ['A002000000000001'] if i < 9 else [
            'A002000000000002', 'A002000000000003', 'A002000000000004',
            'A002000000000005', 'A002000000000006',
        ]
        min_d = None if i < 9 else 3
        qs.append(
            quest_block(
                qid_,
                title,
                x,
                y,
                tasks,
                deps=deps,
                min_deps=min_d,
                desc=[hint],
                icon_id=ic,
                shape='diamond' if i == 9 else 'circle',
            )
        )
    body = chapter_header(
        'main_01_guides', cid, 'Гайды', 'minecraft:map', GROUP_INTRO, 1,
    )
    body += '\n' + ',\n'.join(qs) + '\n' + chapter_footer('Гайды', '~10 мин')
    write_chapter('main_01_guides.snbt', body)


PROLOGUE_NPC_REPLACEMENTS = [
    (
        '§bКто:§r §dДиспетчер якоря§r — у костра, бирюзовая бирка на плаще.',
        '§bЖурнал:§r §eСтраница §8#0§r (ПКМ) или §dЖурнал экспедиции§r → «Хроника».',
    ),
    (
        '§bДальше:§r брифинг у §dДиспетчера§r.',
        '§bДальше:§r §eСтраница §8#0§r в журнале.',
    ),
    (
        '§bДальше:§r брифинг у диспетчера → финал.',
        '§bДальше:§r §eСтраница §8#0§r → финал.',
    ),
    (
        '→ пайки → брифинг → финал"',
        '→ пайки → страница #0 → финал"',
    ),
    (
        '§bДальше:§r пайки → брифинг у диспетчера → финал.',
        '§bДальше:§r пайки → §eСтраница §8#0§r → финал.',
    ),
    (
        '§bКто:§r §dДиспетчер якоря§r — у центра лагеря, у костра.',
        '§bГде:§r §dЛагерь§r — костёр, фиолетовая палатка, сундук.',
    ),
    (
        '1. Поговори с Диспетчером — прочитай приказ до конца.',
        '1. §eПКМ§r по §dСтранице журнала §8#0§r — прочитайте приказ до конца.',
    ),
    (
        '2. Если диспетчер ещё не прибыл — отметься сам, когда будешь готов.',
        '2. Тот же текст — в §dЖурнале экспедиции§r (Patchouli).',
    ),
    (
        '§bГде:§r §eлагерь у костра-маяка§r.',
        '',
    ),
    (
        'title: "Брифинг у Диспетчера якоря"',
        'title: "Приказ из журнала"',
    ),
    (
        'subtitle: "Совместно · брифинг"',
        'subtitle: "Совместно · журнал"',
    ),
    (
        '§bДальше:§r §dЗапись диспетчера§r в журнале.',
        '§bДальше:§r §eСтраница §8#0§r в журнале.',
    ),
]

PROLOGUE_TASK_TITLES = [
    (
        '{ id: "T101000000000003", item: "minecraft:oak_log", count: 64, type: "item" }',
        '{ id: "T101000000000003", item: "minecraft:oak_log", count: 64, title: "64 дубовых бревна", type: "item" }',
    ),
    (
        '{ id: "T101000000000004", item: "minecraft:chest", type: "item" }',
        '{ id: "T101000000000004", item: "minecraft:chest", title: "Сундук", type: "item" }',
    ),
    (
        'id: "T101000000000009"\n\t\t\t\titem: "minecraft:raw_iron"\n\t\t\t\tcount: 64\n\t\t\t\ttype: "item"',
        'id: "T101000000000009", item: "minecraft:raw_iron", count: 64, title: "64 необработ. железа", type: "item"',
    ),
    (
        '{ id: "T101000000000008", item: "naturescompass:naturescompass", type: "item" }',
        '{ id: "T101000000000008", item: "naturescompass:naturescompass", title: "Компас стихий", type: "item" }',
    ),
    (
        '{ id: "T101000000000017", item: "minecraft:raw_iron", count: 48, type: "item" }',
        '{ id: "T101000000000017", item: "minecraft:raw_iron", count: 48, title: "48 необработ. железа", type: "item" }',
    ),
    (
        '{ id: "T101000000000018", item: "minecraft:raw_copper", count: 32, type: "item" }',
        '{ id: "T101000000000018", item: "minecraft:raw_copper", count: 32, title: "32 необработ. меди", type: "item" }',
    ),
    (
        '{ id: "T101000000000019", item: "minecraft:smithing_table", type: "item" }',
        '{ id: "T101000000000019", item: "minecraft:smithing_table", title: "Стол кузнеца", type: "item" }',
    ),
    (
        '{ id: "T101000000000020", item: "farmersdelight:cutting_board", type: "item" }',
        '{ id: "T101000000000020", item: "farmersdelight:cutting_board", title: "Разделочная доска", type: "item" }',
    ),
    (
        '{ id: "T101000000000011", item: "minecraft:cooked_beef", count: 16, type: "item" }',
        '{ id: "T101000000000011", item: "minecraft:cooked_beef", count: 16, title: "16 стейков", type: "item" }',
    ),
    (
        '{ id: "T101000000000012", item: "minecraft:golden_carrot", count: 8, type: "item" }',
        '{ id: "T101000000000012", item: "minecraft:golden_carrot", count: 8, title: "8 золотых морковок", type: "item" }',
    ),
    (
        '{ id: "T101000000000022", item: "kubejs:stabilized_shard_01", type: "item" }',
        '{ id: "T101000000000022", item: "kubejs:stabilized_shard_01", title: "Стабилизированный осколок", type: "item" }',
    ),
    (
        '{ id: "T101000000000013", item: "minecraft:bricks", count: 32, type: "item" }',
        '{ id: "T101000000000013", item: "minecraft:bricks", count: 32, title: "32 кирпича", type: "item" }',
    ),
    (
        '{ id: "T101000000000014", item: "minecraft:lantern", count: 16, type: "item" }',
        '{ id: "T101000000000014", item: "minecraft:lantern", count: 16, title: "16 фонарей", type: "item" }',
    ),
]


def build_prologue_snbt() -> str:
    src = BACKUP / '00_prologue.snbt'
    text = src.read_text(encoding='utf-8')
    for old, new in PROLOGUE_NPC_REPLACEMENTS:
        text = text.replace(old, new)
    text = re.sub(r'group: "[^"]+"', f'group: "{GROUP_MAIN}"', text, count=1)
    text = text.replace('default_quest_shape: "hexagon"', 'default_quest_shape: "circle"')
    for old, new in PROLOGUE_TASK_TITLES:
        text = text.replace(old, new)
    text = re.sub(
        r'tasks: \[\{\s*id: "T101000000000021"[^]]+\}\]',
        'tasks: [{ advancement: "cooptech:journal/dispatcher_briefing", criterion: "unlock", '
        'id: "T101000000000021", title: "ПКМ — Страница §8#0§r", type: "advancement" }]',
        text,
        flags=re.DOTALL,
    )
    text = re.sub(r'(\t\t\tdisable_jei: true\n)(?:\t\t\tdisable_jei: true\n)+', r'\1', text)
    # Старт пролога после гайдов
    text = text.replace(
        'id: "A101000000000001"\n\t\t\tdisable_jei: true',
        'id: "A101000000000001"\n\t\t\tdependencies: ["A002000000000010"]\n\t\t\tdisable_jei: true',
        1,
    )
    m = re.search(r'\tquests: \[\n(.*?)\n\t\]', text, re.DOTALL)
    if not m:
        raise RuntimeError('prologue quests block not found')
    return m.group(1)


def build_ch1_merged() -> None:
    """Глава 1: пролог (backup) + фундамент — одна вкладка."""
    prologue_quests = build_prologue_snbt()
    foundation = [quest_from_spec(CH1_PREFIX, q, PROLOGUE_FINALE) for q in CH1]
    cid = chapter_id(CH1_PREFIX)
    body = chapter_header(
        'main_02_ch1_anchor',
        cid,
        'Глава 1: Якорь лагеря',
        'minecraft:writable_book',
        GROUP_MAIN,
        1,
        default_shape='circle',
        hide_lines=False,
    )
    body += '\n' + prologue_quests + ',\n' + ',\n'.join(foundation) + '\n'
    body += chapter_footer('Глава 1: Якорь лагеря', 'Пролог + инфраструктура · ~12 ч')
    write_chapter('main_02_ch1_anchor.snbt', body)


def build_prologue() -> None:
    """Deprecated — пролог влит в build_ch1_merged."""
    pass


def resolve_deps(prefix: str, q: Q, prev_finale: str) -> list[str]:
    if not q.deps:
        if prefix == CH1_PREFIX and q.num == 7:
            return [PROLOGUE_FINALE]
        if q.y <= -1.5:
            return [prev_finale]
    return [qid(prefix, n) for n in q.deps]


def side_coords(layout: str, i: int, n: int) -> tuple[float, float]:
    """TechnoMagic-like layouts: spine, column, wave, radial."""
    if layout == 'column':
        return 0.0, round(3.0 + i * 2.5, 1)
    if layout == 'wave':
        x = -2.5 if i % 2 == 0 else 2.5
        return x, round(3.0 + i * 2.2, 1)
    if layout == 'radial':
        angle = (2 * math.pi * i / max(n, 1)) - math.pi / 2
        r = 4.0 + (i // 8) * 2.5
        return round(math.cos(angle) * r, 1), round(3.0 + math.sin(angle) * r * 0.6 + i * 0.3, 1)
    row, col = divmod(i, 4)
    xs = [-3.0, -1.0, 1.0, 3.0]
    x = xs[col % 4]
    y = 3.0 + row * 3.0
    if i == n - 1 and n > 1:
        return 0.0, y + 2.0
    return x, round(y, 1)


def quest_from_spec(prefix: str, q: Q, prev_finale: str) -> str:
    deps = resolve_deps(prefix, q, prev_finale)
    tasks = [task_item(tid(prefix, q.num), q.title, q.item, q.count)]
    for i, (item, title, count) in enumerate(q.extra_tasks, start=2):
        tasks.append(task_item(tid(prefix, q.num + i * 1000), title, item, count))
    if q.gate:
        tasks = [task_check(tid(prefix, q.num), 'Рубеж пройден')]
    if q.gate:
        shape, size, icon_id = 'diamond', q.size, 'kubejs:quest_gate'
    elif q.finale:
        shape, size, icon_id = 'gear', q.size or 1.5, q.item
    elif q.y <= -1.5:
        shape, size, icon_id = 'gear', q.size or 1.3, q.item
    else:
        shape, size, icon_id = 'circle', q.size, q.item
    rewards = []
    if q.finale:
        rewards.append(reward_item(rid(prefix, q.num), 'kubejs:journal_page_05', 1))
        rewards.append(reward_xp(rid(prefix, q.num + 1), 100))
    return quest_block(
        qid(prefix, q.num),
        q.title,
        q.x,
        q.y,
        tasks,
        deps=deps,
        desc=q.desc,
        subtitle=q.subtitle or ('Gate' if q.gate else ''),
        shape=shape,
        size=size,
        icon_id=icon_id,
        rewards=rewards or None,
        min_deps=q.min_deps,
    )


def build_main_from_manifest(
    filename: str,
    title: str,
    icon_id: str,
    group: str,
    order: int,
    chapter_id: str,
    prefix: str,
    quests: list[Q],
    prev_finale: str,
    subtitle: str,
) -> None:
    qs = [quest_from_spec(prefix, q, prev_finale) for q in quests]
    body = chapter_header(
        filename.replace('.snbt', ''),
        chapter_id,
        title,
        icon_id,
        group,
        order,
        default_shape='circle',
        hide_lines=False,
    )
    body += '\n' + ',\n'.join(qs) + '\n' + chapter_footer(title, subtitle)
    write_chapter(filename, body)


def build_side_full(
    filename: str,
    title: str,
    icon_id: str,
    group: str,
    unlock_quest_id: str,
    order: int,
    prefix: str,
    quests: list[Q],
    layout: str = 'spine',
) -> None:
    sid = chapter_id(prefix)
    tree: list[str] = []
    n = len(quests)
    for i, q in enumerate(quests):
        rx, ry = side_coords(layout, i, n)
        if i == 0:
            deps = [unlock_quest_id]
            hide = False
            desc = [
                f'§d{title}§r — ветка открыта основной линией.',
                'Следующие узлы появятся по цепочке зависимостей.',
            ]
        else:
            deps = [qid(prefix, quests[i - 1].num)]
            hide = True
            desc = None
        tasks = [task_item(tid(prefix, q.num), q.title, q.item, q.count)]
        tree.append(
            quest_block(
                qid(prefix, q.num),
                q.title,
                rx,
                ry,
                tasks,
                deps=deps,
                desc=desc,
                hide_until_visible=hide,
                icon_id=q.item,
                shape='diamond' if i == n - 1 else 'circle',
                size=1.2 if i == n - 1 else None,
            )
        )
    body = chapter_header(
        filename,
        sid,
        title,
        icon_id,
        group,
        order,
        side=True,
        hide_lines=False,
    )
    body += '\n' + ',\n'.join(tree) + '\n' + chapter_footer(title, 'Сайд-ветка')
    write_chapter(f'{filename}.snbt', body)


def update_chapter_groups() -> None:
    path = QUESTS / 'chapter_groups.snbt'
    body = '''{
\tchapter_groups: [
\t\t{ id: "B100000000000001", title: "Вступ" }
\t\t{ id: "B100000000000002", title: "Прохождение" }
\t\t{ id: "B100000000000003", title: "Технологии" }
\t\t{ id: "B100000000000004", title: "Магия" }
\t\t{ id: "B100000000000005", title: "Другое" }
\t]
}
'''
    path.write_text(body, encoding='utf-8')
    print('  updated chapter_groups.snbt')


def update_data_snbt() -> None:
    path = QUESTS / 'data.snbt'
    text = path.read_text(encoding='utf-8')
    text = re.sub(
        r'title: "[^"]*"',
        'title: "CoopTech — Кодекс экспедиции"',
        text,
        count=1,
    )
    text = text.replace(
        'lock_message: "Сначала завершите предыдущие поручения."',
        'lock_message: "§cЗакрыто.§r Завершите предыдущие поручения или рубеж главы."',
    )
    m = re.search(r'version: (\d+)', text)
    if m:
        text = text.replace(f'version: {m.group(1)}', f'version: {int(m.group(1)) + 1}', 1)
    path.write_text(text, encoding='utf-8')
    print('  updated data.snbt')


def remove_stale_chapters() -> None:
    keep = {
        'main_00_welcome.snbt', 'main_01_guides.snbt', 'main_02_ch1_anchor.snbt',
        'main_03_ch2_surface.snbt', 'main_04_ch3_flux.snbt',
        'main_05_ch4_production.snbt', 'main_06_ch5_nano.snbt', 'main_07_ch6_finale.snbt',
        'side_thermal.snbt', 'side_kitchen.snbt', 'side_storage.snbt', 'side_arcane.snbt',
        'side_flux.snbt', 'side_network.snbt', 'side_apotheosis.snbt', 'side_silent_gear.snbt',
        'side_draconic.snbt', 'side_mekanism.snbt', 'side_immersive.snbt', 'side_enderio.snbt',
        'side_powah.snbt', 'side_bestiary.snbt', 'side_twilight.snbt', 'side_relics.snbt',
        'side_cataclysm.snbt',
    }
    for p in CHAPTERS.glob('*.snbt'):
        if p.name not in keep:
            p.unlink()
            print(f'  removed stale {p.name}')


def remove_tm_chapters() -> None:
    for p in CHAPTERS.glob('tm_*.snbt'):
        p.unlink()
        print(f'  removed {p.name}')


def run_fix_ftb() -> None:
    fix = ROOT / 'scripts' / 'fix_ftb_snbt.py'
    subprocess.run([sys.executable, str(fix)], check=True)


def validate_chapter_icons() -> None:
    """Warn if quests lack icon or use bare paper placeholder."""
    bad = 0
    for path in sorted(CHAPTERS.glob('*.snbt')):
        text = path.read_text(encoding='utf-8')
        blocks = re.findall(r'\{[^{}]*?id: "(A\d+)"[^{}]*?\}', text, re.DOTALL)
        for block in re.finditer(r'\t\t\{[^}]+\}', text):
            chunk = block.group(0)
            if 'id: "A' not in chunk:
                continue
            if 'icon:' not in chunk:
                bad += 1
            elif 'icon: { count: 1, id: "minecraft:paper" }' in chunk:
                bad += 1
    if bad:
        print(f'  WARN: {bad} quest(s) missing proper icon')
    else:
        print('  icon validation OK')


def main() -> int:
    print('CoopTech quests_build_v1')
    CHAPTERS.mkdir(parents=True, exist_ok=True)
    remove_tm_chapters()
    remove_stale_chapters()
    build_welcome()
    build_guides()
    build_ch1_merged()
    for fname, title, icon, group, order, cid, prefix, quests, prev, sub in MAIN_CHAPTERS:
        build_main_from_manifest(
            f'{fname}.snbt', title, icon, group, order, cid, prefix, quests, prev, sub,
        )
    for fn, title, ic, grp, unlock_id, ord_i, prefix, quests, layout in SIDE_BRANCHES:
        build_side_full(fn, title, ic, grp, unlock_id, ord_i, prefix, quests, layout)
    update_chapter_groups()
    update_data_snbt()
    validate_chapter_icons()
    print('Running fix_ftb_snbt.py ...')
    run_fix_ftb()
    count = sum(1 for _ in CHAPTERS.glob('*.snbt'))
    print(f'Chapters: {count}')
    print('Done.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
