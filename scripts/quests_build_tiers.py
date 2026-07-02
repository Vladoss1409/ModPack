#!/usr/bin/env python3
"""Generate T1–T5 main tier chapters from quest-tree.canvas.tsx blueprint."""
from __future__ import annotations

import json
from pathlib import Path

from quest_rewards import branch_rewards_from_tasks, gate_rewards

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "overrides" / "config" / "ftbquests" / "quests" / "chapters"
GROUP = "B100000000000002"
# T0 finale ID was hand-authored with suffix …26; T1+ finales use qid(tier, 26) → …1A
T0_FINALE = "5217A00000000026"


def prev_finale_id(tier: int) -> str | None:
    if tier == 1:
        return T0_FINALE
    if tier >= 2:
        return qid(tier - 1, 26)
    return None


def qid(tier: int, n: int) -> str:
    return f"522{tier}A{n:011X}"


def tid(tier: int, n: int) -> str:
    return f"522{tier}B{n:011X}"


def rid(tier: int, n: int) -> str:
    return f"522{tier}D{n:011X}"


def cid(tier: int) -> str:
    return f"522{tier}C00000000000"


def snbt_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def item_task(tier: int, n: int, item: str, count: int = 1, title: str | None = None) -> str:
    c = f", count: {count}L" if count > 1 else ""
    t = f', title: {snbt_str(title)}' if title else ""
    return f'{{ id: "{tid(tier, n)}", item: "{item}"{c}, type: "item"{t} }}'


def check_task(tier: int, n: int, title: str) -> str:
    return f'{{ id: "{tid(tier, n)}", title: {snbt_str(title)}, type: "checkmark" }}'


def xp_reward(tier: int, n: int, xp: int) -> str:
    return f'{{ id: "{rid(tier, n)}", type: "xp", xp: {xp} }}'


def item_reward(tier: int, n: int, item: str, count: int = 1) -> str:
    c = f", count: {count}" if count > 1 else ""
    return f'{{ id: "{rid(tier, n)}", item: "{item}"{c}, type: "item" }}'


