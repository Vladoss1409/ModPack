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

## 1. Додані моди (117 → 129)

### Аддони з `decompiled\mods`
| Jar | modId | Нотатки |
|---|---|---|
| AdvancedAE-1.3.2-1.20.1.jar | advanced_ae | ae2 ≥15.4.9 ✓; ae2addonlib вшито (jarjar) |
| ExtendedAE-1.20-1.4.8-forge.jar | expatternprovider | потребує guideme ✓ + glodium (додано) |
| Glodium-1.20-1.5-forge.jar | glodium | обовʼязкова залежність ExtendedAE |
| megacells-forge-2.4.6-1.20.1.jar | megacells | cloth_config ✓; appmek ✓ (хім.), appliede (EMC) |
| mae2-1.6.1.jar | mae2 | mixinextras вшито; gtceu відсутній → EU-тунель інертний |
| merequester-forge-1.20.1-1.1.5.jar | merequester | ae2 ✓ |
| next_ae-1.0.0+1.20.1-client.jar | next_ae | потребує Draconic Evolution 3.1.2.621 ✓; Registrate вшито; **«-client» збірка — перевірити на сервері** |
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
- [ ] **Реальний запуск гри/сервера** (особливо `next_ae` як «-client» збірка) — `scripts/launch_smoke_test.py` прив'язаний до чужого шляху (`C:\Users\GameOn_Dp\...`) і потребує `minecraft_launcher_lib`; виконати на цільовій машині.
- [x] **EMC-цінності** (2026-06-29): датапак валідний (JSON, формат ProjectE `values.before`), 6 кореневих значень підтверджено. Рішення — лишити як є; решта рахується ProjectE автоматично. Балансування за смаком — за потреби пізніше.

## Файли, змінені цією роботою
- `mods/` — додано 12 jar-ів.
- `modlist.txt` — перегенеровано (129 рядків).
- `overrides/kubejs/data/projecte/pe_custom_conversions/ae2_base.json` — новий датапак EMC.
- `docs/ae2-integration-plan.md` — цей документ.
