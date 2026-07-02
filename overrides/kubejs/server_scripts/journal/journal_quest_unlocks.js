// Разблокировка записей Patchouli-журнала по завершению квестов FTB Quests.
// Требует FTB XMod Compat (KubeJS + FTB Quests).

var JOURNAL_UNLOCKS = {
  // ── T0 «Разлом» (новое дерево, глава 5217C…) ──
  // Принцип: справочник по МЕХАНИЗМУ открывается, когда квест на его крафт/исполь-
  // зование становится ДОСТУПЕН = по завершению квеста-предпосылки. Лорные «записки»
  // (раздел «Хроника») открываются на маяках вместе с выдачей страницы-награды.
  '5217A00000000001': [
    { adv: 't0_intro', msg: 'Справочник: «Разлом Якоря» — цель тира.' },
    { adv: 't0_lore_rift', msg: 'Хроника: «День ноль у разлома».' }
  ],
  // Гейт 1 пройден → открываются квесты на печь/кухню/склад → даём их справочники заранее
  '5217A00000000008': [
    { adv: 't0_lore_camp', msg: 'Хроника: «Лагерь закреплён».' },
    { adv: 't0_furnace', msg: 'Справочник: «Iron Furnaces — печи».' },
    { adv: 't0_kitchen', msg: 'Справочник: «Farmer\u0027s Delight — кухня».' },
    { adv: 't0_drawers', msg: 'Справочник: «Storage Drawers — ящики».' }
  ],
  '5217A00000000015': [
    { adv: 't0_lore_home', msg: 'Хроника: «Обжитой лагерь».' }
  ],
  // Гейт 3 пройден → открываются квесты рамы/искры → справочник по рубежам-якорям
  '5217A00000000022': [
    { adv: 't0_lore_ready', msg: 'Хроника: «Готовность к энергии».' },
    { adv: 't0_gates', msg: 'Справочник: «Якорные рубежи» — гейтинг тиров.' }
  ],
  '5217A00000000026': [
    { adv: 't0_lore_spark', msg: 'Хроника: «Якорная искра вспыхнула».' },
    { adv: 't0_finale', msg: 'Справочник: «Thermal — первая машина», вход в T1.' }
  ],

  // ── T1 «Искра» ──
  '5221A00000000001': [
    { adv: 't1_lore_intro', msg: 'Хроника T1: «Порог Thermal».' }
  ],
  '5221A00000000008': [
    { adv: 't1_lore_w1', msg: 'Хроника T1: «Контур запущен».' },
    { adv: 't1_thermal', msg: 'Справочник: «Thermal — автоматизация».' },
    { adv: 't1_powah', msg: 'Справочник: «Powah — генерация и батареи».' }
  ],
  '5221A0000000000F': [
    { adv: 't1_lore_w2', msg: 'Хроника T1: «Автоматизация руды».' }
  ],
  '5221A00000000016': [
    { adv: 't1_lore_w3', msg: 'Хроника T1: «Готовность к Mekanism».' }
  ],
  '5221A0000000001A': [
    { adv: 't1_lore_finale', msg: 'Хроника T1: «Якорная ячейка собрана».' }
  ],

  // ── T2 «Контур» ──
  '5222A00000000001': [
    { adv: 't2_lore_intro', msg: 'Хроника T2: «Порог Mekanism».' },
    { adv: 't2_mek', msg: 'Справочник: «Mekanism — промышленный старт».' }
  ],
  '5222A00000000008': [
    { adv: 't2_lore_w1', msg: 'Хроника T2: «Промышленный старт».' },
    { adv: 't2_enderio', msg: 'Справочник: «Ender IO — сплавы и логистика».' },
    { adv: 't2_flux', msg: 'Справочник: «Flux Networks — энергия без проводов».' }
  ],
  '5222A0000000000F': [
    { adv: 't2_lore_w2', msg: 'Хроника T2: «Энергоузел».' }
  ],
  '5222A00000000016': [
    { adv: 't2_lore_w3', msg: 'Хроника T2: «Готовность к сети».' }
  ],
  '5222A0000000001A': [
    { adv: 't2_lore_finale', msg: 'Хроника T2: «Якорная матрица».' }
  ],

  // ── T3 «Сеть» ──
  '5223A00000000001': [
    { adv: 't3_lore_intro', msg: 'Хроника T3: «Порог AE2».' },
    { adv: 't3_ae2', msg: 'Справочник: «AE2 — ME-сеть».' }
  ],
  '5223A00000000008': [
    { adv: 't3_lore_w1', msg: 'Хроника T3: «Сеть зарождается».' },
    { adv: 't3_emc', msg: 'Справочник: «ProjectE — EMC и трансмутация».' }
  ],
  '5223A0000000000F': [
    { adv: 't3_lore_w2', msg: 'Хроника T3: «ME-сеть работает».' }
  ],
  '5223A00000000016': [
    { adv: 't3_lore_w3', msg: 'Хроника T3: «Готовность к Draconic».' }
  ],
  '5223A0000000001A': [
    { adv: 't3_lore_finale', msg: 'Хроника T3: «Якорная сингулярность».' }
  ],

  // ── T4 «Дракон» ──
  '5224A00000000001': [
    { adv: 't4_lore_intro', msg: 'Хроника T4: «Порог Draconic».' },
    { adv: 't4_draconic', msg: 'Справочник: «Draconic Evolution — основы».' }
  ],
  '5224A00000000008': [
    { adv: 't4_lore_w1', msg: 'Хроника T4: «Драконий старт».' },
    { adv: 't4_fusion', msg: 'Справочник: «Draconic — реактор и Chaos».' }
  ],
  '5224A0000000000F': [
    { adv: 't4_lore_w2', msg: 'Хроника T4: «Энергия дракона».' }
  ],
  '5224A00000000016': [
    { adv: 't4_lore_w3', msg: 'Хроника T4: «Готовность к нексусу».' }
  ],
  '5224A0000000001A': [
    { adv: 't4_lore_finale', msg: 'Хроника T4: «Якорный нексус».' }
  ],

  // ── T5 «Схождение» ──
  '5225A00000000001': [
    { adv: 't5_lore_intro', msg: 'Хроника T5: «Порог next_ae».' },
    { adv: 't5_next_ae', msg: 'Справочник: «next_ae — ультра-крафт».' }
  ],
  '5225A00000000008': [
    { adv: 't5_lore_w1', msg: 'Хроника T5: «next_ae запущен».' },
    { adv: 't5_anchor', msg: 'Справочник: «Стабилизация Якоря».' }
  ],
  '5225A0000000000F': [
    { adv: 't5_lore_w2', msg: 'Хроника T5: «Осколки сходятся».' }
  ],
  '5225A00000000016': [
    { adv: 't5_lore_w3', msg: 'Хроника T5: «Готовность к ядру».' }
  ],
  '5225A0000000001A': [
    { adv: 't5_lore_finale', msg: 'Хроника T5: «Ядро Якоря стабилизировано».' }
  ],

  // ── Після якоря (post-T5) ──
  'A900000000000001': [
    { adv: 'post_anchor', msg: 'Хроника: «Після якоря» — три шляхи епілогу.' }
  ],
  'A901000000000001': [
    { adv: 'side_post_caves', msg: 'Після якоря: «Печери розлому».' },
    { adv: 'codex_side_post_caves', msg: 'Справочник: «Alex\'s Caves — глибина».' }
  ],
  'A902000000000001': [
    { adv: 'side_post_bossfarm', msg: 'Після якоря: «Бос-фарм якоря».' },
    { adv: 'codex_side_post_bossfarm', msg: 'Справочник: «Фарм босів після фіналу».' }
  ],
  'A903000000000001': [
    { adv: 'side_post_epilogue', msg: 'Після якоря: «Епілог модів».' },
    { adv: 'codex_side_post_epilogue', msg: 'Справочник: «Фінальний облік модів».' }
  ],

  // ── Сайд-ветки (первый квест после рубежа) ──
  'A802000000000001': [
    { adv: 'side_kitchen', msg: 'Ветки модов: «Полевая кухня».' },
    { adv: 'codex_side_kitchen', msg: 'Справочник: «Полевая кухня — пайки для рейдов».' }
  ],
  'A809000000000001': [
    { adv: 'side_storage', msg: 'Ветки модов: «Склад экспедиции».' },
    { adv: 'codex_side_storage', msg: 'Справочник: «Склад — ящики и бочки».' }
  ],
  'A813000000000001': [
    { adv: 'side_bestiary', msg: 'Ветки модов: «Полевой бестиарий».' },
    { adv: 'codex_side_bestiary', msg: 'Справочник: «Разведка и бестиарий».' }
  ],
  'A801000000000001': [
    { adv: 'side_thermal', msg: 'Ветки модов: «Тепловой контур».' },
    { adv: 'codex_side_thermal', msg: 'Справочник: «Thermal — полный контур».' }
  ],
  'A814000000000001': [
    { adv: 'side_powah', msg: 'Ветки модов: «Резонанс Powah».' },
    { adv: 'codex_side_powah', msg: 'Справочник: «Powah — полная линия».' }
  ],
  'A810000000000001': [
    { adv: 'side_immersive', msg: 'Ветки модов: «Индустриальная ковка».' },
    { adv: 'codex_side_immersive', msg: 'Справочник: «Immersive Engineering».' }
  ],
  'A806000000000001': [
    { adv: 'side_apotheosis', msg: 'Ветки модов: «Апофеоз».' },
    { adv: 'codex_side_apotheosis', msg: 'Справочник: «Apotheosis — перековка».' }
  ],
  'A807000000000001': [
    { adv: 'side_silent_gear', msg: 'Ветки модов: «Ковка Silent Gear».' },
    { adv: 'codex_side_silent_gear', msg: 'Справочник: «Silent Gear — кастомные инструменты».' }
  ],
  'A811000000000001': [
    { adv: 'side_mekanism', msg: 'Ветки модов: «Промышленный узел».' },
    { adv: 'codex_side_mekanism', msg: 'Справочник: «Mekanism — полный завод».' }
  ],
  'A812000000000001': [
    { adv: 'side_enderio', msg: 'Ветки модов: «Проводник Ender IO».' },
    { adv: 'codex_side_enderio', msg: 'Справочник: «Ender IO — кондуиты».' }
  ],
  'A804000000000001': [
    { adv: 'side_flux', msg: 'Ветки модов: «Flux Networks».' },
    { adv: 'codex_side_flux', msg: 'Справочник: «Flux — полная сеть».' }
  ],
  'A803000000000001': [
    { adv: 'side_arcane', msg: 'Ветки модов: «Арканум поля».' },
    { adv: 'codex_side_arcane', msg: 'Справочник: «Iron\u0027s Spells — магия».' }
  ],
  'A805000000000001': [
    { adv: 'side_network', msg: 'Ветки модов: «Молекулярная сеть».' },
    { adv: 'codex_side_network', msg: 'Справочник: «AE2 — углублённая сеть».' }
  ],
  'A815000000000001': [
    { adv: 'side_twilight', msg: 'Ветки модов: «Сумеречный рубеж».' },
    { adv: 'codex_side_twilight', msg: 'Справочник: «Twilight Forest».' }
  ],
  'A808000000000001': [
    { adv: 'side_draconic', msg: 'Ветки модов: «Драконья эволюция».' },
    { adv: 'codex_side_draconic', msg: 'Справочник: «Draconic — сайд-ветка».' }
  ],
  'A817000000000001': [
    { adv: 'side_cataclysm', msg: 'Ветки модов: «Бездна Cataclysm».' },
    { adv: 'codex_side_cataclysm', msg: 'Справочник: «Cataclysm — боссы».' }
  ],
  'A816000000000001': [
    { adv: 'side_relics', msg: 'Ветки модов: «Реликвии».' },
    { adv: 'codex_side_relics', msg: 'Справочник: «Relics — артефакты».' }
  ],

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
  }
}

