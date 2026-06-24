# CoopTech — лагерь экспедиции. Встаньте на землю в центре лагеря, OP.
tellraw @s [{"text":"[CoopTech] ","color":"light_purple"},{"text":"Строю лагерь экспедиции…","color":"white"}]
execute anchored feet run function cooptech:camp/clear_markers

# Площадка (ноги = ~ ~ ~, пол = ~-1)
fill ~-7 ~-2 ~-7 ~7 ~-2 ~7 minecraft:cobblestone
fill ~-6 ~-2 ~-6 ~6 ~-2 ~6 minecraft:mossy_cobblestone
fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 minecraft:podzol
fill ~-6 ~ ~-6 ~6 ~4 ~6 minecraft:air replace minecraft:grass
fill ~-6 ~ ~-6 ~6 ~4 ~6 minecraft:air replace minecraft:tall_grass
fill ~-6 ~ ~-6 ~6 ~4 ~6 minecraft:air replace minecraft:grass_block
fill ~-6 ~ ~-6 ~6 ~4 ~6 minecraft:air replace minecraft:fern
fill ~-6 ~ ~-6 ~6 ~4 ~6 minecraft:air replace minecraft:large_fern

# Костёр и посадка
setblock ~ ~-1 ~ minecraft:campfire[lit=true]
setblock ~1 ~-1 ~ minecraft:spruce_trapdoor[facing=south,half=bottom,open=true]
setblock ~-1 ~-1 ~ minecraft:spruce_trapdoor[facing=south,half=bottom,open=true]
setblock ~ ~-1 ~1 minecraft:spruce_trapdoor[facing=north,half=bottom,open=true]

# Фонари
setblock ~-5 ~-1 ~-5 minecraft:spruce_fence
setblock ~-5 ~ ~-5 minecraft:lantern[hanging=true]
setblock ~5 ~-1 ~-5 minecraft:spruce_fence
setblock ~5 ~ ~-5 minecraft:lantern[hanging=true]
setblock ~-5 ~-1 ~5 minecraft:spruce_fence
setblock ~-5 ~ ~5 minecraft:lantern[hanging=true]
setblock ~5 ~-1 ~5 minecraft:spruce_fence
setblock ~5 ~ ~5 minecraft:lantern[hanging=true]

# Баннеры
setblock ~-5 ~-1 ~ minecraft:purple_banner[rotation=8]
setblock ~5 ~-1 ~ minecraft:purple_banner[rotation=0]
setblock ~ ~-1 ~-5 minecraft:purple_banner[rotation=12]

# Указатель к разлому (122, 90, -102)
setblock ~6 ~-1 ~-4 minecraft:oak_sign[rotation=10]{Text1:'{"text":"⇗ Разлом якоря","color":"gold","bold":true}',Text2:'{"text":"~160 блоков","color":"gray"}',Text3:'{"text":"122 / 90 / -102","color":"dark_gray"}'}

# Тропа северо-восток
fill ~3 ~-2 ~-3 ~10 ~-2 ~-10 minecraft:gravel
fill ~4 ~-2 ~-4 ~9 ~-2 ~-9 minecraft:coarse_dirt
setblock ~8 ~-2 ~-8 minecraft:spruce_pressure_plate

# Навесы-палатки
fill ~3 ~1 ~-6 ~6 ~1 ~-4 minecraft:purple_wool
setblock ~3 ~-1 ~-6 minecraft:spruce_fence
setblock ~6 ~-1 ~-6 minecraft:spruce_fence
setblock ~3 ~-1 ~-4 minecraft:spruce_fence
setblock ~6 ~-1 ~-4 minecraft:spruce_fence
fill ~-6 ~1 ~3 ~-4 ~1 ~6 minecraft:gray_wool
setblock ~-6 ~-1 ~3 minecraft:spruce_fence
setblock ~-4 ~-1 ~3 minecraft:spruce_fence
setblock ~-6 ~-1 ~6 minecraft:spruce_fence
setblock ~-4 ~-1 ~6 minecraft:spruce_fence

# Сундук
setblock ~-3 ~-1 ~3 minecraft:chest[facing=south]

execute anchored feet run function cooptech:camp/markers
execute anchored feet run setworldspawn ~ ~ ~

tellraw @s [{"text":"[CoopTech] ","color":"light_purple"},{"text":"Лагерь готов. NPC — на цветных маркерах.","color":"green"}]
tellraw @s [{"text":"CNPC команда диспетчера: ","color":"gray"},{"text":"ftbquests change_progress @dp complete T101000000000021","color":"yellow"}]
