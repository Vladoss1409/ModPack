"""Quest manifest data for CoopTech FTB Quests v1 (~227 quests)."""
from __future__ import annotations

from dataclasses import dataclass, field

PROLOGUE_FINALE = 'A101000000000009'


@dataclass
class Q:
    """Single quest spec: num is stable ID suffix within chapter prefix."""

    num: int
    title: str
    item: str
    count: int = 1
    x: float = 0.0
    y: float = 0.0
    deps: list[int] = field(default_factory=list)
    min_deps: int | None = None
    gate: bool = False
    finale: bool = False
    shape: str = 'circle'
    size: float | None = None
    subtitle: str = ''
    desc: list[str] = field(default_factory=list)
    extra_tasks: list[tuple[str, str, int]] = field(default_factory=list)  # item, title, count


def qid(prefix: str, num: int) -> str:
    return f'{prefix}{num:012d}'


def tid(prefix: str, num: int) -> str:
    return f'T{prefix[1:]}{num:012d}'


def rid(prefix: str, num: int) -> str:
    return f'R{prefix[1:]}{num:012d}'


# --- Ch1 Foundation (18) — keep gate 005, finale 006 ---
CH1_PREFIX = 'A201'
CH1 = [
    Q(1, 'Автоплавка', 'ironfurnaces:iron_furnace', x=-3, y=24, deps=[7]),
    Q(2, 'Сеть ящиков', 'storagedrawers:controller', x=-1, y=24, deps=[7],
      extra_tasks=[('storagedrawers:oak_full_drawers_2', 'Oak Drawer 2x2', 1)]),
    Q(3, 'Умное хранение', 'sophisticatedstorage:iron_barrel', x=1, y=24, deps=[7]),
    Q(4, 'Железный резерв', 'minecraft:raw_iron', count=512, x=3, y=24, deps=[7]),
    Q(5, 'Фундамент готов', 'kubejs:quest_gate', x=0, y=26,
      deps=[1, 2, 3, 4], min_deps=2, gate=True, shape='diamond'),
    Q(6, 'Фрагмент: Фундамент II', 'thermal:machine_frame', x=0, y=38,
      deps=[18], finale=True, shape='gear', size=1.5),
    Q(7, 'Старт инфраструктуры', 'minecraft:crafting_table', x=0, y=22,
      deps=[], desc=['Рубеж пролога пройден — разверните tech-инфраструктуру якоря.']),
    Q(8, 'Медный контур', 'minecraft:copper_ingot', count=32, x=-3, y=28, deps=[5]),
    Q(9, 'Оловянный контур', 'thermal:tin_ingot', count=32, x=-1, y=28, deps=[5]),
    Q(10, 'Invar слитки', 'thermal:invar_ingot', count=16, x=1, y=28, deps=[5]),
    Q(11, 'RF катушки', 'thermal:rf_coil', count=8, x=3, y=28, deps=[5]),
    Q(12, 'Сплавы готовы', 'kubejs:quest_gate', x=0, y=30,
      deps=[8, 9, 10, 11], min_deps=2, gate=True, shape='diamond'),
    Q(13, 'Redstone Furnace', 'thermal:machine_furnace', x=-3, y=32, deps=[12]),
    Q(14, 'Pulverizer', 'thermal:machine_pulverizer', x=-1, y=32, deps=[12]),
    Q(15, 'Sawmill', 'thermal:machine_sawmill', x=1, y=32, deps=[12]),
    Q(16, 'Energy Cell', 'thermal:energy_cell', x=3, y=32, deps=[12]),
    Q(17, 'Тепловой рубеж', 'kubejs:quest_gate', x=0, y=35,
      deps=[13, 14, 15, 16], min_deps=2, gate=True, shape='diamond'),
    Q(18, 'Мастерская Thermal', 'thermal:machine_crafter', x=0, y=37, deps=[17]),
]

