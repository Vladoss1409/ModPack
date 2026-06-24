# Decorations on podzol floor (~ = walkable surface)
tellraw @a [{"text":"[CoopTech] ","color":"light_purple"},{"text":"Placing camp props...","color":"white"}]
function cooptech_world:camp/clear_markers

setblock ~ ~1 ~ minecraft:campfire[lit=true]
setblock ~1 ~1 ~ minecraft:spruce_trapdoor[facing=south,half=bottom,open=true]
setblock ~-1 ~1 ~ minecraft:spruce_trapdoor[facing=south,half=bottom,open=true]
setblock ~ ~1 ~1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=true]

setblock ~-5 ~1 ~-5 minecraft:spruce_fence
setblock ~-5 ~2 ~-5 minecraft:lantern[hanging=true]
setblock ~5 ~1 ~-5 minecraft:spruce_fence
setblock ~5 ~2 ~-5 minecraft:lantern[hanging=true]
setblock ~-5 ~1 ~5 minecraft:spruce_fence
setblock ~-5 ~2 ~5 minecraft:lantern[hanging=true]
setblock ~5 ~1 ~5 minecraft:spruce_fence
setblock ~5 ~2 ~5 minecraft:lantern[hanging=true]

setblock ~-5 ~1 ~ minecraft:purple_banner[rotation=8]
setblock ~5 ~1 ~ minecraft:purple_banner[rotation=0]
setblock ~ ~1 ~-5 minecraft:purple_banner[rotation=12]

setblock ~6 ~1 ~-4 minecraft:oak_sign[rotation=10]{Text1:'{"text":"Yellowstone POI","color":"gold"}',Text2:'{"text":"/locate biome","color":"gray"}'}

fill ~3 ~1 ~-3 ~10 ~1 ~-10 minecraft:gravel
fill ~4 ~1 ~-4 ~9 ~1 ~-9 minecraft:coarse_dirt

# Purple tent (Dispatcher) — pillars ~1..~4, frame ~4, roof ~5
fill ~3 ~1 ~-6 ~3 ~4 ~-6 minecraft:spruce_fence
fill ~6 ~1 ~-6 ~6 ~4 ~-6 minecraft:spruce_fence
fill ~3 ~1 ~-4 ~3 ~4 ~-4 minecraft:spruce_fence
fill ~6 ~1 ~-4 ~6 ~4 ~-4 minecraft:spruce_fence
fill ~3 ~4 ~-6 ~6 ~4 ~-6 minecraft:spruce_fence
fill ~3 ~4 ~-4 ~6 ~4 ~-4 minecraft:spruce_fence
fill ~3 ~4 ~-6 ~3 ~4 ~-4 minecraft:spruce_fence
fill ~6 ~4 ~-6 ~6 ~4 ~-4 minecraft:spruce_fence
fill ~3 ~5 ~-6 ~6 ~5 ~-4 minecraft:purple_wool

# Gray tent — fence pillars + frame
fill ~-6 ~1 ~3 ~-6 ~3 ~3 minecraft:spruce_fence
fill ~-4 ~1 ~3 ~-4 ~3 ~3 minecraft:spruce_fence
fill ~-6 ~1 ~6 ~-6 ~3 ~6 minecraft:spruce_fence
fill ~-4 ~1 ~6 ~-4 ~3 ~6 minecraft:spruce_fence
fill ~-6 ~3 ~3 ~-4 ~3 ~3 minecraft:spruce_fence
fill ~-6 ~3 ~6 ~-4 ~3 ~6 minecraft:spruce_fence
fill ~-6 ~3 ~3 ~-6 ~3 ~6 minecraft:spruce_fence
fill ~-4 ~3 ~3 ~-4 ~3 ~6 minecraft:spruce_fence
fill ~-6 ~4 ~3 ~-4 ~4 ~6 minecraft:gray_wool

setblock ~-3 ~1 ~3 minecraft:chest[facing=south]

setworldspawn ~ ~1 ~

tellraw @a [{"text":"[CoopTech] ","color":"light_purple"},{"text":"Camp props placed on floor.","color":"green"}]
