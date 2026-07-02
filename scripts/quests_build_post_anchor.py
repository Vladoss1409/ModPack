#!/usr/bin/env python3
"""Generate post-T5 hub «Після якоря» + 3 side branches."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from quest_content_v1 import POST_SIDE_BRANCHES, Q, qid, rid, tid  # noqa: E402
from quest_rewards import side_rewards_from_item
from quests_build_sides import (  # noqa: E402
    GROUP_MAIN,
    OUT,
    chapter_footer,
    side_chapter_header,
    side_item_reward,
    side_quest_block,
    side_xp_reward,
    spine_coords,
    task_check,
    task_item,
    write_chapter,
)
from side_lore import get_side_quest_content, side_intro  # noqa: E402

GROUP_POST = "B100000000000006"
T5_FINALE = "5225A0000000001A"
HUB_PREFIX = "A900"
HUB_CHAPTER_ID = f"{HUB_PREFIX}C00000000000"


def snbt_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def hub_qid(n: int) -> str:
    return qid(HUB_PREFIX, n)


def hub_tid(n: int) -> str:
    return tid(HUB_PREFIX, n)


def hub_rid(n: int) -> str:
    return rid(HUB_PREFIX, n)


def hub_quest_block(
    n: int,
    *,
    title: str,
    desc: list[str],
    icon: str,
    tasks: list[str],
    x: float,
    y: float,
    deps: list[str] | None = None,
    rewards: list[str] | None = None,
    shape: str = "circle",
    size: float | None = None,
) -> str:
    lines = ["\t\t{"]
    lines.append("\t\t\tdescription: [")
    for d in desc:
        lines.append(f"\t\t\t{snbt_str(d)}")
    lines.append("\t\t\t]")
    if deps:
        dep_s = ", ".join(f'"{d}"' for d in deps)
        lines.append(f"\t\t\tdependencies: [{dep_s}]")
    lines.append(f'\t\t\ticon: {{ count: 1, id: "{icon}" }}')
    lines.append(f'\t\t\tid: "{hub_qid(n)}"')
    lines.append("\t\t\tdisable_jei: true")
    if rewards:
        lines.append("\t\t\trewards: [")
        for r in rewards:
            lines.append(f"\t\t\t\t{r}")
        lines.append("\t\t\t]")
    lines.append(f'\t\t\tshape: "{shape}"')
    if size is not None:
        lines.append(f"\t\t\tsize: {size}d")
    lines.append("\t\t\ttasks: [")
    for t in tasks:
        lines.append(f"\t\t\t\t{t}")
    lines.append("\t\t\t]")
    lines.append(f"\t\t\ttitle: {snbt_str(title)}")
    lines.append(f"\t\t\tx: {x}d")
    lines.append(f"\t\t\ty: {y}d")
    lines.append("\t\t},")
    return "\n".join(lines)


def item_reward_snbt(n: int, item: str, count: int = 1) -> str:
    c = f", count: {count}" if count > 1 else ""
    return f'{{ id: "{hub_rid(n)}", item: "{item}"{c}, type: "item" }}'


def xp_reward_hub(n: int, xp: int) -> str:
    return f'{{ id: "{hub_rid(n)}", type: "xp", xp: {xp} }}'


def build_hub() -> None:
    quests: list[str] = []
    quests.append(
        hub_quest_block(
            1,
            title="Після якоря",
            desc=[
                "§l[ Після якоря ]§r",
                "",
                "§7§eЯкір реальності§r стабілізовано. Розлом затих — не зник, але слухає.",
                "",
                "§7У блокноті нова секція: §dщо робити після фіналу§r. Три шляхи —",
                "§7печери, бос-фарм, епілог модів. Кожен відкриває свою ветку.",
                "",
                "§8Потрібен §ekubejs:reality_anchor_core§r — нагорода фіналу T5.",
            ],
            icon="kubejs:reality_anchor_core",
            tasks=[
                f'{{ id: "{hub_tid(1)}", item: "kubejs:reality_anchor_core", title: "Зафіксувати стабілізацію якоря", type: "item" }}',
                f'{{ id: "{hub_tid(101)}", title: "Відкрити розділ «Після якоря»", type: "checkmark" }}',
            ],
            x=0,
            y=0,
            deps=[T5_FINALE],
            rewards=[
                item_reward_snbt(1, "kubejs:journal_page_post_anchor"),
                item_reward_snbt(2, "kubejs:reliquary_convergence"),
                xp_reward_hub(3, 80),
            ],
            shape="hexagon",
            size=1.5,
        )
    )
    branches = [
        (
            2,
            "Печери розлому",
            [
                "§7Під лагерем ще дихають §dAlex's Caves§r — кодекс вказує жили.",
                "",
                "§7Записав маршрут: печери, таблички, ехо-осколки.",
            ],
            "kubejs:decrypted_cave_codex",
            "Взяти маршрут у печери",
            -4,
        ),
        (
            3,
            "Бос-фарм якоря",
            [
                "§7Якір притягує сильних істот. §dCataclysm§r і §dMowzie§r —",
                "§7фарм трофеїв для двох, поки світ ще тримається.",
            ],
            "cataclysm:void_eye",
            "Приняти охоту на босів",
            0,
        ),
        (
            4,
            "Епілог модів",
            [
                "§7Фінальний облік сил: §dAE2§r, §dProjectE§r, §dDraconic§r, §dnext_ae§r.",
                "",
                "§7Закрити всі лінії модпаку — не для якоря, для себе.",
            ],
            "kubejs:anchor_nexus",
            "Приняти епілог модів",
            4,
        ),
    ]
    for n, title, desc, icon, task_title, x in branches:
        quests.append(
            hub_quest_block(
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=[f'{{ id: "{hub_tid(n)}", title: {snbt_str(task_title)}, type: "checkmark" }}'],
                x=x,
                y=-2.5,
                deps=[hub_qid(1)],
                rewards=[xp_reward_hub(10 + n, 35)],
                shape="diamond",
                size=1.1,
            )
        )

    body = "\n".join(quests)
    text = f"""{{
\tdefault_quest_disable_jei: true
\tdefault_hide_dependency_lines: false
\tprogression_mode: "default"
\thide_quest_until_deps_complete: false
\thide_quest_details_until_startable: true
\tdefault_quest_shape: "circle"
\tfilename: "main_post_anchor"
\tgroup: "{GROUP_POST}"
\ticon: {{ count: 1, id: "kubejs:reality_anchor_core" }}
\tid: "{HUB_CHAPTER_ID}"
\torder_index: 61
\tquest_links: [ ]
\tquests: [
{body}
\t]
\tsubtitle: [
\t\t"Після T5 · епілог"
\t]
\ttitle: "Після якоря"
}}
"""
    write_chapter("main_post_anchor.snbt", text)


def build_post_side(
    filename: str,
    title: str,
    icon_id: str,
    prefix: str,
    quests: list[Q],
    order: int,
    hub_branch_id: str,
) -> None:
    sid = f"{prefix}C00000000000"
    lock_id = qid(prefix, 0)

    tree: list[str] = []
    tree.append(
        side_quest_block(
            lock_id,
            title="Якір не стабілізовано",
            desc=[
                "§c§lЗаблокировано.§r",
                "",
                "§7Нужно:",
                "§e1.§r Финал §lT5 · Схождение§r — §eЯкорь реальности§r",
                f"§e2.§r Ветка хаба §e«{title}»§r",
                "",
                f"После этого откроется §d{title}§r.",
            ],
            icon="kubejs:quest_side_lock",
            tasks=[task_check(tid(prefix, 0), f"Финал T5 + «{title}»")],
            x=0.0,
            y=0.0,
            deps=[T5_FINALE, hub_branch_id],
            shape="hexagon",
            size=1.2,
        )
    )

    n = len(quests)
    for i, q in enumerate(quests):
        _lx, ry = spine_coords(i)
        prev_id = qid(prefix, quests[i - 1].num) if i > 0 else lock_id
        deps = [lock_id, prev_id] if i > 0 else [lock_id]
        is_finale = i == n - 1
        ru_title, desc, task_title = get_side_quest_content(filename, q.num, q.title)
        if i == 0:
            intro = side_intro(filename)
            if intro:
                desc = intro + [""] + desc
        tier = 5
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
                tags=["branch_explore"],
                rewards=q_rewards,
            )
        )

    body = side_chapter_header(filename, sid, title, icon_id, order, GROUP_POST)
    body += "\n" + "\n".join(tree) + "\n" + chapter_footer(title, "Після якоря · CoopTech")
    write_chapter(f"{filename}.snbt", body)


def write_advancements() -> None:
    adv_dir = ROOT / "overrides" / "data" / "cooptech" / "advancements" / "journal"
    adv_dir.mkdir(parents=True, exist_ok=True)
    stub = (
        '{\n  "parent": "cooptech:journal/t5_lore_finale",\n'
        '  "criteria": {\n    "unlock": {\n'
        '      "trigger": "minecraft:impossible"\n    }\n  }\n}\n'
    )
    keys = [
        "post_anchor",
        "side_post_caves",
        "side_post_bossfarm",
        "side_post_epilogue",
        "codex_side_post_caves",
        "codex_side_post_bossfarm",
        "codex_side_post_epilogue",
    ]
    for key in keys:
        path = adv_dir / f"{key}.json"
        if not path.exists():
            path.write_text(stub, encoding="utf-8")


def main() -> int:
    print("CoopTech quests_build_post_anchor (hub + 3 post-T5 sides)")
    OUT.mkdir(parents=True, exist_ok=True)
    write_advancements()
    build_hub()
    for fn, title, icon, prefix, quests, order, hub_id in POST_SIDE_BRANCHES:
        build_post_side(fn, title, icon, prefix, quests, order, hub_id)
    print(f"Post-anchor chapters: {1 + len(POST_SIDE_BRANCHES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