# --- Ch2 Surface (22) ---
CH2_PREFIX = 'A301'
CH2_PREV_FINALE = f'{CH1_PREFIX}000000000006'
CH2 = [
    Q(1, 'Компас структур', 'explorerscompass:explorerscompass', x=-3, y=0, deps=[7]),
    Q(2, 'Разведка руин', 'minecraft:name_tag', x=-1, y=0, deps=[7],
      extra_tasks=[('minecraft:emerald', '8 изумрудов', 8)]),
    Q(3, 'Бестиарий', 'alexsmobs:animal_dictionary', x=1, y=0, deps=[7]),
    Q(4, 'Биом-образец', 'minecraft:moss_block', count=16, x=3, y=0, deps=[7]),
    Q(5, 'Поверхность изучена', 'kubejs:quest_gate', x=0, y=2,
      deps=[1, 2, 3, 4], min_deps=2, gate=True, shape='diamond'),
    Q(6, 'Фрагмент: Поверхность', 'mowziesmobs:wroughtnaut_iron', count=2, x=0, y=16,
      deps=[22], finale=True, shape='gear', size=1.5),
    Q(7, 'Выход на поверхность', 'minecraft:compass', x=0, y=-2, deps=[]),
    Q(8, 'Nature\'s Compass', 'naturescompass:naturescompass', x=-3, y=4, deps=[5]),
    Q(9, 'Карта Terralith', 'minecraft:filled_map', x=-1, y=4, deps=[5]),
    Q(10, 'Реликварий поля', 'kubejs:relic_vault', x=1, y=4, deps=[5]),
    Q(11, 'Кооп-маяк', 'kubejs:resonance_beacon', x=3, y=4, deps=[5]),
    Q(12, 'Разведка II', 'kubejs:quest_gate', x=0, y=6,
      deps=[8, 9, 10, 11], min_deps=2, gate=True, shape='diamond'),
    Q(13, 'WDA данж', 'minecraft:golden_apple', x=-3, y=8, deps=[12]),
    Q(14, 'Repurposed Ruins', 'minecraft:emerald', count=4, x=-1, y=8, deps=[12]),
    Q(15, 'Alex Caves', 'minecraft:amethyst_shard', count=8, x=1, y=8, deps=[12]),
    Q(16, 'Twilight ключ', 'twilightforest:liveroot', count=4, x=3, y=8, deps=[12]),
    Q(17, 'Миры рядом', 'kubejs:quest_gate', x=0, y=10,
      deps=[13, 14, 15, 16], min_deps=2, gate=True, shape='diamond'),
    Q(18, 'IE Hammer', 'immersiveengineering:hammer', x=-2, y=12, deps=[17]),
    Q(19, 'Flux Dust заготовка', 'minecraft:redstone', count=64, x=2, y=12, deps=[17]),
    Q(20, 'Wroughtnaut охота', 'mowziesmobs:wrought_helmet', x=-1, y=14, deps=[18, 19], min_deps=1),
    Q(21, 'Полевой трофей', 'minecraft:nether_star', x=1, y=14, deps=[20]),
    Q(22, 'Рубеж поверхности', 'kubejs:quest_gate', x=0, y=15,
      deps=[18, 19, 20, 21], min_deps=2, gate=True, shape='diamond'),
]

# --- Ch3 Flux (18) ---
CH3_PREFIX = 'A401'
CH3_PREV_FINALE = f'{CH2_PREFIX}000000000006'
CH3 = [
    Q(1, 'Thermal машина', 'thermal:machine_furnace', x=-3, y=0, deps=[7]),
    Q(2, 'Базовая энергия', 'powah:furnator_basic', x=-1, y=0, deps=[7]),
    Q(3, 'Coke Oven', 'immersiveengineering:cokebrick', count=27, x=1, y=0, deps=[7]),
    Q(4, 'Поток слитков', 'minecraft:iron_ingot', count=256, x=3, y=0, deps=[7]),
    Q(5, 'Энергоконтур', 'thermal:energy_cell', x=0, y=2,
      deps=[1, 2, 3, 4], min_deps=2, gate=True, shape='diamond'),
    Q(6, 'Фрагмент: Поток', 'thermal:energy_cell', count=4, x=0, y=14,
      deps=[18], finale=True, shape='gear', size=1.5,
      extra_tasks=[('thermal:rf_coil', '16 RF катушек', 16)]),
    Q(7, 'Энергетический старт', 'minecraft:redstone_block', x=0, y=-2, deps=[]),
    Q(8, 'Powah Capacitor', 'powah:capacitor_basic', x=-3, y=4, deps=[5]),
    Q(9, 'IE Capacitor', 'immersiveengineering:capacitor_lv', x=-1, y=4, deps=[5]),
    Q(10, 'Dynamo', 'thermal:dynamo_stirling', x=1, y=4, deps=[5]),
    Q(11, 'Fluid Cell', 'thermal:fluid_cell', x=3, y=4, deps=[5]),
    Q(12, 'Генерация I', 'kubejs:quest_gate', x=0, y=6,
      deps=[8, 9, 10, 11], min_deps=2, gate=True, shape='diamond'),
    Q(13, 'Powah Tier 2', 'powah:capacitor_hardened', x=-3, y=8, deps=[12]),
    Q(14, 'IE Wire', 'immersiveengineering:wirecoil_copper', count=16, x=-1, y=8, deps=[12]),
    Q(15, 'Thermal Upgrade', 'thermal:slot_seal', count=4, x=1, y=8, deps=[12]),
    Q(16, 'EnderIO Cap', 'enderio:basic_capacitor', count=4, x=3, y=8, deps=[12]),
    Q(17, 'Стабильный поток', 'kubejs:quest_gate', x=0, y=11,
      deps=[13, 14, 15, 16], min_deps=2, gate=True, shape='diamond'),
    Q(18, 'Crescent Hammer', 'thermal:crescent_hammer', x=0, y=13, deps=[17],
      extra_tasks=[('fluxnetworks:flux_dust', 'Flux Dust', 8)]),
]

