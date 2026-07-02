#!/usr/bin/env python3
"""Generate side FTB Quest chapters locked to main-tier gate + branch quest."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from quest_content_v1 import Q, SIDE_BRANCHES, qid, rid, tid  # noqa: E402
from quest_rewards import seed_count, side_rewards_from_item
from quests_build_v1 import (  # noqa: E402
    chapter_footer,
    task_check,
    task_item,
    write_chapter,
)
from side_lore import get_side_quest_content, side_intro  # noqa: E402

GROUP_MAIN = "B100000000000002"
OUT = ROOT / "overrides" / "config" / "ftbquests" / "quests" / "chapters"

GATE_NUM = {1: 8, 2: 15, 3: 22}

TIER_LABELS: dict[int, tuple[str, dict[int, str]]] = {
    0: ("T0 · Разлом", {1: "Закрепиться у разлома", 2: "Обжитой лагерь", 3: "Готовность к энергии"}),
    1: ("T1 · Искра", {1: "Контур запущен", 2: "Автоматизация руды", 3: "Готовность к Mekanism"}),
    2: ("T2 · Контур", {1: "Промышленный старт", 2: "Энергоузел", 3: "Готовность к сети"}),
    3: ("T3 · Сеть", {1: "Сеть зарождается", 2: "ME-сеть работает", 3: "Готовность к Draconic"}),
    4: ("T4 · Дракон", {1: "Драконий старт", 2: "Энергия дракона", 3: "Готовность к нексусу"}),
    5: ("T5 · Схождение", {1: "next_ae запущен", 2: "Осколки сходятся", 3: "Готовность к ядру"}),
}

# filename -> (tier, gate 1–3, main quest # in tier chapter, main quest title for lock text)
# T0 quest IDs use decimal suffix (…00000000010); T1+ use hex (…0000000000A).
SIDE_UNLOCKS: dict[str, tuple[int, int, int, str]] = {
    "side_kitchen": (0, 1, 10, "Полевая кухня"),
    "side_storage": (0, 1, 11, "Склад экспедиции"),
    "side_bestiary": (0, 2, 20, "Компас разведки"),
    "side_thermal": (1, 1, 2, "Машинная рама"),
    "side_powah": (1, 1, 5, "Урановая жила"),
    "side_immersive": (1, 2, 6, "Молот ковки"),
    "side_apotheosis": (1, 2, 12, "Стол перековки"),
    "side_silent_gear": (1, 2, 7, "Шаблон ковки"),
    "side_mekanism": (2, 1, 2, "Стальной корпус"),
    "side_enderio": (2, 1, 5, "Проводящий сплав"),
    "side_flux": (2, 1, 12, "Flux контроллер"),
    "side_arcane": (2, 2, 28, "Магическая эссенция"),
    "side_network": (3, 1, 11, "ME-контроллер"),
    "side_twilight": (3, 2, 16, "Автокрафт"),
    "side_draconic": (4, 1, 2, "Ядро дракония"),
    "side_cataclysm": (4, 2, 18, "Реликвария Cataclysm"),
    "side_relics": (4, 2, 16, "Chaos Guardian"),
}

# Interleaved sidebar order inside «Прохождение»
SIDE_MENU_ORDER: dict[str, int] = {
    "side_kitchen": 11,
    "side_storage": 12,
    "side_bestiary": 13,
    "side_thermal": 21,
    "side_powah": 22,
    "side_immersive": 23,
    "side_apotheosis": 24,
    "side_silent_gear": 25,
    "side_mekanism": 31,
    "side_enderio": 32,
    "side_flux": 33,
    "side_arcane": 34,
    "side_network": 41,
    "side_twilight": 42,
    "side_draconic": 51,
    "side_cataclysm": 52,
    "side_relics": 53,
}


def side_chapter_id(prefix: str) -> str:
    return f"{prefix}C00000000000"


def main_qid(tier: int, n: int) -> str:
    if tier == 0:
        return f"5217A{n:011d}"
    return f"522{tier}A{n:011X}"


def tier_gate_id(tier: int, gate: int) -> str:
    return main_qid(tier, GATE_NUM[gate])


def snbt_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def side_xp_reward(prefix: str, num: int, xp: int) -> str:
    return f'{{ id: "{rid(prefix, num + 900)}", type: "xp", xp: {xp} }}'


def side_item_reward(prefix: str, num: int, item: str, count: int = 1) -> str:
    c = f", count: {count}" if count > 1 else ""
    return f'{{ id: "{rid(prefix, num + 800)}", item: "{item}"{c}, type: "item" }}'


def side_quest_block(
    quest_id: str,
    *,
    title: str,
    desc: list[str] | None = None,
    icon: str,
    tasks: list[str],
    x: float,
    y: float,
    deps: list[str] | None = None,
    min_deps: int | None = None,
    rewards: list[str] | None = None,
    shape: str = "circle",
    size: float | None = None,
    tags: list[str] | None = None,
) -> str:
    """Quest SNBT block — same field order and flags as quests_build_tiers.quest_block."""
    lines = ["\t\t{"]
    if desc:
        lines.append("\t\t\tdescription: [")
        for d in desc:
            lines.append(f"\t\t\t{snbt_str(d)}")
        lines.append("\t\t\t]")
    if deps:
        dep_s = ", ".join(f'"{d}"' for d in deps)
        lines.append(f"\t\t\tdependencies: [{dep_s}]")
    if min_deps is not None:
        lines.append(f"\t\t\tmin_required_dependencies: {min_deps}")
    lines.append(f'\t\t\ticon: {{ count: 1, id: "{icon}" }}')
    lines.append(f'\t\t\tid: "{quest_id}"')
    lines.append("\t\t\tdisable_jei: true")
    if rewards:
        lines.append("\t\t\trewards: [")
        for r in rewards:
            lines.append(f"\t\t\t\t{r}")
        lines.append("\t\t\t]")
    lines.append(f'\t\t\tshape: "{shape}"')
    if size is not None:
        lines.append(f"\t\t\tsize: {size}d")
    if tags:
        tag_s = ", ".join(f'"{t}"' for t in tags)
        lines.append(f"\t\t\ttags: [{tag_s}]")
    lines.append("\t\t\ttasks: [")
    for t in tasks:
        lines.append(f"\t\t\t\t{t}")
    lines.append("\t\t\t]")
    lines.append(f"\t\t\ttitle: {snbt_str(title)}")
    lines.append(f"\t\t\tx: {x}d")
    lines.append(f"\t\t\ty: {y}d")
    lines.append("\t\t},")
    return "\n".join(lines)


def spine_coords(i: int) -> tuple[float, float]:
    """Vertical spine like main-tier prep chains — dependency lines stay visible."""
    return 0.0, 2.5 + i * 2.0


def side_chapter_header(
    filename: str,
    chapter_obj_id: str,
    chapter_title: str,
    icon_id: str,
    order: int,
    group: str,
) -> str:
    return f"""{{
\tdefault_quest_disable_jei: true
\tdefault_hide_dependency_lines: true
\tprogression_mode: "default"
\thide_quest_until_deps_complete: true
\thide_quest_details_until_startable: true
\tdefault_quest_shape: "circle"
\tfilename: "{filename}"
\tgroup: "{group}"
\ticon: {{ count: 1, id: "{icon_id}" }}
\tid: "{chapter_obj_id}"
\torder_index: {order}
\tquest_links: [ ]
\tquests: ["""


def build_side(
    filename: str,
    title: str,
    icon_id: str,
    order: int,
    group: str,
    prefix: str,
    quests: list[Q],
    layout: str,
    tier: int,
    gate: int,
    main_quest: int,
    main_quest_title: str,
) -> None:
    sid = side_chapter_id(prefix)
    lock_id = qid(prefix, 0)
    gate_id = tier_gate_id(tier, gate)
    branch_id = main_qid(tier, main_quest)
    tier_label, gates = TIER_LABELS[tier]
    gate_label = gates[gate]

    tree: list[str] = []
    n = len(quests)

    tree.append(
        side_quest_block(
            lock_id,
            title="Рубеж не пройден",
            desc=[
                "§c§lЗаблокировано.§r",
                "",
                f"Нужно в §l{tier_label}§r:",
                f"§e1.§r Рубеж §e«{gate_label}»§r",
                f"§e2.§r Квест ветки §e«{main_quest_title}»§r",
                "",
                f"После этого откроется §d{title}§r.",
            ],
            icon="kubejs:quest_side_lock",
            tasks=[task_check(tid(prefix, 0), f"Рубеж «{gate_label}» + «{main_quest_title}»")],
            x=0.0,
            y=0.0,
            deps=[gate_id, branch_id],
            shape="hexagon",
            size=1.2,
        )
    )

    for i, q in enumerate(quests):
        _lx, ry = spine_coords(i)
        prev_id = qid(prefix, quests[i - 1].num) if i > 0 else lock_id
        # Same pattern as main wave 2/3: gate + column predecessor (here lock + prev quest).
        deps = [lock_id, prev_id] if i > 0 else [lock_id]
        is_finale = i == n - 1
        ru_title, desc, task_title = get_side_quest_content(filename, q.num, q.title)
        if i == 0:
            intro = side_intro(filename)
            if intro:
                desc = intro + [""] + desc
        if is_finale:
            q_rewards = side_rewards_from_item(
                q.item,
                q.count,
                item_fn=lambda _rid, item, count: side_item_reward(prefix, q.num, item, count),
                xp_fn=lambda _rid, xp: side_xp_reward(prefix, q.num, xp),
                reliquary_fn=lambda _rid, item: side_item_reward(prefix, q.num + 700, item, 1),
                rid_item=q.num + 800,
                rid_xp=q.num + 900,
                rid_relic=q.num + 700,
                tier=tier,
                quest_num=q.num,
                finale=True,
            )
        else:
            q_rewards = side_rewards_from_item(
                q.item,
                q.count,
                item_fn=lambda _rid, item, count: side_item_reward(prefix, q.num, item, count),
                xp_fn=lambda _rid, xp: side_xp_reward(prefix, q.num, xp),
                reliquary_fn=lambda _rid, item: side_item_reward(prefix, q.num + 700, item, 1),
                rid_item=q.num + 800,
                rid_xp=q.num + 900,
                rid_relic=q.num + 700,
                tier=tier,
                quest_num=q.num,
            )
        tree.append(
            side_quest_block(
                qid(prefix, q.num),
                title=ru_title,
                desc=desc,
                icon=q.item,
                tasks=[task_item(tid(prefix, q.num), task_title, q.item, q.count)],
                x=0.0,
                y=ry,
                deps=deps,
                shape="pentagon" if is_finale and n > 3 else ("diamond" if is_finale else "circle"),
                size=1.3 if is_finale else None,
                tags=["branch_craft"],
                rewards=q_rewards,
            )
        )

    body = side_chapter_header(filename, sid, title, icon_id, order, group)
    body += "\n" + "\n".join(tree) + "\n" + chapter_footer(title, "Сайд-ветка · CoopTech")
    write_chapter(f"{filename}.snbt", body)


def write_side_advancements() -> None:
    adv_dir = ROOT / "overrides" / "data" / "cooptech" / "advancements" / "journal"
    adv_dir.mkdir(parents=True, exist_ok=True)
    stub = (
        '{\n  "parent": "cooptech:journal/t0_intro",\n'
        '  "criteria": {\n    "unlock": {\n'
        '      "trigger": "minecraft:impossible"\n    }\n  }\n}\n'
    )
    for fn, _title, _ic, _grp, _old_unlock, _ord_i, _prefix, _quests, _layout in SIDE_BRANCHES:
        if fn not in SIDE_UNLOCKS:
            continue
        path = adv_dir / f"{fn}.json"
        if not path.exists():
            path.write_text(stub, encoding="utf-8")


def main() -> int:
    print("CoopTech quests_build_sides (gate + branch unlock, interleaved menu)")
    OUT.mkdir(parents=True, exist_ok=True)
    write_side_advancements()
    for fn, title, ic, grp, _old_unlock, ord_i, prefix, quests, layout in SIDE_BRANCHES:
        if fn not in SIDE_UNLOCKS:
            print(f"  skip {fn}: no unlock mapping")
            continue
        tier, gate, main_q, main_title = SIDE_UNLOCKS[fn]
        build_side(fn, title, ic, ord_i, grp, prefix, quests, layout, tier, gate, main_q, main_title)
    print(f"Side chapters: {len(list(OUT.glob('side_*.snbt')))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
