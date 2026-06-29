# План інтеграції AE2-аддонів у MyModPack

Статус: **застосовано** · Дата: 2026-06-29 · MC 1.20.1 / Forge 47.4.10

## Ціль
Додати AE2-аддони + ProjectE + AppliedE у `MyModPack` і визначити долю всіх крос-мод
рецептів AE2-екосистеми під реальний склад паку.

> Важлива поправка: попередній аналіз робився по теці `decompiled` (10 аддонів), а сам
> `MyModPack` мав з AE2-екосистеми лише `ae2 + AE2-Things + Applied-Mekanistics`. Усе звірено
> наново по `MyModPack\mods` та `mods.toml` кожного аддона.

## Головний висновок
«Замінювати рецепти на аналоги» майже не потрібно: у паку **Mekanism + MekanismGenerators вже є**,
тож більшість крос-мод рецептів оживає автоматично, а решта — після додавання ProjectE + AppliedE.
Без аналогів у паку лишаються лише 4 мертві гілки (appflux / EU / mana / source) — вони інертні.

## 0. Фікс краша next_ae (2026-06-29)

**Симптом:** `next_ae has failed to load correctly — java.lang.NoClassDefFoundError:
dev/nexteam/next/core/common/api/network/Network`.

**Причина:** `next_ae-1.0.0+1.20.1-client.jar` містить лише класи `dev/nexteam/next/ae/...`
і викликає `dev.nexteam.next.core.common.api.network.Network`, але **не вшиває** ці класи і
**не оголошує** залежність `next_core` у своєму `mods.toml` (там лише forge/minecraft/ae2/
draconicevolution). `next_core` — частина пропрієтарного серверного пакета «Next» (mcskill.net).

**Виправлення:** додано `next_core-1.51.1+1.20.1-client.jar` (з `decompiled\mods`) у `mods/`.
Він надає відсутній клас `Network`. Його єдина додаткова залежність — `luckperms` з
`side = "SERVER"`, тож на клієнті/синглплеєрі вона не обовʼязкова; для запуску на **сервері**
треба додатково встановити LuckPerms.

## 0b. Фікс конфлікту модулів Kotlin (2026-06-29)

**Симптом:** після додавання `next_core` гра падала на старті:
`java.lang.module.ResolutionException: Modules kotlinx.coroutines.core and
thedarkcolour.kotlinforforge export package kotlinx.coroutines.flow to module relics`.

**Причина:** `next_core` у `META-INF/jarjar/` віз власний Kotlin-рантайм, який уже надає
`kotlinforforge-4.12.0-all` (той самий набір версій: Kotlin 2.2.0 / coroutines 1.10.2 /
serialization 1.9.0). Через дубль два модулі експортували ті самі пакети Kotlin → JPMS-конфлікт.

**Виправлення:** `next_core` перепаковано — вирізано 5 дублюючих бібліотек із `META-INF/jarjar/`
і оновлено `metadata.json`:
- видалено: `kotlin-stdlib-2.2.0`, `kotlin-reflect-2.2.0`, `kotlinx-coroutines-core-jvm-1.10.2`,
  `kotlinx-serialization-core-jvm-1.9.0`, `kotlinx-serialization-json-jvm-1.9.0`;
- лишено: `mixinextras-forge-0.4.1`, `reactor-core-3.6.6`, `kotlinx-coroutines-reactive-1.10.2`,
  `reactive-streams-1.0.4` (їх kotlinforforge не надає).

Тепер Kotlin/coroutines/serialization дає лише `kotlinforforge`. Оригінал збережено:
`backups/next_core-1.51.1+1.20.1-client.jar.orig`. Розмір jar: 8.88 МБ → 2.37 МБ.

> Технічна нотатка: перша спроба перепакування через .NET ZIP у режимі Update залишила
> вкладені jar-и «STORED» з EXT-дескриптором, і Forge впав з
> `java.util.zip.ZipException: only DEFLATED entries can have EXT descriptor`. Тому jar
> перебрано з нуля: усі 221 записів стиснено DEFLATE, `MANIFEST.MF` — першим записом.
> Перевірено: 0 записів STORED → помилка більше неможлива.

## 1. Додані моди (117 → 130)

