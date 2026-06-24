# CoopTech — дизайн NPC (CustomNPCs)

**Прогрессия:** только FTB Quests. CNPC = диалоги, торговля, атмосфера, триггеры.

## Таксономия (вся сборка)

| Класс | Роли | Прогрессия FTB |
|-------|------|----------------|
| Функциональные | Vendor, Quest Giver (диалог), Trainer, Crafter, Teleporter | Giver → `ftbquests change_progress` |
| Враждебные | Mob, Elite, Boss | kill tasks / joint finale |
| Нейтральные | Ambient, Guard | атмосфера |
| Сюжетные | Companion, Mentor, Antagonist | лор + gate |

## Prologue — лager у спавна (~0, 64, 0)

Разместить в **Creative + CNPC tools** после первого запуска с модом. Экспорт → `overrides/bootstrap/customnpcs/`.

| NPC | Роль | Позиция (пример) | FTB bridge |
|-----|------|------------------|------------|
| **Диспетчер якоря** | Mentor / Giver | 8, 64, 8 | Dialog Command → `ftbquests change_progress @dp complete T101000000000021` |
| **Квартирмейстер** | Vendor | 4, 64, 12 | торговля torch/food за iron |
| **Полевой наставник** | Trainer | -4, 64, 8 | hints: JEI, Excavation, SolCarrot |
| **Кооп-маяк** (декор) | Marker | 0, 64, 4 | KubeJS: ПКМ `resonance_beacon` |
| **Патрульный** | Ambient | 12, 64, 0 | патруль 20 блоков |
| **Техник** | Ambient | -8, 64, 4 | сидит у костра |

## Настройка сервера для CNPC → FTB

1. `server.properties`: `enable-command-blocks=true`
2. `config/customnpcs*.toml` или `.cfg`: `NpcUseOpCommands=true` (только trusted dialogs)
3. Диалог: опция типа **Command** (без `/`): `ftbquests change_progress @dp complete T101000000000021`

## ID задач Prologue для диалогов

| Task ID | Квест |
|---------|-------|
| `T101000000000021` | Брифинг у диспетчера (Joint) |
| `T101000000000015` | Кооп-синхронизация (KubeJS маяк, не CNPC) |

## Ch2+ (шаблон)

- 1 Mentor + 1 Vendor на главу
- Boss CNPC только если нет мода-босса
- Teleporter — после Ch6, не в Prologue
