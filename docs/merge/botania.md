# Маніфест переносу: видалення **Botania**

Джерело: `C:\Users\vlado\Desktop\ТехноМагия\ТехноМагия` (далі `TM/`).
Призначення: `MyModPack` (гілка `merge/technomagic`).
Карта зв'язків: `technomagic-modmap.canvas.tsx` (схема «мод → файли»).

**Рішення:** ботанічну гілку в MyModPack НЕ переносимо (`skip_all`). Scope переносу — `everything` з фільтрацією по видалених модах.

---

## 0. Ботанічна гілка (моди, що видаляються разом із Botania)

Усі hard-залежать від `botania` (за `dependency-graph`), тож виключаються як одне ціле:

`botania`, `aiotbotania`, `extrabotany`, `mythicbotany`, `appbot` (Applied Botanics), `kubejs_botania`.

> `next_botany` — окремий «next»-плагін, НЕ частина botania-гілки, але його контент посилається на `botania:*`. Рішення по ньому — на кроці обробки `next_botany`. Тут лише прибираємо його botania-посилання (див. §3).

---

## 1. MyModPack — зроблено (commit на гілці)

Прибрано мертві посилання на Botania (мода в MyModPack немає):
- `overrides/config/supplementaries-common.toml` — `clean_blacklist`: 5× `botania:*`
- `overrides/config/entityculling.json` — 4× `botania:*`
- `overrides/config/blue_skies-common.toml`, `patchouli-client.toml` — приклади в коментарях
- `assets/ftbquests/lang/{en_us,ru_ru,pt_br,es_es,es_mx,zh_cn}.json` — ключі `botania_mana`

---

## 2. EXCLUDE — НЕ переносити з TM (власні файли ботанічної гілки)

### config/
- `config/botania-common.toml`
- `config/botania-client.toml`
- `config/extrabotany-common.toml`
- `config/extrabotany-client.toml`
- `config/mythicbotany-client.toml`
- `config/mythicbotany.json5`
- `config/aiotbotania-common.toml`
- `config/aiotbotania-client.toml`

### kubejs/assets/
- `kubejs/assets/botania/**` (13 файлів: моделі `quartz_*`, patchouli `mythicbotany_infuser`/`infuser`, `lang/ru_ru.json`)
- `kubejs/assets/aiotbotania/lang/ru_ru.json`
- `kubejs/assets/extrabotany/lang/ru_ru.json`
- `kubejs/assets/mythicbotany/lang/ru_ru.json`

### kubejs/scripts (повністю botania)
- `kubejs/client_scripts/tooltips/botania.js` — тултіпи вартості мани (увесь файл)

---

## 3. REWRITE — переносимо файл, але прибираємо botania-частини

| Файл (TM/) | Що прибрати |
|---|---|
| `kubejs/startup_scripts/technomagic/item.js` | `//region Botania` (рядки 24–67): `quartz_*_ingot`, `big_petal_*`, `flower_*`, `botania_heart` |
| `kubejs/startup_scripts/technomagic/rarity.js` | botania-записи (вкл. `botania:creative_pool` L677 та rarity для technomagic-пелюсток/кварців) |
| `kubejs/startup_scripts/next/blood/souls.js` | душі `botania:doppleganger1/2/3` (L54–97) + loot `botania:ender_air_bottle` (L392) |
| `kubejs/client_scripts/technomagic/lang.js` | `//region Botania` (L26–35), вкл. `botania_heart` |
| `kubejs/client_scripts/tooltips/limit.js` | `//region Botania` (L92–93, `botania:loonium`), `botania:spark` (L254) |
| `kubejs/client_scripts/tooltips/info.js` | записи з `botania/aiotbotania/mythicbotany/extrabotany` (L65, L78, L91) |
| `kubejs/client_scripts/tooltips/next_botany.js` | `botania:spark` (L10); решту next_botany лишити (див. §0) |
| `kubejs/assets/ftb_quests/lang/ru_ru.json` | рядки квестів про Botania |

### config — дрібні згадки (прибрати рядок при переносі)
- `config/patchouli-client.toml` — приклад у коментарі
- `config/titanium/titanium-tags.toml` — botania-тег
- `config/apotheosis/names.cfg` — botania-ім'я
- `config/raised.json` — botania-запис
- `config/sound_physics_remastered/allowed_sounds.properties` — botania-звук

---

## 4. Наслідки для modlist MyModPack

НЕ додавати jar: `Botania`, `aiotbotania`, `extrabotany`, `MythicBotany`, `Applied-Botanics` (appbot), `kubejs_botania`.
Перевірити інші видалені моди на hard-dep `botania` під час їх обробки: `allthecompressed` (optional — ок), `mysticalagriculture`/`mysticalagradditions` (рецепти всередині jar — нас не стосуються).

---

## 5. Статус

- [x] MyModPack: мертві посилання прибрано + коміт
- [x] TM: EXCLUDE/REWRITE списки складено (за схемою)
- [ ] Застосувати EXCLUDE/REWRITE під час фінального pull (після проходу всіх видалених модів)
