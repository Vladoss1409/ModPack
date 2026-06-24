// FTB Quests 2001.4.22 + ftb-xmod-compat: clicking an item task with an empty/air filter
// calls JEI and crashes (Focus value is invalid: minecraft:air). disable_jei in data.snbt
// does not affect this code path. Wrap the JEI helper after xmod-compat registers it.

var ftbJeiGuardInstalled = false

ClientEvents.tick(function (event) {
  if (ftbJeiGuardInstalled || !event.player) return
  if (event.level.gameTime % 10 !== 0) return

  try {
    var FTBQuests = Java.loadClass('dev.ftb.mods.ftbquests.FTBQuests')
    var RecipeModHelper = Java.loadClass('dev.ftb.mods.ftbquests.integration.RecipeModHelper')
    var ItemStack = Java.loadClass('net.minecraft.world.item.ItemStack')
    var Items = Java.loadClass('net.minecraft.world.item.Items')

    var original = FTBQuests.getRecipeModHelper()
    if (!original || !String(original.getClass().getName()).includes('JEI')) return

    var safe = Java.extend(RecipeModHelper, {
      refreshAll: function (components) {
        original.refreshAll(components)
      },
      refreshRecipes: function (questObject) {
        original.refreshRecipes(questObject)
      },
      showRecipes: function (stack) {
        if (!stack || stack.isEmpty() || stack.is(Items.AIR)) {
          console.warn('[CoopTech] Blocked JEI for empty/air quest item (client crash avoided)')
          return
        }
        original.showRecipes(stack)
      },
      getHelperName: function () {
        return original.getHelperName()
      },
      isRecipeModAvailable: function () {
        return original.isRecipeModAvailable()
      },
      updateItemsDynamic: function (added, removed) {
        original.updateItemsDynamic(added, removed)
      }
    })

    FTBQuests.setRecipeModHelper(new safe())
    ftbJeiGuardInstalled = true
    console.info('[CoopTech] FTB Quests JEI click guard active')
  } catch (e) {
    console.warn('[CoopTech] FTB Quests JEI guard failed: ' + e)
  }
})
