// Якорные рубежи — ЖЁСТКИЙ гейтинг прогрессии T0→T5.
//
// Механика (две части на каждый переход):
//   1) Gate-предмет (kubejs:anchor_*) крафтится ТОЛЬКО из сигнатурных выходов
//      предыдущего тира → нельзя получить, не освоив прошлый тир.
//   2) Рецепт «чокпоинта» следующего тира (универсальной базы) переопределяется
//      так, чтобы требовать соответствующий gate-предмет.
//
// Чокпоинты тиров (универсальные базы — без них весь тир не собрать):
//   T1  thermal:machine_frame            (база всех машин Thermal)
//   T2  mekanism:steel_casing            (база всех машин Mekanism)
//   T3  ae2:inscriber + projecte:philosophers_stone (процессоры AE2 + вся EMC)
//   T4  draconicevolution:draconium_core (база всей Draconic Evolution)
//   T5  next_ae:machine_core             (база ультра-эндгейма next_ae)
//
// ID всех предметов/блоков сверены по реальным jar'ам пака (2026-06-29).

ServerEvents.recipes(event => {
  const A = {
    spark: 'kubejs:anchor_spark',
    cell: 'kubejs:anchor_cell',
    matrix: 'kubejs:anchor_matrix',
    singularity: 'kubejs:anchor_singularity',
    nexus: 'kubejs:anchor_nexus'
  }

  const shaped = (result, pattern, keys, rid) =>
    event.shaped(result, pattern, keys).id('cooptech:gate/' + rid)

  // ───────────────────── 1. Рецепты gate-предметов (цепочка тиров) ─────────────────────

  // T0 → T1: только ванилла + Iron Furnace (T0).
  shaped(A.spark, [
    ' R ',
    'IFI',
    ' L '
  ], {
    R: 'minecraft:redstone',
    I: 'minecraft:iron_ingot',
    F: 'ironfurnaces:iron_furnace',
    L: 'minecraft:flint'
  }, 'anchor_spark')

  // T1 → T2: сигнатурные выходы Thermal (rf_coil, machine_frame) + прошлый рубеж.
  shaped(A.cell, [
    'PRP',
    'FAF',
    'PRP'
  ], {
    P: 'thermal:rf_coil',
    R: 'minecraft:redstone_block',
    F: 'thermal:machine_frame',
    A: A.spark
  }, 'anchor_cell')

  // T2 → T3: выходы Mekanism + Ender IO + прошлый рубеж.
  shaped(A.matrix, [
    'VCV',
    'SAS',
    'VCV'
  ], {
    V: 'enderio:vibrant_alloy_ingot',
    C: 'mekanism:advanced_control_circuit',
    S: 'mekanism:steel_casing',
    A: A.cell
  }, 'anchor_matrix')

  // T3 → T4: выходы AE2 + EMC (ProjectE) + прошлый рубеж.
  shaped(A.singularity, [
    'EFE',
    'FAF',
    'EPE'
  ], {
    E: 'ae2:engineering_processor',
    F: 'ae2:fluix_crystal',
    A: A.matrix,
    P: 'projecte:transmutation_table'
  }, 'anchor_singularity')

  // T4 → T5: эндгейм-выходы Draconic + Ender IO + прошлый рубеж.
  shaped(A.nexus, [
    'GBG',
    'HAH',
    'GCG'
  ], {
    G: 'enderio:grains_of_infinity',
    B: 'draconicevolution:awakened_draconium_block',
    H: 'draconicevolution:dragon_heart',
    C: 'draconicevolution:chaos_shard',
    A: A.singularity
  }, 'anchor_nexus')

  // ───────────────────── 2. Переопределение чокпоинтов тиров ─────────────────────

  // T1 — Thermal: Машинная рама требует Якорную искру.
  event.remove({ id: 'thermal:machine_frame' })
  shaped('thermal:machine_frame', [
    'III',
    'RAR',
    'III'
  ], { I: 'minecraft:iron_ingot', R: 'minecraft:redstone', A: A.spark }, 'lock_machine_frame')

  // T2 — Mekanism: Стальной корпус требует Якорную ячейку.
  event.remove({ id: 'mekanism:steel_casing' })
  shaped('mekanism:steel_casing', [
    'RIR',
    'IAI',
    'RIR'
  ], { R: 'minecraft:redstone', I: 'minecraft:iron_block', A: A.cell }, 'lock_steel_casing')

  // T3 — AE2: Гравёр требует Якорную матрицу (без него нет процессоров → нет ME-сети).
  event.remove({ id: 'ae2:network/blocks/inscribers' })
  shaped('ae2:inscriber', [
    'III',
    'PAP',
    'III'
  ], { I: 'minecraft:iron_block', P: 'minecraft:piston', A: A.matrix }, 'lock_inscriber')

  // T3 — ProjectE: Камень философов требует Якорную матрицу (привязка EMC к T3).
  // Это запирает ВСЮ EMC-экономику (трансмутация/конденсатор/Кляйн) до T3.
  event.remove({ id: 'projecte:philosophers_stone' })
  event.remove({ id: 'projecte:philosophers_stone_alt' })
  shaped('projecte:philosophers_stone', [
    'GRG',
    'RAR',
    'GRG'
  ], { G: 'minecraft:glowstone_dust', R: 'minecraft:redstone', A: A.matrix }, 'lock_philosophers_stone')

  // T4 — Draconic: Ядро дракония требует Якорную сингулярность (база всей ветки).
  event.remove({ id: 'draconicevolution:components/draconium_core' })
  shaped('draconicevolution:draconium_core', [
    'DDD',
    'DAD',
    'DDD'
  ], { D: 'draconicevolution:draconium_ingot', A: A.singularity }, 'lock_draconium_core')

  // T5 — next_ae: Ядро машины требует Якорный нексус.
  // Удаляем рецепт из 02_next_ae_recipes.js (id next_ae:craft/machine_core) и пересобираем с гейтом.
  event.remove({ id: 'next_ae:craft/machine_core' })
  shaped('next_ae:machine_core', [
    'VEV',
    'DND',
    'VEV'
  ], {
    V: 'enderio:vibrant_alloy_ingot',
    E: 'ae2:engineering_processor',
    D: 'draconicevolution:draconium_core',
    N: A.nexus
  }, 'lock_machine_core')
})
