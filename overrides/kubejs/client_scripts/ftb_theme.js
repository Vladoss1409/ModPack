function reloadCoopTheme() {
  try {
    var ThemeLoader = Java.loadClass('dev.ftb.mods.ftbquests.quest.theme.ThemeLoader')
    var Minecraft = Java.loadClass('net.minecraft.client.Minecraft')
    ThemeLoader.loadTheme(Minecraft.getInstance().getResourceManager())
    console.info('[CoopTech] FTB Quests theme reloaded')
  } catch (e) {
    console.warn('[CoopTech] FTB theme reload: ' + e)
  }
}

ClientEvents.loggedIn(function () {
  Client.scheduleInTicks(40, reloadCoopTheme)
})
