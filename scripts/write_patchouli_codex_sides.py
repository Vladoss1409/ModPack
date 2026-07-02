#!/usr/bin/env python3
"""Write Patchouli codex entries for 17 side branches."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from quest_content_v1 import POST_SIDE_BRANCHES, SIDE_BRANCHES  # noqa: E402

ENTRIES_DIR = ROOT / "overrides" / "patchouli_books" / "expedition_journal" / "en_us" / "entries" / "codex_branches"
ADV_DIR = ROOT / "overrides" / "data" / "cooptech" / "advancements" / "journal"

ADV_STUB = (
    '{\n  "parent": "cooptech:journal/t0_intro",\n'
    '  "criteria": {\n    "unlock": {\n'
    '      "trigger": "minecraft:impossible"\n    }\n  }\n}\n'
)

# side filename -> (adv_suffix, codex title, pages)
GUIDES: dict[str, tuple[str, list[dict]]] = {
    "side_kitchen": (
        "Полевая кухня — пайки для рейдов",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Базовая кухня T0 — в разделе «Лагерь». Эта ветка — $(#FFAA00)продвинутые блюда$() "
                "и запасы для длинных рейдов и боссов.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "farmersdelight:roast_chicken_block",
                "text": "$(#FFAA00)Праздничные блюда$() (жареная курица, пирог): дают сильные баффы на группу. "
                "Готовь блоками — делите порции.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "minecraft:golden_carrot",
                "text": "$(#FFAA00)Золотая морковь$(): must-have перед босс-файтами. "
                "Кооп: один варит, второй тащит морковь и золото.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "farmersdelight:rich_soil",
                "text": "$(#FFAA00)Богатая почва$() (финал ветки): ускоряет грядки — кухня сама восполняет ингредиенты.",
            },
        ],
    ),
    "side_storage": (
        "Склад — ящики и бочки",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)T0 даёт основы Drawers. Ветка добавляет $(#DD55DD)Sophisticated Storage$() "
                "и продвинутые схемы склада.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "storagedrawers:controller",
                "text": "$(#FFAA00)Контроллер ящиков$(): один вброс — авто-раскладка. Стена 2×2 ячеек на тип руды.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "sophisticatedstorage:barrel",
                "text": "$(#FFAA00)Бочки$(): апгрейды вместимости (железо → золото). Один столб бочек = целый склад.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "sophisticatedstorage:controller",
                "text": "$(#FFAA00)Контроллер бочек$(): связывает бочки; воронки качают через него.",
            },
        ],
    ),
    "side_bestiary": (
        "Разведка и бестиарий",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Компасы и бестиарий находят $(#DD55DD)структуры, биомы и мобов$(). "
                "Трофеи — ресурсы для других веток.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "explorerscompass:explorerscompass",
                "text": "$(#FFAA00)Explorer's Compass$(): поиск данжей и структур. Кооп: один сканирует, второй строит базу у точки.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "naturescompass:naturescompass",
                "text": "$(#FFAA00)Nature's Compass$(): нужный биом без блужданий — ускоряет фарм редких ресурсов.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "alexsmobs:animal_dictionary",
                "text": "$(#FFAA00)Бестиарий$(): механики мобов Alex's Mobs — как приручить, что дропает.",
            },
        ],
    ),
    "side_thermal": (
        "Thermal — полный контур",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Главная T1 знакомит с рамой. Сайд-ветка — $(#FFAA00)все ключевые машины$() "
                "Thermal и резонансные апгрейды.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "thermal:machine_smelter",
                "text": "$(#FFAA00)Индукционная плавильня$(): сплавы (invar, electrum) в одном блоке.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "thermal:machine_sawmill",
                "text": "$(#FFAA00)Лесопилка$(): дерево → доски + побочные продукты.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "thermal:machine_crafter",
                "text": "$(#FFAA00)Machine Crafter$() (финал): автокрафт по шаблону — мост к AE2.",
            },
        ],
    ),
    "side_powah": (
        "Powah — полная линия",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Сайд проходит $(#FFAA00)все тиры Powah$(): furnator → nitro cell. "
                "Дополняет гайд T1 в «Энергия и машины».",
            },
            {
                "type": "patchouli:spotlight",
                "item": "powah:capacitor_hardened",
                "text": "$(#FFAA00)Hardened → Niotic$(): каждый тир ×ёмкости. Строй башню батарей.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "powah:crystal_blazing",
                "text": "$(#FFAA00)Blazing Crystal$(): топливо/компонент высоких тиров.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "powah:energy_cell_nitro",
                "text": "$(#FFAA00)Nitro Energy Cell$() (финал): огромный буфер RF для Draconic/Reactor.",
            },
        ],
    ),
    "side_immersive": (
        "Immersive Engineering",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)IE — $(#FFAA00)мультиблоки$(), кокс, провода. "
                "Дополняет Thermal, не заменяет.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "immersiveengineering:coke_oven",
                "text": "$(#FFAA00)Коксовая печь$(): уголь → кокс + creosote. 27 кирпичей 3×3×3.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "immersiveengineering:metal_press",
                "text": "$(#FFAA00)Metal Press$(): пластины, провода, шестерни по формам.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "immersiveengineering:light_engineering",
                "text": "$(#FFAA00)Light Engineering$() (финал): компонент продвинутых мультиблоков.",
            },
        ],
    ),
    "side_apotheosis": (
        "Apotheosis — перековка",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Apotheosis усиливает $(#DD55DD)оружие, броню и спавнеры$(). "
                "Редкость растёт через перековку и гемы.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "apotheosis:simple_reforging_table",
                "text": "$(#FFAA00)Стол перековки$(): трать материалы — меняй аффиксы предмета.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "apotheosis:salvaging_table",
                "text": "$(#FFAA00)Salvaging$(): разбор магического лута на пыль/гемы.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "apotheosis:reforging_table",
                "text": "$(#FFAA00)Reforging Table$() (финал): высшие тиры перековки.",
            },
        ],
    ),
    "side_silent_gear": (
        "Silent Gear — кастомные инструменты",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Silent Gear — $(#FFAA00)модульные$() кирки и мечи. "
                "Материалы задают статы; инструмент растёт с использованием.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "silentgear:template_board",
                "text": "$(#FFAA00)Шаблонная доска + чертёж$(): проектируешь форму инструмента.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "silentgear:pickaxe_head",
                "text": "$(#FFAA00)Головка + связка + покрытие$(): три слота — три свойства.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "silentgear:pickaxe",
                "text": "$(#FFAA00)Готовый инструмент$(): ремонт и апгрейд без полной перековки.",
            },
        ],
    ),
    "side_mekanism": (
        "Mekanism — полный завод",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Сайд проходит $(#FFAA00)всю рудную линию$() Mek до телепорта. "
                "Идеален, если главная T2 идёт через EIO/Flux.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "mekanism:basic_smelting_factory",
                "text": "$(#FFAA00)Factory$(): 3 операции параллельно — ×3 throughput.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "mekanism:digital_miner",
                "text": "$(#FFAA00)Digital Miner$(): карьер в чанке. Питай FE, фильтруй руду.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "mekanism:teleportation_core",
                "text": "$(#FFAA00)Teleportation Core$() (финал): телепорты предметов/игроков.",
            },
        ],
    ),
    "side_enderio": (
        "Ender IO — кондуиты",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Полная ветка EIO: $(#FFAA00)сплавы, SAG, кондуиты$(), wireless.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "enderio:item_conduit",
                "text": "$(#FFAA00)Item Conduit$(): предметы по цветовым каналам. Фильтры на каждом извлечении.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "enderio:basic_capacitor_bank",
                "text": "$(#FFAA00)Capacitor Bank$(): RF-буфер для SAG и Smelter.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "enderio:vibrant_capacitor_bank",
                "text": "$(#FFAA00)Wireless Antenna$() (финал): доступ к сети EIO удалённо.",
            },
        ],
    ),
    "side_flux": (
        "Flux — полная сеть",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Сайд собирает $(#FFAA00)всю Flux-сеть$(): от пыли до gargantuan storage.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "fluxnetworks:basic_flux_storage",
                "text": "$(#FFAA00)Flux Storage$(): буфер энергии внутри сети.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "fluxnetworks:gargantuan_flux_storage",
                "text": "$(#FFAA00)Gargantuan Storage$(): гигантский буфер — для реакторов.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "fluxnetworks:flux_controller",
                "text": "$(#FFAA00)Controller$() (финал): управление всей сетью, права игроков.",
            },
        ],
    ),
    "side_arcane": (
        "Iron's Spells — магия",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Арканическая ветка — $(#DD55DD)заклинания$() в бою и на рейдах. "
                "Эссенция → руны → том.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "irons_spellbooks:inscription_table",
                "text": "$(#FFAA00)Стол надписей$(): записываешь заклинания в том.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "irons_spellbooks:fire_rune",
                "text": "$(#FFAA00)Руны стихий$(): огонь, лёд, молния — комбо с melee.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "irons_spellbooks:legendary_ink",
                "text": "$(#FFAA00)Legendary Ink$() (финал): апгрейд маны и tier заклинаний.",
            },
        ],
    ),
    "side_network": (
        "AE2 — углублённая сеть",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Сайд строит $(#FFAA00)полную ME-сеть$() с автокрафтом и wireless. "
                "Дополняет гайд T3.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "ae2:growth_accelerator",
                "text": "$(#FFAA00)Growth Accelerator$(): ферма certus-кварца на базе.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "ae2:crafting_unit",
                "text": "$(#FFAA00)Crafting CPU$(): автокрафт — заказ из терминала.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "ae2:wireless_access_point",
                "text": "$(#FFAA00)Wireless AP$() (финал): терминал работает в радиусе.",
            },
        ],
    ),
    "side_twilight": (
        "Twilight Forest",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Twilight — $(#DD55DD)отдельное измерение$() с боссами и уникальными материалами.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "twilightforest:liveroot",
                "text": "$(#FFAA00)Liveroot$(): входной ресурс — инструменты и блоки леса.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "twilightforest:naga_scale",
                "text": "$(#FFAA00)Naga Scale$(): первый босс — броня и мечи.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "twilightforest:phantom_helmet",
                "text": "$(#FFAA00)Phantom Helmet$() (финал): броня из Phantom Plate.",
            },
        ],
    ),
    "side_draconic": (
        "Draconic — сайд-ветка",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Полный путь DE $(#FFAA00)параллельно T4$(): wyvern → draconic → reactor.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "draconicevolution:wyvern_pickaxe",
                "text": "$(#FFAA00)Wyvern tier$(): первые инструменты и cores.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "draconicevolution:awakened_core",
                "text": "$(#FFAA00)Draconic Core$(): апгрейд после wyvern.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "draconicevolution:draconic_pickaxe",
                "text": "$(#FFAA00)Draconic Pick$() (финал): скорость и AoE добычи.",
            },
        ],
    ),
    "side_cataclysm": (
        "Cataclysm — боссы",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Cataclysm — $(#DD55DD)эндгейм-боссы$() и оружие. "
                "Готовь броню, зелья, кооп-роли.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "cataclysm:void_core",
                "text": "$(#FFAA00)Void Core$(): компонент высоких крафтов.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "cataclysm:gauntlet_of_guard",
                "text": "$(#FFAA00)Gauntlet of Guard$(): трофей и мощное оружие.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "cataclysm:the_incinerator",
                "text": "$(#FFAA00)The Incinerator$() (финал): топовое оружие ветки.",
            },
        ],
    ),
    "side_relics": (
        "Relics — артефакты",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Зачем$()$(br2)Relics даёт $(#FFAA00)пассивные артефакты$() — скорость, вода, удача. "
                "Носи в слотах curios/accessory.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "relics:roller_skates",
                "text": "$(#FFAA00)Roller Skates$(): скорость на ровной поверхности.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "relics:aqua_walker",
                "text": "$(#FFAA00)Aqua Walker$(): ходьба по воде.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "relics:amphibian_boot",
                "text": "$(#FFAA00)Amphibian Boots$() (финал): вода + скорость.",
            },
        ],
    ),
    "side_post_caves": (
        "Alex's Caves — глибина",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Після якоря$()$(br2)Ветка відкривається після §eЯдра реальності§r. "
                "Кодекс печер → таблички → ехо-осколки — повне кільце Alex's Caves.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "kubejs:decrypted_cave_codex",
                "text": "$(#FFAA00)Розшифрований кодекс$(): старт ветки. JEI — рецепти табличок.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "alexscaves:cave_tablet",
                "text": "$(#FFAA00)Таблички печер$(): відкривають біоми. Кооп: один копає, другий збирає.",
            },
        ],
    ),
    "side_post_bossfarm": (
        "Фарм босів після фіналу",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Бос-фарм$()$(br2)Після стабілізації якоря — полювання на §eCataclysm§r і §eMowzie§r. "
                "Трофеї для двох: зірки Незера, void eye, Wroughtnaut.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "minecraft:nether_star",
                "text": "$(#FFAA00)Зірки Незера$(): 2 шт. — кооп-рейд Withер/інших босів.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "cataclysm:the_annihilator",
                "text": "$(#FFAA00)The Annihilator$() (фінал): ендгейм-зброя Cataclysm.",
            },
        ],
    ),
    "side_post_epilogue": (
        "Фінальний облік модів",
        [
            {
                "type": "patchouli:text",
                "text": "$(bold)Епілог$()$(br2)Збірка вершин модпаку: §eAE2 16k§r, §eProjectE tablet§r, "
                "§eDraconic chaotic§r, §enext_ae core§r, маяк над лагерем.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "kubejs:reality_anchor_core",
                "text": "$(#FFAA00)Ядро якоря$(): символ завершення основної лінії.",
            },
            {
                "type": "patchouli:spotlight",
                "item": "projecte:transmutation_tablet",
                "text": "$(#FFAA00)EMC-планшет$(): пік ProjectE — трансмутація в долоні.",
            },
        ],
    ),
}


def quest_id(prefix: str) -> str:
    return f"{prefix}000000000001"


def main() -> None:
    ENTRIES_DIR.mkdir(parents=True, exist_ok=True)
    ADV_DIR.mkdir(parents=True, exist_ok=True)
    unlocks: list[dict] = []

    for sortnum, (fn, _title, icon, _grp, _ord_i, _old, prefix, _quests, _layout) in enumerate(
        SIDE_BRANCHES, start=1
    ):
        if fn not in GUIDES:
            print(f"  skip {fn}: no guide")
            continue
        name, pages = GUIDES[fn]
        adv_key = f"codex_{fn}"
        qid = quest_id(prefix)

        entry = {
            "name": name,
            "icon": icon,
            "category": "patchouli:codex_branches",
            "advancement": f"cooptech:journal/{adv_key}",
            "secret": True,
            "sortnum": sortnum,
            "pages": pages,
        }
        out_path = ENTRIES_DIR / f"{fn.replace('side_', '')}.json"
        out_path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  wrote {out_path.name}")

        adv_path = ADV_DIR / f"{adv_key}.json"
        if not adv_path.exists():
            adv_path.write_text(ADV_STUB, encoding="utf-8")

        unlocks.append({"quest": qid, "adv": adv_key, "name": name, "side": fn})

    for sortnum, (fn, _title, icon, prefix, _quests, _order, _hub_id) in enumerate(
        POST_SIDE_BRANCHES, start=18
    ):
        if fn not in GUIDES:
            print(f"  skip {fn}: no guide")
            continue
        name, pages = GUIDES[fn]
        adv_key = f"codex_{fn}"
        qid = quest_id(prefix)
        entry = {
            "name": name,
            "icon": icon,
            "category": "patchouli:codex_branches",
            "advancement": f"cooptech:journal/{adv_key}",
            "secret": True,
            "sortnum": sortnum,
            "pages": pages,
        }
        out_name = fn.replace("side_post_", "post_")
        out_path = ENTRIES_DIR / f"{out_name}.json"
        out_path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  wrote {out_path.name}")
        adv_path = ADV_DIR / f"{adv_key}.json"
        if not adv_path.exists():
            adv_path.write_text(ADV_STUB, encoding="utf-8")
        unlocks.append({"quest": qid, "adv": adv_key, "name": name, "side": fn})

    ref = ROOT / "scripts" / "codex_side_unlocks_ref.json"
    ref.write_text(json.dumps(unlocks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  {len(unlocks)} side codex entries")


if __name__ == "__main__":
    main()
