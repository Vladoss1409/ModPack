// Next: AE — крафт-рецепти (ULTRA ENDGAME, Ender IO + Draconic Evolution).
// Мод next_ae НЕ містить власних крафтів (роздавалися серверним пакетом mcskill.net),
// тож у синглі його предмети неможливо створити. Цей скрипт додає лінійку крафтів.
//
// Філософія балансу (гібрид): функціональні AE2-бази лишаються там, де вони логічні
// (inscriber, molecular_assembler, crafting_unit, storage cell, pattern terminal, wireless),
// а ВСІ тірові/гейт-матеріали прив'язані до Ender IO + Draconic Evolution.
// Ладдер матеріалів: EnderIO alloy/crystal -> grains_of_infinity -> draconium ->
//   wyvern_core -> awakened_draconium / awakened_core -> dragon_heart -> chaos_shard / chaotic_core.
//
// Прогресія:
//   1) machine_core (vibrant_alloy + engineering_processor + draconium_core) -> базовий компонент.
//   2) Машини advanced_inscriber / charger / fluix_aggregator = machine_core + AE2-аналог + EnderIO.
//   3) У машинах робляться проміжні матеріали мода (НАВМИСНО без крафту, бо машинні):
//        fluix_aggregator -> fluix_steel, carbonic_fluix_complex, space_gem
//        advanced_inscriber -> parallel_processor
//   4) Решта блоків/предметів — крафти нижче.

