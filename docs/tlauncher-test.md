# TLauncher — тестовый инстанс

**Профиль:** `Мой мод пак`  
**Путь:** `%APPDATA%\.minecraft\versions\Мой мод пак\`

Все проверки и duo-playtest — здесь, до запуска хостинга.

## Синхронизация изменений

После правок в репозитории `CoopTech-Test/` агент спрашивает:

> **Загрузить изменения для теста?**

При ответе **да** — переносятся:

| Источник | Куда | Действие |
|----------|------|----------|
| `overrides/config/ftbquests/` | `config/ftbquests/` | **полная замена** |
| `overrides/kubejs/` | `kubejs/` | копия |
| `overrides/resourcepacks/CoopTechTheme/` | `resourcepacks/CoopTechTheme/` | копия |
| `overrides/defaultconfigs/` | `defaultconfigs/` | merge |
| `overrides/data/` | `data/` | merge (loot tables) |
| `overrides/datapacks/` | `datapacks/` | merge (Terralith, Incendium, Nullscape) |

**Не копируется автоматически:** `mods/` (только при `install_mods.py`), миры, CNPC bootstrap в мире.

### Worldgen (Terralith / Incendium / Nullscape) на Forge

На **Forge** эти паки ставятся как **моды** (`.jar` в `mods/`), не как datapacks в мире:

- `Terralith_1.20.x_v2.5.4.jar` + `TerraBlender-forge-…`
- `Incendium_1.20.x_v5.3.5.jar`
- `Nullscape_1.20.x_v1.2.8.jar`

Папка `datapacks/` в мире для них **не нужна**. После добавления jar — **полный перезапуск** и **новый мир** (старые чанки без Terralith не перегенерируются).

Проверка Terralith: `/locate biome terralith:yellowstone` (лорный спавн — см. [world-spawn.md](world-spawn.md))

### Datapacks в новом мире (устаревший путь для Terralith на Forge)

Папка `datapacks/` в корне инстанса **не подключает** генерацию к миру автоматически. Скрипт `setup_world_datapacks.py` оставлен для совместимости, но для CoopTech на Forge используйте **mod jar** (см. выше).

### Команда вручную

```bash
python scripts/sync_to_tlauncher.py
```

### После синхронизации

1. **Minecraft полностью закрыт** перед sync (иначе игра перезапишет квесты при выходе).
2. Полный перезапуск клиента.
3. В книге квестов: **Reload Themes** (если фон/линии не обновились).
4. **Не нажимайте карандаш** (Editing Mode) — он ломает SNBT → «воздух», «?», краш JEI.
5. Если карандаш уже включён: `/ftbquests editing_mode false`

## Хостинг (позже)

На VPS те же `mods/` + `overrides/` (без client-only из `client-only-mods.txt`). Конфиг квестов и kubejs — идентичны тестовому инстансу.
