// Серверная команда /wiki — ссылка на веб-справочник (без клиентских модов).
// URL вики: GitHub Pages репозитория Vladoss1409/ModPack

;(function () {
var WIKI_URL = 'https://vladoss1409.github.io/ModPack/'

function wikiUrl(query) {
  if (!query || query.length === 0) return WIKI_URL
  return WIKI_URL + '?q=' + encodeURIComponent(query)
}

function sendWikiLink(source, query) {
  var url = wikiUrl(query)
  var label = query ? 'Поиск: «' + query + '»' : 'Открыть справочник модов'
  source.sendSystemMessage(Component.literal('§5§l[Вики]§r §f' + label))
  source.sendSystemMessage(Component.literal('§b§n' + url))
  if (!query) {
    source.sendSystemMessage(Component.literal('§7Или: §e/wiki <запрос>§7 — поиск по ключевым словам'))
  }
}

ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  var Arguments = event.arguments
  event.register(
    Commands.literal('wiki')
      .executes(function (ctx) {
        sendWikiLink(ctx.source, null)
        return 1
      })
      .then(
        Commands.argument('query', Arguments.STRING.create(event)).executes(function (ctx) {
          var q = Arguments.STRING.getResult(ctx, 'query')
          sendWikiLink(ctx.source, q)
          return 1
        })
      )
  )
})

PlayerEvents.loggedIn(function (event) {
  var player = event.player
  if (!player || !player.persistentData) return
  if (player.persistentData.wiki_hint_shown) return
  player.persistentData.wiki_hint_shown = true

  player.tell('§5§l[Вики]§r §fСправочник по модам доступен в браузере.')
  player.tell('§b§n' + WIKI_URL)
  player.tell('§7Команда: §e/wiki§7 или §e/wiki mekanism')
})

console.info('[CoopTech] Wiki command: /wiki [query] -> ' + WIKI_URL)
})()
