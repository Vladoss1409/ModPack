// CoopTech — эксклюзивные ветки на волну (тег branch_exclusive).
// Первый игрок, открывший квест, «забирает» его; напарнику показываем предупреждение.
// Прогресс FTB Teams по-прежнему общий: кто первый сдал — закрыл квест для команды.

var EXCLUSIVE_TAG = 'branch_exclusive'
var CLAIMS_KEY = 'cooptech_exclusive_claims'

function parseClaims(level) {
  var data = level.persistentData
  if (!data.contains(CLAIMS_KEY)) {
    return {}
  }
  try {
    return JSON.parse(data.getString(CLAIMS_KEY))
  } catch (e) {
    return {}
  }
}

function saveClaims(level, claims) {
  level.persistentData.putString(CLAIMS_KEY, JSON.stringify(claims))
}

function teamKey(player) {
  try {
    var questFile = global.cooptechGetQuestFile ? global.cooptechGetQuestFile(player) : null
    if (!questFile) return String(player.uuid)
    var teamData = questFile.getOrCreateTeamData(player)
    return String(teamData.getTeamId())
  } catch (e) {
    return String(player.uuid)
  }
}

function questHasTag(event, tag) {
  try {
    var quest = event.quest || event.getQuest()
    if (!quest || !quest.tags) return false
    var it = quest.tags.iterator()
    while (it.hasNext()) {
      if (String(it.next()) === tag) return true
    }
  } catch (e2) { /* optional */ }
  return false
}

function registerExclusiveQuests() {
  if (typeof FTBQuestsEvents === 'undefined') {
    console.warn('[CoopTech] FTBQuestsEvents missing — exclusive branch quests disabled')
    return
  }

  FTBQuestsEvents.started(EXCLUSIVE_TAG, function (event) {
    var player = event.player
    if (!player || !questHasTag(event, EXCLUSIVE_TAG)) return

    var quest = event.quest || event.getQuest()
    if (!quest) return
    var questId = String(quest.id)
    var level = player.level
    var claims = parseClaims(level)
    var tKey = teamKey(player)
    if (!claims[tKey]) claims[tKey] = {}

    var owner = claims[tKey][questId]
    var myId = String(player.uuid)
    if (!owner) {
      claims[tKey][questId] = myId
      saveClaims(level, claims)
      player.tell('§d[Кооп] §fВы взяли §e«' + quest.title.getString() + '§f». Напарник не сможет закрыть этот квест сам.')
      return
    }
    if (owner !== myId) {
      player.tell('§d[Кооп] §cЭтот квест уже ведёт напарник. Выберите другую ветку из четырёх.')
    }
  })

  FTBQuestsEvents.completed(EXCLUSIVE_TAG, function (event) {
    var player = event.player
    if (!player || !questHasTag(event, EXCLUSIVE_TAG)) return
    var quest = event.quest || event.getQuest()
    if (!quest) return
    var questId = String(quest.id)
    var level = player.level
    var claims = parseClaims(level)
    var tKey = teamKey(player)
    if (claims[tKey]) {
      delete claims[tKey][questId]
      saveClaims(level, claims)
    }
    player.server.runCommandSilent('tellraw @a ["",{"text":"[Кооп] ","color":"light_purple"},{"text":"' + player.name.getString() + '","color":"gold"},{"text":" закрыл эксклюзивную ветку: ","color":"white"},{"text":"' + quest.title.getString() + '","color":"yellow"}]')
  })

  console.info('[CoopTech] Exclusive branch quest claims registered (tag: ' + EXCLUSIVE_TAG + ')')
}

registerExclusiveQuests()
