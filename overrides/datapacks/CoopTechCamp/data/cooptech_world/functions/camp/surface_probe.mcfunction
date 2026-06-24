# Find top solid block Y at current column; update global max.
scoreboard players set $y cooptech.y 319
execute positioned ~ 319 ~ run function cooptech_world:camp/surface_step
