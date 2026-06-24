var JOURNAL_BOOK_ID = 'patchouli:expedition_journal'

function journalBookLocation() {
  var ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
  return new ResourceLocation('patchouli', 'expedition_journal')
}

function openJournalClient() {
  try {
    var PatchouliAPI = Java.loadClass('vazkii.patchouli.api.PatchouliAPI')
    PatchouliAPI.get().openBookGUI(journalBookLocation())
    return true
  } catch (e) {
    console.warn('[CoopTech] client journal open: ' + e)
    return false
  }
}

function journalFallbackMessage(player) {
  if (!player || !player.tell) return
  player.tell('§6§lЖурнал экспедиции «Якорь»§r')
  player.tell('§7Не удалось открыть книгу. Попробуйте в чате (§eT§r):')
  player.tell('§e/open-patchouli-book @s ' + JOURNAL_BOOK_ID)
}

NetworkEvents.dataReceived('cooptech_open_journal', function (event) {
  if (!openJournalClient()) {
    journalFallbackMessage(event.player)
  }
})

// Страницы журнала — только чат на сервере; блокируем лишние клиентские обработчики
for (var pi = 0; pi <= 12; pi++) {
  ;(function (pageItemId) {
    ItemEvents.rightClicked(pageItemId, function (event) {
      if (event.level.isClientSide()) {
        event.cancel()
      }
    })
  })('kubejs:journal_page_' + String(pi).padStart(2, '0'))
}
