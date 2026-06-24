# Чеклист: первый запуск CoopTech Test

> **Интерактивный чеклист (кликабельный):** открой в браузере  
> [`prologue-checklist.html`](prologue-checklist.html) — двойной клик по файлу.  
> Галочки сохраняются автоматически.
>
> В Cursor `.md` галочки часто **не кликаются** — используй HTML-версию.

---

## A. Перед миром (один раз)

- [ ] Java 17
- [ ] Forge 1.20.1 (47.4.x)
- [ ] В `mods\` все jar из `CoopTech-Test\mods\` (**без CustomNPCs**)
- [ ] Папка `overrides\` скопирована в корень инстанса (`python scripts/sync_to_tlauncher.py`)
- [ ] Клиенту выделено 6 GB RAM
- [ ] Игра через VPS (не локальный сервер на том же ПК)

### Сервер (VPS)

- [ ] JVM: `-Xms6G -Xmx6G`
- [ ] `enable-command-blocks=true`
- [ ] `spawn-protection=0`, `max-players=2`

---

## B. Первые 10 минут в мире

- [ ] Оба игрока в одной FTB Team
- [ ] Gr → **Кодекс экспедиции** → Welcome → Guides → Prologue
- [ ] Тема фиолетовая, список глав **белый на фиолетовом** (см. ниже «Тема книги»)
- [ ] Первый квест закреплён (pin)
- [ ] Welcome «Сигнал якоря» завершён — получены **Журнал** и **Страница #0**

---

## C. Лагерь (без NPC)

- [ ] `/function cooptech_world:camp/force` или deploy через `deploy_camp_world.py --preset test1 --force`
- [ ] Лагерь у world spawn: костёр, палатки, сундук, таблички
- [ ] **Брифинг** — §eПКМ§r по `kubejs:journal_page_00` (не NPC)
- [ ] Лор диспетчера — в **Журнале экспедиции** (Patchouli) и в чате при ПКМ по странице

---

## D. Prologue — волна 1 (2 из 4)

- [ ] Крафт: Cooking Pot + 3 блюда FD
- [ ] Кооп-база: 64 oak_log + chest
- [ ] Исследование: Nature's Compass + новый биом
- [ ] Добыча: 64 raw_iron
- [ ] Gate 1 «Стабилизация лагеря»

---

## E. Prologue — волна 2 (2 из 4)

- [ ] «Усиление сигнала» + маяк в инвентаре
- [ ] Explorer's Compass
- [ ] 48 raw_iron + 32 raw_copper
- [ ] smithing table + cutting board
- [ ] Кооп: оба ПКМ с маяком у спавна (2/2)
- [ ] Gate 2 «Резонанс якоря» + anchor_shard_01

---

## F. Финал Prologue

- [ ] Пайки: 16 cooked_beef + 8 golden_carrot
- [ ] **Приказ диспетчера:** ПКМ по **Странице #0** после Рубежа II (advancement `dispatcher_briefing`)
- [ ] Финал: stabilized_shard_01 + 32 bricks + 16 lanterns
- [ ] Ch1 Foundation открылась

---

## G. После сессии

- [ ] Prologue пройден duo без softlock
- [ ] RAM клиента (F3) → `docs/hosting-budget.md`
- [ ] RAM сервера (Spark) → `docs/hosting-budget.md`
- [ ] Заметки по багам / балансу

---

## Быстрая помощь

| Проблема | Решение |
|----------|---------|
| Серая книга квестов | **Полный перезапуск** после sync. Тема подгружается автоматически. Вручную: внизу книги квестов кнопка **Edit Settings** → **Reload Theme**. Дополнительно: Resource Packs → **CoopTechTheme** |
| Маяк «далеко от лагеря» | Подойти к world spawn |
| Кооп не засчитывается | FTB Team + оба ПКМ с маяком |
| Журнал / ранние страницы | **Полный перезапуск** (не `/reload`). ПКМ в основной руке |
| Брифинг не засчитывается | Сначала Рубеж II, затем ПКМ по **journal_page_00** |