# --- Ch4 Production (35) ---
CH4_PREFIX = 'A501'
CH4_PREV_FINALE = f'{CH3_PREFIX}000000000006'
CH4 = [
    Q(1, 'Mekanism Core', 'mekanism:metallurgic_infuser', x=0, y=-2, deps=[]),
    Q(2, 'Enrichment', 'mekanism:enrichment_chamber', x=-3, y=0, deps=[1]),
    Q(3, 'Crusher', 'mekanism:crusher', x=-1, y=0, deps=[1]),
    Q(4, 'Energized Smelter', 'mekanism:energized_smelter', x=1, y=0, deps=[1]),
    Q(5, 'Basic Factory', 'mekanism:basic_smelting_factory', x=3, y=0, deps=[1]),
    Q(6, 'Mek Gate I', 'kubejs:quest_gate', x=0, y=2,
      deps=[2, 3, 4, 5], min_deps=2, gate=True, shape='diamond'),
    Q(7, 'Steel Ingot', 'mekanism:ingot_steel', count=32, x=-3, y=4, deps=[6]),
    Q(8, 'Osmium', 'mekanism:ingot_osmium', count=16, x=-1, y=4, deps=[6]),
    Q(9, 'Basic Control', 'mekanism:basic_control_circuit', count=8, x=1, y=4, deps=[6]),
    Q(10, 'Pressurized Tube', 'mekanism:basic_pressurized_tube', count=16, x=3, y=4, deps=[6]),
    Q(11, 'Mek Gate II', 'kubejs:quest_gate', x=0, y=6,
      deps=[7, 8, 9, 10], min_deps=2, gate=True, shape='diamond'),
    Q(12, 'Digital Miner', 'mekanism:digital_miner', x=-2, y=8, deps=[11]),
    Q(13, 'Advanced Factory', 'mekanism:advanced_factory', x=2, y=8, deps=[11]),
    Q(14, 'EnderIO Alloy', 'enderio:conductive_alloy_ingot', count=32, x=-3, y=10, deps=[11]),
    Q(15, 'Capacitor Bank', 'enderio:basic_capacitor_bank', x=3, y=10, deps=[11]),
    Q(16, 'SAG Mill', 'enderio:sag_mill', x=-1, y=10, deps=[11]),
    Q(17, 'Alloy Smelter', 'enderio:alloy_smelter', x=1, y=10, deps=[11]),
    Q(18, 'Production Gate', 'kubejs:quest_gate', x=0, y=12,
      deps=[12, 13, 14, 15, 16, 17], min_deps=3, gate=True, shape='diamond'),
    Q(19, 'AE2 Inscriber', 'ae2:inscriber', x=-3, y=14, deps=[18]),
    Q(20, 'AE2 Press', 'ae2:calculation_processor_press', x=-1, y=14, deps=[18]),
    Q(21, 'Mek QIO', 'mekanism:qio_drive_array', x=1, y=14, deps=[18]),
    Q(22, 'EnderIO Conduit', 'enderio:item_conduit', count=32, x=3, y=14, deps=[18]),
    Q(23, 'Network Gate', 'kubejs:quest_gate', x=0, y=16,
      deps=[19, 20, 21, 22], min_deps=2, gate=True, shape='diamond'),
    Q(24, 'Mek Reactor', 'mekanism:reactor_glass', count=16, x=-2, y=18, deps=[23]),
    Q(25, 'Induction Matrix', 'mekanism:induction_cell', x=2, y=18, deps=[23]),
    Q(26, 'AE2 Controller', 'ae2:controller', x=0, y=20, deps=[24, 25], min_deps=1),
    Q(27, 'Mek Gate III', 'kubejs:quest_gate', x=0, y=22,
      deps=[26], gate=True, shape='diamond'),
    Q(28, 'Ultimate Factory', 'mekanism:ultimate_factory', x=-2, y=24, deps=[27]),
    Q(29, 'Creative-ish Cell', 'mekanism:basic_energy_cube', x=2, y=24, deps=[27]),
    Q(30, 'Production Hub', 'mekanism:teleportation_core', x=0, y=26, deps=[28, 29], min_deps=1),
    Q(31, 'Apotheosis Altar', 'apotheosis:simple_reforging_table', x=-2, y=28, deps=[30]),
    Q(32, 'Spawner', 'apotheosis:ender_lead', x=2, y=28, deps=[30]),
    Q(33, 'Boss Trophy', 'minecraft:dragon_head', x=0, y=30, deps=[31, 32], min_deps=1),
    Q(34, 'Рубеж IV', 'kubejs:quest_gate', x=0, y=32,
      deps=[33], gate=True, shape='diamond'),
    Q(35, 'Фрагмент: Production', 'kubejs:anchor_shard_05', x=0, y=34,
      deps=[34], finale=True, shape='gear', size=1.5),
]

