const JOURNAL_BOOK = 'patchouli:expedition_journal'

const RELIQUARY_LOOT = {
  reliquary_field: 'cooptech:reliquary/field',
  reliquary_resonant: 'cooptech:reliquary/resonant',
  reliquary_arcane: 'cooptech:reliquary/arcane',
  reliquary_primordial: 'cooptech:reliquary/primordial',
  reliquary_convergence: 'cooptech:reliquary/convergence'
}

function isServer(level) {
  return level && !level.isClientSide()
}

function interactItem(item) {
  return item
    .useAnimation('none')
    .useDuration(function () { return 1 })
    .use(function (level, player, hand) {
      return true
    })
}

StartupEvents.registry('item', event => {
  interactItem(event.create('expedition_journal')
    .displayName('Журнал экспедиции')
    .maxStackSize(1)
    .glow(true))
    .tooltip('§7Записи о разломах Якоря реальности.')
    .tooltip('§eПКМ§r — открыть книгу записей.')
    .finishUsing(function (stack, level, entity) {
      if (isServer(level)) {
        global.cooptechOpenJournal(entity)
      }
      return stack
    })

  for (var i = 0; i <= 12; i++) {
    var pageId = 'journal_page_' + String(i).padStart(2, '0')
    interactItem(event.create(pageId)
      .displayName('Страница журнала §8#' + i)
      .maxStackSize(16))
      .tooltip('§7Фрагмент полевых записей экспедиции.')
      .tooltip('§eПКМ§r — прочитать текст в чате.')
      .finishUsing((function (pid) {
        return function (stack, level, entity) {
          if (isServer(level)) {
            global.cooptechReadJournalPage(entity, pid)
          }
          return stack
        }
      })(pageId))
  }

  for (var j = 1; j <= 12; j++) {
    var n = String(j).padStart(2, '0')
    event.create('anchor_shard_' + n)
      .displayName('Фрагмент якоря §b#' + j)
      .maxStackSize(64)
      .glow(true)
      .tooltip('§7Нестабильный осколок Якоря реальности.')

    event.create('stabilized_shard_' + n)
      .displayName('Стабилизированный фрагмент §b#' + j)
      .maxStackSize(16)
      .glow(true)
      .tooltip('§7Готов к установке в Якорь.')
  }

  event.create('reality_anchor_core')
    .displayName('Ядро Якоря реальности')
    .maxStackSize(1)
    .glow(true)
    .tooltip('§dСтабилизированное ядро. Финал экспедиции.')

  var reliquaries = [
    ['reliquary_field', '§aПолевая реликвария'],
    ['reliquary_resonant', '§bРезонансная реликвария'],
    ['reliquary_arcane', '§5Арканная реликвария'],
    ['reliquary_primordial', '§6Первозданная реликвария'],
    ['reliquary_convergence', '§dРеликвария схождения']
  ]

  reliquaries.forEach(function (entry) {
    var id = entry[0]
    var name = entry[1]
    var lootId = RELIQUARY_LOOT[id]

    interactItem(event.create(id).displayName(name).maxStackSize(16).glow(true))
      .tooltip('§7Редкая находка. §8ПКМ — вскрыть.')
      .tooltip('§8Содержимое нестабильно. Не обязательна для прогресса.')
      .finishUsing((function (lid) {
        return function (stack, level, entity) {
          if (isServer(level)) {
            global.cooptechOpenReliquary(entity, lid)
            return stack.withCount(Math.max(0, stack.count - 1))
          }
          return stack
        }
      })(lootId))
  })

  interactItem(event.create('resonance_beacon')
    .displayName('Резонансный маяк')
    .maxStackSize(1))
    .tooltip('§7Помогает найти метеор AE2.')
    .tooltip('§7Prologue: ПКМ у лагеря экспедиции — кооп-синхронизация.')
    .tooltip('§8Ch11+: подсказка к метеорам AE2.')
    .finishUsing(function (stack, level, entity) {
      if (isServer(level)) {
        global.cooptechUseBeacon(entity)
      }
      return stack
    })

  event.create('decrypted_cave_codex')
    .displayName('Расшифрованный кодекс пещер')
    .maxStackSize(1)
    .tooltip('§7Альтернатива провалу Spelunkery.')

  var questIconItems = [
  ['quest_gate', 'Рубеж квестов'],
  ['quest_side_lock', 'Замок ветки'],
  ['quest_lock', 'Замок главы'],
  ['quest_pool', 'Пул квестов'],
  ['quest_finale', 'Финал главы'],
  ['quest_chapter_start', 'Старт главы'],
  ['quest_wave', 'Новая волна']
  ]

  questIconItems.forEach(function (entry) {
    event.create(entry[0])
      .displayName(entry[1])
      .maxStackSize(1)
      .tooltip('§8Служебная иконка FTB Quests')
  })
})
