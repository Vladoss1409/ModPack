ServerEvents.recipes(event => {
  event.remove({ output: 'irons_spellbooks:arcane_essence' })

  event.shaped('kubejs:expedition_journal', [
    'BPB',
    'PJP',
    'BPB'
  ], {
    B: 'minecraft:book',
    P: 'minecraft:paper',
    J: 'minecraft:writable_book'
  })

  event.shaped('4x irons_spellbooks:arcane_essence', [
    'LRL',
    'RGR',
    'LRL'
  ], {
    L: 'minecraft:lapis_lazuli',
    R: 'minecraft:redstone',
    G: 'minecraft:glowstone_dust'
  }).id('cooptech:arcane_essence_craft')

  event.shaped('kubejs:decrypted_cave_codex', [
    'PTP',
    'TBT',
    'PLP'
  ], {
    P: 'minecraft:paper',
    T: 'alexscaves:cave_tablet',
    B: 'minecraft:book',
    L: 'minecraft:lapis_lazuli'
  })

  event.shaped('kubejs:resonance_beacon', [
    'ECE',
    'CNC',
    'ERE'
  ], {
    E: 'minecraft:ender_pearl',
    C: 'explorerscompass:explorerscompass',
    N: 'minecraft:nether_star',
    R: 'minecraft:redstone_block'
  })

  for (var i = 1; i <= 12; i++) {
    var n = String(i).padStart(2, '0')
    event.shapeless('kubejs:stabilized_shard_' + n, [
      `kubejs:anchor_shard_${n}`,
      '2x minecraft:iron_ingot',
      'minecraft:gold_ingot',
      'minecraft:redstone'
    ]).id('cooptech:stabilized_shard_' + n)
  }

  event.shaped('kubejs:reality_anchor_core', [
    'SAS',
    'ACA',
    'SAS'
  ], {
    S: 'kubejs:stabilized_shard_12',
    A: 'kubejs:anchor_shard_12',
    C: 'minecraft:nether_star'
  }).id('cooptech:reality_anchor_core')
})
