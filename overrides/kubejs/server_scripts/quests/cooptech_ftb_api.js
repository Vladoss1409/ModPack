// Shared FTB Quests API helpers (FTB Quests 2001.x uses api package).
var FTB_QUESTS_API = 'dev.ftb.mods.ftbquests.api.FTBQuestsAPI'

global.cooptechGetQuestFile = function (player) {
  if (!player) return null
  try {
    var API = Java.loadClass(FTB_QUESTS_API)
    return API.api().getQuestFile(player.serverLevel())
  } catch (e) {
    return null
  }
}

global.cooptechGetTeamData = function (player) {
  var questFile = global.cooptechGetQuestFile(player)
  if (!questFile) return null
  try {
    return questFile.getOrCreateTeamData(player)
  } catch (e) {
    return null
  }
}
