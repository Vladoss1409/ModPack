# Auto-deploy camp (datapack surface scan)
data remove storage cooptech_world:config camp_built
tellraw @a [{"text":"[CoopTech] ","color":"light_purple"},{"text":"Building expedition camp...","color":"white"}]
function cooptech_world:camp/find_surface_build
data merge storage cooptech_world:config {camp_built:1b}
tellraw @a [{"text":"[CoopTech] ","color":"light_purple"},{"text":"Camp ready.","color":"green"}]
