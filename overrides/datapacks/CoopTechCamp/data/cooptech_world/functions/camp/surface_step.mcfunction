execute if block ~ ~ ~ #minecraft:replaceable if score $y cooptech.y matches -64..319 run scoreboard players remove $y cooptech.y 1
execute if block ~ ~ ~ #minecraft:replaceable if score $y cooptech.y matches -64..319 positioned ~ ~-1 ~ run function cooptech_world:camp/surface_step
execute unless block ~ ~ ~ #minecraft:replaceable run scoreboard players operation $max cooptech.max > $y cooptech.y