# --- Ch5 Nano (22) ---
CH5_PREFIX = 'A601'
CH5_PREV_FINALE = f'{CH4_PREFIX}000000000035'
CH5 = [
    Q(1, 'Netherite шаблон', 'minecraft:netherite_upgrade_smithing_template', x=0, y=-2, deps=[]),
    Q(2, 'Ancient Debris', 'minecraft:ancient_debris', count=8, x=-2, y=0, deps=[1]),
    Q(3, 'Netherite Ingot', 'minecraft:netherite_ingot', count=4, x=2, y=0, deps=[1]),
    Q(4, 'Silent Template', 'silentgear:template_board', x=-3, y=2, deps=[2, 3], min_deps=1),
    Q(5, 'Blueprint', 'silentgear:blueprint_paper', count=8, x=3, y=2, deps=[2, 3], min_deps=1),
    Q(6, 'Nano Gate I', 'kubejs:quest_gate', x=0, y=4,
      deps=[4, 5], gate=True, shape='diamond'),
    Q(7, 'Pickaxe Head', 'silentgear:pickaxe_head', x=-3, y=6, deps=[6]),
    Q(8, 'Sword Blade', 'silentgear:sword_blade', x=-1, y=6, deps=[6]),
    Q(9, 'Armor Plate', 'silentgear:plate', count=4, x=1, y=6, deps=[6]),
    Q(10, 'Binding', 'silentgear:binding', count=4, x=3, y=6, deps=[6]),
    Q(11, 'Gear Craft', 'silentgear:pickaxe', x=0, y=8, deps=[7, 8, 9, 10], min_deps=2),
    Q(12, 'Nano Gate II', 'kubejs:quest_gate', x=0, y=10,
      deps=[11], gate=True, shape='diamond'),
    Q(13, 'Mek Meka-Tool', 'mekanism:meka_tool', x=-2, y=12, deps=[12]),
    Q(14, 'Mek Suit', 'mekanism:mekasuit_helmet', x=2, y=12, deps=[12]),
    Q(15, 'Relics', 'relics:roller_skates', x=-2, y=14, deps=[13]),
    Q(16, 'Iron Spells', 'irons_spellbooks:arcane_essence', count=16, x=2, y=14, deps=[14]),
    Q(17, 'Enchant Table', 'minecraft:enchanting_table', x=0, y=16, deps=[15, 16], min_deps=1),
    Q(18, 'Apotheosis Gem', 'apotheosis:gem', x=-2, y=18, deps=[17]),
    Q(19, 'Reforging', 'apotheosis:reforging_table', x=2, y=18, deps=[17]),
    Q(20, 'Nano Gate III', 'kubejs:quest_gate', x=0, y=20,
      deps=[18, 19], gate=True, shape='diamond'),
    Q(21, 'Рубеж V', 'kubejs:quest_gate', x=0, y=22,
      deps=[20], gate=True, shape='diamond'),
    Q(22, 'Фрагмент: Nano', 'kubejs:anchor_shard_06', x=0, y=24,
      deps=[21], finale=True, shape='gear', size=1.5),
]

# --- Ch6 Finale (30) ---
CH6_PREFIX = 'A701'
CH6_PREV_FINALE = f'{CH5_PREFIX}000000000022'
CH6 = [
    Q(1, 'Draconium Dust', 'draconicevolution:draconium_dust', count=16, x=0, y=-2, deps=[]),
    Q(2, 'Wyvern Core', 'draconicevolution:wyvern_core', x=-2, y=0, deps=[1]),
    Q(3, 'Draconic Core', 'draconicevolution:awakened_core', x=2, y=0, deps=[1]),
    Q(4, 'Energy Core', 'draconicevolution:energy_core', x=0, y=2, deps=[2, 3], min_deps=1),
    Q(5, 'Finale Gate I', 'kubejs:quest_gate', x=0, y=4,
      deps=[4], gate=True, shape='diamond'),
    Q(6, 'Fusion Crafting', 'draconicevolution:crafting_core', x=-3, y=6, deps=[5]),
    Q(7, 'Draconium Block', 'draconicevolution:draconium_block', count=4, x=3, y=6, deps=[5]),
    Q(8, 'Chaos Shard', 'draconicevolution:chaos_shard', x=0, y=8, deps=[6, 7], min_deps=1),
    Q(9, 'Finale Gate II', 'kubejs:quest_gate', x=0, y=10,
      deps=[8], gate=True, shape='diamond'),
    Q(10, 'Wyvern Sword', 'draconicevolution:wyvern_sword', x=-2, y=12, deps=[9]),
    Q(11, 'Wyvern Pick', 'draconicevolution:wyvern_pickaxe', x=2, y=12, deps=[9]),
    Q(12, 'Draconic Armor', 'draconicevolution:wyvern_chestpiece', x=0, y=14, deps=[10, 11], min_deps=1),
    Q(13, 'Cataclysm Weapon', 'cataclysm:gauntlet_of_guard', x=-2, y=16, deps=[12]),
    Q(14, 'Twilight Boss', 'twilightforest:knightmetal_ingot', count=8, x=2, y=16, deps=[12]),
    Q(15, 'Небесный рубеж', 'blue_skies:pyrope_gem', count=8, x=0, y=18, deps=[13, 14], min_deps=1),
    Q(16, 'Finale Gate III', 'kubejs:quest_gate', x=0, y=20,
      deps=[15], gate=True, shape='diamond'),
    Q(17, 'Beacon', 'minecraft:beacon', x=-2, y=22, deps=[16]),
    Q(18, 'Nether Star Farm', 'minecraft:nether_star', count=4, x=2, y=22, deps=[16]),
    Q(19, 'Elytra', 'minecraft:elytra', x=0, y=24, deps=[17, 18], min_deps=1),
    Q(20, 'Creative Cell', 'powah:energy_cell_nitro', x=-2, y=26, deps=[19]),
    Q(21, 'Flux Point', 'fluxnetworks:flux_point', x=2, y=26, deps=[19]),
    Q(22, 'Draconic Reactor', 'draconicevolution:reactor_core', x=0, y=28, deps=[20, 21], min_deps=1),
    Q(23, 'Chaos Guardian', 'draconicevolution:chaos_shard', count=4, x=-2, y=30, deps=[22]),
    Q(24, 'Anchor Shard', 'kubejs:anchor_shard_07', x=2, y=30, deps=[22]),
    Q(25, 'Finale Gate IV', 'kubejs:quest_gate', x=0, y=32,
      deps=[23, 24], gate=True, shape='diamond'),
    Q(26, 'Expedition Seal', 'kubejs:expedition_seal', x=-2, y=34, deps=[25]),
    Q(27, 'Journal Finale', 'kubejs:expedition_journal', x=2, y=34, deps=[25]),
    Q(28, 'Coop Trophy', 'minecraft:dragon_egg', x=0, y=36, deps=[26, 27], min_deps=1),
    Q(29, 'Рубеж VI', 'kubejs:quest_gate', x=0, y=38,
      deps=[28], gate=True, shape='diamond'),
    Q(30, 'Кодекс завершён', 'minecraft:nether_star', x=0, y=40,
      deps=[29], finale=True, shape='gear', size=1.6),
]