### Аддони з `decompiled\mods`
| Jar | modId | Нотатки |
|---|---|---|
| AdvancedAE-1.3.2-1.20.1.jar | advanced_ae | ae2 ≥15.4.9 ✓; ae2addonlib вшито (jarjar) |
| ExtendedAE-1.20-1.4.8-forge.jar | expatternprovider | потребує guideme ✓ + glodium (додано) |
| Glodium-1.20-1.5-forge.jar | glodium | обовʼязкова залежність ExtendedAE |
| megacells-forge-2.4.6-1.20.1.jar | megacells | cloth_config ✓; appmek ✓ (хім.), appliede (EMC) |
| mae2-1.6.1.jar | mae2 | mixinextras вшито; gtceu відсутній → EU-тунель інертний |
| merequester-forge-1.20.1-1.1.5.jar | merequester | ae2 ✓ |
| next_ae-1.0.0+1.20.1-client.jar | next_ae | потребує Draconic Evolution 3.1.2.621 ✓; Registrate вшито; **потребує next_core** (див. фікс нижче) |
| next_core-1.51.1+1.20.1-client.jar | next_core | надає `dev.nexteam.next.core.*` (клас `Network`), якого вимагає `next_ae`; залежності: forge, minecraft, **luckperms (тільки SERVER)** |
| ae2wtlib-15.3.1-forge.jar | ae2wtlib | ae2 [15.4.10,16) ✓; cloth/architectury/curios ✓ |
| ae2ct-1.20.1-1.1.0.jar | ae2ct | ae2 ✓ |
| AEInfinityBooster-1.20.1-1.0.0+51.jar | aeinfinitybooster | ae2 ✓ |

### Завантажені EMC-моди
| Jar | modId | Джерело | Сумісність |
|---|---|---|---|
| ProjectE-1.20.1-PE1.0.1.jar | projecte | CurseForge (cfwidget→edge.forgecdn) | Forge ≥47.0.47 ✓ |
| appliede-0.14.3.jar | appliede | Modrinth | ae2 ≥15.1.0 ✓, projecte ≥1.0.1 ✓ (рівно 1.0.1), ae2wtlib опц. ✓ |

Залежності в паку (усі присутні): cloth-config, architectury, curios, guideme, Glodium, Draconic, Mekanism.

## 2. Доля крос-мод гілок рецептів

| Гілка | Мод | Рецептів | Чужі моди | Рішення |
|---|---|---|---|---|
| MEGA хімічні комірки (1M–256M, портативні, корпус) | megacells | 16 | appmek + mekanism | **АКТИВНО (само)** — Mekanism у паку є |
| MEGA радіоактивна хім-комірка + компонент | megacells | 2 | mekanism + generators | **АКТИВНО (само)** |
| Quantum Infused Dust (альт. через Дробарку) | advanced_ae | 1 | mekanism | **АКТИВНО (само)** |
| ExtendedAE EMC-лінійка (інтерфейс, шини, апгрейди) | expatternprovider | 7 | appliede + projecte | **АКТИВНО (EMC)** + EMC-цінності |
| MEGA EMC-інтерфейс (блок + кабельна частина) | megacells | 3 | appliede + projecte | **АКТИВНО (EMC)** |
| ae2:capacity_card → EMC-рецепти (використання) | ae2 | 3 | appliede + projecte | **АКТИВНО (EMC)** |
| MEGA mana-комірки (Botania) | megacells | 11 | appbot + botania | **ПРИБРАТИ** — Botania виключено, предмети не реєструються |
| MEGA source-комірки (Ars Nouveau) | megacells | 11 | arseng + ars_nouveau | **ПРИБРАТИ** — Ars немає |
| Advanced AE ↔ Applied Flux (reaction) | advanced_ae | 3 | appflux | **ПРИБРАТИ** — appflux не додаємо; роблять appflux-предмети |
| mae2 EU Multi P2P тунель (GregTech) | mae2 | 1 | gtceu | **ПРИБРАТИ** — EU-споживачів немає |

Мертві гілки лишені **інертними** (умовні `forge:mod_loaded` рецепти просто не вантажаться;
у JEI не показуються). Фізичне видалення JSON не виконувалось.

> Рішення (2026-06-29): крок явного прибирання через KubeJS свідомо пропущено — гілки вже
> неактивні через `mod_loaded`, тож видалення нічого функціонально не змінює. План завершено.

## 3. EMC-цінності (ProjectE)
Датапак: `overrides/kubejs/data/projecte/pe_custom_conversions/ae2_base.json`

Вручну задано лише «кореневі» ресурси AE2 — решта рахується ProjectE автоматично з рецептів:

| Предмет | EMC |
|---|---|
| ae2:certus_quartz_crystal | 256 |
| ae2:charged_certus_quartz_crystal | 256 |
| ae2:fluix_crystal | 256 |
| ae2:certus_quartz_dust | 256 |
| ae2:sky_stone_block | 64 |
| ae2:sky_dust | 64 |

Значення легко підлаштувати у тому ж файлі.

