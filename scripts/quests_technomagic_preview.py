#!/usr/bin/env python3
"""
Тестовий прев'ю FTB Quests у стилі ТехноМагії (структура сайдбару + макети дерев).

  python scripts/quests_technomagic_preview.py install   # бекап + тестовий каркас
  python scripts/quests_technomagic_preview.py restore   # відкат до бекапу
  python scripts/quests_technomagic_preview.py status    # що зараз активно
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTS = ROOT / "overrides" / "config" / "ftbquests" / "quests"
BACKUP = ROOT / "overrides" / "config" / "ftbquests" / "quests_backup_original"
MARKER = BACKUP / ".backup_info.txt"


def _q(
    qid: str,
    title: str,
    x: float,
    y: float,
    icon: str,
    deps: list[str] | None = None,
    shape: str = "circle",
    size: float = 1.0,
    subtitle: str = "",
    desc: str | None = None,
    theme: str | None = None,
) -> str:
    lines = ["\t\t{"]
    if deps:
        dep_str = ", ".join(f'"{d}"' for d in deps)
        lines.append(f"\t\t\tdependencies: [{dep_str}]")
    if desc:
        lines.append("\t\t\tdescription: [")
        for part in desc.split("|"):
            lines.append(f'\t\t\t\t"{part}"')
        lines.append("\t\t\t]")
    lines.append(f'\t\t\ticon: {{ id: "{icon}" }}')
    lines.append(f'\t\t\tid: "{qid}"')
    if theme:
        lines.append(f'\t\t\tquest_theme_override: "{theme}"')
    if subtitle:
        lines.append(f'\t\t\tsubtitle: "{subtitle}"')
    lines.append("\t\t\trewards: [")
    lines.append(f'\t\t\t\t{{ id: "R{qid[1:]}", type: "xp", xp: 10 }}')
    lines.append("\t\t\t]")
    lines.append(f'\t\t\tshape: "{shape}"')
    if size != 1.0:
        lines.append(f"\t\t\tsize: {size}d")
    lines.append("\t\t\ttasks: [{")
    lines.append(f'\t\t\t\tid: "T{qid[1:]}", title: "Готово", type: "checkmark"')
    lines.append("\t\t\t}]")
    lines.append(f'\t\t\ttitle: "{title}"')
    lines.append(f"\t\t\tx: {x}d")
    lines.append(f"\t\t\ty: {y}d")
    lines.append("\t\t}")
    return "\n".join(lines)


def _chapter(
    filename: str,
    cid: str,
    group: str,
    title: str,
    icon: str,
    order: int,
    progression: str,
    quests_body: str,
    subtitle: str = "Тестовый макет — TechnoMagic preview",
) -> str:
    hide = "true" if progression == "flexible" else "false"
    return f"""{{
\tdefault_quest_disable_jei: true
\tdefault_hide_dependency_lines: false
\tprogression_mode: "{progression}"
\thide_quest_until_deps_complete: {hide}
\thide_quest_details_until_startable: true
\tdefault_quest_shape: "circle"
\tfilename: "{filename}"
\tgroup: "{group}"
\ticon: {{ id: "{icon}" }}
\tid: "{cid}"
\torder_index: {order}
\tquest_links: [ ]
\tquests: [
{quests_body}
\t]
\tsubtitle: [
\t\t"{subtitle}"
\t]
\ttitle: "{title}"
}}
"""


def chapter_groups() -> str:
    return """{
\tchapter_groups: [
\t\t{ id: "B100000000000001", title: "Вступ" }
\t\t{ id: "B100000000000002", title: "Прохождение" }
\t\t{ id: "B100000000000003", title: "Технологии" }
\t\t{ id: "B100000000000004", title: "Магия и другое" }
\t]
}
"""


def data_snbt() -> str:
    return """{
\tdefault_autoclaim_rewards: "always"
\tdefault_consume_items: false
\tdefault_quest_disable_jei: true
\tdefault_quest_shape: "circle"
\tdefault_reward_team: true
\tdefault_team_reward: true
\tdisable_gui: false
\tdrop_book_on_death: false
\tdrop_loot_crates: false
\temergency_quests: [ ]
\temergency_quests_cooldown: 300
\tgrid_scale: 0.75d
\ticon: { id: "minecraft:writable_book" }
\tlock_message: "Сначала завершите предыдущие поручения."
\tloot_crate_no_drop: true
\tpause_game: false
\tprogression_mode: "linear"
\tquest_links: [ ]
\ttitle: "CoopTech [TEST TechnoMagic preview]"
\tversion: 14
}
"""


def build_chapters() -> dict[str, str]:
    chapters: dict[str, str] = {}

    w = [
        _q(
            "A901000000000001",
            "Сигнал якоря",
            0,
            0,
            "minecraft:oak_log",
            shape="gear",
            size=1.4,
            desc="§e[TEST]§r Макет «Добро пожаловать».|Лор CoopTech + ветвление как в ТехноМагии.",
        ),
        _q(
            "A901000000000002",
            "Полевой штаб",
            -3,
            2,
            "minecraft:chest",
            ["A901000000000001"],
            theme="branch_explore",
        ),
        _q(
            "A901000000000003",
            "Верстак экспедиции",
            0,
            2,
            "minecraft:crafting_table",
            ["A901000000000001"],
            theme="branch_craft",
        ),
        _q(
            "A901000000000004",
            "Компас биомов",
            3,
            2,
            "minecraft:compass",
            ["A901000000000001"],
            theme="branch_explore",
        ),
        _q(
            "A901000000000005",
            "Рубеж I",
            0,
            4,
            "cooptech:textures/quests/gate.png",
            ["A901000000000002", "A901000000000003", "A901000000000004"],
            shape="diamond",
            size=1.2,
            subtitle="2 из 3 · gate",
        ),
    ]
    chapters["tm_00_welcome.snbt"] = _chapter(
        "tm_00_welcome",
        "A900000000000001",
        "B100000000000001",
        "Добро пожаловать!",
        "minecraft:oak_log",
        0,
        "linear",
        ",\n".join(w),
    )

    guides = []
    grid = [
        ("Кодекс", "minecraft:book"),
        ("Кооп-клятва", "minecraft:compass"),
        ("Журнал", "kubejs:expedition_journal"),
        ("Реликварии", "minecraft:ender_chest"),
        ("Маяк", "minecraft:beacon"),
        ("Пайки", "farmersdelight:cooking_pot"),
        ("JEI", "minecraft:writable_book"),
        ("Карта", "minecraft:filled_map"),
        ("FTB Teams", "ftbquests:book"),
    ]
    ids = []
    for i, (name, icon) in enumerate(grid):
        row, col = divmod(i, 3)
        qid = f"A9020000000000{i + 1:02d}"
        ids.append(qid)
        guides.append(_q(qid, name, (col - 1) * 2.5, row * 2, icon))
    guides.append(
        _q(
            "A902000000000010",
            "Хаб гайдов",
            0,
            7,
            "minecraft:torch",
            deps=ids[:3],
            shape="hexagon",
            size=1.3,
            desc="§e[TEST]§r Центральный узел как жёлтый хаб в ТехноМагии.",
        )
    )
    chapters["tm_01_guides.snbt"] = _chapter(
        "tm_01_guides",
        "A900000000000002",
        "B100000000000001",
        "Гайды",
        "minecraft:book",
        1,
        "linear",
        ",\n".join(guides),
    )

    main_defs = [
        ("tm_02_main_start", "A900000000000003", "Глава 1: Начало", "minecraft:iron_pickaxe", 0),
        ("tm_03_main_flux", "A900000000000004", "Глава 2: Энергоконтур", "thermal:energy_cell", 1),
        ("tm_04_main_molecular", "A900000000000005", "Глава 3: Молекулярка", "ae2:certus_quartz_crystal", 2),
        (
            "tm_05_main_production",
            "A900000000000006",
            "Глава 4: Промышленный разлом",
            "mekanism:basic_control_circuit",
            3,
        ),
        ("tm_06_main_nano", "A900000000000007", "Глава 5: Нанослой", "minecraft:netherite_ingot", 4),
        ("tm_07_main_finale", "A900000000000008", "Глава 6: Схождение", "minecraft:nether_star", 5),
    ]
    prev_gate: str | None = None
    for idx, (fname, chap_id, chap_title, chap_icon, order) in enumerate(main_defs):
        base = 903 + idx
        intro = f"A{base}00000000001"
        b1 = f"A{base}00000000002"
        b2 = f"A{base}00000000003"
        b3 = f"A{base}00000000004"
        gate = f"A{base}00000000005"
        intro_deps = [prev_gate] if prev_gate else None
        qs = [
            _q(
                intro,
                "Старт главы",
                0,
                0,
                chap_icon,
                deps=intro_deps,
                shape="gear",
                size=1.3,
                desc=f"§e[TEST]§r {chap_title}.|Главная линия «Прохождение».",
            ),
            _q(b1, "Ветка A", -3, 2, "minecraft:iron_ingot", [intro], theme="branch_mine"),
            _q(b2, "Ветка B", 0, 2, "minecraft:redstone", [intro], theme="branch_craft"),
            _q(b3, "Ветка C", 3, 2, "minecraft:gold_ingot", [intro], theme="branch_coop"),
            _q(
                gate,
                "Рубеж главы",
                0,
                4,
                "cooptech:textures/quests/gate.png",
                [b1, b2, b3],
                shape="diamond",
                size=1.2,
                subtitle="2 из 3",
                desc="§e[TEST]§r Gate открывает сайд-ветки модов.",
            ),
        ]
        prev_gate = gate
        chapters[f"{fname}.snbt"] = _chapter(
            fname, chap_id, "B100000000000002", chap_title, chap_icon, order, "linear", ",\n".join(qs)
        )

    thermal = [
        _q(
            "A910000000000001",
            "Открыто: Thermal",
            0,
            6,
            "cooptech:textures/quests/chapter_start.png",
            ["A90300000000005"],
            shape="hexagon",
            desc="§e[TEST]§r Открывается после Рубежа Гл.1.",
        ),
        _q("A910000000000002", "Machine Frame", 0, 0, "thermal:machine_frame", ["A910000000000001"]),
        _q(
            "A910000000000003",
            "Redstone Furnace",
            -3,
            -2,
            "thermal:machine_furnace",
            ["A910000000000002"],
            theme="branch_craft",
        ),
        _q(
            "A910000000000004",
            "Pulverizer",
            3,
            -2,
            "thermal:pulverizer",
            ["A910000000000002"],
            theme="branch_craft",
        ),
        _q(
            "A910000000000005",
            "Energy Cell",
            0,
            -4,
            "thermal:energy_cell",
            ["A910000000000003", "A910000000000004"],
            shape="diamond",
        ),
    ]
    chapters["tm_side_thermal.snbt"] = _chapter(
        "tm_side_thermal",
        "A900000000000010",
        "B100000000000003",
        "Thermal Expansion",
        "thermal:machine_frame",
        0,
        "flexible",
        ",\n".join(thermal),
    )

    flux = [
        _q("A911000000000001", "Открыто: Flux", 0, 4, "minecraft:redstone_block", ["A90400000000005"]),
        _q("A911000000000002", "Flux Dust", 0, 2, "minecraft:glowstone_dust", ["A911000000000001"]),
        _q("A911000000000003", "Flux Plug", 0, 0, "minecraft:observer", ["A911000000000002"]),
        _q("A911000000000004", "Wireless network", 0, -2, "minecraft:end_rod", ["A911000000000003"], shape="diamond"),
    ]
    chapters["tm_side_flux.snbt"] = _chapter(
        "tm_side_flux",
        "A900000000000011",
        "B100000000000003",
        "Flux Networks",
        "minecraft:redstone_block",
        1,
        "flexible",
        ",\n".join(flux),
    )

    net = [
        _q("A912000000000001", "Открыто: Сеть", 0, 4, "ae2:fluix_crystal", ["A90500000000005"]),
        _q("A912000000000002", "Certus", -2, 2, "ae2:certus_quartz_crystal", ["A912000000000001"]),
        _q("A912000000000003", "ME Drive", 2, 2, "ae2:drive", ["A912000000000001"]),
        _q(
            "A912000000000004",
            "Autocraft",
            0,
            0,
            "ae2:crafting_unit",
            ["A912000000000002", "A912000000000003"],
            shape="diamond",
        ),
    ]
    chapters["tm_side_network.snbt"] = _chapter(
        "tm_side_network",
        "A900000000000012",
        "B100000000000003",
        "Продвинутое хранилище",
        "ae2:controller",
        2,
        "flexible",
        ",\n".join(net),
    )

    drac = [
        _q("A913000000000001", "Открыто: Draconic", 0, 6, "minecraft:dragon_breath", ["A90800000000005"]),
        _q("A913000000000002", "Draconium Dust", 0, 4, "minecraft:amethyst_shard", ["A913000000000001"]),
        _q("A913000000000003", "Wyvern Core", 0, 2, "minecraft:echo_shard", ["A913000000000002"]),
        _q("A913000000000004", "Chaos Shard", 0, 0, "minecraft:nether_star", ["A913000000000003"], shape="diamond"),
    ]
    chapters["tm_side_draconic.snbt"] = _chapter(
        "tm_side_draconic",
        "A900000000000013",
        "B100000000000003",
        "Draconic Evolution",
        "minecraft:dragon_head",
        3,
        "flexible",
        ",\n".join(drac),
    )

    kq = [_q("A914000000000001", "Открыто: Кухня", 0, 4, "farmersdelight:cooking_pot", ["A90300000000005"])]
    center = "A914000000000002"
    kq.append(
        _q(
            center,
            "Кухня якоря",
            0,
            0,
            "farmersdelight:cooking_pot",
            ["A914000000000001"],
            shape="gear",
            size=1.3,
        )
    )
    kitchen_items = [
        ("Рис", "farmersdelight:cooked_rice", -3, -2),
        ("Салат", "farmersdelight:mixed_salad", 3, -2),
        ("Пирог", "farmersdelight:apple_pie", -3, 2),
        ("Суп", "farmersdelight:beef_stew", 3, 2),
    ]
    for i, (name, icon, x, y) in enumerate(kitchen_items, start=3):
        kq.append(_q(f"A9140000000000{i:02d}", name, x, y, icon, [center], theme="branch_craft"))
    chapters["tm_side_kitchen.snbt"] = _chapter(
        "tm_side_kitchen",
        "A900000000000014",
        "B100000000000004",
        "Кухня",
        "farmersdelight:cooking_pot",
        0,
        "flexible",
        ",\n".join(kq),
    )

    arc = [
        _q("A915000000000001", "Открыто: Арканум", 0, 2, "irons_spellbooks:arcane_essence", ["A90300000000005"]),
        _q("A915000000000002", "Пергамент", 0, 0, "irons_spellbooks:common_ink", ["A915000000000001"]),
        _q(
            "A915000000000003",
            "Посох",
            0,
            -2,
            "irons_spellbooks:graybeard_staff",
            ["A915000000000002"],
            shape="diamond",
        ),
    ]
    chapters["tm_side_arcane.snbt"] = _chapter(
        "tm_side_arcane",
        "A900000000000015",
        "B100000000000004",
        "Арканум",
        "irons_spellbooks:arcane_essence",
        1,
        "flexible",
        ",\n".join(arc),
    )

    sg = [
        _q("A916000000000001", "Открыто: Silent Gear", 0, 4, "minecraft:diamond_pickaxe", ["A90700000000005"]),
        _q("A916000000000002", "Шаблон", 0, 2, "minecraft:paper", ["A916000000000001"]),
        _q(
            "A916000000000003",
            "Кастомная кирка",
            0,
            0,
            "minecraft:diamond_pickaxe",
            ["A916000000000002"],
            shape="diamond",
        ),
    ]
    chapters["tm_side_silent_gear.snbt"] = _chapter(
        "tm_side_silent_gear",
        "A900000000000016",
        "B100000000000004",
        "Silent Gear",
        "minecraft:diamond_pickaxe",
        2,
        "flexible",
        ",\n".join(sg),
    )

    return chapters


def install() -> None:
    if BACKUP.exists() and any(BACKUP.iterdir()):
        print(f"Бекап уже есть: {BACKUP}")
        print("Для повторного install спочатку: python scripts/quests_technomagic_preview.py restore")
        sys.exit(1)

    if not QUESTS.exists():
        print(f"Немає папки квестів: {QUESTS}")
        sys.exit(1)

    print(f"Бекап -> {BACKUP}")
    shutil.copytree(QUESTS, BACKUP)
    MARKER.write_text(
        "CoopTech FTB Quests — оригінал до TechnoMagic preview.\n"
        "Відкат: python scripts/quests_technomagic_preview.py restore\n",
        encoding="utf-8",
    )

    chapters_dir = QUESTS / "chapters"
    for old in chapters_dir.glob("*.snbt"):
        old.unlink()

    (QUESTS / "chapter_groups.snbt").write_text(chapter_groups(), encoding="utf-8", newline="\n")
    (QUESTS / "data.snbt").write_text(data_snbt(), encoding="utf-8", newline="\n")

    built = build_chapters()
    for name, body in built.items():
        (chapters_dir / name).write_text(body, encoding="utf-8", newline="\n")

    print(f"Встановлено {len(built)} тестових глав.")
    print("У грі: повний перезапуск -> FTB Quests -> перевірте 4 групи в сайдбарі.")
    print("Відкат: python scripts/quests_technomagic_preview.py restore")


def restore() -> None:
    if not BACKUP.exists():
        print(f"Бекап не знайдено: {BACKUP}")
        sys.exit(1)

    if QUESTS.exists():
        shutil.rmtree(QUESTS)
    shutil.copytree(BACKUP, QUESTS)
    print(f"Відновлено з {BACKUP}")
    print("Повний перезапуск Minecraft.")


def status() -> None:
    if BACKUP.exists():
        n = len(list((BACKUP / "chapters").glob("*.snbt"))) if (BACKUP / "chapters").exists() else 0
        print(f"Бекап: є ({n} глав у backup)")
    else:
        print("Бекап: немає")

    if QUESTS.exists():
        active = list((QUESTS / "chapters").glob("*.snbt"))
        preview = sum(1 for f in active if f.name.startswith("tm_"))
        print(f"Активно: {len(active)} глав ({preview} tm_* preview)")
        data = (QUESTS / "data.snbt").read_text(encoding="utf-8-sig")
        if "TEST TechnoMagic preview" in data:
            print("Режим: TEST PREVIEW")
        else:
            print("Режим: оригінал (або після restore)")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "install":
        install()
    elif cmd == "restore":
        restore()
    elif cmd == "status":
        status()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