# --- Side branches: (prefix_idx, gate_id, lock_num, quests after lock) ---
# prefix A801..A808


def _side(start: int, items: list[tuple[str, str, int]]) -> list[Q]:
    out: list[Q] = []
    for i, (title, item, count) in enumerate(items, start=start):
        prev = [i - 1] if i > start else []
        out.append(Q(i, title, item, count=count, deps=prev))
    return out


SIDE_THERMAL = _side(1, [
    ('Machine Frame', 'thermal:machine_frame', 1),
    ('Redstone Furnace', 'thermal:machine_furnace', 1),
    ('Pulverizer', 'thermal:machine_pulverizer', 1),
    ('Sawmill', 'thermal:machine_sawmill', 1),
    ('Induction Smelter', 'thermal:machine_smelter', 1),
    ('Fluid Cell', 'thermal:fluid_cell', 1),
    ('Dynamo', 'thermal:dynamo_stirling', 1),
    ('Energy Cell', 'thermal:energy_cell', 1),
    ('Augment', 'thermal:slot_seal', 4),
    ('Resonant Cell', 'thermal:energy_cell', 4),
    ('Thermal Drive', 'thermal:rf_coil', 16),
    ('Thermal Finale', 'thermal:machine_crafter', 1),
    ('Resonant Upgrade', 'thermal:flux_capacitor', 4),
])

SIDE_KITCHEN = _side(1, [
    ('Cooking Pot', 'farmersdelight:cooking_pot', 1),
    ('Cutting Board', 'farmersdelight:cutting_board', 1),
    ('Skillet', 'farmersdelight:skillet', 1),
    ('Stove', 'farmersdelight:stove', 1),
    ('Cabinet', 'farmersdelight:spruce_cabinet', 4),
    ('Pie', 'farmersdelight:apple_pie', 4),
    ('Feast', 'farmersdelight:roast_chicken_block', 1),
    ('Hot Cocoa', 'farmersdelight:hot_cocoa', 8),
    ('Dog Food', 'farmersdelight:dog_food', 8),
    ('Bacon', 'farmersdelight:cooked_bacon', 16),
    ('Steak', 'minecraft:cooked_beef', 32),
    ('Golden Carrot', 'minecraft:golden_carrot', 16),
    ('Suspicious Stew', 'minecraft:suspicious_stew', 4),
    ('Cake', 'minecraft:cake', 1),
    ('Honey', 'minecraft:honey_bottle', 8),
    ('Campfire', 'minecraft:campfire', 4),
    ('Barrel', 'minecraft:barrel', 8),
    ('Kitchen Finale', 'farmersdelight:rich_soil', 8),
])

SIDE_ARCANE = _side(1, [
    ('Arcane Essence', 'irons_spellbooks:arcane_essence', 16),
    ('Inscription Table', 'irons_spellbooks:inscription_table', 1),
    ('Spell Book', 'irons_spellbooks:copper_spell_book', 1),
    ('Mana Upgrade', 'irons_spellbooks:common_ink', 8),
    ('Fire Spell', 'irons_spellbooks:fire_rune', 1),
    ('Ice Spell', 'irons_spellbooks:ice_rune', 1),
    ('Lightning', 'irons_spellbooks:lightning_rune', 1),
    ('Priest Robe', 'irons_spellbooks:pumpkin_helmet', 1),
    ('Arcane Finale', 'irons_spellbooks:legendary_ink', 4),
])

SIDE_FLUX = _side(1, [
    ('Flux Dust', 'fluxnetworks:flux_dust', 16),
    ('Flux Core', 'fluxnetworks:flux_core', 4),
    ('Flux Plug', 'fluxnetworks:flux_plug', 1),
    ('Flux Point', 'fluxnetworks:flux_point', 4),
    ('Basic Storage', 'fluxnetworks:basic_flux_storage', 1),
    ('Gargantuan', 'fluxnetworks:gargantuan_flux_storage', 1),
    ('Wireless', 'fluxnetworks:flux_controller', 1),
])