def quest_block(
    tier: int,
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
    lines.append(f'\t\t\tid: "{qid(tier, n)}"')
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


def lore(main: str, flavor: str) -> list[str]:
    return [main, "", f"§o§8«{flavor}»§r"]


def gate_desc(text: str) -> list[str]:
    return [
        f"§dРубеж.§r {text}",
        "",
        "§7Нужны §eвсе 4§r ветки волны.",
        "§7Кооп: делите ветки между напарником.",
    ]


def wave_branch_deps(tier: int, start: int) -> list[str]:
    return [qid(tier, start + i) for i in range(4)]


# ── Tier definitions ─────────────────────────────────────────────────────────

TIERS: dict[int, dict] = {
    1: {
        "file": "main_t1_spark",
        "order": 20,
        "chapter_icon": "kubejs:anchor_spark",
        "title": "T1 · Искра",
        "subtitle": "T1 · ~45–60 мин",
        "intro_title": "Порог Thermal",
        "intro_desc": [
            "§l[ T1 · Искра ]§r",
            "",
            "§7§eЯкорная искра§r всё ещё тёплая в ладони. Разлом отпустил — в блокноте новая глава: §dThermal§r,",
            "§7первый RF, первая машинная рама.",
            "",
            "§7Записал цель: собрать §eМашинную раму§r — без неё ни одна машина не встанет.",
            "§7Потом плавка, дробление, энергия.",
            "",
            "§8Цель тира: запустить RF-контур и собрать §eЯкорную ячейку§r (рубеж T1→T2).",
        ],
        "intro_task": "Принять искру и открыть главу Thermal",
        "page_item": "kubejs:journal_page_spark_00",
        "finale_title": "Якорная ячейка",
        "finale_icon": "kubejs:anchor_cell",
        "finale_reward": "kubejs:anchor_cell",
        "finale_desc": [
            "§l[ Финал тира T1 ]§r",
            "",
            "§7Руда течёт через дробилку, RF стабилен, кузница молчит. Контур перестал глохнуть на каждом скачке.",
            "",
            "§7В журнале — новая отметка: §eЯкорная ячейка§r собрана. За ней откроется §dMekanism§r —",
            "§7порог настоящей промышленности.",
            "",
            "§8Награда — Якорная ячейка (рубеж T1 → T2).§r",
        ],
        "finale_task": "Зафиксировать ячейку в журнале",
        "pages": [
            "kubejs:journal_page_spark_01",
            "kubejs:journal_page_spark_02",
            "kubejs:journal_page_spark_03",
            "kubejs:journal_page_spark_04",
        ],
        "w1": [
            ("Машинная рама", lore("Сердце Thermal — рама, на которой стоят все машины. Соберу первой.", "Без рамы контур глохнет на первом же скачке — так пишут в старых записках."), "thermal:machine_frame", [item_task(1, 2, "thermal:machine_frame", title="Собрать машинную раму")], "gear", None, "branch_craft"),
            ("Красная печь", lore("Машинная печь Thermal плавит быстрее ванильной — пора отпустить железную печь с почётом.", "Первый автомат в контуре — печь, что не спит."), "thermal:machine_furnace", [item_task(1, 3, "thermal:machine_furnace", title="Собрать машинную печь")], "gear", None, "branch_craft"),
            ("Дробилка", lore("Pulverizer удваивает выход руды — основа автоплавки, о которой мечтал ещё у разлома.", "Дроблёная руда — вдвое богаче; так держали лагерь."), "thermal:machine_pulverizer", [item_task(1, 4, "thermal:machine_pulverizer", title="Собрать дробилку")], "gear", None, "branch_craft"),
            ("Урановая жила", lore("Уран для Powah — первый серьёзный генератор. Искать глубже, чем железо.", "Уран фонит сильнее редстоуна — разлом будто подсказывает жилу."), "powah:uraninite", [item_task(1, 5, "powah:uraninite", 16, title="Добыть урановую руду")], "circle", None, "branch_mine"),
            ("Молот ковки", lore("§8Опционально.§r IE Hammer — инструмент Immersive Engineering, если пойду в металл.", "Старый молот бьёт по металлу иначе — IE помнит."), "immersiveengineering:hammer", [item_task(1, 6, "immersiveengineering:hammer", title="Сковать молот IE")], "circle", 0.75, None),
            ("Шаблон ковки", lore("§8Опционально.§r Silent Gear — свой путь снаряжения, растущего вместе с экспедицией.", "Шаблон на доске — начало клинка, что растёт с тобой."), "silentgear:template_board", [item_task(1, 7, "silentgear:template_board", title="Вырезать шаблон ковки")], "circle", 0.75, None),
        ],
        "gate1_title": "Контур запущен",
        "gate1_desc": gate_desc("Первая волна Thermal и Powah позади. Рама стоит, руда идёт — записал рубеж."),
        "w2": [
            ("RF-катушка", lore("Катушка передаёт энергию между машинами Thermal — свяжу печь и дробилку.", "Ток по катушке — кровь контура."), "thermal:rf_coil", [item_task(1, 9, "thermal:rf_coil", 4, title="Собрать RF-катушки")], "gear", None, "branch_craft"),
            ("Сервопривод", lore("Серво автоматизирует ввод и вывод — меньше ручной возни у машин.", "Серво помнит ритм — машина работает без рук."), "thermal:redstone_servo", [item_task(1, 10, "thermal:redstone_servo", 4, title="Собрать сервоприводы")], "gear", None, "branch_craft"),
            ("Диэлектрик Powah", lore("Корпус Powah — основа энергохранилища. Соберу, пока генератор не перегревается.", "Кристалл в корпусе — батарея, что не боится скачков."), "powah:dielectric_casing", [item_task(1, 11, "powah:dielectric_casing", 4, title="Собрать диэлектрические корпуса")], "gear", None, "branch_craft"),
            ("Стол перековки", lore("Apotheosis — перековка и усиление снаряжения, если оружие снова должно расти.", "Новый стол у костра — оружие снова может меняться."), "apotheosis:simple_reforging_table", [item_task(1, 12, "apotheosis:simple_reforging_table", title="Собрать стол перековки")], "gear", None, "branch_craft"),
            ("Магматический динамо", lore("§8Опционально.§r Динамо жжёт лаву и даёт стабильный RF — если добуду лаву у разлома.", "Лава — дар и ловушка; динамо превращает её в силу."), "thermal:dynamo_magmatic", [item_task(1, 13, "thermal:dynamo_magmatic", title="Собрать магматическое динамо")], "circle", 0.75, None),
            ("Энергоячейка", lore("§8Опционально.§r Буфер RF на базе — подушка на пике нагрузки.", "Запас энергии спасает, когда дробилка жрёт всё сразу."), "thermal:energy_cell", [item_task(1, 14, "thermal:energy_cell", title="Собрать энергоячейку Thermal")], "circle", 0.75, None),
            ("Медный провод", lore("§8Опционально.§r Проводка между машинами — без неё контур рассыпается.", "Медь соединяет — я не хочу тянуть энергию вручную."), "thermal:energy_duct", [item_task(1, 28, "thermal:energy_duct", 8, title="Собрать энергоканалы")], "circle", 0.75, None),
        ],
        "gate2_title": "Автоматизация руды",
        "gate2_desc": gate_desc("Дробилка, серво и энергия связаны — руда течёт сама. Второй рубеж закрыт."),
        "w3": [
            ("Медь и никель", lore("Сплавы Thermal — основа продвинутых машин. Медь и никель в один заход.", "Никель редок у разлома — придётся копать глубже."), "minecraft:copper_ingot", [item_task(1, 16, "minecraft:copper_ingot", 32, title="Накопать медь"), item_task(1, 17, "thermal:nickel_ingot", 16, title="Накопать никель")], "circle", None, "branch_mine"),
            ("Серебро и олово", lore("Благородные металлы для апгрейдов Thermal — запас на будущие рецепты.", "Олово плавится быстро — удобно для первых улучшений."), "thermal:silver_ingot", [item_task(1, 18, "thermal:silver_ingot", 16, title="Накопать серебро"), item_task(1, 19, "thermal:tin_ingot", 16, title="Накопать олово")], "circle", None, "branch_mine"),
            ("Усиленный слиток", lore("Invar — сплав для машин, что выдерживают жар дробилки.", "Сплав держит форму дольше чистого железа."), "thermal:invar_ingot", [item_task(1, 20, "thermal:invar_ingot", 16, title="Выплавить инвар")], "circle", None, "branch_craft"),
            ("Стабилизатор RF", lore("Закалённое стекло и редстоун — стабильность контура перед рубежом.", "Стекло держит искру внутри корпуса — я видел, как без него горит."), "thermal:obsidian_glass", [item_task(1, 21, "thermal:obsidian_glass", 8, title="Собрать закалённое стекло")], "circle", None, "branch_craft"),
            ("Лук перековки", lore("§8Опционально.§r Первое усиленное оружие через Apotheosis.", "Перекованный лук — страх хищников разлома на дистанции."), "minecraft:bow", [item_task(1, 27, "minecraft:bow", title="Перековать лук")], "circle", 0.75, None),
            ("Кирка Silent Gear", lore("§8Опционально.§r Первая кирка Silent Gear — растёт с каждой жилой.", "Клинок из шаблона помнит каждый удар."), "silentgear:pickaxe", [item_task(1, 22, "silentgear:pickaxe", title="Собрать кирку Silent Gear")], "circle", 0.75, None),
            ("Базовая батарея Powah", lore("§8Опционально.§r Накопитель Powah — запас на ночную смену дробилки.", "Батарея гудит тихо — это звук спокойствия."), "powah:battery_basic", [item_task(1, 23, "powah:battery_basic", title="Собрать батарею Powah")], "circle", 0.75, None),
        ],
        "gate3_title": "Готовность к Mekanism",
        "gate3_desc": gate_desc("Сплавы, стабильность и запас энергии — в журнале. Осталось собрать ячейку."),
        "prep": [
            ("Чертёж ячейки", lore("В блокноте — схема якорной ячейки. Соберу ещё две рамы под корпус.", "Чертёж пульсирует — Mekanism ждёт за следующим порогом."), "thermal:machine_frame", [item_task(1, 24, "thermal:machine_frame", 2, title="Собрать рамы для ячейки")], "hexagon", None, None),
            ("Сбор для ячейки", lore("RF-катушки, редстоун и рама — тело якорной ячейки, которую я собираю сам.", "Три стихии в ячейке: ток, камень и искра T0."), "thermal:rf_coil", [item_task(1, 25, "thermal:rf_coil", 8, title="RF-катушки для ячейки"), item_task(1, 26, "minecraft:redstone_block", 4, title="Редстоун-блоки")], "gear", None, None),
        ],
        "prep_opt": ("Резонансный замер II", lore("§8Опционально.§r Замер RF-контура перед финалом — график должен быть ровным.", "Ровная линия на бумаге — ячейка примет резонанс."), "minecraft:redstone_torch", [item_task(1, 30, "minecraft:redstone_torch", 8, title="Установить факелы для замера")], "circle", 0.75),
    },
    2: {
        "file": "main_t2_circuit",
        "order": 30,
        "chapter_icon": "kubejs:anchor_cell",
        "title": "T2 · Контур",
        "subtitle": "T2 · ~60–75 мин",
        "intro_title": "Порог Mekanism",
        "intro_desc": [
            "§l[ T2 · Контур ]§r",
            "",
            "§7§eЯкорная ячейка§r открыла новую главу: §dMekanism§r — заводы, что перемалывают руду в пыль",
            "§7и выдают слитки втрое. Параллельно — Ender IO и Flux.",
            "",
            "§7Записал первый шаг: §eстальной корпус§r Mek. Без него ни одна машина не встанет.",
            "",
            "§8Цель тира: промышленная переработка и §eЯкорная матрица§r (рубеж T2→T3).",
        ],
        "intro_task": "Принять ячейку и открыть главу Mekanism",
        "page_item": "kubejs:journal_page_cell_00",
        "finale_title": "Якорная матрица",
        "finale_icon": "kubejs:anchor_matrix",
        "finale_reward": "kubejs:anchor_matrix",
        "finale_desc": [
            "§l[ Финал тира T2 ]§r",
            "",
            "§7Стальной корпус гудит, провода Ender IO светятся, Flux тянет энергию сквозь базу.",
            "",
            "§7§eЯкорная матрица§r собрана — в журнале отметка о пороге T2→T3. За ней §dAE2§r",
            "§7и сеть, что помнит каждый предмет.",
            "",
            "§8Награда — Якорная матрица (рубеж T2 → T3).§r",
        ],
        "finale_task": "Зафиксировать матрицу в журнале",
        "pages": [
            "kubejs:journal_page_cell_01",
            "kubejs:journal_page_cell_02",
            "kubejs:journal_page_cell_03",
            "kubejs:journal_page_cell_04",
        ],
        "w1": [
            ("Стальной корпус", lore("База Mekanism — без корпуса ни одна машина. Соберу первым делом.", "Сталь держит давление — Mek требует больше, чем Thermal."), "mekanism:steel_casing", [item_task(2, 2, "mekanism:steel_casing", 4, title="Собрать стальные корпуса")], "gear", None, "branch_craft"),
            ("Металлургический инфузер", lore("Инфузер Mek — первый шаг к сплавам, которые печь не смешает.", "Инфузер смешивает то, что казалось несовместимым."), "mekanism:metallurgic_infuser", [item_task(2, 3, "mekanism:metallurgic_infuser", title="Собрать металлургический инфузер")], "gear", None, "branch_craft"),
            ("Обогатительная фабрика", lore("Обогатитель удваивает руду — сердце промышленного Mek.", "Три руды на входе — больше слитков на выходе; так и записал в план."), "mekanism:enrichment_chamber", [item_task(2, 4, "mekanism:enrichment_chamber", title="Собрать обогатительную фабрику")], "gear", None, "branch_craft"),
            ("Проводящий сплав", lore("Проводящий сплав Ender IO — первый мост в другую ветку техники.", "Сплав слабо светится — будто помнит иной мир."), "enderio:conductive_alloy_ingot", [item_task(2, 5, "enderio:conductive_alloy_ingot", 16, title="Выплавить проводящий сплав")], "circle", None, "branch_craft"),
            ("Сплав душ", lore("§8Опционально.§r Колба душ Ender IO — моб становится ресурсом.", "Душа в стекле — спорная мораль, но эффективно."), "enderio:empty_soul_vial", [item_task(2, 6, "enderio:empty_soul_vial", title="Собрать колбу душ")], "circle", 0.75, None),
            ("Flux пыль", lore("§8Опционально.§r Flux-пыль — начало сети без проводов.", "Пыль тянет энергию сквозь воздух — странно, но работает."), "fluxnetworks:flux_dust", [item_task(2, 7, "fluxnetworks:flux_dust", 8, title="Собрать Flux-пыль")], "circle", 0.75, None),
        ],
        "gate1_title": "Промышленный старт",
        "gate1_desc": gate_desc("Mek и Ender IO встали на базу. Записал: промышленный ритм начался."),
        "w2": [
            ("Дробитель", lore("Дробитель Mek — вторая ступень переработки, руда не застаивается.", "Дробитель не спит — руда течёт рекой."), "mekanism:crusher", [item_task(2, 9, "mekanism:crusher", title="Собрать дробитель")], "gear", None, "branch_craft"),
            ("Энергетический куб", lore("Энергокуб Mek — буфер, чтобы завод не падал на пике.", "Куб гудит — это звук стабильности."), "mekanism:basic_energy_cube", [item_task(2, 10, "mekanism:basic_energy_cube", title="Собрать энергокуб")], "gear", None, "branch_craft"),
            ("Сплавная печь", lore("Сплавная печь EIO — три металла в одном блоке.", "Три слота — один сплав; экономия места и нервов."), "enderio:alloy_smelter", [item_task(2, 11, "enderio:alloy_smelter", title="Собрать сплавную печь")], "gear", None, "branch_craft"),
            ("Flux контроллер", lore("Flux-контроллер — энергия по всей базе без паутины проводов.", "Контроллер видит углы лагеря — я вижу меньше кабелей."), "fluxnetworks:flux_controller", [item_task(2, 12, "fluxnetworks:flux_controller", title="Собрать Flux-контроллер")], "gear", None, "branch_craft"),
            ("Газовый танк", lore("§8Опционально.§r Газовый танк Mek — хранение под давлением.", "С вентилем осторожнее — урок из разлома."), "mekanism:basic_chemical_tank", [item_task(2, 13, "mekanism:basic_chemical_tank", title="Собрать газовый танк")], "circle", 0.75, None),
            ("Конденсатор", lore("§8Опционально.§r Конденсатор EIO — запас для мощных ударов.", "Копит тихо — бьёт громко."), "enderio:basic_capacitor", [item_task(2, 14, "enderio:basic_capacitor", 4, title="Собрать конденсаторы")], "circle", 0.75, None),
            ("Магическая эссенция", lore("§8Опционально.§r Арканическая эссенция — зацепка к магии.", "Эссенция в ладони — заклинание ждёт формулы."), "irons_spellbooks:arcane_essence", [item_task(2, 28, "irons_spellbooks:arcane_essence", 16, title="Собрать магическую эссенцию")], "circle", 0.75, None),
        ],
        "gate2_title": "Энергоузел",
        "gate2_desc": gate_desc("Энергия и переработка держатся. Второй рубеж T2 — в журнале."),
        "w3": [
            ("Осмий", lore("Осмий Mek — редкий металл для роста завода.", "Синий слиток — Mek просит его всё громче."), "mekanism:ingot_osmium", [item_task(2, 16, "mekanism:ingot_osmium", 32, title="Накопать осмий")], "circle", None, "branch_mine"),
            ("Вибрантный сплав", lore("Вибрантный сплав — вершина линии Ender IO.", "Сплав поёт на частоте, которую слышит только сеть."), "enderio:vibrant_alloy_ingot", [item_task(2, 17, "enderio:vibrant_alloy_ingot", 16, title="Выплавить вибрантный сплав")], "circle", None, "branch_craft"),
            ("Продвинутая схема", lore("Продвинутая схема — мозг машин Mek.", "Схема помнит команды — я записываю свои."), "mekanism:advanced_control_circuit", [item_task(2, 18, "mekanism:advanced_control_circuit", 4, title="Собрать продвинутые схемы")], "circle", None, "branch_craft"),
            ("Flux точка", lore("Flux-точка — энергия в угол базы без новых проводов.", "Точка на стене — как розетка в пустоте."), "fluxnetworks:flux_point", [item_task(2, 19, "fluxnetworks:flux_point", 4, title="Установить Flux-точки")], "circle", None, "branch_craft"),
            ("Том заклинаний", lore("§8Опционально.§r Медный том заклинаний — тяжёлый, но нужный.", "Знание весит — я готов нести."), "irons_spellbooks:copper_spell_book", [item_task(2, 27, "irons_spellbooks:copper_spell_book", title="Собрать том заклинаний")], "circle", 0.75, None),
            ("Генератор", lore("§8Опционально.§r Тепловой генератор Mek — жар разлома в ток.", "Тепло, что раньше пугало, теперь кормит завод."), "mekanismgenerators:heat_generator", [item_task(2, 20, "mekanismgenerators:heat_generator", title="Собрать тепловой генератор")], "circle", 0.75, None),
            ("SAG Mill", lore("§8Опционально.§r SAG Mill — ещё один слой измельчения EIO.", "Руда уходит пылью — возвращается богаче."), "enderio:sag_mill", [item_task(2, 21, "enderio:sag_mill", title="Собрать SAG Mill")], "circle", 0.75, None),
        ],
        "gate3_title": "Готовность к сети",
        "gate3_desc": gate_desc("Сырьё для матрицы собрано. Осталось сложить якорь T2."),
        "prep": [
            ("Чертёж матрицы", lore("В блокноте — чертёж якорной матрицы. Ещё корпуса Mek под опору.", "Чертёж пульсирует — AE2 ждёт за следующей дверью."), "mekanism:steel_casing", [item_task(2, 24, "mekanism:steel_casing", 4, title="Корпуса под матрицу")], "hexagon", None, None),
            ("Сбор для матрицы", lore("Вибрантный сплав, схемы и сталь — тело матрицы своими руками.", "Три силы в одном кристалле: Mek, EIO и Flux."), "enderio:vibrant_alloy_ingot", [item_task(2, 25, "enderio:vibrant_alloy_ingot", 8, title="Сплав для матрицы"), item_task(2, 26, "mekanism:advanced_control_circuit", 4, title="Схемы для матрицы")], "gear", None, None),
        ],
        "prep_opt": ("Резонансный замер III", lore("§8Опционально.§r Замер промышленного контура перед финалом.", "Все три мода в такт — матрица примет сигнал."), "minecraft:comparator", [item_task(2, 30, "minecraft:comparator", 4, title="Замерить контур")], "circle", 0.75),
    },
    3: {
        "file": "main_t3_network",
        "order": 40,
        "chapter_icon": "kubejs:anchor_matrix",
        "title": "T3 · Сеть",
        "subtitle": "T3 · ~75–90 мин",
        "intro_title": "Порог AE2",
        "intro_desc": [
            "§l[ T3 · Сеть ]§r",
            "",
            "§7§eЯкорная матрица§r открыла §dApplied Energistics 2§r — сеть, что помнит",
            "§7каждый предмет на базе. EMC придёт сюда же, но как инструмент логистики.",
            "",
            "§7Первый шаг в блокноте: §eгравёр§r — без процессоров сеть слепа.",
            "",
            "§8Цель тира: рабочая ME-сеть и §eЯкорная сингулярность§r (рубеж T3→T4).",
        ],
        "intro_task": "Принять матрицу и открыть главу AE2",
        "page_item": "kubejs:journal_page_matrix_00",
        "finale_title": "Якорная сингулярность",
        "finale_icon": "kubejs:anchor_singularity",
        "finale_reward": "kubejs:anchor_singularity",
        "finale_desc": [
            "§l[ Финал тира T3 ]§r",
            "",
            "§7ME-контроллер пульсирует, автокрафт срабатывает, EMC слушается матрицы.",
            "",
            "§7§eЯкорная сингулярность§r собрана — порог T3→T4. В следующей главе §dDraconic§r",
            "§7и сила, что помнит древних драконов.",
            "",
            "§8Награда — Якорная сингулярность (рубеж T3 → T4).§r",
        ],
        "finale_task": "Зафиксировать сингулярность в журнале",
        "pages": ["kubejs:journal_page_matrix_01", "kubejs:journal_page_matrix_02", "kubejs:journal_page_matrix_03", "kubejs:journal_page_matrix_04"],
        "w1": [
            ("Гравёр AE2", lore("Гравёр — сердце процессоров AE2. Без него сеть слепа.", "Высечу мозг сети своими руками — так начинается T3."), "ae2:inscriber", [item_task(3, 2, "ae2:inscriber", title="Собрать гравёр AE2")], "gear", None, "branch_craft"),
            ("Кварц Certus", lore("Certus-кварц — кровь AE2. Наберу запас, пока жила не ушла глубже.", "Кристалл поёт на частоте якоря — я уже привыкаю к звуку."), "ae2:certus_quartz_crystal", [item_task(3, 3, "ae2:certus_quartz_crystal", 32, title="Добыть certus-кварц")], "circle", None, "branch_mine"),
            ("Fluix", lore("Fluix — мост между кварцем и редстоуном. Сеть оживёт здесь.", "Сплав светится — первый пульс ME."), "ae2:fluix_crystal", [item_task(3, 4, "ae2:fluix_crystal", 16, title="Синтезировать fluix")], "gear", None, "branch_craft"),
            ("Камень философов", lore("Камень философов ProjectE — EMC как логистика, не магия ради магии.", "Камень тяжёл — в нём спят рецепты мира."), "projecte:philosophers_stone", [item_task(3, 5, "projecte:philosophers_stone", title="Создать камень философов")], "gear", None, "branch_craft"),
            ("Трансмутационный стол", lore("§8Опционально.§r Первый стол трансмутации — EMC в действии.", "Стол помнит всё, что я на него положу."), "projecte:transmutation_table", [item_task(3, 6, "projecte:transmutation_table", title="Собрать стол трансмутации")], "circle", 0.75, None),
            ("ME-кабель", lore("§8Опционально.§r Первые fluix-кабели — нервы сети.", "Без кабеля терминал одинок."), "ae2:fluix_glass_cable", [item_task(3, 7, "ae2:fluix_glass_cable", 16, title="Собрать ME-кабели")], "circle", 0.75, None),
        ],
        "gate1_title": "Сеть зарождается",
        "gate1_desc": gate_desc("Гравёр, кварц, fluix и EMC — фундамент сети заложен."),
        "w2": [
            ("Процессор расчёта", lore("Процессор расчёта — мозг автокрафта, который я наконец соберу.", "Считает быстрее, чем я успеваю записывать."), "ae2:calculation_processor", [item_task(3, 9, "ae2:calculation_processor", 4, title="Собрать процессоры расчёта")], "gear", None, "branch_craft"),
            ("Инженерный процессор", lore("Инженерный процессор — для тяжёлой техники AE2.", "Чип для машин, что не прощают ошибок."), "ae2:engineering_processor", [item_task(3, 10, "ae2:engineering_processor", 4, title="Собрать инженерные процессоры")], "gear", None, "branch_craft"),
            ("ME-контроллер", lore("Контроллер — сердце ME-сети. Без него всё рассыпется.", "Пульс контроллера — пульс всего лагеря."), "ae2:controller", [item_task(3, 11, "ae2:controller", title="Собрать ME-контроллер")], "gear", None, "branch_craft"),
            ("Терминал", lore("ME-терминал — окно в склад, который помнит всё.", "Один экран — тысячи стаков в ладони."), "ae2:terminal", [item_task(3, 12, "ae2:terminal", title="Собрать ME-терминал")], "gear", None, "branch_craft"),
            ("EMC конденсатор", lore("§8Опционально.§r Алхимический сундук — накопление EMC.", "Жрёт предметы — отдаёт силу трансмутации."), "projecte:alchemical_chest", [item_task(3, 13, "projecte:alchemical_chest", title="Собрать алхимический сундук")], "circle", 0.75, None),
            ("ME-диск", lore("§8Опционально.§r Первый диск 1k — память сети.", "Диск помнит больше, чем я могу унести."), "ae2:item_storage_cell_1k", [item_task(3, 14, "ae2:item_storage_cell_1k", title="Собрать диск 1k")], "circle", 0.75, None),
            ("Заряженный кварц", lore("§8Опционально.§r Заряженный certus для продвинутых рецептов.", "Заряд в кристалле — сеть просит больше."), "ae2:charged_certus_quartz_crystal", [item_task(3, 28, "ae2:charged_certus_quartz_crystal", 16, title="Зарядить certus-кварц")], "circle", 0.75, None),
        ],
        "gate2_title": "ME-сеть работает",
        "gate2_desc": gate_desc("Контроллер, терминал и процессоры — сеть жива. Записал второй рубеж T3."),
        "w3": [
            ("Автокрафт", lore("Crafting CPU — сеть сама крафтит, я только заказываю.", "Автокрафт — конец эры беготни по сундукам."), "ae2:crafting_unit", [item_task(3, 16, "ae2:crafting_unit", 4, title="Собрать блоки автокрафта")], "gear", None, "branch_craft"),
            ("Шаблоны", lore("Пустые шаблоны — рецепты, записанные в кристалл.", "Каждый шаблон — один ритуал, что повторится сам."), "ae2:blank_pattern", [item_task(3, 17, "ae2:blank_pattern", 16, title="Собрать шаблоны")], "circle", None, "branch_craft"),
            ("Импорт шина", lore("Импорт-шина тянет предметы в сеть без моих рук.", "Шина питается — склад растёт сам."), "ae2:import_bus", [item_task(3, 18, "ae2:import_bus", 4, title="Установить импорт-шины")], "gear", None, "branch_craft"),
            ("Экспорт шина", lore("Экспорт-шина отдаёт из сети машинам.", "Машины снабжаются — я смотрю в журнал."), "ae2:export_bus", [item_task(3, 19, "ae2:export_bus", 4, title="Установить экспорт-шины")], "gear", None, "branch_craft"),
            ("Коллектор EMC", lore("§8Опционально.§r Коллектор MK1 — EMC из мира вокруг.", "Тянет ценность — спорно, но эффективно."), "projecte:collector_mk1", [item_task(3, 27, "projecte:collector_mk1", title="Собрать коллектор EMC")], "circle", 0.75, None),
            ("Беспроводной терминал", lore("§8Опционально.§r Беспроводной терминал — склад в кармане.", "Терминал следует за мной, как тень."), "ae2wtlib:wireless_universal_terminal", [item_task(3, 20, "ae2wtlib:wireless_universal_terminal", title="Собрать беспроводной терминал")], "circle", 0.75, None),
            ("4k диск", lore("§8Опционально.§r Диск 4k — память сети растёт.", "Четыре тысячи типов — база не захлебнётся."), "ae2:item_storage_cell_4k", [item_task(3, 21, "ae2:item_storage_cell_4k", title="Собрать диск 4k")], "circle", 0.75, None),
        ],
        "gate3_title": "Готовность к Draconic",
        "gate3_desc": gate_desc("Автокрафт и шины замкнули логистику. Готовлю сингулярность."),
        "prep": [
            ("Чертёж сингулярности", lore("Чертёж якорной сингулярности — сжать сеть в точку силы.", "Линии сходятся — Draconic ждёт за горизонтом."), "ae2:engineering_processor", [item_task(3, 24, "ae2:engineering_processor", 8, title="Процессоры под сингулярность")], "hexagon", None, None),
            ("Сбор для сингулярности", lore("Fluix, процессоры и стол EMC — тело сингулярности.", "Три силы в одной точке: сеть, EMC и матрица."), "ae2:fluix_crystal", [item_task(3, 25, "ae2:fluix_crystal", 32, title="Fluix для сингулярности"), item_task(3, 26, "projecte:transmutation_table", title="Стол EMC для сингулярности")], "gear", None, None),
        ],
        "prep_opt": ("Резонансный замер IV", lore("§8Опционально.§r Замер ME-контура перед финалом T3.", "Пульс ровный — сингулярность примет сеть."), "minecraft:repeater", [item_task(3, 30, "minecraft:repeater", 8, title="Замерить ME-контур")], "circle", 0.75),
    },
    4: {
        "file": "main_t4_dragon",
        "order": 50,
        "chapter_icon": "kubejs:anchor_singularity",
        "title": "T4 · Дракон",
        "subtitle": "T4 · ~90–120 мин",
        "intro_title": "Порог Draconic",
        "intro_desc": [
            "§l[ T4 · Дракон ]§r",
            "",
            "§7§eЯкорная сингулярность§r сжала логистику в одну точку — и открыла §dDraconic Evolution§r.",
            "§7Сила, что помнит древних драконов. В блокноте первый шаг: §eядро дракония§r.",
            "",
            "§7Дальше — fusion-крафт, реактор, Chaos Guardian. Я записал: без ядра вся ветка молчит.",
            "",
            "§8Цель тира: awakened-технологии и §eЯкорный нексус§r (рубеж T4→T5).",
        ],
        "intro_task": "Принять сингулярность и открыть главу Draconic",
        "page_item": "kubejs:journal_page_singularity_00",
        "finale_title": "Якорный нексус",
        "finale_icon": "kubejs:anchor_nexus",
        "finale_reward": "kubejs:anchor_nexus",
        "finale_desc": [
            "§l[ Финал тира T4 ]§r",
            "",
            "§7Драконий реактор гудит ровно. Awakened-металл течёт по инфузору, Chaos отступил.",
            "",
            "§7§eЯкорный нексус§r собран — в журнале отметка о пороге T4→T5. За ней §dnext_ae§r",
            "§7и финальная схватка со стабилизацией Якоря.",
            "",
            "§8Награда — Якорный нексус (рубеж T4 → T5).§r",
        ],
        "finale_task": "Зафиксировать нексус в журнале",
        "pages": ["kubejs:journal_page_singularity_01", "kubejs:journal_page_singularity_02", "kubejs:journal_page_singularity_03", "kubejs:journal_page_singularity_04"],
        "w1": [
            ("Ядро дракония", lore("Draconium Core — база всей Draconic. Соберу первым, пока сингулярность ещё тёплая.", "Ядро в ладони — дракон ещё не ушёл из металла."), "draconicevolution:draconium_core", [item_task(4, 2, "draconicevolution:draconium_core", title="Собрать ядро дракония")], "gear", None, "branch_craft"),
            ("Дракониевая пыль", lore("Draconium dust — первый контакт с модом. Наберу запас из глубинных жил.", "Пыль фиолетовая — разлом и дракон оказались родней, чем думал."), "draconicevolution:draconium_dust", [item_task(4, 3, "draconicevolution:draconium_dust", 32, title="Добыть дракониевую пыль")], "circle", None, "branch_mine"),
            ("Энергоядро DE", lore("Energy Core — сердце энергосистемы Draconic. Без него реактор — мечта.", "Ядро пульсирует — энергия дракона в корпусе."), "draconicevolution:energy_core", [item_task(4, 4, "draconicevolution:energy_core", title="Собрать энергоядро DE")], "gear", None, "branch_craft"),
            ("Пробуждённый слиток", lore("Awakened draconium — вершина металла DE. Первый шаг к awakened-технологиям.", "Пробуждённый металл помнит Chaos — беру осторожно."), "draconicevolution:awakened_draconium_ingot", [item_task(4, 5, "draconicevolution:awakened_draconium_ingot", 8, title="Выплавить пробуждённый слиток")], "gear", None, "branch_craft"),
            ("Меч Cataclysm", lore("§8Опционально.§r Первое оружие Cataclysm — пригодится до Chaos Guardian.", "Меч из руин — босс дрожит на расстоянии."), "cataclysm:black_steel_sword", [item_task(4, 6, "cataclysm:black_steel_sword", title="Сковать меч Cataclysm")], "circle", 0.75, None),
            ("Звезда Незера", lore("§8Опционально.§r Редкий компонент для ритуалов и финальных крафтов.", "Звезда холодная — Chaos любит контраст."), "minecraft:nether_star", [item_task(4, 7, "minecraft:nether_star", title="Добыть звезду Незера")], "circle", 0.75, None),
        ],
        "gate1_title": "Драконий старт",
        "gate1_desc": gate_desc("Draconic встал на базу — ядро, пыль, энергия. Записал первый рубеж T4."),
        "w2": [
            ("Дракониевый инфузор", lore("Fusion crafting — сердце DE. Здесь сливаются миры в один предмет.", "Инфузор гудит — я слышу дракона в металле."), "draconicevolution:wyvern_crafting_injector", [item_task(4, 9, "draconicevolution:wyvern_crafting_injector", 4, title="Установить инфузоры fusion")], "gear", None, "branch_craft"),
            ("Реактор DE", lore("Draconic Reactor — вершина генерации. Ставлю с осторожностью — ошибок не прощает.", "Реактор не спит — я тоже не буду, пока контур стабилен."), "draconicevolution:reactor_core", [item_task(4, 10, "draconicevolution:reactor_core", title="Собрать ядро реактора DE")], "gear", None, "branch_craft"),
            ("Полная EMC", lore("Трансмутационный планшет — пик ProjectE. EMC теперь в кармане.", "Материя светится — всё может стать всем."), "projecte:transmutation_tablet", [item_task(4, 11, "projecte:transmutation_tablet", title="Собрать планшет трансмутации")], "gear", None, "branch_craft"),
            ("Хаос-осколок", lore("Chaos shard — ключ к awakened. Добыча у Chaos Island не для слабых.", "Осколок режет реальность — рукавицы обязательны."), "draconicevolution:chaos_shard", [item_task(4, 12, "draconicevolution:chaos_shard", 4, title="Добыть хаос-осколки")], "circle", None, "branch_mine"),
            ("Драконье сердце", lore("§8Опционально.§r Dragon heart для ритуалов нексуса.", "Сердце ещё бьётся — уважаю добычу."), "draconicevolution:dragon_heart", [item_task(4, 13, "draconicevolution:dragon_heart", title="Добыть драконье сердце")], "circle", 0.75, None),
            ("Wyvern кирка", lore("§8Опционально.§r Первая кирка DE — руда сдаётся без боя.", "Кирка поёт на частоте дракона."), "draconicevolution:wyvern_pickaxe", [item_task(4, 14, "draconicevolution:wyvern_pickaxe", title="Сковать wyvern-кирку")], "circle", 0.75, None),
            ("Броня DE", lore("§8Опционально.§r Wyvern chestplate — живая броня.", "Броня растёт с носителем — как Silent Gear, но драконья."), "draconicevolution:wyvern_chestpiece", [item_task(4, 28, "draconicevolution:wyvern_chestpiece", title="Сковать wyvern-нагрудник")], "circle", 0.75, None),
        ],
        "gate2_title": "Энергия дракона",
        "gate2_desc": gate_desc("Реактор, инфузор и EMC — сила на пике. Второй рубеж T4 в журнале."),
        "w3": [
            ("Chaos Guardian", lore("Chaos Guardian — страж Draconic. Финальный бой перед нексусом.", "Страж Chaos — последний страж, которого я записал в план."), "draconicevolution:chaos_shard", [item_task(4, 16, "draconicevolution:chaos_shard", 16, title="Победить Chaos Guardian")], "circle", None, "branch_explore"),
            ("Awakened блок", lore("Awakened draconium block — для финальных крафтов нексуса.", "Блок тяжелее якоря — несём вдвоём."), "draconicevolution:awakened_draconium_block", [item_task(4, 17, "draconicevolution:awakened_draconium_block", 4, title="Собрать awakened-блоки")], "circle", None, "branch_craft"),
            ("Реликвария Cataclysm", lore("Трофей Cataclysm — знак победы над боссом ветки.", "Череп шепчет — следующий босс уже ближе."), "cataclysm:remnant_skull", [item_task(4, 18, "cataclysm:remnant_skull", title="Добыть реликварию Cataclysm")], "circle", None, "branch_explore"),
            ("Зерна бесконечности", lore("Grains of Infinity — мост к next_ae. Соберу запас заранее.", "Зёрна бесконечны — как аппетит разлома."), "enderio:grains_of_infinity", [item_task(4, 19, "enderio:grains_of_infinity", 32, title="Собрать зёрна бесконечности")], "circle", None, "branch_mine"),
            ("Draconic посох", lore("§8Опционально.§r Staff of power — сила дракона в руке.", "Посох гудит — я привыкаю к этому звуку."), "draconicevolution:draconic_staff", [item_task(4, 27, "draconicevolution:draconic_staff", title="Сковать draconic-посох")], "circle", 0.75, None),
            ("Red matter", lore("§8Опционально.§r Red matter — предел трансмутации ProjectE.", "Материя красная — граница, за которой EMC молчит."), "projecte:red_matter", [item_task(4, 20, "projecte:red_matter", title="Создать red matter")], "circle", 0.75, None),
            ("Chaos шард большой", lore("§8Опционально.§r Крупный chaotic shard — редкая добыча.", "Осколок режет воздух — храню в ME-ячейке."), "draconicevolution:chaos_shard", [item_task(4, 21, "draconicevolution:chaos_shard", title="Добыть chaotic shard")], "circle", 0.75, None),
        ],
        "gate3_title": "Готовность к нексусу",
        "gate3_desc": gate_desc("Chaos побеждён, компоненты на месте. Осталось собрать нексус."),
        "prep": [
            ("Чертёж нексуса", lore("В блокноте — чертёж якорного нексуса. Все тиры сойдутся в одной точке.", "Чертёж светится всеми цветами якоря — красиво и страшно."), "draconicevolution:awakened_draconium_block", [item_task(4, 24, "draconicevolution:awakened_draconium_block", 2, title="Awakened-блоки под нексус")], "hexagon", None, None),
            ("Сбор для нексуса", lore("Chaos, сердце и зёрна — тело нексуса своими руками.", "Три силы в одном кристалле: дракон, хаос и бесконечность."), "draconicevolution:dragon_heart", [item_task(4, 25, "draconicevolution:dragon_heart", title="Драконье сердце для нексуса"), item_task(4, 26, "enderio:grains_of_infinity", 16, title="Зёрна для нексуса")], "gear", None, None),
        ],
        "prep_opt": ("Резонансный замер V", lore("§8Опционально.§r Замер драконьего контура перед финалом T4.", "Пульс Chaos затих — нексус готов принять сигнал."), "minecraft:beacon", [item_task(4, 30, "minecraft:beacon", title="Замерить драконий контур")], "circle", 0.75),
    },
    5: {
        "file": "main_t5_convergence",
        "order": 60,
        "chapter_icon": "kubejs:anchor_nexus",
        "title": "T5 · Схождение",
        "subtitle": "T5 · ~120+ мин",
        "intro_title": "Порог next_ae",
        "intro_desc": [
            "§l[ T5 · Схождение ]§r",
            "",
            "§7§eЯкорный нексус§r — все тиры сходятся в одной точке. В блокноте последняя глава:",
            "§dnext_ae§r и финал экспедиции.",
            "",
            "§7Записал цель: собрать §eядро машины§r next_ae, стабилизировать §dЯкорь реальности§r",
            "§7— или разлом поглотит всё, что мы построили.",
            "",
            "§8Цель тира: ультра-эндгейм и §dЯдро Якоря реальности§r.",
        ],
        "intro_task": "Принять нексус и открыть главу next_ae",
        "page_item": "kubejs:journal_page_nexus_00",
        "finale_title": "Ядро Якоря",
        "finale_icon": "kubejs:reality_anchor_core",
        "finale_reward": "kubejs:reality_anchor_core",
        "finale_desc": [
            "§l[ Финал экспедиции ]§r",
            "",
            "§7Все осколки на месте. next_ae гудит в унисон с разломом. Якорь впервые слушается.",
            "",
            "§7§dЯдро Якоря реальности§r стабилизировано. В журнале — последняя запись экспедиции.",
            "§7Связь молчит, но разлом затих. Мы выстояли.",
            "",
            "§8Награда — Ядро Якоря реальности. Финал CoopTech.§r",
        ],
        "finale_task": "Стабилизировать Якорь реальности",
        "pages": ["kubejs:journal_page_nexus_01", "kubejs:journal_page_nexus_02", "kubejs:journal_page_nexus_03", "kubejs:journal_page_nexus_04"],
        "w1": [
            ("Ядро next_ae", lore("Machine Core — база next_ae. Последний рубеж техники в блокноте.", "Ядро машины — финальная дверь."), "next_ae:machine_core", [item_task(5, 2, "next_ae:machine_core", title="Собрать ядро next_ae")], "gear", None, "branch_craft"),
            ("Осколок якоря #1", lore("Первый стабилизированный осколок — круг начинается.", "Осколок поёт — якорь отвечает тихо."), "kubejs:stabilized_shard_01", [item_task(5, 3, "kubejs:stabilized_shard_01", title="Стабилизировать осколок #1")], "circle", None, "branch_explore"),
            ("Осколок якоря #6", lore("Шестой осколок — половина круга замкнута.", "Шесть из двенадцати — ритм становится слышным."), "kubejs:stabilized_shard_06", [item_task(5, 4, "kubejs:stabilized_shard_06", title="Стабилизировать осколок #6")], "circle", None, "branch_explore"),
            ("Осколок якоря #12", lore("Двенадцатый осколок — полный круг стабилизации.", "Двенадцать осколков — якорь почти цел."), "kubejs:stabilized_shard_12", [item_task(5, 5, "kubejs:stabilized_shard_12", title="Стабилизировать осколок #12")], "circle", None, "branch_explore"),
            ("Ultimate стол", lore("§8Опционально.§r Ultimate crafting table — сетка 9×9.", "Стол огромен — реальность подчиняется размеру."), "next_ae:ultimate_crafting_table", [item_task(5, 6, "next_ae:ultimate_crafting_table", title="Собрать ultimate-стол")], "circle", 0.75, None),
            ("Parallel процессор", lore("§8Опционально.§r Parallel processor — считает параллельно вселенным.", "Процессор не устаёт — я устаю быстрее."), "next_ae:parallel_processor", [item_task(5, 7, "next_ae:parallel_processor", title="Собрать parallel-процессор")], "circle", 0.75, None),
        ],
        "gate1_title": "next_ae запущен",
        "gate1_desc": gate_desc("Ядро машины и осколки на месте — next_ae ожил. Первый рубеж T5."),
        "w2": [
            ("Advanced Inscriber", lore("Продвинутый гравёр next_ae — AE2 на стероидах.", "Гравёр высечет то, что сеть не смогла."), "next_ae:advanced_inscriber", [item_task(5, 9, "next_ae:advanced_inscriber", title="Собрать advanced inscriber")], "gear", None, "branch_craft"),
            ("Зарядник next_ae", lore("Charger — питание сети next_ae. Жрёт RF, отдаёт скорость.", "Зарядник гудит — привычный звук контура."), "next_ae:charger", [item_task(5, 10, "next_ae:charger", title="Собрать зарядник next_ae")], "gear", None, "branch_craft"),
            ("Осколки 3+9", lore("Два осколка для симметрии якоря — ритуал требует баланса.", "Симметрия успокаивает разлом."), "kubejs:stabilized_shard_03", [item_task(5, 111, "kubejs:stabilized_shard_03", title="Стабилизировать осколок #3"), item_task(5, 112, "kubejs:stabilized_shard_09", title="Стабилизировать осколок #9")], "circle", None, "branch_explore"),
            ("Резонансный маяк", lore("Маяк для финальной синхронизации — кооп-ритуал у костра.", "Два сигнала у маяка — якорь слушает только вдвоём."), "kubejs:resonance_beacon", [item_task(5, 13, "kubejs:resonance_beacon", title="Установить резонансный маяк")], "gear", None, "branch_coop"),
            ("Финальный босс", lore("§8Опционально.§r Трофей Cataclysm эндгейма.", "Трофей тяжёлый — победа осязаема."), "cataclysm:void_eye", [item_task(5, 14, "cataclysm:void_eye", title="Добыть трофей Cataclysm")], "circle", 0.75, None),
            ("Реликвария схождения", lore("§8Опционально.§r Reliquary convergence — голоса всех тиров.", "Реликвария поёт хором — красиво и жутко."), "kubejs:reliquary_convergence", [item_task(5, 28, "kubejs:reliquary_convergence", title="Собрать реликварию схождения")], "circle", 0.75, None),
            ("Все осколки", lore("§8Опционально.§r Полный набор 12 осколков якоря.", "Круг замкнут — ядро готово родиться."), "kubejs:anchor_shard_12", [item_task(5, 15, "kubejs:anchor_shard_12", title="Собрать все осколки якоря")], "circle", 0.75, None),
        ],
        "gate2_title": "Осколки сходятся",
        "gate2_desc": gate_desc("next_ae и осколки синхронизированы. Второй рубеж T5 — в журнале."),
        "w3": [
            ("Сборка якоря", lore("Компоненты ядра якоря — предпоследний шаг.", "Ядро ждёт — не тороплюсь с последним ударом."), "kubejs:reality_anchor_core", [item_task(5, 16, "kubejs:anchor_shard_01", title="Осколок #1 для ядра"), item_task(5, 17, "kubejs:anchor_shard_06", title="Осколок #6 для ядра"), item_task(5, 18, "kubejs:anchor_shard_12", title="Осколок #12 для ядра")], "gear", None, "branch_craft"),
            ("Кооп-синхрон", lore("Двое у маяка — финальный ритуал стабилизации.", "Только вдвоём якорь слушает до конца."), "kubejs:resonance_beacon", [check_task(5, 19, "Синхронизация у маяка")], "gear", None, "branch_coop"),
            ("Финальный рейд", lore("Совместный рейд на разлом — последняя проверка силы.", "Разлом бьётся — мы держим удар вместе."), "minecraft:netherite_sword", [item_task(5, 20, "minecraft:netherite_sword", title="Пройти финальный рейд")], "circle", None, "branch_explore"),
            ("Стабилизация", lore("Подготовка к установке ядра — последний вдох перед тишиной.", "Тишина после гула — знак, что готовы."), "minecraft:beacon", [item_task(5, 21, "minecraft:beacon", title="Подготовить стабилизацию")], "circle", None, "branch_craft"),
            ("Кодекс пещер", lore("§8Опционально.§r Decrypted cave codex — пещеры открыты.", "Кодекс шепчет координаты — исследование не кончилось."), "kubejs:decrypted_cave_codex", [item_task(5, 27, "kubejs:decrypted_cave_codex", title="Расшифровать кодекс пещер")], "circle", 0.75, None),
            ("Полная сеть", lore("§8Опционально.§r Диск 16k — сеть помнит всё.", "Сеть помнит даже страх — и это утешает."), "ae2:item_storage_cell_16k", [item_task(5, 22, "ae2:item_storage_cell_16k", title="Собрать диск 16k")], "circle", 0.75, None),
            ("Draconic финал", lore("§8Опционально.§r Chaotic tier — хаос подчинён почти.", "Почти — слово, которое я больше не люблю."), "draconicevolution:chaotic_pickaxe", [item_task(5, 23, "draconicevolution:chaotic_pickaxe", title="Сковать chaotic-кирку")], "circle", 0.75, None),
        ],
        "gate3_title": "Готовность к ядру",
        "gate3_desc": gate_desc("Всё готово к финальной стабилизации. Осталось ядро."),
        "prep": [
            ("Чертёж ядра", lore("Последний чертёж в блокноте. После него — тишина.", "Чертёж дрожит — якорь ждёт."), "kubejs:reality_anchor_core", [check_task(5, 24, "Принять финальный чертёж")], "hexagon", None, None),
            ("Сбор для ядра", lore("Осколки, нексус и ядро next_ae — финальный ритуал.", "Все тиры в одной ладони — тяжело и правильно."), "kubejs:anchor_nexus", [item_task(5, 25, "kubejs:anchor_nexus", title="Нексус для ядра"), item_task(5, 26, "next_ae:machine_core", title="Ядро next_ae для ритуала")], "gear", None, None),
        ],
        "prep_opt": ("Резонансный замер · финал", lore("§8Опционально.§r Последний замер разлома перед рождением ядра.", "График ровный — якорь готов."), "minecraft:end_crystal", [item_task(5, 30, "minecraft:end_crystal", 4, title="Финальный замер разлома")], "circle", 0.75),
    },
}


def gate_deps(tier: int, gate_n: int) -> list[str]:
    if gate_n == 8:
        return [qid(tier, 1)] + wave_branch_deps(tier, 2)
    if gate_n == 15:
        return [qid(tier, 8)] + wave_branch_deps(tier, 9)
    return [qid(tier, 15)] + wave_branch_deps(tier, 16)


def pool_tags(tag: str | None, pool_index: int, tier: int, wave: int) -> list[str]:
    tags: list[str] = ["branch_pool", f"pool_t{tier}_w{wave}"]
    if tag:
        tags.append(tag)
    if pool_index in (1, 3):
        tags.append("branch_exclusive")
    return tags


def branch_rewards(tier: int, n: int, tasks: list[str], *, optional: bool = False) -> list[str]:
    return branch_rewards_from_tasks(
        tasks,
        tier,
        item_fn=lambda rid, item, count: item_reward(tier, rid, item, count),
        xp_fn=lambda rid, xp: xp_reward(tier, rid, xp),
        reliquary_fn=lambda rid, item: item_reward(tier, rid, item),
        rid_item=0xA0 + n,
        rid_xp=0xB0 + n,
        rid_relic=0xC0 + n,
        quest_num=n,
        optional=optional,
    )


def build_chapter(tier: int, cfg: dict) -> str:
    prev = prev_finale_id(tier)
    w1_ids = [qid(tier, i) for i in range(2, 6)]
    w2_ids = [qid(tier, i) for i in range(9, 13)]
    w3_ids = [qid(tier, i) for i in range(16, 20)]

    quests: list[str] = []

    intro_rewards = [
        item_reward(tier, 1, cfg["page_item"]),
        xp_reward(tier, 2, 25),
    ]
    intro_deps = [prev] if prev else []
    quests.append(
        quest_block(
            tier,
            1,
            title=cfg["intro_title"],
            desc=cfg["intro_desc"],
            icon=cfg["chapter_icon"],
            tasks=[check_task(tier, 1, cfg["intro_task"])],
            x=0,
            y=0,
            deps=intro_deps or None,
            rewards=intro_rewards,
            shape="hexagon",
            size=1.5,
        )
    )

    xs_w1 = [-6, -2, 2, 6]
    for i in range(4):
        title, desc, icon, tasks, shape, sz, tag = cfg["w1"][i]
        n = i + 2
        quests.append(
            quest_block(
                tier,
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=tasks,
                x=xs_w1[i],
                y=2,
                deps=[qid(tier, 1)],
                shape=shape,
                size=sz,
                tags=pool_tags(tag, i, tier, 1),
                rewards=branch_rewards(tier, n, tasks),
            )
        )

    if len(cfg["w1"]) > 4:
        n = 6
        title, desc, icon, tasks, shape, sz, _ = cfg["w1"][4]
        quests.append(
            quest_block(
                tier,
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=tasks,
                x=-8,
                y=3.5,
                deps=[qid(tier, 2)],
                shape=shape,
                size=sz,
                rewards=branch_rewards(tier, n, tasks, optional=True),
            )
        )
    if len(cfg["w1"]) > 5:
        n = 7
        title, desc, icon, tasks, shape, sz, _ = cfg["w1"][5]
        quests.append(
            quest_block(
                tier,
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=tasks,
                x=8,
                y=3.5,
                deps=[qid(tier, 5)],
                shape=shape,
                size=sz,
                rewards=branch_rewards(tier, n, tasks, optional=True),
            )
        )

    quests.append(
        quest_block(
            tier,
            8,
            title=cfg["gate1_title"],
            desc=cfg["gate1_desc"],
            icon="kubejs:quest_gate",
            tasks=[check_task(tier, 8, cfg["gate1_title"])],
            x=0,
            y=4.5,
            deps=gate_deps(tier, 8),
            rewards=gate_rewards(
                tier,
                item_fn=lambda rid, item, count=1: item_reward(tier, rid, item, count),
                xp_fn=lambda rid, xp: xp_reward(tier, rid, xp),
                reliquary_fn=lambda rid, item: item_reward(tier, rid, item),
                page_item=cfg["pages"][0],
                rid_page=29,
                rid_xp=9,
                rid_relic=0xD8,
            ),
            shape="diamond",
            size=1.2,
        )
    )

    for i in range(4):
        title, desc, icon, tasks, shape, sz, tag = cfg["w2"][i]
        n = i + 9
        quests.append(
            quest_block(
                tier,
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=tasks,
                x=xs_w1[i],
                y=6,
                deps=[qid(tier, 8), qid(tier, 2 + i)],
                shape=shape,
                size=sz,
                tags=pool_tags(tag, i, tier, 2),
                rewards=branch_rewards(tier, n, tasks),
            )
        )

    opt_w2 = [(13, 8, 7.5, 11, 4), (14, -4, 7.5, 10, 5), (28, -8, 7.5, 9, 6)]
    for n, xi, yi, dep_q, wi in opt_w2:
        if wi < len(cfg["w2"]):
            title, desc, icon, tasks, shape, sz, _ = cfg["w2"][wi]
            quests.append(
                quest_block(
                    tier,
                    n,
                    title=title,
                    desc=desc,
                    icon=icon,
                    tasks=tasks,
                    x=xi,
                    y=yi,
                    deps=[qid(tier, dep_q)],
                    shape=shape,
                    size=sz,
                    rewards=branch_rewards(tier, n, tasks, optional=True),
                )
            )

    quests.append(
        quest_block(
            tier,
            15,
            title=cfg["gate2_title"],
            desc=cfg["gate2_desc"],
            icon="kubejs:quest_gate",
            tasks=[check_task(tier, 15, cfg["gate2_title"])],
            x=0,
            y=8.5,
            deps=gate_deps(tier, 15),
            rewards=gate_rewards(
                tier,
                item_fn=lambda rid, item, count=1: item_reward(tier, rid, item, count),
                xp_fn=lambda rid, xp: xp_reward(tier, rid, xp),
                reliquary_fn=lambda rid, item: item_reward(tier, rid, item),
                page_item=cfg["pages"][1],
                rid_page=30,
                rid_xp=17,
                rid_relic=0xD9,
            ),
            shape="diamond",
            size=1.2,
        )
    )

    for i in range(4):
        title, desc, icon, tasks, shape, sz, tag = cfg["w3"][i]
        n = i + 16
        quests.append(
            quest_block(
                tier,
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=tasks,
                x=xs_w1[i],
                y=10,
                deps=[qid(tier, 15), qid(tier, 9 + i)],
                shape=shape,
                size=sz,
                tags=pool_tags(tag, i, tier, 3),
                rewards=branch_rewards(tier, n, tasks),
            )
        )

    opt_w3 = [(27, -8, 11.5, 19, 4), (20, 4, 11.5, 18, 5), (21, 8, 11.5, 17, 6)]
    for n, xi, yi, dep_q, wi in opt_w3:
        if wi < len(cfg["w3"]):
            title, desc, icon, tasks, shape, sz, _ = cfg["w3"][wi]
            quests.append(
                quest_block(
                    tier,
                    n,
                    title=title,
                    desc=desc,
                    icon=icon,
                    tasks=tasks,
                    x=xi,
                    y=yi,
                    deps=[qid(tier, dep_q)],
                    shape=shape,
                    size=sz,
                    rewards=branch_rewards(tier, n, tasks, optional=True),
                )
            )

    quests.append(
        quest_block(
            tier,
            22,
            title=cfg["gate3_title"],
            desc=cfg["gate3_desc"],
            icon="kubejs:quest_gate",
            tasks=[check_task(tier, 22, cfg["gate3_title"])],
            x=0,
            y=12.5,
            deps=gate_deps(tier, 22),
            rewards=gate_rewards(
                tier,
                item_fn=lambda rid, item, count=1: item_reward(tier, rid, item, count),
                xp_fn=lambda rid, xp: xp_reward(tier, rid, xp),
                reliquary_fn=lambda rid, item: item_reward(tier, rid, item),
                page_item=cfg["pages"][2],
                rid_page=31,
                rid_xp=22,
                rid_relic=0xDA,
            ),
            shape="diamond",
            size=1.2,
        )
    )

    for i, (title, desc, icon, tasks, shape, sz, _) in enumerate(cfg["prep"]):
        n = 23 + i
        quests.append(
            quest_block(
                tier,
                n,
                title=title,
                desc=desc,
                icon=icon,
                tasks=tasks,
                x=-2 + i * 4,
                y=14,
                deps=[qid(tier, 22)],
                shape=shape,
                size=sz,
                rewards=branch_rewards(tier, n, tasks) if i == 0 else [xp_reward(tier, 23 + i, 25 + tier * 3)],
            )
        )

    po = cfg["prep_opt"]
    quests.append(
        quest_block(
            tier,
            25,
            title=po[0],
            desc=po[1],
            icon=po[2],
            tasks=po[3],
            x=5,
            y=15.5,
            deps=[qid(tier, 23)],
            shape=po[4],
            size=po[5],
            rewards=[xp_reward(tier, 24, 15)],
        )
    )

    finale_rewards = [
        item_reward(tier, 25, cfg["finale_reward"]),
        item_reward(tier, 32, cfg["pages"][3]),
        xp_reward(tier, 27, 130),
    ]
    quests.append(
        quest_block(
            tier,
            26,
            title=cfg["finale_title"],
            desc=cfg["finale_desc"],
            icon=cfg["finale_icon"],
            tasks=[check_task(tier, 29, cfg["finale_task"])],
            x=0,
            y=16.5,
            deps=[qid(tier, 23), qid(tier, 24)],
            min_deps=2,
            rewards=finale_rewards,
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
\tfilename: "{cfg["file"]}"
\tgroup: "{GROUP}"
\ticon: {{ count: 1, id: "{cfg["chapter_icon"]}" }}
\tid: "{cid(tier)}"
\torder_index: {cfg["order"]}
\tquest_links: [ ]
\tquests: [
{body}
\t]
\tsubtitle: [
\t\t"{cfg["subtitle"]}"
\t]
\ttitle: "{cfg["title"]}"
}}
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    adv_dir = ROOT / "overrides" / "data" / "cooptech" / "advancements" / "journal"
    adv_dir.mkdir(parents=True, exist_ok=True)
    for tier, cfg in TIERS.items():
        path = OUT / f"{cfg['file']}.snbt"
        path.write_text(build_chapter(tier, cfg), encoding="utf-8")
        print(f"  wrote {path.name}")
        # advancement stubs for lore beats
        keys = ["intro", "g1", "g2", "g3", "finale"]
        for k in keys:
            prefix = {1: "spark", 2: "cell", 3: "matrix", 4: "singularity", 5: "nexus"}[tier]
            adv_key = f"t{tier}_lore_{k}" if k != "intro" else f"t{tier}_lore_intro"
            if k == "g1":
                adv_key = f"t{tier}_lore_w1"
            elif k == "g2":
                adv_key = f"t{tier}_lore_w2"
            elif k == "g3":
                adv_key = f"t{tier}_lore_w3"
            elif k == "finale":
                adv_key = f"t{tier}_lore_finale"
            adv_path = adv_dir / f"{adv_key}.json"
            if not adv_path.exists():
                adv_path.write_text(
                    '{\n  "parent": "cooptech:journal/t0_intro",\n'
                    '  "criteria": {\n    "unlock": {\n'
                    '      "trigger": "minecraft:impossible"\n    }\n  }\n}\n',
                    encoding="utf-8",
                )
    print("Done. Generated T1–T5 tier chapters + lore advancement stubs.")


if __name__ == "__main__":
    main()