var JOURNAL_ADV_PREFIX = 'cooptech:journal/'

function grantJournalAdvancement(player, advKey) {
  if (!player || !advKey) return false
  var path = JOURNAL_ADV_PREFIX + advKey
  try {
    player.runCommandSilent('advancement grant ' + player.username + ' until ' + path)
    return true
  } catch (e) {
    console.warn('[CoopTech] journal unlock cmd failed: ' + e)
    return false
  }
}

function notifyJournalUnlock(player, message) {
  if (!player || !player.tell) return
  player.tell('§5§l[Журнал «Якорь»]§r §f' + message)
  if (message.indexOf('Справочник') >= 0) {
    player.tell('§7Откройте §dЖурнал экспедиции§7 — раздел «Справочник» (или «Сайд-ветки»).')
  } else if (message.indexOf('Ветки модов') >= 0) {
    player.tell('§7Откройте §dЖурнал экспедиции§7 — раздел «Ветки модов».')
  } else {
    player.tell('§7Откройте §dЖурнал экспедиции§7 — раздел «Хроника экспедиции».')
  }
}

global.cooptechUnlockJournal = function (player, advKey, message) {
  if (grantJournalAdvancement(player, advKey)) {
    notifyJournalUnlock(player, message)
  }
}

// Значение карты может быть одиночной записью {adv,msg} или массивом таких записей.
function unlockList(entry) {
  if (!entry) return []
  return entry.adv ? [entry] : entry
}