ServerEvents.recipes(event => {
  const NS = 'next_ae:'
  const out = id => NS + id

  const shaped = (result, pattern, keys, rid) =>
    event.shaped(result, pattern, keys).id('next_ae:craft/' + rid)
  const shapeless = (result, ingredients, rid) =>
    event.shapeless(result, ingredients).id('next_ae:craft/' + rid)

  // зручні аліаси матеріалів
  const E = {
    conductive: 'enderio:conductive_alloy_ingot',
    redstone: 'enderio:redstone_alloy_ingot',
    energetic: 'enderio:energetic_alloy_ingot',
    vibrant: 'enderio:vibrant_alloy_ingot',
    darkSteel: 'enderio:dark_steel_ingot',
    darkSteelBlock: 'enderio:dark_steel_block',
    endSteel: 'enderio:end_steel_ingot',
    grains: 'enderio:grains_of_infinity',
    vibrantCrystal: 'enderio:vibrant_crystal',
    pulsatingCrystal: 'enderio:pulsating_crystal',
    fusedQuartz: 'enderio:fused_quartz',
    vibrantGear: 'enderio:vibrant_gear',
    octadic: 'enderio:octadic_capacitor'
  }
  const D = {
    dust: 'draconicevolution:draconium_dust',
    ingot: 'draconicevolution:draconium_ingot',
    block: 'draconicevolution:draconium_block',
    core: 'draconicevolution:draconium_core',
    wyvernCore: 'draconicevolution:wyvern_core',
    awakenedIngot: 'draconicevolution:awakened_draconium_ingot',
    awakenedBlock: 'draconicevolution:awakened_draconium_block',
    awakenedCore: 'draconicevolution:awakened_core',
    dragonHeart: 'draconicevolution:dragon_heart',
    chaosShard: 'draconicevolution:chaos_shard',
    chaoticCore: 'draconicevolution:chaotic_core',
    infusedObsidian: 'draconicevolution:infused_obsidian'
  }

  // ───────────────────────── 1. Базовий компонент ─────────────────────────
  shaped(out('machine_core'), [
    'VEV',
    'EDE',
    'VEV'
  ], {
    V: E.vibrant,
    E: 'ae2:engineering_processor',
    D: D.core
  }, 'machine_core')

  // ───────────────────────── 2. Машини мода ─────────────────────────
  shaped(out('advanced_inscriber'), [
    'GIG',
    'DMD',
    'GGG'
  ], { G: E.grains, I: 'ae2:inscriber', D: E.darkSteel, M: out('machine_core') }, 'advanced_inscriber')

  shaped(out('charger'), [
    'GHG',
    'DMD',
    'GGG'
  ], { G: E.grains, H: 'ae2:charger', D: E.darkSteel, M: out('machine_core') }, 'charger')

  shaped(out('fluix_aggregator'), [
    'GAG',
    'DMD',
    'GGG'
  ], { G: E.grains, A: 'ae2:growth_accelerator', D: E.darkSteel, M: out('machine_core') }, 'fluix_aggregator')

  // ───────────────────────── 3. Столи крафту (advanced→ultimate; basic-тіру в моді немає) ─────────────────────────
  shaped(out('advanced_crafting_table'), [
    'CUC',
    'UMU',
    'CUC'
  ], { C: E.vibrant, U: 'ae2:crafting_unit', M: out('machine_core') }, 'advanced_crafting_table')

  // ПРИМІТКА: elite/ultimate столи тепер крафтяться В ПОПЕРЕДНЬОМУ тірі столу
  // (elite -> у advanced 5x5; ultimate -> у elite 7x7). Див. 03_next_ae_extended_crafting.js.
  // Тут лишається тільки базовий advanced_crafting_table (на звичайному верстаку).

  // ───────────────────────── 4. Молекулярні асемблери (advanced→ultimate; basic-тіру в моді немає) ─────────────────────────
  shaped(out('advanced_molecular_assembler'), [
    'CAC',
    'FMF',
    'CAC'
  ], { A: 'ae2:molecular_assembler', C: E.vibrantCrystal, F: 'ae2:fluix_crystal', M: out('machine_core') }, 'advanced_molecular_assembler')

  shaped(out('elite_molecular_assembler'), [
    'DPD',
    'PTP',
    'DPD'
  ], { T: out('advanced_molecular_assembler'), P: out('parallel_processor'), D: D.core }, 'elite_molecular_assembler')

  shaped(out('ultimate_molecular_assembler'), [
    'HPH',
    'PTP',
    'HPH'
  ], { T: out('elite_molecular_assembler'), P: out('parallel_processor'), H: D.awakenedCore }, 'ultimate_molecular_assembler')

  // ───────────────────────── 5. Бездротові конектори (basic→ultimate) ─────────────────────────
  shaped(out('basic_wireless_connector'), [
    'CWC',
    'FMF',
    'CWC'
  ], { W: 'ae2:wireless_receiver', C: E.pulsatingCrystal, F: 'ae2:fluix_crystal', M: out('machine_core') }, 'basic_wireless_connector')

  shaped(out('advanced_wireless_connector'), [
    'BWB',
    'FTF',
    'BWB'
  ], { T: out('basic_wireless_connector'), W: 'ae2:wireless_booster', B: E.vibrant, F: out('fluix_steel') }, 'advanced_wireless_connector')

  shaped(out('elite_wireless_connector'), [
    'BWB',
    'STS',
    'BWB'
  ], { T: out('advanced_wireless_connector'), W: D.wyvernCore, S: out('space_gem'), B: D.block }, 'elite_wireless_connector')

  shaped(out('ultimate_wireless_connector'), [
    'BWB',
    'GTG',
    'BWB'
  ], { T: out('elite_wireless_connector'), W: D.awakenedCore, G: D.dragonHeart, B: D.awakenedIngot }, 'ultimate_wireless_connector')

  // ───────────────────────── 6. Massive Crafter (мультиблок) ─────────────────────────
  shaped(out('massive_crafter_frame'), [
    'DFD',
    'FMF',
    'DFD'
  ], { D: E.darkSteelBlock, F: out('fluix_steel'), M: out('machine_core') }, 'massive_crafter_frame')

  shaped('2x ' + out('massive_crafter_wall'), [
    'FDF',
    'DDD',
    'FDF'
  ], { D: E.darkSteelBlock, F: E.grains }, 'massive_crafter_wall')

  shaped('2x ' + out('massive_crafter_glass'), [
    'FGF',
    'GMG',
    'FGF'
  ], { G: E.fusedQuartz, F: out('fluix_steel'), M: out('machine_core') }, 'massive_crafter_glass')

  shaped(out('massive_crafter_core'), [
    'PCP',
    'CMC',
    'PCP'
  ], { C: D.core, P: out('parallel_processor'), M: out('machine_core') }, 'massive_crafter_core')

  shaped(out('massive_crafter_pattern'), [
    'FPF',
    'PMP',
    'FPF'
  ], { P: 'ae2:cable_pattern_provider', F: out('fluix_steel'), M: out('machine_core') }, 'massive_crafter_pattern')

  shaped(out('massive_crafter_speed'), [
    'FAF',
    'AMA',
    'FAF'
  ], { A: E.vibrantGear, F: out('fluix_steel'), M: out('machine_core') }, 'massive_crafter_speed')

  shaped(out('massive_crafter_expansion'), [
    'WCW',
    'CMC',
    'WCW'
  ], { W: out('massive_crafter_wall'), C: D.block, M: out('machine_core') }, 'massive_crafter_expansion')

  shaped(out('massive_crafter_filler'), [
    'DFD',
    'FMF',
    'DFD'
  ], { D: E.endSteel, F: out('fluix_steel'), M: out('machine_core') }, 'massive_crafter_filler')

  // ───────────────────────── 7. Stabilized Spawner ─────────────────────────
  shaped(out('stabilized_core'), [
    'GFG',
    'FHF',
    'GMG'
  ], { H: D.dragonHeart, F: out('space_gem'), G: E.grains, M: out('machine_core') }, 'stabilized_core')

  shaped(out('stabilized_spawner'), [
    'OSO',
    'SCS',
    'OSO'
  ], { O: D.infusedObsidian, S: out('space_gem'), C: out('stabilized_core') }, 'stabilized_spawner')

  // ───────────────────────── 8. Інструменти / утиліти ─────────────────────────
  shaped(out('network_analyzer'), [
    'CTC',
    'FMF',
    'CRC'
  ], { T: 'ae2:network_tool', F: 'ae2:fluix_crystal', C: E.vibrantCrystal, R: E.redstone, M: out('machine_core') }, 'network_analyzer')

  shaped(out('wireless_connector'), [
    'CWC',
    'FMF',
    'CFC'
  ], { W: 'ae2:wireless_booster', F: 'ae2:fluix_crystal', C: E.pulsatingCrystal, M: out('machine_core') }, 'wireless_connector_tool')

  shaped(out('cable_auto_router'), [
    'CTC',
    'RMR',
    'CRC'
  ], { T: 'ae2:network_tool', C: E.conductive, R: E.redstone, M: out('machine_core') }, 'cable_auto_router')

  // ───────────────────────── 9. Комірки (ultra endgame) ─────────────────────────
  // ПРИМІТКА: unlimited_item/fluid_storage_cell перенесено на 9x9 Ultimate-стіл
  // (див. 03_next_ae_extended_crafting.js) — тут їх 3x3-рецептів більше немає.

  // ПРИМІТКА: next_ae:infinite_cell — НЕ звичайний предмет (немає моделі/реєстру).
  // Мод реєструє KubeJS-типи 'next_ae:infinite_item_cell' / 'next_ae:infinite_fluid_cell':
  // інфініт-комірки створюються в startup-скрипті з прив'язкою до КОНКРЕТНОГО предмета/рідини
  // (наприклад .item('minecraft:diamond') або .fluid('minecraft:water')), після чого тут
  // можна додати їм ultra-рецепт. Цільові ресурси узгоджуються окремо.

  // ───────────────────────── 10. Модулі апгрейдів ─────────────────────────
  shaped(out('module_speed'), [
    ' R ',
    'FCF',
    ' R '
  ], { C: 'ae2:calculation_processor', F: E.energetic, R: E.redstone }, 'module_speed')

  shaped(out('module_recipe_multiplier'), [
    ' P ',
    'FCF',
    ' P '
  ], { C: 'ae2:engineering_processor', P: out('parallel_processor'), F: E.vibrant }, 'module_recipe_multiplier')

  // ───────────────────────── 11. Кабельні частини (тіри) ─────────────────────────
  shapeless('2x ' + out('advanced_cable_part'), [
    'ae2:fluix_smart_cable',
    E.conductive
  ], 'advanced_cable_part')

  shapeless(out('elite_cable_part'), [
    out('advanced_cable_part'),
    'ae2:fluix_smart_dense_cable',
    E.vibrant
  ], 'elite_cable_part')

  shapeless(out('flawless_cable_part'), [
    out('elite_cable_part'),
    D.awakenedIngot
  ], 'flawless_cable_part')

  // ───────────────────────── 12. Speculation Cores (x1 -> x64) ─────────────────────────
  shaped(out('speculation_core_1'), [
    'FSF',
    'SPS',
    'FSF'
  ], { P: out('parallel_processor'), S: out('space_gem'), F: D.ingot }, 'speculation_core_1')

  const tiers = [2, 4, 8, 16, 32, 64]
  tiers.forEach(t => {
    const prev = t / 2
    shapeless(out('speculation_core_' + t), [
      '2x ' + out('speculation_core_' + prev),
      D.dust
    ], 'speculation_core_' + t)
  })

  // ───────────────────────── 13. Термінали патернів (advanced→ultimate; basic-тіру в моді НЕМАЄ) ─────────────────────────
  // ПРИМІТКА: next_ae:basic_pattern_terminal НЕ зареєстрований (є лише модель-пустишка),
  // тому базового рецепта немає, а advanced будується напряму з ae2:pattern_access_terminal.
  shaped(out('advanced_pattern_terminal'), [
    'SFS',
    'FTF',
    'SFS'
  ], { T: 'ae2:pattern_access_terminal', F: out('fluix_steel'), S: E.grains }, 'advanced_pattern_terminal')

  shaped(out('elite_pattern_terminal'), [
    'SPS',
    'PTP',
    'SPS'
  ], { T: out('advanced_pattern_terminal'), P: out('parallel_processor'), S: D.block }, 'elite_pattern_terminal')

  shaped(out('ultimate_pattern_terminal'), [
    'GPG',
    'PTP',
    'GPG'
  ], { T: out('elite_pattern_terminal'), P: out('parallel_processor'), G: D.awakenedCore }, 'ultimate_pattern_terminal')

  // ───────────────────────── 14. Патерни крафту (advanced→ultimate; basic-тіру в моді немає) ─────────────────────────
  shapeless('2x ' + out('advanced_crafting_pattern'), [
    'ae2:blank_pattern',
    E.vibrantCrystal,
    out('fluix_steel')
  ], 'advanced_crafting_pattern')

  shapeless(out('elite_crafting_pattern'), [
    out('advanced_crafting_pattern'),
    D.ingot
  ], 'elite_crafting_pattern')

  shapeless(out('ultimate_crafting_pattern'), [
    out('elite_crafting_pattern'),
    D.awakenedIngot
  ], 'ultimate_crafting_pattern')
})
