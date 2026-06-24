# CoopTech Test — налаштування сервера

## Вимоги
- Java 17
- 8 GB RAM (виділити JVM 6G)
- Forge 1.20.1 (47.4.10)

## Кроки
1. Завантажте Forge 1.20.1 installer з https://files.minecraftforge.net/
2. Створіть server.jar через installer (Install server).
3. Скопіюйте всі mods крім client-only (див. client-only-mods.txt).
4. Скопіюйте overrides/config, defaultconfigs, kubejs, datapacks.
5. Запустіть один раз, погодьтесь EULA (eula.txt -> eula=true).
6. server.properties: max-players=2, difficulty=hard, spawn-protection=0, **enable-command-blocks=true**.
7. Whitelist двох гравців.

## CustomNPCs + FTB Quests

1. Мод **CustomNPCs-Unofficial** — на клиент и сервер (`scripts/install_mods.py`).
2. `NpcUseOpCommands=true` в config CNPC (після першого запуску) — для dialog → FTB commands.
3. Лager NPC у спавну — [docs/npc-design.md](docs/npc-design.md), [bootstrap/customnpcs/README.md](overrides/bootstrap/customnpcs/README.md).
4. Диспетчер: dialog command `ftbquests change_progress @dp complete T101000000000021`

## Мониторинг RAM (Spark)

- Baseline VPS: 8 GB, JVM `-Xms6G -Xmx6G`
- Якщо steady >5.8G: VPS 10 GB, `-Xmx7G` — [docs/hosting-budget.md](docs/hosting-budget.md)
- `/spark profiler --timeout 120` при 2 гравцях онлайн

## Client-only (не на сервер)
- embeddium
- oculus
- entityculling
- journeymap

> **Не ставьте** `textrues_embeddium_options` — Embeddium 0.3.31+ помечает его как несовместимый. Настройки видео уже встроены в Embeddium (Video Settings в меню).

## Pregen (Chunky)
Після першого успішного старту встановіть Chunky мод на сервер або використайте плагін-аналог через мод — для test достатньо прогнати `/chunky start 5000` якщо Chunky додано.

## Aternos / MineStrator
Оберіть Custom Forge 1.20.1, завантажте zip папки mods + configs.
