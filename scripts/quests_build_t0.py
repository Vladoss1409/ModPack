#!/usr/bin/env python3
"""Generate T0 main chapter «Разлом» — journal-voice lore."""
from __future__ import annotations

import json
from pathlib import Path

from quest_rewards import branch_rewards_from_tasks, gate_rewards

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "overrides" / "config" / "ftbquests" / "quests" / "chapters"
GROUP = "B100000000000002"


def snbt_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def qid(n: int) -> str:
    return f"5217A{n:011d}"


def tid(n: int) -> str:
    return f"5217B{n:011d}"


def rid(n: int) -> str:
    return f"5217D{n:011d}"


def lore(main: str, flavor: str) -> list[str]:
    return [main, "", f"§o§8«{flavor}»§r"]


def gate_desc(text: str) -> list[str]:
    return [
        f"§dРубеж.§r {text}",
        "",
        "§7Нужны §eвсе 4§r ветки волны.",
        "§7Кооп: делите ветки между напарником.",
    ]


def wave_branch_deps(start: int) -> list[str]:
    return [qid(start + i) for i in range(4)]


def item_task(n: int, item: str, title: str, count: int = 1) -> str:
    c = f", count: {count}L" if count > 1 else ""
    return f'{{ id: "{tid(n)}", item: "{item}", title: {snbt_str(title)}{c}, type: "item" }}'


def check_task(n: int, title: str) -> str:
    return f'{{ id: "{tid(n)}", title: {snbt_str(title)}, type: "checkmark" }}'


def item_reward(n: int, item: str, count: int = 1) -> str:
    c = f", count: {count}" if count > 1 else ""
    return f'{{ id: "{rid(n)}", item: "{item}"{c}, type: "item" }}'


def xp_reward(n: int, xp: int) -> str:
    return f'{{ id: "{rid(n)}", type: "xp", xp: {xp} }}'


