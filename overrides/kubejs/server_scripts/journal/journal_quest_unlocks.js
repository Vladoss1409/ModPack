// Разблокировка записей Patchouli-журнала по завершению квестов FTB Quests.
// Требует FTB XMod Compat (KubeJS + FTB Quests).

var JOURNAL_UNLOCKS = {
  A001000000000001: {
    adv: 'welcome',
    msg: 'Новая запись: «Добро пожаловать в экспедицию».'
  },
  A001000000000008: {
    adv: 'welcome_done',
    msg: 'Вступление завершено — откройте Гайды и Главу 1.'
  },
  A002000000000010: {
    adv: 'guides_done',
    msg: 'Путеводитель прочитан — справка в журнале.'
  },
  A101000000000001: {
    adv: 'start',
    msg: 'Новые записи: лагерь, маяк, реликварии.'
  },
  A101000000000007: {
    adv: 'rubeg_1',
    msg: 'Рубеж I — запись о наставнике и Волне 2.'
  },
  A101000000000010: {
    adv: 'wave_2',
    msg: 'Приказ на Волну 2 — компас руин и кооп-синхрон.'
  },
  A101000000000015: {
    adv: 'rubeg_2',
    msg: 'Рубеж II — запись об Якоре реальности.'
  },
  A101000000000016: {
    adv: 'dispatcher_briefing',
    msg: 'Приказ диспетчера — запись в хронике.'
  },
  A101000000000009: {
    adv: 'prologue_finale',
    msg: 'Prologue завершён — мост к Главе I.'
  },
  A201000000000005: {
    adv: 'ch1_gate',
    msg: 'Глава I — инфраструктура и Thermal.'
  },
  A201000000000006: {
    adv: 'ch1_finale',
    msg: 'Финал Главы I — подготовка к Поверхности.'
  },
  A301000000000005: {
    adv: 'ch2_gate',
    msg: 'Глава II — компас, руины, Terralith.'
  },
  A301000000000006: {
    adv: 'ch2_finale',
    msg: 'Финал Главы II — переход к Потоку.'
  },
  A401000000000005: {
    adv: 'ch3_gate',
    msg: 'Глава III — RF, Thermal, Powah, IE.'
  },
  A401000000000006: {
    adv: 'ch3_finale',
    msg: 'Финал Главы III — стабильный поток.'
  },
  A501000000000034: {
    adv: 'ch4_gate',
    msg: 'Глава IV — рубеж Production.'
  },
  A501000000000035: {
    adv: 'ch4_finale',
    msg: 'Финал Главы IV — сеть и Mekanism.'
  },
  A601000000000021: {
    adv: 'ch5_gate',
    msg: 'Глава V — рубеж Nano.'
  },
  A601000000000022: {
    adv: 'ch5_finale',
    msg: 'Финал Главы V — Silent Gear и реликвии.'
  },
  A701000000000029: {
    adv: 'ch6_gate',
    msg: 'Глава VI — рубеж Finale.'
  },
  A701000000000030: {
    adv: 'ch6_finale',
    msg: 'Кодекс экспедиции завершён!'
  },
  A801000000000001: {
    adv: 'side_thermal',
    msg: 'Открыта ветка Thermal — запись в «Ветки модов».'
  },
  A802000000000001: {
    adv: 'side_kitchen',
    msg: 'Открыта ветка Kitchen — запись в «Ветки модов».'
  },
  A803000000000001: {
    adv: 'side_arcane',
    msg: 'Открыта ветка Arcane — запись в «Ветки модов».'
  },
  A804000000000001: {
    adv: 'side_flux',
    msg: 'Открыта ветка Flux Networks — запись в «Ветки модов».'
  },
  A805000000000001: {
    adv: 'side_network',
    msg: 'Открыта ветка AE2 — запись в «Ветки модов».'
  },
  A806000000000001: {
    adv: 'side_apotheosis',
    msg: 'Открыта ветка Apotheosis — запись в «Ветки модов».'
  },
  A807000000000001: {
    adv: 'side_silent_gear',
    msg: 'Открыта ветка Silent Gear — запись в «Ветки модов».'
  },
  A808000000000001: {
    adv: 'side_draconic',
    msg: 'Открыта ветка Draconic Evolution — запись в «Ветки модов».'
  }
}

var JOURNAL_ADV_PREFIX = 'cooptech:journal/'

function grantJournalAdvancement(player, advKey) {
  if (!player || !advKey) return false
  var path = JOURNAL_ADV_PREFIX + advKey
  try {
    player.runCommandSilent('advancement grant ' + player.username + ' only ' + path)
    return true
  } catch (e) {
    console.warn('[CoopTech] journal unlock cmd failed: ' + e)
    return false
  }
}

function notifyJournalUnlock(player, message) {
  if (!player || !player.tell) return
  player.tell('§5§l[Журнал «Якорь»]§r §f' + message)
  player.tell('§7Откройте §dЖурнал экспедиции§7 — раздел «Хроника экспедиции».')
}

global.cooptechUnlockJournal = function (player, advKey, message) {
  if (grantJournalAdvancement(player, advKey)) {
    notifyJournalUnlock(player, message)
  }
}

function registerJournalQuestUnlocks() {
  if (typeof FTBQuestsEvents === 'undefined') {
    console.warn('[CoopTech] FTBQuestsEvents missing — journal quest unlocks disabled (need FTB XMod Compat)')
    return
  }

  Object.keys(JOURNAL_UNLOCKS).forEach(function (questId) {
    var entry = JOURNAL_UNLOCKS[questId]
    FTBQuestsEvents.completed(questId, function (event) {
      var player = event.player
      if (!player) return
      global.cooptechUnlockJournal(player, entry.adv, entry.msg)
    })
  })

  console.info('[CoopTech] Journal quest unlocks registered (' + Object.keys(JOURNAL_UNLOCKS).length + ' milestones)')
}

registerJournalQuestUnlocks()

// При открытии журнала — догоняем разблокировки для уже пройденных квестов (существующие миры)
global.cooptechSyncJournalUnlocks = function (player) {
  if (!player) return
  try {
    var API = Java.loadClass('dev.ftb.mods.ftbquests.FTBQuestsAPI')
    var questFile = API.api().getQuestFile(player.serverLevel())
    var teamData = questFile.getOrCreateTeamData(player)

    Object.keys(JOURNAL_UNLOCKS).forEach(function (questId) {
      var quest = questFile.getQuest(questId)
      if (!quest) return
      if (teamData.isCompleted(quest)) {
        grantJournalAdvancement(player, JOURNAL_UNLOCKS[questId].adv)
      }
    })
  } catch (e) {
    // optional — новые квесты всё равно разблокируют через FTBQuestsEvents.completed
  }
}

PlayerEvents.loggedIn(function (event) {
  if (event.player && global.cooptechSyncJournalUnlocks) {
    global.cooptechSyncJournalUnlocks(event.player)
  }
})
