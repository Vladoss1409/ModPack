# Center column surface only (not max of hill — avoids sky platform)
scoreboard objectives add cooptech.y dummy
scoreboard objectives add cooptech.max dummy
scoreboard players set $max cooptech.max -64

execute positioned ~ ~ ~ run function cooptech_world:camp/surface_probe

kill @e[type=marker,tag=cooptech_surface_temp]
summon marker ~ ~ ~ {Tags:["cooptech_surface_temp"],Marker:1b,Invisible:1b}
execute as @e[type=marker,tag=cooptech_surface_temp,limit=1] store result entity @s Pos[1] double 1 run scoreboard players get $max cooptech.max
execute as @e[type=marker,tag=cooptech_surface_temp,limit=1] at @s run function cooptech_world:camp/wipe
execute as @e[type=marker,tag=cooptech_surface_temp,limit=1] at @s run function cooptech_world:camp/flatten
execute as @e[type=marker,tag=cooptech_surface_temp,limit=1] at @s run function cooptech_world:camp/build
execute as @e[type=marker,tag=cooptech_surface_temp,limit=1] at @s run setworldspawn ~ ~1 ~
kill @e[type=marker,tag=cooptech_surface_temp]

tellraw @a [{"text":"[CoopTech] ","color":"light_purple"},{"text":"Floor Y=","color":"green"},{"score":{"name":"$max","objective":"cooptech.max"},"color":"yellow"}]
