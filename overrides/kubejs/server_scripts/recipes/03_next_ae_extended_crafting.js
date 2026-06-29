// Next: AE — Ultimate Crafting Station (Avaritia-style).
// Верстаки next_ae мають збільшену сітку: advanced 5x5, elite 7x7, ultimate 9x9
// з власними типами рецептів next_ae:<tier>_crafting_shaped (звичайний Forge shaped:
// pattern + key + result через CraftingHelper). Мод НЕ постачає жодного рецепта для них,
// тож столи безкорисні. Цей скрипт робить їх ЄДИНИМ способом отримати топ-предмети
// (replace_all): оригінальні рецепти прибираються, додаються великі NxN-візерунки.
//
// Старші тіри вміють рецепти молодших (advanced ⊂ elite ⊂ ultimate), тож:
//   advanced 5x5 -> next_ae:advanced_crafting_shaped
//   elite    7x7 -> next_ae:elite_crafting_shaped
//   ultimate 9x9 -> next_ae:ultimate_crafting_shaped
// Ті самі рецепти автоматизуються в AE2 через термінал шаблонів + молекулярний
// сборщик відповідного тіру.

ServerEvents.recipes(event => {
  // Хелпер: розширений shaped-рецепт у столі тіру.
  // (Rhino у KubeJS не має Object.fromEntries — будуємо key вручну.)
  const ext = (tier, resultId, count, pattern, key, id) => {
    const wrapped = {}
    for (const k in key) wrapped[k] = { item: key[k] }
    return event.custom({
      type: 'next_ae:' + tier + '_crafting_shaped',
      pattern: pattern,
      key: wrapped,
      result: { item: resultId, count: count }
    }).id('next_ae:extended/' + id)
  }

  // Прибрати всі наявні способи отримання (крафт/ф'южн/машина), де такі є.
  const replace = id => event.remove({ output: id })

  // ───────────────────────── Апгрейд столів (кожен тір — у попередньому) ─────────────────────────
  // elite_crafting_table крафтиться В advanced-столі (5x5, тип advanced_crafting_shaped).
  ext('advanced', 'next_ae:elite_crafting_table', 1, [
    'DFDFD',
    'FCMCF',
    'DMTMD',
    'FCMCF',
    'DFDFD'
  ], {
    D: 'draconicevolution:draconium_block', F: 'next_ae:fluix_steel',
    C: 'ae2:crafting_accelerator', M: 'next_ae:machine_core', T: 'next_ae:advanced_crafting_table'
  }, 'elite_crafting_table')

  // ultimate_crafting_table крафтиться В elite-столі (7x7, тип elite_crafting_shaped).
  ext('elite', 'next_ae:ultimate_crafting_table', 1, [
    'AWAWAWA',
    'WPCPCPW',
    'ACMHMCA',
    'WPHTHPW',
    'ACMHMCA',
    'WPCPCPW',
    'AWAWAWA'
  ], {
    A: 'draconicevolution:awakened_draconium_block', W: 'draconicevolution:wyvern_core',
    P: 'next_ae:parallel_processor', C: 'ae2:crafting_accelerator', M: 'next_ae:machine_core',
    H: 'draconicevolution:dragon_heart', T: 'next_ae:elite_crafting_table'
  }, 'ultimate_crafting_table')

  // ───────────────────────── ADVANCED (5x5) ─────────────────────────
  // AE2 256k cell component
  replace('ae2:cell_component_256k')
  ext('advanced', 'ae2:cell_component_256k', 1, [
    'FSPSF',
    'SCPCS',
    'PPMPP',
    'SCPCS',
    'FSPSF'
  ], {
    F: 'ae2:fluix_block', S: 'ae2:smooth_sky_stone_block', P: 'ae2:engineering_processor',
    C: 'ae2:cell_component_64k', M: 'next_ae:machine_core'
  }, 'ae2_cell_component_256k')

  // MEGA 1M cell component
  replace('megacells:cell_component_1m')
  ext('advanced', 'megacells:cell_component_1m', 1, [
    'DSDSD',
    'SCPCS',
    'DPMPD',
    'SCPCS',
    'DSDSD'
  ], {
    D: 'draconicevolution:draconium_block', S: 'ae2:smooth_sky_stone_block',
    C: 'ae2:cell_component_256k', P: 'ae2:engineering_processor', M: 'next_ae:machine_core'
  }, 'megacells_cell_component_1m')

  // Mekanism teleportation core
  replace('mekanism:teleportation_core')
  ext('advanced', 'mekanism:teleportation_core', 1, [
    'AOAOA',
    'ODGDO',
    'AGMGA',
    'ODGDO',
    'AOAOA'
  ], {
    A: 'mekanism:alloy_atomic', O: 'mekanism:alloy_reinforced', D: 'draconicevolution:draconium_ingot',
    G: 'next_ae:space_gem', M: 'next_ae:machine_core'
  }, 'mekanism_teleportation_core')

  // Draconic awakened core
  replace('draconicevolution:awakened_core')
  ext('advanced', 'draconicevolution:awakened_core', 1, [
    'WBWBW',
    'BIWIB',
    'WWMWW',
    'BIWIB',
    'WBWBW'
  ], {
    W: 'draconicevolution:awakened_draconium_ingot', B: 'draconicevolution:draconium_block',
    I: 'draconicevolution:wyvern_core', M: 'next_ae:machine_core'
  }, 'draconic_awakened_core')

  // ───────────────────────── ELITE (7x7) ─────────────────────────
  // MEGA 256M cell component
  replace('megacells:cell_component_256m')
  ext('elite', 'megacells:cell_component_256m', 1, [
    'AFCFCFA',
    'FMPGPMF',
    'CPSXSPC',
    'FGXMXGF',
    'CPSXSPC',
    'FMPGPMF',
    'AFCFCFA'
  ], {
    A: 'draconicevolution:awakened_draconium_block', F: 'ae2:fluix_block',
    C: 'megacells:cell_component_1m', M: 'next_ae:machine_core', P: 'next_ae:parallel_processor',
    G: 'next_ae:space_gem', S: 'ae2:smooth_sky_stone_block', X: 'ae2:cell_component_256k'
  }, 'megacells_cell_component_256m')

  // AE2 spatial 128 cell component
  replace('ae2:spatial_cell_component_128')
  ext('elite', 'ae2:spatial_cell_component_128', 1, [
    'FSFSFSF',
    'SPGPGPS',
    'FGXCXGF',
    'SPCMCPS',
    'FGXCXGF',
    'SPGPGPS',
    'FSFSFSF'
  ], {
    F: 'ae2:fluix_block', S: 'ae2:smooth_sky_stone_block', P: 'ae2:engineering_processor',
    G: 'next_ae:space_gem', X: 'ae2:spatial_cell_component_16', C: 'ae2:cell_component_256k',
    M: 'next_ae:machine_core'
  }, 'ae2_spatial_cell_component_128')

  // Mekanism supermassive QIO drive
  replace('mekanism:qio_drive_supermassive')
  ext('elite', 'mekanism:qio_drive_supermassive', 1, [
    'AOAOAOA',
    'ODQDQDO',
    'AQPGPQA',
    'ODGMGDO',
    'AQPGPQA',
    'ODQDQDO',
    'AOAOAOA'
  ], {
    A: 'mekanism:alloy_atomic', O: 'mekanism:alloy_reinforced', D: 'mekanism:hdpe_sheet',
    Q: 'mekanism:qio_drive_hyper_dense', P: 'next_ae:parallel_processor', G: 'next_ae:space_gem',
    M: 'next_ae:machine_core'
  }, 'mekanism_qio_drive_supermassive')

  // Draconic chaotic core
  replace('draconicevolution:chaotic_core')
  ext('elite', 'draconicevolution:chaotic_core', 1, [
    'WCWCWCW',
    'CAKAKAC',
    'WKHRHKW',
    'CARMRAC',
    'WKHRHKW',
    'CAKAKAC',
    'WCWCWCW'
  ], {
    W: 'draconicevolution:awakened_draconium_block', C: 'draconicevolution:awakened_core',
    A: 'draconicevolution:awakened_draconium_ingot', K: 'draconicevolution:wyvern_core',
    H: 'draconicevolution:dragon_heart', R: 'draconicevolution:chaos_shard', M: 'next_ae:machine_core'
  }, 'draconic_chaotic_core')

  // ───────────────────────── ULTIMATE (9x9) ─────────────────────────
  // ExtendedAE Infinity Cell
  replace('expatternprovider:infinity_cell')
  ext('ultimate', 'expatternprovider:infinity_cell', 1, [
    'FSFSFSFSF',
    'SPGPGPGPS',
    'FGXCXCXGF',
    'SPCMWMCPS',
    'FGXWHWXGF',
    'SPCMWMCPS',
    'FGXCXCXGF',
    'SPGPGPGPS',
    'FSFSFSFSF'
  ], {
    F: 'ae2:fluix_block', S: 'ae2:smooth_sky_stone_block', P: 'next_ae:parallel_processor',
    G: 'next_ae:space_gem', X: 'ae2:cell_component_256k', C: 'megacells:cell_component_1m',
    M: 'next_ae:machine_core', W: 'draconicevolution:awakened_draconium_block',
    H: 'draconicevolution:dragon_heart'
  }, 'extendedae_infinity_cell')

  // MEGA crafting unit
  replace('megacells:mega_crafting_unit')
  ext('ultimate', 'megacells:mega_crafting_unit', 1, [
    'FAFAFAFAF',
    'APGPGPGPA',
    'FGMUMUMGF',
    'APUSWSUPA',
    'FGMWHWMGF',
    'APUSWSUPA',
    'FGMUMUMGF',
    'APGPGPGPA',
    'FAFAFAFAF'
  ], {
    F: 'ae2:fluix_block', A: 'draconicevolution:awakened_draconium_block',
    P: 'next_ae:parallel_processor', G: 'next_ae:space_gem', M: 'next_ae:machine_core',
    U: 'ae2:crafting_accelerator', S: 'ae2:smooth_sky_stone_block',
    W: 'megacells:mega_crafting_accelerator', H: 'draconicevolution:dragon_heart'
  }, 'megacells_mega_crafting_unit')

  // Mekanism antimatter pellet
  replace('mekanism:pellet_antimatter')
  ext('ultimate', 'mekanism:pellet_antimatter', 1, [
    'AOAOAOAOA',
    'ODQDQDQDO',
    'AQGPGPGQA',
    'ODPHWHPDO',
    'AQGWMWGQA',
    'ODPHWHPDO',
    'AQGPGPGQA',
    'ODQDQDQDO',
    'AOAOAOAOA'
  ], {
    A: 'mekanism:alloy_atomic', O: 'mekanism:alloy_reinforced', D: 'mekanism:hdpe_sheet',
    Q: 'mekanism:pellet_plutonium', G: 'next_ae:space_gem', P: 'next_ae:parallel_processor',
    H: 'draconicevolution:dragon_heart', W: 'draconicevolution:awakened_draconium_block',
    M: 'next_ae:machine_core'
  }, 'mekanism_pellet_antimatter')

  // Draconic chaotic energy core
  replace('draconicevolution:chaotic_energy_core')
  ext('ultimate', 'draconicevolution:chaotic_energy_core', 1, [
    'WCWCWCWCW',
    'CAKAKAKAC',
    'WKHRHRHKW',
    'CARZRZRAC',
    'WKHZMZHKW',
    'CARZRZRAC',
    'WKHRHRHKW',
    'CAKAKAKAC',
    'WCWCWCWCW'
  ], {
    W: 'draconicevolution:awakened_draconium_block', C: 'draconicevolution:chaotic_core',
    A: 'draconicevolution:awakened_draconium_ingot', K: 'draconicevolution:awakened_core',
    H: 'draconicevolution:dragon_heart', R: 'draconicevolution:chaos_shard',
    Z: 'draconicevolution:draconium_block', M: 'next_ae:machine_core'
  }, 'draconic_chaotic_energy_core')

  // next_ae безлімітні комірки — тільки тут, на 9x9 (їх 3x3-рецепти прибрано з 02-скрипта).
  ext('ultimate', 'next_ae:unlimited_item_storage_cell', 1, [
    'AFAFAFAFA',
    'FPGPGPGPF',
    'AGXCXCXGA',
    'FPCMWMCPF',
    'AGXWHWXGA',
    'FPCMWMCPF',
    'AGXCXCXGA',
    'FPGPGPGPF',
    'AFAFAFAFA'
  ], {
    A: 'draconicevolution:awakened_draconium_ingot', F: 'ae2:fluix_block',
    P: 'next_ae:parallel_processor', G: 'next_ae:space_gem', X: 'ae2:cell_component_256k',
    C: 'ae2:item_storage_cell_256k', M: 'next_ae:machine_core',
    W: 'draconicevolution:awakened_draconium_block', H: 'draconicevolution:dragon_heart'
  }, 'unlimited_item_storage_cell')

  ext('ultimate', 'next_ae:unlimited_fluid_storage_cell', 1, [
    'AFAFAFAFA',
    'FPGPGPGPF',
    'AGXCXCXGA',
    'FPCMWMCPF',
    'AGXWHWXGA',
    'FPCMWMCPF',
    'AGXCXCXGA',
    'FPGPGPGPF',
    'AFAFAFAFA'
  ], {
    A: 'draconicevolution:awakened_draconium_ingot', F: 'ae2:fluix_block',
    P: 'next_ae:parallel_processor', G: 'next_ae:space_gem', X: 'ae2:cell_component_256k',
    C: 'ae2:fluid_storage_cell_256k', M: 'next_ae:machine_core',
    W: 'draconicevolution:awakened_draconium_block', H: 'draconicevolution:dragon_heart'
  }, 'unlimited_fluid_storage_cell')
})
