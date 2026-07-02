#!/usr/bin/env python3
"""Write Patchouli codex (mechanism guide) entries T1–T5 + advancement stubs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "overrides" / "patchouli_books" / "expedition_journal" / "en_us" / "entries"
ADV_DIR = ROOT / "overrides" / "data" / "cooptech" / "advancements" / "journal"

# (subdir, filename, adv_key, quest_id, sortnum, entry_dict)
CODEX: list[tuple[str, str, str, str, int, dict]] = [
    (
        "codex_energy",
        "thermal_machines",
        "t1_thermal",
        "5221A00000000008",
        1,
        {
            "name": "Thermal — автоматизация",
            "icon": "thermal:machine_pulverizer",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Зачем$()$(br2)После рамы и печи — $(#FFAA00)цепочка руды$(): дробилка → плавка → слиток. "
                    "Thermal даёт $(#DD55DD)×2 выход$() из руды и автоматизацию через сервоприводы.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "thermal:machine_pulverizer",
                    "text": "$(#FFAA00)Дробилка (Pulverizer)$(): руда → пыль/слиток. Основа автоплавки. "
                    "Питай RF, вывод — в печь или сундук.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "thermal:redstone_servo",
                    "text": "$(#FFAA00)Сервопривод$(): автоматический ввод/вывод предметов в машину. "
                    "Ставится в слоты машины — настраивается фильтром.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "thermal:rf_coil",
                    "text": "$(#FFAA00)RF-катушка$(): передаёт энергию между соседними блоками Thermal без проводов. "
                    "Соедини печь ↔ дробилку ↔ динамо.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Мини-линия$()$(br2)$(li)Динамо жжёт топливо → RF в машины.$(li)Серво подаёт руду в дробилку.$(li)Вторая серво выводит пыль в печь.$(li)Слитки — в ящик или ME.$(br2)"
                    "$(bold)Кооп:$() один строит линию, второй копает и подвозит руду.",
                },
            ],
        },
    ),
    (
        "codex_energy",
        "powah_intro",
        "t1_powah",
        "5221A00000000008",
        2,
        {
            "name": "Powah — генерация и батареи",
            "icon": "powah:furnator_basic",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Зачем$()$(br2)Thermal жрёт RF на машины — Powah даёт $(#FFAA00)генераторы$() и $(#DD55DD)батареи$(). "
                    "Урановая руда — топливо для мощных установок.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "powah:uraninite",
                    "text": "$(#FFAA00)Урановая руда (Uraninite)$(): копай глубже железа. Перерабатывается в топливо для Furnator.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "powah:dielectric_casing",
                    "text": "$(#FFAA00)Диэлектрический корпус$(): основа всех блоков Powah — генераторов, батарей, кабелей.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "powah:battery_basic",
                    "text": "$(#FFAA00)Батарея$(): буфер RF на пиках нагрузки (дробилка + печь одновременно). "
                    "Апгрейды: Hardened → Blazing → Nitro.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Схема$()$(br2)Furnator → кабель Powah → батарея → машины Thermal.$(br2)"
                    "Один следит за генерацией, второй — за потреблением машин.",
                },
            ],
        },
    ),
    (
        "codex_energy",
        "mekanism_basics",
        "t2_mek",
        "5222A00000000001",
        3,
        {
            "name": "Mekanism — промышленный старт",
            "icon": "mekanism:steel_casing",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Порог T2$()$(br2)$(#FFAA00)Якорная ячейка$() открывает Mekanism. "
                    "База — $(#DD55DD)стальной корпус$(); без него ни одна машина не встанет.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "mekanism:metallurgic_infuser",
                    "text": "$(#FFAA00)Металлургический инфузер$(): смешивает металлы и материалы для сплавов Mek. "
                    "Первый крафт после корпусов.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "mekanism:enrichment_chamber",
                    "text": "$(#FFAA00)Обогатительная фабрика$(): удваивает руду (2 dust → 3 ingot в цепочке). "
                    "Сердце рудной линии.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "mekanism:basic_energy_cube",
                    "text": "$(#FFAA00)Энергокуб$(): буфер FE для завода. Mek использует $(#DD55DD)FE$() — совместим с RF Thermal.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Цепочка$()$(br2)Руда → обогатитель → дробитель → плавильня → слиток.$(br2)"
                    "Газы и жидкости — через $(#FFAA00)pressurized tubes$() (позже).",
                },
            ],
        },
    ),
    (
        "codex_energy",
        "enderio_basics",
        "t2_enderio",
        "5222A00000000008",
        4,
        {
            "name": "Ender IO — сплавы и логистика",
            "icon": "enderio:alloy_smelter",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Зачем$()$(br2)Ender IO — $(#FFAA00)сплавы$(), SAG Mill и $(#DD55DD)кондуиты$(). "
                    "Параллельная ветка к Mek, синергия на одной базе.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "enderio:conductive_alloy_ingot",
                    "text": "$(#FFAA00)Проводящий сплав$(): базовый сплав EIO. Нужен для машин и проводов.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "enderio:alloy_smelter",
                    "text": "$(#FFAA00)Сплавная печь$(): три слота — три металла → один сплав. "
                    "Vibrant alloy — вершина линии.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "enderio:sag_mill",
                    "text": "$(#FFAA00)SAG Mill$(): измельчение руды и материалов. Альтернатива/дополнение к Mek Crusher.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Кооп$()$(br2)Один тянет Mek-линию, второй EIO-сплавы — ресурсы не дублируются, выход растёт.",
                },
            ],
        },
    ),
    (
        "codex_energy",
        "flux_networks",
        "t2_flux",
        "5222A00000000008",
        5,
        {
            "name": "Flux Networks — энергия без проводов",
            "icon": "fluxnetworks:flux_controller",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Зачем$()$(br2)Flux передаёт $(#FFAA00)RF/FE по сети$() без физических кабелей. "
                    "Один контроллер — энергия на всю базу.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "fluxnetworks:flux_dust",
                    "text": "$(#FFAA00)Flux-пыль$(): крафтится из редстоуна и обсидиана. Основа всей сети.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "fluxnetworks:flux_plug",
                    "text": "$(#FFAA00)Flux Plug$(): ввод энергии в сеть (от генератора).",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "fluxnetworks:flux_point",
                    "text": "$(#FFAA00)Flux Point$(): вывод энергии к машине. Поставь на стену рядом с потребителем.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Настройка$()$(br2)1) Скрафтить Flux Controller.$(br2)2) Plug на генератор, Points на машины.$(br2)"
                    "3) Открыть GUI контроллера — назвать сеть, включить.$(br2)Беспроводно = меньше лагов от проводов.",
                },
            ],
        },
    ),
    (
        "codex_network",
        "ae2_network",
        "t3_ae2",
        "5223A00000000001",
        6,
        {
            "name": "AE2 — ME-сеть",
            "icon": "ae2:controller",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Порог T3$()$(br2)$(#FFAA00)Якорная матрица$() открывает Applied Energistics 2. "
                    "ME-сеть $(#DD55DD)помнит каждый предмет$() на базе.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "ae2:inscriber",
                    "text": "$(#FFAA00)Гравёр (Inscriber)$(): вычитает процессоры из пластин и кристаллов. "
                    "Без него сеть слепа.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "ae2:controller",
                    "text": "$(#FFAA00)ME-контроллер$(): сердце сети. Максимум 7×7×7, но на старте хватит одного блока.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "ae2:drive",
                    "text": "$(#FFAA00)ME Drive + ячейки$(): хранение. Диск 1k → 4k → 16k. Fluix-кабели соединяют всё.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Стартовый набор$()$(br2)Controller → Drive с ячейкой → Terminal → fluix cables.$(br2)"
                    "$(#FFAA00)Import/Export bus$() — автоматизация: шина тянет руду в сеть, отдаёт слитки машинам.",
                },
            ],
        },
    ),
    (
        "codex_network",
        "projecte_emc",
        "t3_emc",
        "5223A00000000008",
        7,
        {
            "name": "ProjectE — EMC и трансмутация",
            "icon": "projecte:philosophers_stone",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Зачем$()$(br2)EMC — $(#DD55DD)«стоимость» предмета$() в единой валюте. "
                    "Не замена AE2, а $(#FFAA00)логистика и дубликатор$() редких ресурсов.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "projecte:philosophers_stone",
                    "text": "$(#FFAA00)Камень философов$(): инструмент трансмутации. Крафт — первый шаг в EMC.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "projecte:transmutation_table",
                    "text": "$(#FFAA00)Стол трансмутации$(): кладёшь предметы → получаешь EMC → крафтишь другое из «банка».",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "projecte:collector_mk1",
                    "text": "$(#FFAA00)Коллектор$(): генерирует EMC из света/fuel. MK1 → MK2 → MK3.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)С AE2$()$(br2)EMC дополняет сеть: дубликат редких слитков, топливо для крафта. "
                    "Не ломай баланс — используй для логистики, не для «всё из алмазов».",
                },
            ],
        },
    ),
    (
        "codex_energy",
        "draconic_evolution",
        "t4_draconic",
        "5224A00000000001",
        8,
        {
            "name": "Draconic Evolution — основы",
            "icon": "draconicevolution:draconium_core",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Порог T4$()$(br2)$(#FFAA00)Якорная сингулярность$() открывает Draconic. "
                    "Draconium → Wyvern → Draconic → Chaotic — $(#DD55DD)ступени силы$().",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "draconicevolution:draconium_core",
                    "text": "$(#FFAA00)Ядро дракония$(): базовый компонент всех крафтов DE.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "draconicevolution:wyvern_crafting_injector",
                    "text": "$(#FFAA00)Crafting Injector$(): fusion-крафт — несколько пьедесталов вокруг ядра. "
                    "Сложные рецепты требуют несколько injectors.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "draconicevolution:energy_core",
                    "text": "$(#FFAA00)Energy Core + Storage$(): ORB энергии DE — миллиарды RF. "
                    "Строй многослойно по рецепту.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Порядок$()$(br2)Пыль → Core → Wyvern gear → Awakened draconium → Draconic tier.$(br2)"
                    "Chaos Guardian — источник $(#FFAA00)chaos shards$() для awakened.",
                },
            ],
        },
    ),
    (
        "codex_energy",
        "draconic_reactor",
        "t4_fusion",
        "5224A00000000008",
        9,
        {
            "name": "Draconic — реактор и Chaos",
            "icon": "draconicevolution:reactor_core",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Энергия дракона$()$(br2)Draconic Reactor — $(#DD55DD)вершина генерации$(). "
                    "Ошибка в настройке = взрыв. Читай рецепт и stabilizer.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "draconicevolution:reactor_core",
                    "text": "$(#FFAA00)Reactor Core$(): сердце реактора. Обязательны stabilizers и правильная сборка.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "draconicevolution:chaos_shard",
                    "text": "$(#FFAA00)Chaos Shard$(): добыча на Chaos Island / Chaos Guardian. "
                    "Нужен для awakened и chaotic tier.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Chaos Guardian$()$(br2)Босс DE — финал ветки. Готовь $(#FFAA00)draconic armor$(), "
                    "зелья, кооп-роли: один танкует, второй бьёт.$(br2)Трофей — chaos shards для нексуса.",
                },
            ],
        },
    ),
    (
        "codex_network",
        "next_ae_intro",
        "t5_next_ae",
        "5225A00000000001",
        10,
        {
            "name": "next_ae — ультра-крафт",
            "icon": "next_ae:machine_core",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Порог T5$()$(br2)$(#FFAA00)Якорный нексус$() открывает next_ae — "
                    "надстройка над AE2: $(#DD55DD)параллельный крафт$(), ultimate table, advanced machines.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "next_ae:machine_core",
                    "text": "$(#FFAA00)Machine Core$(): база всех машин next_ae. Требует нексус и компоненты T4.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "next_ae:ultimate_crafting_table",
                    "text": "$(#FFAA00)Ultimate Crafting Table$(): сетка 9×9 для эндгейм-рецептов.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "next_ae:advanced_inscriber",
                    "text": "$(#FFAA00)Advanced Inscriber$(): быстрее AE2 inscriber, нужен для процессоров next_ae.",
                },
                {
                    "type": "patchouli:text",
                    "text": "$(bold)С AE2$()$(br2)next_ae не заменяет ME-сеть — $(#FFAA00)расширяет$() её. "
                    "Подключай к существующему controller и terminal.",
                },
            ],
        },
    ),
    (
        "codex",
        "anchor_stabilization",
        "t5_anchor",
        "5225A00000000008",
        11,
        {
            "name": "Стабилизация Якоря",
            "icon": "kubejs:reality_anchor_core",
            "pages": [
                {
                    "type": "patchouli:text",
                    "text": "$(bold)Финал экспедиции$()$(br2)12 $(#FFAA00)осколков якоря$() → стабилизация → "
                    "$(#DD55DD)Ядро реальности$(). Кооп-ритуал у $(#FFAA00)резонансного маяка$() обязателен.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "kubejs:stabilized_shard_01",
                    "text": "$(#FFAA00)Стабилизированные осколки$(): собираются по квестам T5. "
                    "Симметрия (#1, #6, #12…) важна для ритуала.",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "kubejs:resonance_beacon",
                    "text": "$(#FFAA00)Резонансный маяк$(): оба игрока у маяка — финальная синхронизация. "
                    "Checkmark-квест «Синхронизация у маяка».",
                },
                {
                    "type": "patchouli:spotlight",
                    "item": "kubejs:reality_anchor_core",
                    "text": "$(#FFAA00)Ядро Якоря реальности$(): награда финала. "
                    "Разлом стабилизируется — экспедиция завершена.",
                },
            ],
        },
    ),
]

ADV_STUB = (
    '{\n  "parent": "cooptech:journal/t0_intro",\n'
    '  "criteria": {\n    "unlock": {\n'
    '      "trigger": "minecraft:impossible"\n    }\n  }\n}\n'
)


def main() -> None:
    ADV_DIR.mkdir(parents=True, exist_ok=True)
    unlocks: list[tuple[str, str, str]] = []

    for subdir, filename, adv_key, quest_id, sortnum, body in CODEX:
        out_dir = ENTRIES_DIR / subdir
        out_dir.mkdir(parents=True, exist_ok=True)
        entry = {
            **body,
            "category": f"patchouli:{subdir}",
            "advancement": f"cooptech:journal/{adv_key}",
            "secret": True,
            "sortnum": sortnum,
        }
        path = out_dir / f"{filename}.json"
        path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  wrote {subdir}/{filename}.json")

        adv_path = ADV_DIR / f"{adv_key}.json"
        if not adv_path.exists():
            adv_path.write_text(ADV_STUB, encoding="utf-8")
            print(f"  adv {adv_key}.json")

        unlocks.append((quest_id, adv_key, body["name"]))

    # Write unlock map snippet for manual merge / reference
    ref = ROOT / "scripts" / "codex_unlocks_ref.json"
    ref.write_text(
        json.dumps(
            [{ "quest": q, "adv": a, "name": n } for q, a, n in unlocks],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"  reference: {ref.name} ({len(unlocks)} unlocks)")


if __name__ == "__main__":
    main()
