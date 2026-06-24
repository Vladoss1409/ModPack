# Bootstrap — CustomNPCs data

CNPC хранит NPC/диалоги в `world/customnpcs/`. Эта папка — **инструкция и шаблон**, не готовый мир.

## Быстрый старт (первый раз)

1. Установите `CustomNPCs-Unofficial` (Forge 1.20.1) на клиент и сервер.
2. Синхронизируйте overrides: `python scripts/sync_to_tlauncher.py`
3. В мире **CoopTech Expedition** (сид `5998437775939784656`), OP + Creative.
4. Встаньте на месте лагеря → `/function cooptech:camp/build`  
   Подробно: [docs/camp-build-guide.md](../../docs/camp-build-guide.md)
5. Создайте NPC на цветных маркерах по [docs/npc-design.md](../../docs/npc-design.md).
5. **Global → Dialogs** — категория `CoopTech/Prologue`.
6. Диспетчер: диалог «Брифинг» → опция **Command**:  
   `ftbquests change_progress @dp complete T101000000000021`
7. Экспорт: Global → **Export** → сохраните в эту папку для бэкапа.

## Кооп-маяк (без CNPC-квестов)

Игроки используют предмет **`kubejs:resonance_beacon`** (награда волны 2) — ПКМ у спавна в радиусе 48 блоков. Скрипт: `kubejs/server_scripts/quests/coop_beacon.js`.

## Лагерь — минимальная постройка

```
  [Nastavnik]     [Dispatcher]     [Vendor]
       ·              ·               ·
            [ Coop marker / fire ]
                    spawn
```

Координаты относительно world spawn; Y — поверхность.
