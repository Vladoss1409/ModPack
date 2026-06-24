# Rebuild camp at center surface (single wipe at detected floor only)
tellraw @a [{"text":"[CoopTech] ","color":"light_purple"},{"text":"Scanning camp center...","color":"white"}]
execute positioned -60 0 97 run function cooptech_world:camp/surface_scan