SIDE_NETWORK = _side(1, [
    ('Certus', 'ae2:certus_quartz_crystal', 32),
    ('Growth Accelerator', 'ae2:growth_accelerator', 4),
    ('Inscriber', 'ae2:inscriber', 1),
    ('Processor', 'ae2:calculation_processor', 4),
    ('ME Drive', 'ae2:drive', 1),
    ('ME Interface', 'ae2:interface', 2),
    ('Import Bus', 'ae2:import_bus', 4),
    ('Export Bus', 'ae2:export_bus', 4),
    ('Crafting CPU', 'ae2:crafting_unit', 4),
    ('Controller', 'ae2:controller', 1),
    ('Wireless', 'ae2:wireless_access_point', 1),
])

SIDE_APOTHEOSIS = _side(1, [
    ('Simple Reforging', 'apotheosis:simple_reforging_table', 1),
    ('Salvaging', 'apotheosis:salvaging_table', 1),
    ('Gem', 'apotheosis:gem', 1),
    ('Sigil', 'apotheosis:sigil_of_enhancement', 1),
    ('Spawner', 'apotheosis:ender_lead', 1),
    ('Boss Summoner', 'apotheosis:boss_summoner', 1),
    ('Mythic Gem', 'apotheosis:mythic_material', 1),
    ('Apothic Finale', 'apotheosis:reforging_table', 1),
])

SIDE_SILENT = _side(1, [
    ('Template Board', 'silentgear:template_board', 4),
    ('Blueprint', 'silentgear:blueprint_paper', 8),
    ('Pick Head', 'silentgear:pickaxe_head', 1),
    ('Axe Head', 'silentgear:axe_head', 1),
    ('Binding', 'silentgear:binding', 4),
    ('Coating', 'silentgear:coating', 4),
    ('Silent Pick', 'silentgear:pickaxe', 1),
    ('Silent Sword', 'silentgear:sword', 1),
])

SIDE_DRACONIC = _side(1, [
    ('Draconium', 'draconicevolution:draconium_dust', 32),
    ('Wyvern Core', 'draconicevolution:wyvern_core', 1),
    ('Energy Core', 'draconicevolution:energy_core', 1),
    ('Crafting Core', 'draconicevolution:crafting_core', 1),
    ('Wyvern Pick', 'draconicevolution:wyvern_pickaxe', 1),
    ('Wyvern Sword', 'draconicevolution:wyvern_sword', 1),
    ('Draconic Core', 'draconicevolution:awakened_core', 1),
    ('Chaos Shard', 'draconicevolution:chaos_shard', 2),
    ('Reactor', 'draconicevolution:reactor_core', 1),
    ('Draconic Finale', 'draconicevolution:draconic_pickaxe', 1),
])

SIDE_STORAGE = _side(1, [
    ('Drawer 1x1', 'storagedrawers:oak_full_drawers_1', 4),
    ('Drawer 2x2', 'storagedrawers:oak_full_drawers_2', 4),
    ('Controller', 'storagedrawers:controller', 1),
    ('Keyring', 'storagedrawers:drawer_key', 1),
    ('Barrel', 'sophisticatedstorage:barrel', 4),
    ('Iron Barrel', 'sophisticatedstorage:iron_barrel', 1),
    ('Storage Controller', 'sophisticatedstorage:controller', 1),
    ('Storage Finale', 'sophisticatedstorage:gold_barrel', 1),
])

SIDE_MEKANISM = _side(1, [
    ('Metallurgic Infuser', 'mekanism:metallurgic_infuser', 1),
    ('Enrichment Chamber', 'mekanism:enrichment_chamber', 1),
    ('Crusher', 'mekanism:crusher', 1),
    ('Energized Smelter', 'mekanism:energized_smelter', 1),
    ('Basic Factory', 'mekanism:basic_smelting_factory', 1),
    ('Digital Miner', 'mekanism:digital_miner', 1),
    ('Mekanism Finale', 'mekanism:teleportation_core', 1),
])

SIDE_IMMERSIVE = _side(1, [
    ('Engineer\'s Hammer', 'immersiveengineering:hammer', 1),
    ('Coke Brick', 'immersiveengineering:cokebrick', 27),
    ('Coke Oven', 'immersiveengineering:coke_oven', 1),
    ('LV Capacitor', 'immersiveengineering:capacitor_lv', 1),
    ('Copper Wire', 'immersiveengineering:wirecoil_copper', 16),
    ('Metal Press', 'immersiveengineering:metal_press', 1),
    ('IE Finale', 'immersiveengineering:light_engineering', 4),
])

SIDE_ENDERIO = _side(1, [
    ('Grains of Infinity', 'enderio:grains_of_infinity', 8),
    ('Conductive Alloy', 'enderio:conductive_alloy_ingot', 16),
    ('SAG Mill', 'enderio:sag_mill', 1),
    ('Alloy Smelter', 'enderio:alloy_smelter', 1),
    ('Capacitor Bank', 'enderio:basic_capacitor_bank', 1),
    ('Item Conduit', 'enderio:item_conduit', 32),
    ('EnderIO Finale', 'enderio:vibrant_capacitor_bank', 1),
])