## 4. Що ще перевірити
- [x] **Валідація jar-ів** (`scripts/validate_mods.py`, 2026-06-29): усі 129 jar валідні; 0 попереджень для AE2/EMC модів. Лишились 2 раніше наявні попередження не з цієї роботи: `aether` та `cumulus_menus` — NeoForge-збірки в Forge-паку.
- [x] **Статичний смоук-тест** (`scripts/smoke_test_mods.py --mods mods`, 2026-06-29): усі 129 jar відкриваються як коректний ZIP, 0 помилок. Попередження не з цієї роботи: `aether`, `cumulus_menus` (NeoForge) і хибне спрацювання патерна на `textrues_embeddium_options` (нормальний Forge-мод).
- [~] **Реальний запуск гри** (тестовий інстанс `…\.minecraft\versions\ModPack`, 2026-06-29): перший запуск крашнув через несумісність `embeddium 0.3.31` ↔ `textrues_embeddium_options 0.1.5`. **Виправлено:** мод прибрано з паку (jar + modlist), пак тепер 129 → **128**. Лишилось перевірити `next_ae` («-client» збірка) на наступному запуску.
- [x] **EMC-цінності** (2026-06-29): датапак валідний (JSON, формат ProjectE `values.before`), 6 кореневих значень підтверджено. Рішення — лишити як є; решта рахується ProjectE автоматично. Балансування за смаком — за потреби пізніше.

## 5. Крафт-рецепти next_ae (2026-06-29)
**Проблема:** предмети/блоки `next_ae` неможливо скрафтити. Мод задумано як серверний (mcskill.net) і
власних крафт-рецептів у jar немає — лише 12 машинних рецептів (advanced_inscriber / fluix_aggregator /
charger). У сингл-/звичайному паку рецепти крафту мали роздаватися серверним датапаком, якого тут немає.

**Виправлення:** додано KubeJS server-скрипт `overrides/kubejs/server_scripts/recipes/02_next_ae_recipes.js`
(**52 рецепти, ULTRA ENDGAME** на Ender IO + Draconic Evolution, гібрид з AE2). Баланс:
функціональні AE2-бази лишаються там, де логічні (inscriber, molecular_assembler, crafting_unit,
storage cell, pattern terminal, wireless), а всі тірові/гейт-матеріали — на EnderIO+Draconic.
Ладдер: EnderIO alloy/crystal → `grains_of_infinity` → `draconium` → `wyvern_core` →
`awakened_draconium`/`awakened_core` → `dragon_heart` → `chaos_shard`/`chaotic_core`.
Прогресія:
1. `machine_core` — базовий компонент (`vibrant_alloy_ingot` + `ae2:engineering_processor` + `draconium_core`).
2. Машини `advanced_inscriber`, `charger`, `fluix_aggregator` = machine_core + AE2-аналог + `grains_of_infinity`/`dark_steel`.
3. У цих машинах робляться проміжні матеріали мода (НАВМИСНО без крафту, бо машинні):
   `fluix_steel`, `carbonic_fluix_complex`, `space_gem` (fluix_aggregator) і `parallel_processor` (advanced_inscriber).
4. Решта — крафти на основі machine_core + проміжних матеріалів:
   - столи крафту basic→advanced→elite→ultimate;
   - молекулярні асемблери basic→advanced→elite→ultimate;
   - бездротові конектори basic→advanced→elite→ultimate;
   - термінали патернів basic→advanced→elite→ultimate; патерни basic→…→ultimate;
   - Massive Crafter (8 компонентів мультиблоку);
   - інструменти: network_analyzer, wireless_connector, cable_auto_router;
   - unlimited item/fluid storage cell; модулі speed / recipe_multiplier; кабельні частини advanced/elite/flawless;
   - speculation_core x1 (крафт) → x2…x64 (подвоєння + carbonic_fluix_complex).

**Топ-гейти (max-hardcore):** `ultimate_*` тіри — на `awakened_draconium`/`awakened_core`/`dragon_heart`;
`unlimited_*` комірки — `awakened_draconium_ingot` + `dragon_heart`;
`infinite_cell` — найвищий гейт: апгрейд `unlimited_item_storage_cell` через `chaos_shard` + `chaotic_core` +
`awakened_draconium_block` + `dragon_heart` (тепер craftable як ультра-ендгейм).

**Валідація:** усі ID звірені з реальними реєстрами модів — next_ae 49 (lang), ae2 20, enderio 13,
draconicevolution 12; лінт без помилок. Скрипт також скопійовано в інстанс
`…\.minecraft\versions\ModPack\kubejs\server_scripts\recipes\`.

> Застосування: рецепти підхопляться при старті світу або командою `/reload`. Перегляд дерева крафту — у JEI/EMI.

## Файли, змінені цією роботою
- `mods/` — додано 12 jar-ів.
- `modlist.txt` — перегенеровано (129 рядків).
- `overrides/kubejs/data/projecte/pe_custom_conversions/ae2_base.json` — новий датапак EMC.
- `overrides/kubejs/server_scripts/recipes/02_next_ae_recipes.js` — крафт-рецепти next_ae (51 шт.).
- `docs/ae2-integration-plan.md` — цей документ.