def quest_block(
    n: int,
    *,
    title: str,
    desc: list[str],
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
    lines = ["\t\t{"]
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
    lines.append(f'\t\t\tid: "{qid(n)}"')
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


def gate_deps(gate_n: int) -> list[str]:
    if gate_n == 8:
        return [qid(1)] + wave_branch_deps(2)
    if gate_n == 15:
        return [qid(8)] + wave_branch_deps(9)
    return [qid(15)] + wave_branch_deps(16)


def pool_tags(tag: str, pool_index: int, wave: int) -> list[str]:
    tags = ["branch_pool", f"pool_t0_w{wave}"]
    tags.append(tag)
    if pool_index in (1, 3):
        tags.append("branch_exclusive")
    return tags


def t0_branch_rewards(n: int, tasks: list[str], *, optional: bool = False) -> list[str]:
    return branch_rewards_from_tasks(
        tasks,
        0,
        item_fn=lambda rid, item, count: item_reward(rid, item, count),
        xp_fn=lambda rid, xp: xp_reward(rid, xp),
        reliquary_fn=lambda rid, item: item_reward(rid, item),
        rid_item=0x40 + n,
        rid_xp=0x50 + n,
        rid_relic=0x60 + n,
        quest_num=n,
        optional=optional,
    )


def build_t0() -> str:
    xs_w1 = [-6, -2, 2, 6]
    quests: list[str] = []

    quests.append(
        quest_block(
            1,
            title="Пробуждение у разлома",
            desc=[
                "§l[ T0 · Разлом ]§r",
                "",
                "§7Проснулся под гулом земли. Сканер на поясе уже мигал — §dгеотермальный разлом Якоря§r",
                "§7дышит паром и кислотой. Неба почти не видно, связи нет.",
                "",
                "§7Открыл блокнот. Первая строка: §eвыжить, обжить лагерь, поймать искру§r —",
                "§7без неё машины останутся чертежом.",
                "",
                "§8Цель записи: дойти до §eЯкорной искры§r и открыть путь к первому тиру.",
            ],
            icon="minecraft:compass",
            tasks=[check_task(1, "Записать пробуждение и принять поручение")],
            x=0,
            y=0,
            rewards=[
                item_reward(1, "kubejs:expedition_journal"),
                item_reward(28, "kubejs:journal_page_rift"),
                item_reward(2, "minecraft:torch", 8),
                xp_reward(3, 20),
            ],
            shape="hexagon",
            size=1.5,
        )
    )

    w1 = [
        (
            2,
            "Древесина разлома",
            lore(
                "Первым делом — древесина. Без рукояти не собрать ни кирку, ни топор.",
                "Древесина у разлома звенит сухо — лес помнит мир до трещины.",
            ),
            "minecraft:oak_log",
            [item_task(2, "minecraft:oak_log", "Срубить древесину у разлома", 16)],
            "branch_craft",
        ),
        (
            3,
            "Каменный век",
            lore(
                "Камень держит первый инструмент. Набью породы — пригодится и на печь.",
                "Камень тёплый от геотермы — Якорь греет даже породу.",
            ),
            "minecraft:cobblestone",
            [item_task(3, "minecraft:cobblestone", "Добыть булыжник", 32)],
            "branch_mine",
            [item_reward(4, "minecraft:stone_pickaxe")],
        ),
        (
            4,
            "Полевой паёк",
            lore(
                "Голодным разлом не пройти. Сварю хоть простой паёк — силы уходят быстрее, чем кажется.",
                "Голод обостряет слух: у разлома кажется, будто он шепчет ближе.",
            ),
            "minecraft:bread",
            [item_task(4, "minecraft:bread", "Приготовить хлеб", 3)],
            "branch_craft",
            [item_reward(5, "minecraft:apple", 6)],
        ),
        (
            5,
            "Железная жила",
            lore(
                "В породе — железо. С него, по записям предшественников, начинается всё остальное.",
                "Руда фонит в руке — Якорь будто метит металл для будущих машин.",
            ),
            "minecraft:raw_iron",
            [item_task(5, "minecraft:raw_iron", "Добыть сырое железо", 8)],
            "branch_mine",
            [xp_reward(6, 15)],
        ),
    ]
    for i, (n, title, desc, icon, tasks, tag, *extra_rewards) in enumerate(w1):
        rewards = list(extra_rewards[0]) if extra_rewards else t0_branch_rewards(n, tasks)
        quests.append(
            quest_block(
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=tasks,
                x=xs_w1[i],
                y=2,
                deps=[qid(1)],
                tags=pool_tags(tag, i, 1),
                rewards=rewards,
            )
        )

    quests.append(
        quest_block(
            6,
            title="Ночлег у костра",
            desc=lore(
                "§8Опционально.§r Поставлю кровать у костра — чтобы ночь не отбросила к разлому без сил.",
                "У огня ночь не отматывает назад — так писали те, кто успел оставить записку.",
            ),
            icon="minecraft:red_bed",
            tasks=[item_task(6, "minecraft:red_bed", "Поставить кровать у лагеря")],
            x=-8,
            y=3.5,
            deps=[qid(2)],
            rewards=[xp_reward(7, 10)],
            size=0.75,
        )
    )
    quests.append(
        quest_block(
            7,
            title="Кузнечный запас",
            desc=lore(
                "§8Опционально.§r Переплавлю руду в слитки — запас на инструменты и первую раму.",
                "Слитки лягут в основу всего, что мы построим здесь.",
            ),
            icon="minecraft:iron_ingot",
            tasks=[item_task(7, "minecraft:iron_ingot", "Переплавить железные слитки", 16)],
            x=8,
            y=3.5,
            deps=[qid(5)],
            rewards=[item_reward(8, "minecraft:bucket")],
            size=0.75,
        )
    )

    quests.append(
        quest_block(
            8,
            title="Закрепиться у разлома",
            desc=gate_desc(
                "Записал: первая волна позади. Лагерь дышит, руки помнят удар топора. "
                "Кодекс не пустит дальше, пока не закрою все четыре линии."
            ),
            icon="kubejs:quest_gate",
            tasks=[check_task(8, "Отметить рубеж в журнале")],
            x=0,
            y=4.5,
            deps=gate_deps(8),
            rewards=gate_rewards(
                0,
                item_fn=lambda rid, item, count=1: item_reward(rid, item, count),
                xp_fn=lambda rid, xp: xp_reward(rid, xp),
                reliquary_fn=lambda rid, item: item_reward(rid, item),
                page_item="kubejs:journal_page_camp",
                rid_page=29,
                rid_xp=9,
                rid_relic=0xD8,
            ),
            shape="diamond",
            size=1.2,
        )
    )

    w2 = [
        (
            9,
            "Железная печь",
            lore(
                "Железная печь плавит сама — первый шаг от костра к настоящему лагерю.",
                "Печь, что не требует руки у дверцы, — роскошь, которую мы заслужили.",
            ),
            "ironfurnaces:iron_furnace",
            [item_task(9, "ironfurnaces:iron_furnace", "Собрать железную печь")],
            "branch_craft",
            [item_reward(10, "minecraft:coal", 8)],
            "gear",
        ),
        (
            10,
            "Полевая кухня",
            lore(
                "Котёл кухни превращает сырьё в сытные блюда — экспедиция держится на горячем.",
                "Горячий котёл — сердце лагеря; на пустой похлёбке далеко не уйдёшь.",
            ),
            "farmersdelight:cooking_pot",
            [item_task(10, "farmersdelight:cooking_pot", "Собрать котёл Farmer's Delight")],
            "branch_craft",
            [item_reward(11, "minecraft:bread", 4)],
            "gear",
        ),
        (
            11,
            "Склад экспедиции",
            lore(
                "Контроллер ящиков связывает склад в сеть. Порядок в вещах — порядок в голове.",
                "Хаос разлома любит беспорядок; я не дам ему зайти в сундуки.",
            ),
            "storagedrawers:controller",
            [item_task(11, "storagedrawers:controller", "Собрать контроллер ящиков")],
            "branch_craft",
            [xp_reward(12, 20)],
            "gear",
        ),
        (
            12,
            "Угольный запас",
            lore(
                "Древесный уголь не кончится так быстро, как ветки у костра. Запас на печи и факелы.",
                "Свет держит периметр — без огня трещины кажутся ближе.",
            ),
            "minecraft:charcoal",
            [item_task(12, "minecraft:charcoal", "Накопать древесный уголь", 32)],
            "branch_mine",
            [item_reward(13, "minecraft:torch", 16)],
            "circle",
        ),
    ]
    for i, row in enumerate(w2):
        n, title, desc, icon, tasks, tag, rewards, shape = row
        quests.append(
            quest_block(
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=tasks,
                x=xs_w1[i],
                y=6,
                deps=[qid(8), qid(2 + i)],
                tags=pool_tags(tag, i, 2),
                rewards=rewards,
                shape=shape,
            )
        )

    quests.append(
        quest_block(
            13,
            title="Сортировка",
            desc=lore(
                "§8Опционально.§r Воронки сбросят добычу прямо в ящики — меньше беготни между сундуками.",
                "Пусть железо трудится за меня — руки нужны для разлома, не для перекладывания.",
            ),
            icon="minecraft:hopper",
            tasks=[item_task(13, "minecraft:hopper", "Собрать воронки", 2)],
            x=8,
            y=7.5,
            deps=[qid(11)],
            rewards=[xp_reward(14, 15)],
            size=0.75,
        )
    )
    quests.append(
        quest_block(
            14,
            title="Сытный обед",
            desc=lore(
                "§8Опционально.§r Горячий обед на кухне — больше сил на следующую вылазку.",
                "Сытый разведчик уходит дальше и возвращается живым.",
            ),
            icon="minecraft:cooked_beef",
            tasks=[item_task(14, "minecraft:cooked_beef", "Приготовить жареное мясо", 8)],
            x=-4,
            y=7.5,
            deps=[qid(10)],
            rewards=[xp_reward(15, 15)],
            size=0.75,
        )
    )
    quests.append(
        quest_block(
            28,
            title="Печёный провиант",
            desc=lore(
                "§8Опционально.§r Печёный картофель на железной печи — долгий запас в кармане.",
                "Обратный путь всегда длиннее: разлом сдвигает тропы, пока спишь.",
            ),
            icon="minecraft:baked_potato",
            tasks=[item_task(28, "minecraft:baked_potato", "Испечь картофель", 8)],
            x=-8,
            y=7.5,
            deps=[qid(9)],
            rewards=[xp_reward(16, 15)],
            size=0.75,
        )
    )

    quests.append(
        quest_block(
            15,
            title="Обжитой лагерь",
            desc=gate_desc(
                "Печь гудит, котёл кипит, ящики помнят, что в них лежит. Лагерь перестал быть временным."
                " Теперь — сырьё под первую энергию."
            ),
            icon="kubejs:quest_gate",
            tasks=[check_task(15, "Отметить второй рубеж")],
            x=0,
            y=8.5,
            deps=gate_deps(15),
            rewards=gate_rewards(
                0,
                item_fn=lambda rid, item, count=1: item_reward(rid, item, count),
                xp_fn=lambda rid, xp: xp_reward(rid, xp),
                reliquary_fn=lambda rid, item: item_reward(rid, item),
                page_item="kubejs:journal_page_home",
                rid_page=30,
                rid_xp=17,
                rid_relic=0xD9,
            ),
            shape="diamond",
            size=1.2,
        )
    )

    w3 = [
        (
            16,
            "Медь и сплавы",
            lore(
                "Медь пойдёт в проводку первых машин. Набью запас, пока руки ещё помнят кирку.",
                "Медь тёплая на ощупь — будто Якорь уже тянет её в контур.",
            ),
            "minecraft:copper_ingot",
            [item_task(16, "minecraft:copper_ingot", "Добыть медные слитки", 16)],
            "branch_mine",
        ),
        (
            17,
            "Редстоун-разведка",
            lore(
                "Редстоун — кровь механизмов. Без него искра так и останется идеей в блокноте.",
                "Редстоун гудит в такт разлому — слушаю, как пульс меняется с глубиной.",
            ),
            "minecraft:redstone",
            [item_task(17, "minecraft:redstone", "Добыть редстоун", 32)],
            "branch_mine",
        ),
        (
            18,
            "Кремень и щебень",
            lore(
                "Кремень из гравия — ударный элемент искры. Просею щебень у кислотных озёр.",
                "Кремень высечет первую искру — древний приём против новой бездны.",
            ),
            "minecraft:flint",
            [item_task(18, "minecraft:flint", "Добыть кремень", 8)],
            "branch_explore",
        ),
        (
            19,
            "Железная броня",
            lore(
                "Кислотные пары не щадят. Железная кираса — минимум, прежде чем лезть глубже.",
                "Металл на груди — цена ещё одного дня у разлома.",
            ),
            "minecraft:iron_chestplate",
            [item_task(19, "minecraft:iron_chestplate", "Сковать железную кирасу")],
            "branch_craft",
            [xp_reward(18, 20)],
        ),
    ]
    for i, row in enumerate(w3):
        n, title, desc, icon, tasks, tag, *extra = row
        rewards = list(extra[0]) if extra else t0_branch_rewards(n, tasks)
        quests.append(
            quest_block(
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=tasks,
                x=xs_w1[i],
                y=10,
                deps=[qid(15), qid(9 + i)],
                tags=pool_tags(tag, i, 3),
                rewards=rewards,
            )
        )

    quests.append(
        quest_block(
            27,
            title="Лук и стрелы",
            desc=lore(
                "§8Опционально.§r Соберу лук — хищники разлома чуют слабость слишком рано.",
                "Держу их на расстоянии стрелы — ближе не хочу.",
            ),
            icon="minecraft:bow",
            tasks=[item_task(27, "minecraft:bow", "Собрать лук")],
            x=-8,
            y=11.5,
            deps=[qid(16)],
            rewards=[item_reward(19, "minecraft:arrow", 16)],
            size=0.75,
        )
    )
    quests.append(
        quest_block(
            20,
            title="Компас разведки",
            desc=lore(
                "§8Опционально.§r Компас поможет не потерять лагерь в паре и тумане.",
                "Игла тянет домой — разлом крутит стороны света, как ему вздумается.",
            ),
            icon="minecraft:compass",
            tasks=[item_task(20, "minecraft:compass", "Собрать компас")],
            x=4,
            y=11.5,
            deps=[qid(18)],
            rewards=[xp_reward(20, 10)],
            size=0.75,
        )
    )
    quests.append(
        quest_block(
            21,
            title="Карта лагеря",
            desc=lore(
                "§8Опционально.§r Нанесу разлом на карту — измеренное пугает меньше неизвестного.",
                "Линии на бумаге — единственная география, которой я сейчас доверяю.",
            ),
            icon="minecraft:map",
            tasks=[item_task(21, "minecraft:map", "Составить карту лагеря")],
            x=8,
            y=11.5,
            deps=[qid(19)],
            rewards=[xp_reward(21, 10)],
            size=0.75,
        )
    )

    quests.append(
        quest_block(
            22,
            title="Готовность к энергии",
            desc=gate_desc(
                "Медь, редстоун, кремень — в ящиках; броня на плечах. В блокноте — чертёж рамы."
                " Разлом, кажется, готов принять искру."
            ),
            icon="kubejs:quest_gate",
            tasks=[check_task(22, "Отметить готовность к энергии")],
            x=0,
            y=12.5,
            deps=gate_deps(22),
            rewards=gate_rewards(
                0,
                item_fn=lambda rid, item, count=1: item_reward(rid, item, count),
                xp_fn=lambda rid, xp: xp_reward(rid, xp),
                reliquary_fn=lambda rid, item: item_reward(rid, item),
                page_item="kubejs:journal_page_ready",
                rid_page=31,
                rid_xp=22,
                rid_relic=0xDA,
            ),
            shape="diamond",
            size=1.2,
        )
    )

    quests.append(
        quest_block(
            23,
            title="Чертёж машинной рамы",
            desc=lore(
                "На странице блокнота — схема опорных блоков. Отолью железо: на них ляжет первая энергия.",
                "Чертёж дрожит от жара разлома — но линии читаются.",
            ),
            icon="minecraft:iron_block",
            tasks=[item_task(23, "minecraft:iron_block", "Отлить опорные блоки", 2)],
            x=-2,
            y=14,
            deps=[qid(22)],
            rewards=[xp_reward(23, 30)],
            shape="hexagon",
        )
    )
    quests.append(
        quest_block(
            24,
            title="Сбор для искры",
            desc=lore(
                "Соберу компоненты искры: железо, редстоун и кремень. Печь уже в лагере — осталось сложить.",
                "Три стихии в одной искре: металл, ток и удар кремня.",
            ),
            icon="minecraft:flint_and_steel",
            tasks=[
                item_task(24, "minecraft:iron_ingot", "Железные слитки", 8),
                item_task(25, "minecraft:redstone", "Редстоун", 8),
                item_task(26, "minecraft:flint", "Кремень", 2),
            ],
            x=2,
            y=14,
            deps=[qid(22)],
            shape="gear",
            rewards=t0_branch_rewards(24, [
                item_task(24, "minecraft:iron_ingot", "Железные слитки", 8),
            ]),
        )
    )
    quests.append(
        quest_block(
            25,
            title="Резонансный замер",
            desc=lore(
                "§8Опционально.§r Сетка редстоун-факелов — первый замер пульса у края разлома.",
                "График в блокноте ровнее — значит, искра примет контур.",
            ),
            icon="minecraft:redstone_torch",
            tasks=[item_task(30, "minecraft:redstone_torch", "Установить редстоун-факелы", 4)],
            x=5,
            y=15.5,
            deps=[qid(23)],
            rewards=[xp_reward(24, 15)],
            size=0.75,
        )
    )

    quests.append(
        quest_block(
            26,
            title="Якорная искра",
            desc=[
                "§l[ Финал тира T0 ]§r",
                "",
                "§7Печь раскалена, редстоун поёт в ящиках, кремень бьёт по металлу. Разлом §dвздрогнул§r —",
                "§7и впервые ответил не угрозой, а теплом в ладони.",
                "",
                "§7Записал: §eЯкорная искра§r поймана. С ней откроется §dМашинная рама§r —",
                "§7порог первого тира, где выживание станет производством.",
                "",
                "§8Награда — Якорная искра (рубеж T0 → T1).§r",
            ],
            icon="kubejs:anchor_spark",
            tasks=[check_task(29, "Зафиксировать искру в журнале")],
            x=0,
            y=16.5,
            deps=[qid(23), qid(24)],
            min_deps=2,
            rewards=[
                item_reward(25, "kubejs:anchor_spark"),
                item_reward(32, "kubejs:journal_page_spark"),
                item_reward(26, "minecraft:torch", 32),
                xp_reward(27, 120),
            ],
            shape="pentagon",
            size=1.6,
        )
    )

    body = "\n".join(quests)
    return f"""{{
\tdefault_quest_disable_jei: true
\tdefault_hide_dependency_lines: false
\tprogression_mode: "default"
\thide_quest_until_deps_complete: false
\thide_quest_details_until_startable: true
\tdefault_quest_shape: "circle"
\tfilename: "main_t0_rift"
\tgroup: "{GROUP}"
\ticon: {{ count: 1, id: "minecraft:flint_and_steel" }}
\tid: "5217C00000000000"
\torder_index: 10
\tquest_links: [ ]
\tquests: [
{body}
\t]
\tsubtitle: [
\t\t"T0 · ~30–45 мин"
\t]
\ttitle: "T0 · Разлом"
}}
"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "main_t0_rift.snbt"
    path.write_text(build_t0(), encoding="utf-8")
    print(f"  wrote {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
