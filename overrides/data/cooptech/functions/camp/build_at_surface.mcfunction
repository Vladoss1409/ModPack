# Find motion_blocking surface at current X/Z (call: execute positioned X 0 Z run function ...)
scoreboard objectives add cooptech.const dummy
summon marker ~ ~ ~ {Tags:["cooptech_camp_probe"],Marker:1b,Invisible:1b}
execute as @e[type=marker,tag=cooptech_camp_probe,limit=1,sort=nearest] store result entity @s Pos[1] double 1 run heightmap motion.blocking
execute as @e[type=marker,tag=cooptech_camp_probe,limit=1] at @s positioned ~ ~ ~ run function cooptech:camp/build
kill @e[type=marker,tag=cooptech_camp_probe,distance=..128]
