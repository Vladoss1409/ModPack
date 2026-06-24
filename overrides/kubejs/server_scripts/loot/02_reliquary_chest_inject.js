LootJS.modifiers(event => {
  const inject = (pattern, item, chance) => {
    event.addLootTableModifier(pattern).addLoot(item).randomChance(chance)
  }

  inject(/minecraft:chests\/.*dungeon.*/, 'kubejs:reliquary_field', 0.05)
  inject(/minecraft:chests\/.*mineshaft.*/, 'kubejs:reliquary_field', 0.04)
  inject(/minecraft:chests\/.*stronghold.*/, 'kubejs:reliquary_resonant', 0.06)
  inject(/minecraft:chests\/.*nether.*/, 'kubejs:reliquary_resonant', 0.05)
  inject(/minecraft:chests\/.*end.*/, 'kubejs:reliquary_primordial', 0.04)
})

console.info('CoopTech: reliquary chest injection loaded')
