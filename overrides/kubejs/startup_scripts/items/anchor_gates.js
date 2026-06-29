// Якорные гейт-предметы — жёсткие рубежи прогрессии T0→T5.
// Каждый предмет открывает крафт стартового «чокпоинта» следующего тира
// (универсальной базы, без которой весь тир не собрать).
// Рецепты предметов и переопределение чокпоинтов: server_scripts/recipes/04_anchor_gates.js

StartupEvents.registry('item', event => {
  const gates = [
    ['anchor_spark', 'Якорная искра §8(T0→T1)',
      '§eОткрывает: Thermal — Машинная рама', '§7База всех машин Thermal.'],
    ['anchor_cell', 'Якорная ячейка §8(T1→T2)',
      '§eОткрывает: Mekanism — Стальной корпус', '§7База всех машин Mekanism.'],
    ['anchor_matrix', 'Якорная матрица §8(T2→T3)',
      '§eОткрывает: AE2 — Гравёр + ProjectE (EMC)', '§7Процессоры, ME-сеть и трансмутация.'],
    ['anchor_singularity', 'Якорная сингулярность §8(T3→T4)',
      '§eОткрывает: Draconic — Ядро дракония', '§7База всей ветки Draconic Evolution.'],
    ['anchor_nexus', 'Якорный нексус §8(T4→T5)',
      '§eОткрывает: next_ae — Ядро машины', '§7База ультра-эндгейма next_ae.']
  ]

  gates.forEach(g => {
    event.create(g[0])
      .displayName(g[1])
      .maxStackSize(16)
      .glow(true)
      .tooltip(g[2])
      .tooltip(g[3])
      .tooltip('§8Стабилизированный рубеж Якоря реальности.')
  })
})
