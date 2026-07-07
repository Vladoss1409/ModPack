// Серверная команда /wiki — ссылка на веб-справочник (без клиентских модов).
// URL вики: GitHub Pages репозитория Vladoss1409/ModPack

var WIKI_URL = 'https://vladoss1409.github.io/ModPack/'

var Component = Java.loadClass('net.minecraft.network.chat.Component')
var Style = Java.loadClass('net.minecraft.network.chat.Style')
var ClickEvent = Java.loadClass('net.minecraft.network.chat.ClickEvent')
var HoverEvent = Java.loadClass('net.minecraft.network.chat.HoverEvent')
var ClickAction = Java.loadClass('net.minecraft.network.chat.ClickEvent$Action')
var HoverAction = Java.loadClass('net.minecraft.network.chat.HoverEvent$Action')

function wikiUrl(query) {
  if (!query || query.length === 0) return WIKI_URL
  return WIKI_URL + '?q=' + encodeURIComponent(query)
}

function wikiClickable(url, label) {
  return Component.literal(label).withStyle(
    Style.EMPTY
      .withColor(0x55FFFF)
      .withUnderlined(true)
      .withClickEvent(new ClickEvent(ClickAction.OPEN_URL, url))
      .withHoverEvent(
        new HoverEvent(HoverAction.SHOW_TEXT, Component.literal('§7Открыть в браузере'))
      )
  )
}

function sendWikiLink(source, query) {
  var url = wikiUrl(query)
  var prefix = Component.literal('§5§l[Вики]§r §f')
  var link = wikiClickable(url, query ? 'Поиск: «' + query + '»' : 'Открыть справочник модов')
  source.sendSystemMessage(prefix.append(link))
  if (!query) {
    source.sendSystemMessage(
      Component.literal('§7Или: §e/wiki <запрос>§7 — поиск по ключевым словам')
    )
  }
}

ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  event.register(
    Commands.literal('wiki')
      .executes(function (ctx) {
        sendWikiLink(ctx.source, null)
        return 1
      })
      .then(
        Commands.argument('query', Commands.STRING()).executes(function (ctx) {
          var q = ctx.getArgument('query', Java.loadClass('java.lang.String'))
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
  if (player.sendSystemMessage) {
    player.sendSystemMessage(wikiClickable(WIKI_URL, 'Открыть MyModPack Wiki'))
  }
  player.tell('§7Команда: §e/wiki§7 или §e/wiki mekanism')
})

console.info('[CoopTech] Wiki command: /wiki [query] -> ' + WIKI_URL)
