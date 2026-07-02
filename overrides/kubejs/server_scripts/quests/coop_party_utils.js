// CoopTech — пара у маяка и предупреждение про FTB party.

var PAIR_KEY_PREFIX = 'cooptech_pair_'

global.cooptechRegisterPair = function (level, uuidA, uuidB) {
  var data = level.persistentData
  data.putString(PAIR_KEY_PREFIX + uuidA, uuidB)
  data.putString(PAIR_KEY_PREFIX + uuidB, uuidA)
}

PlayerEvents.loggedIn(function (event) {
  var player = event.player
  if (!player || player.level.isClientSide()) return

  try {
    var TeamsAPI = Java.loadClass('dev.ftb.ftbteams.api.FTBTeamsAPI')
    var team = TeamsAPI.api().getManager().getTeamForPlayer(player)
    if (team && team.getMembers().size() > 1) {
      player.tell('§c[CoopTech] §fВы в §eFTB party§f — прогресс квестов общий на всех.')
      player.tell('§7Для CoopTech: §eне объединяйтесь в party§7. Играйте вдвоём без общей FTB-команды.')
    }
  } catch (e) { /* optional */ }
})