SIDE_POWAH = _side(1, [
    ('Furnator', 'powah:furnator_basic', 1),
    ('Capacitor', 'powah:capacitor_basic', 1),
    ('Hardened Cap', 'powah:capacitor_hardened', 1),
    ('Blazing Crystal', 'powah:crystal_blazing', 4),
    ('Niotic Cap', 'powah:capacitor_niotic', 1),
    ('Powah Finale', 'powah:energy_cell_nitro', 1),
])

SIDE_BESTIARY = _side(1, [
    ('Animal Dictionary', 'alexsmobs:animal_dictionary', 1),
    ('Explorer\'s Compass', 'explorerscompass:explorerscompass', 1),
    ('Nature\'s Compass', 'naturescompass:naturescompass', 1),
    ('Grizzly Fur', 'alexsmobs:bear_fur', 4),
    ('Void Worm Eye', 'alexsmobs:void_worm_eye', 1),
    ('Wrought Helm', 'mowziesmobs:wrought_helmet', 1),
    ('Dungeon Loot', 'minecraft:golden_apple', 4),
    ('Bestiary Finale', 'minecraft:nether_star', 1),
])

SIDE_TWILIGHT = _side(1, [
    ('Liveroot', 'twilightforest:liveroot', 4),
    ('Torchberries', 'twilightforest:torchberries', 8),
    ('Naga Scale', 'twilightforest:naga_scale', 4),
    ('Steeleaf', 'twilightforest:steeleaf_ingot', 8),
    ('Knightmetal', 'twilightforest:knightmetal_ingot', 8),
    ('Twilight Finale', 'twilightforest:phantom_helmet', 1),
])

SIDE_RELICS = _side(1, [
    ('Roller Skates', 'relics:roller_skates', 1),
    ('Horse Shoe', 'relics:lucky_horseshoe', 1),
    ('Aqua Walker', 'relics:aqua_walker', 1),
    ('Midnight Roast', 'relics:midnight_robe', 1),
    ('Relics Finale', 'relics:amphibian_boot', 1),
])

SIDE_CATACLYSM = _side(1, [
    ('Void Core', 'cataclysm:void_core', 2),
    ('Witherite', 'cataclysm:witherite_ingot', 4),
    ('Gauntlet', 'cataclysm:gauntlet_of_guard', 1),
    ('Ignitium', 'cataclysm:ignitium_ingot', 4),
    ('Cataclysm Finale', 'cataclysm:the_incinerator', 1),
])

# --- Post-T5 (after reality anchor) ---
SIDE_POST_CAVES = _side(1, [
    ('Cave Codex', 'kubejs:decrypted_cave_codex', 1),
    ('Cave Tablet', 'alexscaves:cave_tablet', 2),
    ('Echo Shards', 'minecraft:echo_shard', 8),
    ('Limestone', 'alexscaves:limestone', 32),
    ('Sulfur', 'alexscaves:sulfur', 16),
    ('Metal Swarf', 'alexscaves:metal_swarf', 16),
    ('Caves Finale', 'alexscaves:cave_tablet', 4),
])

SIDE_POST_BOSS = _side(1, [
    ('Nether Star', 'minecraft:nether_star', 2),
    ('Void Eye', 'cataclysm:void_eye', 1),
    ('Wroughtnaut Helm', 'mowziesmobs:wrought_helmet', 1),
    ('Monstrous Horn', 'cataclysm:monstrous_horn', 1),
    ('Dragon Head', 'minecraft:dragon_head', 1),
    ('Black Steel', 'cataclysm:black_steel_ingot', 8),
    ('Boss Finale', 'cataclysm:the_annihilator', 1),
])

SIDE_POST_EPILOGUE = _side(1, [
    ('Anchor Core', 'kubejs:reality_anchor_core', 1),
    ('ME 16k', 'ae2:item_storage_cell_16k', 1),
    ('EMC Tablet', 'projecte:transmutation_tablet', 1),
    ('Chaotic Pick', 'draconicevolution:chaotic_pickaxe', 1),
    ('Next AE Core', 'next_ae:machine_core', 1),
    ('Anchor Nexus', 'kubejs:anchor_nexus', 1),
    ('Convergence Relic', 'kubejs:reliquary_convergence', 1),
    ('Epilogue Finale', 'minecraft:beacon', 1),
])

GROUP_POST = 'B100000000000006'

# hub_branch_quest_id for lock deps
POST_SIDE_BRANCHES = [
    ('side_post_caves', 'Печери розлому', 'kubejs:decrypted_cave_codex', 'A901', SIDE_POST_CAVES, 62, 'A900000000000002'),
    ('side_post_bossfarm', 'Бос-фарм якоря', 'cataclysm:void_eye', 'A902', SIDE_POST_BOSS, 63, 'A900000000000003'),
    ('side_post_epilogue', 'Епілог модів', 'kubejs:reality_anchor_core', 'A903', SIDE_POST_EPILOGUE, 64, 'A900000000000004'),
]