function registerJournalQuestUnlocks() {
  if (typeof FTBQuestsEvents === 'undefined') {
    console.warn('[CoopTech] FTBQuestsEvents missing — journal quest unlocks disabled (need FTB XMod Compat)')
    return
  }

  Object.keys(JOURNAL_UNLOCKS).forEach(function (questId) {
    var list = unlockList(JOURNAL_UNLOCKS[questId])
    FTBQuestsEvents.completed(questId, function (event) {
      var player = event.player
      if (!player) return
      list.forEach(function (u) {
        global.cooptechUnlockJournal(player, u.adv, u.msg)
      })
    })
  })

  console.info('[CoopTech] Journal quest unlocks registered (' + Object.keys(JOURNAL_UNLOCKS).length + ' milestones)')
}

registerJournalQuestUnlocks()

// При открытии журнала — догоняем разблокировки для уже пройденных квестов (существующие миры)
global.cooptechSyncJournalUnlocks = function (player) {
  if (!player) return
  var questFile = global.cooptechGetQuestFile ? global.cooptechGetQuestFile(player) : null
  var teamData = global.cooptechGetTeamData ? global.cooptechGetTeamData(player) : null
  if (!questFile || !teamData) return
  try {
    Object.keys(JOURNAL_UNLOCKS).forEach(function (questId) {
      var quest = questFile.getQuest(questId)
      if (!quest) return
      if (teamData.isCompleted(quest)) {
        unlockList(JOURNAL_UNLOCKS[questId]).forEach(function (u) {
          grantJournalAdvancement(player, u.adv)
        })
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
