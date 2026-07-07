// CoopTech — система телепортов (Forge 1.20.1 / KubeJS 2001), только сервер.
// Команды:
//   /set home            — записать точку дома (перезапись, 1 дом на игрока)
//   /home                — телепорт на дом
//   /set warp <имя>      — создать варп (имена глобально уникальны, лимит 3 на игрока)
//   /warp <имя>          — телепорт на варп (можно на чужой)
//   /delete warp <имя>   — удалить свой варп (админ уровня 2 может удалить любой)
//   /warp list           — список всех варпов сервера
//
// Хранение:
//   дом   -> player.persistentData ключ 'cooptech_home' (JSON-строка)
//   варпы -> overworld persistentData ключ 'cooptech_warps' (JSON-объект {имя: запись})

;(function () {
var Component = Java.loadClass('net.minecraft.network.chat.Component')
var Style = Java.loadClass('net.minecraft.network.chat.Style')
var ClickEvent = Java.loadClass('net.minecraft.network.chat.ClickEvent')
var HoverEvent = Java.loadClass('net.minecraft.network.chat.HoverEvent')
var ClickAction = Java.loadClass('net.minecraft.network.chat.ClickEvent$Action')
var HoverAction = Java.loadClass('net.minecraft.network.chat.HoverEvent$Action')
var ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
var ResourceKey = Java.loadClass('net.minecraft.resources.ResourceKey')
var Registries = Java.loadClass('net.minecraft.core.registries.Registries')

var WARPS_KEY = 'cooptech_warps'
var HOME_KEY = 'cooptech_home'
var WARP_LIMIT = 3
var COOLDOWN_MS = 3000

// Кулдаун в памяти (сбрасывается при рестарте — это ок).
var lastTp = {}

// ---------- утилиты ----------

function dimOf(entity) {
  return String(entity.level.dimension().location())
}

function levelByDim(server, dimStr) {
  try {
    var key = ResourceKey.create(Registries.DIMENSION, new ResourceLocation(dimStr))
    return server.getLevel(key)
  } catch (e) {
    return null
  }
}

function playerOf(ctx) {
  try {
    return ctx.source.getPlayerOrException()
  } catch (e) {
    ctx.source.sendFailure(Component.literal('§cЭту команду может выполнять только игрок.'))
    return null
  }
}

function checkCooldown(player) {
  var now = Date.now()
  var last = lastTp[String(player.uuid)] || 0
  var remain = COOLDOWN_MS - (now - last)
  return remain > 0 ? Math.ceil(remain / 1000) : 0
}

function markTp(player) {
  lastTp[String(player.uuid)] = Date.now()
}

function locationRecord(player) {
  return {
    dim: dimOf(player),
    x: player.getX(),
    y: player.getY(),
    z: player.getZ(),
    yaw: player.getYRot(),
    pitch: player.getXRot()
  }
}

function teleportTo(player, server, rec, label) {
  var lvl = levelByDim(server, rec.dim)
  if (!lvl) {
    player.tell('§c[TP] Измерение недоступно: §f' + rec.dim)
    return 0
  }
  player.teleportTo(lvl, rec.x, rec.y, rec.z, rec.yaw, rec.pitch)
  markTp(player)
  player.tell('§a[TP] §fТелепорт: §e' + label)
  return 1
}

// ---------- варпы (глобальное хранилище в overworld) ----------

function getWarps(server) {
  var data = server.overworld().persistentData
  if (!data.contains(WARPS_KEY)) return {}
  try {
    return JSON.parse(data.getString(WARPS_KEY)) || {}
  } catch (e) {
    return {}
  }
}

function saveWarps(server, warps) {
  server.overworld().persistentData.putString(WARPS_KEY, JSON.stringify(warps))
}

function countOwned(warps, uuid) {
  var n = 0
  for (var name in warps) {
    if (warps.hasOwnProperty(name) && warps[name].owner === uuid) n++
  }
  return n
}

// ---------- дом ----------

function setHome(ctx) {
  var player = playerOf(ctx)
  if (!player) return 0
  var rec = locationRecord(player)
  player.persistentData.putString(HOME_KEY, JSON.stringify(rec))
  player.tell('§a[TP] §fТочка дома сохранена.')
  return 1
}

function goHome(ctx) {
  var player = playerOf(ctx)
  if (!player) return 0
  var cd = checkCooldown(player)
  if (cd > 0) {
    player.tell('§c[TP] Подождите §e' + cd + 'с§c перед следующим телепортом.')
    return 0
  }
  if (!player.persistentData.contains(HOME_KEY)) {
    player.tell('§c[TP] Дом не установлен. Используйте §e/set home§c.')
    return 0
  }
  var rec
  try {
    rec = JSON.parse(player.persistentData.getString(HOME_KEY))
  } catch (e) {
    player.tell('§c[TP] Не удалось прочитать точку дома.')
    return 0
  }
  return teleportTo(player, ctx.source.getServer(), rec, 'дом')
}

// ---------- команды варпов ----------

function setWarp(ctx, name) {
  var player = playerOf(ctx)
  if (!player) return 0
  var server = ctx.source.getServer()
  var warps = getWarps(server)
  var uuid = String(player.uuid)

  var existing = warps[name]
  if (existing && existing.owner !== uuid) {
    player.tell('§c[TP] Варп §e' + name + '§c уже занят игроком §f' + existing.ownerName + '§c.')
    return 0
  }
  // Новый варп -> проверяем лимит. Перезапись своего варпа лимит не тратит.
  if (!existing && countOwned(warps, uuid) >= WARP_LIMIT) {
    player.tell('§c[TP] Достигнут лимит варпов (§e' + WARP_LIMIT + '§c). Удалите ненужный: §e/delete warp <имя>§c.')
    return 0
  }

  var rec = locationRecord(player)
  rec.owner = uuid
  rec.ownerName = String(player.username)
  warps[name] = rec
  saveWarps(server, warps)
  player.tell('§a[TP] §fВарп §e' + name + '§f сохранён. (' + countOwned(warps, uuid) + '/' + WARP_LIMIT + ')')
  return 1
}

function goWarp(ctx, name) {
  var player = playerOf(ctx)
  if (!player) return 0
  var cd = checkCooldown(player)
  if (cd > 0) {
    player.tell('§c[TP] Подождите §e' + cd + 'с§c перед следующим телепортом.')
    return 0
  }
  var server = ctx.source.getServer()
  var warps = getWarps(server)
  var rec = warps[name]
  if (!rec) {
    player.tell('§c[TP] Варп §e' + name + '§c не найден. Список: §e/warp list§c.')
    return 0
  }
  return teleportTo(player, server, rec, 'варп ' + name + ' §7(' + rec.ownerName + ')')
}

function deleteWarp(ctx, name) {
  var player = playerOf(ctx)
  if (!player) return 0
  var server = ctx.source.getServer()
  var warps = getWarps(server)
  var rec = warps[name]
  if (!rec) {
    player.tell('§c[TP] Варп §e' + name + '§c не найден.')
    return 0
  }
  var isOwner = rec.owner === String(player.uuid)
  if (!isOwner && !ctx.source.hasPermission(2)) {
    player.tell('§c[TP] Это чужой варп (владелец §f' + rec.ownerName + '§c). Удалять может только владелец.')
    return 0
  }
  delete warps[name]
  saveWarps(server, warps)
  player.tell('§a[TP] §fВарп §e' + name + '§f удалён.')
  return 1
}

function warpClickable(name, ownerName) {
  return Component.literal('§b' + name).withStyle(
    Style.EMPTY
      .withColor(0x55FFFF)
      .withClickEvent(new ClickEvent(ClickAction.RUN_COMMAND, '/warp ' + name))
      .withHoverEvent(new HoverEvent(HoverAction.SHOW_TEXT, Component.literal('§7Телепорт на §f' + name + '\n§7Владелец: §f' + ownerName)))
  )
}

function listWarps(ctx) {
  var server = ctx.source.getServer()
  var warps = getWarps(server)
  var names = []
  for (var n in warps) {
    if (warps.hasOwnProperty(n)) names.push(n)
  }
  names.sort()
  if (names.length === 0) {
    ctx.source.sendSystemMessage(Component.literal('§6[TP]§7 Варпов пока нет. Создайте: §e/set warp <имя>'))
    return 1
  }
  ctx.source.sendSystemMessage(Component.literal('§6[TP]§f Варпы сервера (§e' + names.length + '§f):'))
  for (var i = 0; i < names.length; i++) {
    var rec = warps[names[i]]
    var line = Component.literal('§7 • ')
      .append(warpClickable(names[i], rec.ownerName))
      .append(Component.literal('§7 — ' + rec.ownerName))
    ctx.source.sendSystemMessage(line)
  }
  return 1
}

// ---------- регистрация ----------

ServerEvents.commandRegistry(function (event) {
  var Commands = event.commands
  var Arguments = event.arguments

  // /home
  event.register(
    Commands.literal('home').executes(function (ctx) { return goHome(ctx) })
  )

  // /warp <имя> | /warp list
  event.register(
    Commands.literal('warp')
      .executes(function (ctx) {
        ctx.source.sendSystemMessage(Component.literal('§6[TP]§7 Использование: §e/warp <имя>§7 или §e/warp list'))
        return 1
      })
      .then(Commands.literal('list').executes(function (ctx) { return listWarps(ctx) }))
      .then(
        Commands.argument('name', Arguments.STRING.create(event)).executes(function (ctx) {
          return goWarp(ctx, Arguments.STRING.getResult(ctx, 'name'))
        })
      )
  )

  // /set home | /set warp <имя>
  event.register(
    Commands.literal('set')
      .then(Commands.literal('home').executes(function (ctx) { return setHome(ctx) }))
      .then(
        Commands.literal('warp').then(
          Commands.argument('name', Arguments.STRING.create(event)).executes(function (ctx) {
            return setWarp(ctx, Arguments.STRING.getResult(ctx, 'name'))
          })
        )
      )
  )

  // /delete warp <имя>
  event.register(
    Commands.literal('delete')
      .then(
        Commands.literal('warp').then(
          Commands.argument('name', Arguments.STRING.create(event)).executes(function (ctx) {
            return deleteWarp(ctx, Arguments.STRING.getResult(ctx, 'name'))
          })
        )
      )
  )
})

console.info('[CoopTech] Teleports loaded: /set home, /home, /set warp <name>, /warp <name>, /delete warp <name>, /warp list')
})()
