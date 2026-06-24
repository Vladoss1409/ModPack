scoreboard objectives add cooptech.const dummy
execute store success score #camp cooptech.const run data get storage cooptech_world:config camp_built
execute unless score #camp cooptech.const matches 1 run function cooptech_world:camp/deploy
