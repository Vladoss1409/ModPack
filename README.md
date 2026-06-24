# MyModPack — кооперативна збірка (Forge 1.20.1)

**Версія:** 0.1.0  
**Гравці:** 2 (кооп)  
**Фокус:** Tech (AE2) + легка магія + боси + виміри + FTB Quests

## Швидкий старт (TLauncher / Forge)

1. Встановіть **Java 17** (вже є в системі).
2. Створіть профіль **Minecraft 1.20.1** + **Forge 47.4.x** (рекомендовано 47.4.10).
3. Скопіюйте в папку `mods` інстансу **усі `.jar` з `mods/`**.
4. Скопіюйте папку **`overrides/`** повністю в корінь інстансу (merge `config`, `kubejs`, `defaultconfigs`, `datapacks`).
5. Виділіть **6 GB RAM** (лаптоп 16 GB).
6. Перший запуск — 3–10 хв (ModernFix + багато модів).

## Сервер (оренда 8 GB)

1. Forge 1.20.1 server + Java 17.
2. Скопіюйте `mods/` **без client-only** (див. `client-only-mods.txt`).
3. JVM: `-Xms6G -Xmx6G`.
4. Після першого запуску — pregen overworld (Chunky, радіус 3000–5000).

## Що в тестовій версії

- 117 модів, 3 datapack (Terralith, Incendium, Nullscape)
- Repurposed Structures — як **мод** (не datapack)
- **Aether** — jar з позначкою NeoForge; на Forge 47 може потребувати перевірки. Якщо краш — тимчасово приберіть `aether*.jar` і `cumulus*.jar`
- **FTB Quests v0.2:** Prologue эталон (16 квестов, 2 волны); Ch1–3 базовые; Ch4–12 WIP
- **CustomNPCs-Unofficial** + CNPC лager (ручная настройка, см. docs/npc-design.md)
- **Ore Excavation** + **LootJS** + **Аномальные реликварии** (KubeJS)
- Деталі: [docs/quests-status.md](docs/quests-status.md)

## Скрипти

- `scripts/install_mods.py` — повне завантаження з Modrinth
- `scripts/install_missing.py` / `install_cf_edge.py` — дозавантаження
- `scripts/sync_to_tlauncher.py` — перенос overrides у TLauncher «Мой мод пак» (див. [docs/tlauncher-test.md](docs/tlauncher-test.md))

## Відомі обмеження test

- FTB Quests — Prologue + Ch1–3 повні; Ch4–12 WIP (див. docs/quests-status.md)
- TLauncher + орендований сервер може не працювати (online-mode)
- Перевірте стабільність перед довгим проходженням

## Оновлення test → release

1. Прогнати 2+ години в duo.
2. Зафіксувати конфлікти рецептів (Polymorph/JEI).
3. Написати FTB Quests глави + RU переклад.
