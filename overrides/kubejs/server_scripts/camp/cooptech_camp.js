// Camp build with hillside surface scan (Forge 1.20.1 / KubeJS 2001)
const CAMP_X = -60
const CAMP_Z = 97
const CAMP_RADIUS = 7
const LEGACY_ANCHORS = [[-60, 92, 97], [-60, 94, 97]]

const Component = Java.loadClass('net.minecraft.network.chat.Component')
const HeightmapTypes = Java.loadClass('net.minecraft.world.level.levelgen.Heightmap$Types')

function campMessage(source, text) {
  source.sendSystemMessage(Component.literal('[CoopTech] ' + text))
}

function scanFloorY(level) {
  const h = level.getHeight(HeightmapTypes.MOTION_BLOCKING, CAMP_X, CAMP_Z)
  return h - 1
}

function campBuild(source) {
  const level = source.getLevel()
  const server = source.getServer()
  const floorY = scanFloorY(level)

  campMessage(source, 'Surface scan: building floor at Y=' + floorY)

  for (const anchor of LEGACY_ANCHORS) {
    server.runCommandSilent('execute positioned ' + anchor[0] + ' ' + anchor[1] + ' ' + anchor[2] + ' run function cooptech_world:camp/wipe')
  }
  server.runCommandSilent('execute positioned ' + CAMP_X + ' ' + floorY + ' ' + CAMP_Z + ' run function cooptech_world:camp/wipe')
  server.runCommandSilent('execute positioned ' + CAMP_X + ' ' + floorY + ' ' + CAMP_Z + ' run function cooptech_world:camp/flatten')
  server.runCommandSilent('execute positioned ' + CAMP_X + ' ' + floorY + ' ' + CAMP_Z + ' run function cooptech_world:camp/build')
  server.runCommandSilent('setworldspawn ' + CAMP_X + ' ' + (floorY + 1) + ' ' + CAMP_Z)

  campMessage(source, 'Camp ready at ' + CAMP_X + ' ' + floorY + ' ' + CAMP_Z)
}

function campForce(source) {
  const server = source.getServer()
  server.runCommandSilent('data remove storage cooptech_world:config camp_built')
  campBuild(source)
  server.runCommandSilent('data merge storage cooptech_world:config {camp_built:1b}')
}

ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event
  event.register(
    Commands.literal('cooptech')
      .requires(src => src.hasPermission(2))
      .then(
        Commands.literal('camp')
          .then(Commands.literal('build').executes(ctx => { campBuild(ctx.source); return 1 }))
          .then(Commands.literal('force').executes(ctx => { campForce(ctx.source); return 1 }))
      )
  )
})

console.info('CoopTech camp commands: /cooptech camp build | force')