GROUP_INTRO = 'B100000000000001'
GROUP_MAIN = 'B100000000000002'
GROUP_TECH = 'B100000000000003'
GROUP_MAGIC = 'B100000000000004'
GROUP_OTHER = 'B100000000000005'

# (filename, title, icon, group, unlock_main_quest_id, order, prefix, quests, layout)
SIDE_BRANCHES = [
    ('side_kitchen', 'Полевая кухня', 'farmersdelight:cooking_pot', GROUP_OTHER,
     'A101000000000002', 0, 'A802', SIDE_KITCHEN, 'wave'),
    ('side_storage', 'Склад экспедиции', 'storagedrawers:controller', GROUP_OTHER,
     'A201000000000002', 1, 'A809', SIDE_STORAGE, 'spine'),
    ('side_thermal', 'Тепловой контур', 'thermal:machine_frame', GROUP_TECH,
     'A201000000000013', 0, 'A801', SIDE_THERMAL, 'spine'),
    ('side_bestiary', 'Полевой бестиарий', 'alexsmobs:animal_dictionary', GROUP_OTHER,
     'A301000000000003', 2, 'A813', SIDE_BESTIARY, 'radial'),
    ('side_immersive', 'Индустриальная ковка', 'immersiveengineering:hammer', GROUP_TECH,
     'A301000000000018', 1, 'A810', SIDE_IMMERSIVE, 'column'),
    ('side_twilight', 'Сумеречный рубеж', 'twilightforest:liveroot', GROUP_OTHER,
     'A301000000000016', 3, 'A815', SIDE_TWILIGHT, 'column'),
    ('side_powah', 'Резонанс Powah', 'powah:furnator_basic', GROUP_TECH,
     'A401000000000002', 2, 'A814', SIDE_POWAH, 'wave'),
    ('side_flux', 'Flux Networks', 'fluxnetworks:flux_dust', GROUP_TECH,
     'A401000000000018', 3, 'A804', SIDE_FLUX, 'spine'),
    ('side_mekanism', 'Промышленный узел', 'mekanism:metallurgic_infuser', GROUP_TECH,
     'A501000000000001', 4, 'A811', SIDE_MEKANISM, 'spine'),
    ('side_enderio', 'Проводник Ender IO', 'enderio:conductive_alloy_ingot', GROUP_TECH,
     'A501000000000014', 5, 'A812', SIDE_ENDERIO, 'wave'),
    ('side_network', 'Молекулярная сеть', 'ae2:controller', GROUP_TECH,
     'A501000000000019', 6, 'A805', SIDE_NETWORK, 'spine'),
    ('side_apotheosis', 'Апофеоз', 'apotheosis:simple_reforging_table', GROUP_MAGIC,
     'A501000000000031', 0, 'A806', SIDE_APOTHEOSIS, 'wave'),
    ('side_arcane', 'Арканум поля', 'irons_spellbooks:arcane_essence', GROUP_MAGIC,
     'A601000000000016', 1, 'A803', SIDE_ARCANE, 'wave'),
    ('side_relics', 'Реликвии', 'relics:roller_skates', GROUP_MAGIC,
     'A601000000000015', 2, 'A816', SIDE_RELICS, 'wave'),
    ('side_silent_gear', 'Ковка Silent Gear', 'silentgear:pickaxe', GROUP_OTHER,
     'A601000000000004', 4, 'A807', SIDE_SILENT, 'spine'),
    ('side_draconic', 'Драконья эволюция', 'draconicevolution:wyvern_core', GROUP_TECH,
     'A701000000000001', 7, 'A808', SIDE_DRACONIC, 'column'),
    ('side_cataclysm', 'Бездна Cataclysm', 'cataclysm:gauntlet_of_guard', GROUP_MAGIC,
     'A701000000000013', 3, 'A817', SIDE_CATACLYSM, 'column'),
]

MAIN_CHAPTERS = [
    ('main_03_ch2_surface', 'Глава 2: Разведка поверхности', 'explorerscompass:explorerscompass', GROUP_MAIN, 2,
     'A300000000000000', CH2_PREFIX, CH2, CH2_PREV_FINALE, '~12 ч'),
    ('main_04_ch3_flux', 'Глава 3: Энергетический поток', 'thermal:energy_cell', GROUP_MAIN, 3,
     'A400000000000000', CH3_PREFIX, CH3, CH3_PREV_FINALE, '~14 ч'),
    ('main_05_ch4_production', 'Глава 4: Промышленный узел', 'mekanism:metallurgic_infuser', GROUP_MAIN, 4,
     'A500000000000000', CH4_PREFIX, CH4, CH4_PREV_FINALE, '~20 ч'),
    ('main_06_ch5_nano', 'Глава 5: Наноковка', 'silentgear:pickaxe', GROUP_MAIN, 5,
     'A600000000000000', CH5_PREFIX, CH5, CH5_PREV_FINALE, '~16 ч'),
    ('main_07_ch6_finale', 'Глава 6: Сход с якорем', 'minecraft:beacon', GROUP_MAIN, 6,
     'A700000000000000', CH6_PREFIX, CH6, CH6_PREV_FINALE, '~24 ч'),
]
