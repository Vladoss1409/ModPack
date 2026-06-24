# CoopTech Test — контрольная точка разработки

> **Дата:** 2026-06-21  
> **Версия сборки:** v0.4-quest-tree  
> **Инстанс теста:** TLauncher «Мой мод пак»  
> **Статус:** 16 глав FTB scaffold; quest-only (без CNPC); журнал + advancement tasks.

---

## Как вернуться к этой точке

1. Откройте папку `CoopTech-Test/` (репозиторий git).
2. Посмотрите последний коммит: `git log -1`
3. Откат при необходимости: `git checkout <hash>` или `git restore .`
4. Синхронизация в игру: `python scripts/sync_to_tlauncher.py`
5. **Полный перезапуск** Minecraft (не `/reload` для startup/client scripts).

---

## Что работает (подтверждено в тесте)

| Область | Статус |
|---------|--------|
| Страницы журнала #0–12 | ПКМ → lore-текст в чат, без краша |
| Реликварии | ПКМ → лут в инвентарь (`player.give`) |
| Резонансный маяк | Кооп-синхронизация у спавна |
| Тексты Prologue | Фэнтезийные подсказки (без FTB Team / JEI / Gate) |
| FTB Quests | 16 глав (`main_*` + `side_*`), генератор `quests_build_v1.py` |
| Prologue брифинг | ПКМ `journal_page_00` → advancement `dispatcher_briefing` |
| CustomNPCs | **Снят** — прогрессия через FTB + журнал |
| Sync TLauncher | `scripts/sync_to_tlauncher.py` |

---

## В процессе / проверить при возобновлении

| Задача | Примечание |
|--------|------------|
| **Журнал экспедиции (Patchouli GUI)** | Исправлено: `PatchouliAPI` + `client_scripts/journal_open.js`. Нужен retest после перезапуска |
| **FTB тема (фиолетовая книга)** | Авто-reload + ресурспак `CoopTechTheme`; кнопка **Edit Settings** внизу книги |
| **Duo playtest Prologue** | ~1.5–2 ч, [prologue-checklist.md](prologue-checklist.md) — без NPC |
| **Ch4–Ch6 + сайды** | Scaffold WIP, [Квестовое дерево.md](Квестовое%20дерево.md) |

---

## План продолжения (порядок)

1. **Sync + retest** — `python scripts/quests_build_v1.py` → `sync_to_tlauncher.py` → полный перезапуск
2. **Duo playtest** — Welcome → Guides → Prologue до Ch1 (журнал вместо NPC)
3. **Волна B** — real tasks в Welcome/Guides; Patchouli entries для gates
4. **RAM / hosting** — F3 + Spark → [hosting-budget.md](hosting-budget.md)
5. **Ch1–3** — тексты + journal unlocks; Ch4–6 контент

---

## Ключевые файлы (v0.3)

| Файл | Назначение |
|------|------------|
| `overrides/kubejs/startup_scripts/items/cooptech_items.js` | Предметы, `.use()` / `.finishUsing()` |
| `overrides/kubejs/server_scripts/items/cooptech_interact.js` | Lore страниц, лут реликварий, маяк, открытие журнала (API) |
| `overrides/kubejs/client_scripts/journal_open.js` | Открытие Patchouli на клиенте |
| `overrides/kubejs/client_scripts/ftb_theme.js` | Авто-reload темы FTB |
| `overrides/config/ftbquests/quests/chapters/main_*.snbt` | 16 глав квестов |
| `scripts/quests_build_v1.py` | Генератор глав из backup + scaffold |
| `overrides/kubejs/assets/cooptech/patchouli_books/expedition_journal/` | Книга журнала |
| `overrides/resourcepacks/CoopTechTheme/` | Тема FTB (ручное включение опционально) |
| `scripts/sync_to_tlauncher.py` | Деплой в TLauncher |
| `scripts/fix_ftb_snbt.py` | BOM, disable_jei, flatten items |
| `scripts/generate_cooptech_assets.py` | Текстуры и иконки |

---

## Известные ограничения

- **Не включать Editing Mode** в FTB Quests — ломает SNBT → air → краш JEI
- **Startup scripts** требуют полного перезапуска MC
- **Loot tables** в `overrides/data/` не используются для реликварий — лут через KubeJS `player.give()`
- Quest SNBT после sync — read-only в инстансе

---

## История сессии (кратко)

- Исправлен краш страниц журнала (`playSound` → `/playsound`)
- Реликварии: пустой инвентарь → прямой выдачей предметов
- Страницы журнала: уникальный lore, не дублируют квесты
- Prologue SNBT: фэнтезийные формулировки
- Журнал Patchouli: переход с `runCommandSilent` на API + client script

---

*Следующее обновление этого файла — после duo playtest или крупного milestone.*
