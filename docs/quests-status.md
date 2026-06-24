# CoopTech Quests — статус реализации

**План:** [Квестовое дерево.md](Квестовое%20дерево.md) · **Pivot v0.4:** quest-only, без CustomNPCs

## Готово (v0.4 — quest tree scaffold)

- **quests_build_v1.py** — генератор 16 глав (`main_*` + `side_*`), удалены `tm_*`
- **Welcome** (8) + **Guides** (10) — журнал, кодекс, кооп-маяк
- **Prologue** — из backup, тексты без NPC (запись диспетчера = журнал §8#0§r)
- **Ch1–Ch3** — из backup (Foundation, Surface, Flux)
- **Ch4–Ch6** — scaffold + gate placeholder
- **8 сайдов** — lock-квест + 2 узла WIP
- **UX:** тонкие линии, `default_hide_dependency_lines: true`
- **Журнал:** unlocks для Welcome/Guides + Prologue milestones
- **Лагерь:** без NPC-маркеров; CustomNPCs убран из modlist/install

## Готово (v0.3)

- KubeJS предметы, Patchouli-журнал, FTB theme, sync TLauncher

## Следующие шаги (волна B→D)

1. Наполнить Ch1–Ch3 pool/gate текстами (не checkmark-заглушки где возможно)
2. Journal Patchouli entries для Welcome/Guides gates
3. Ch4–Ch6 полный контент (~87 квестов)
4. Сайды — полные деревья после установки Flux/Draconic/Silent Gear
5. Duo playtest Prologue по [prologue-checklist.md](prologue-checklist.md) (секция NPC удалена)

## Сборка

```bash
python scripts/quests_build_v1.py   # пересобрать SNBT
python scripts/sync_to_tlauncher.py # в инстанс
```

**Не включать Editing Mode** в FTB Quests — ломает SNBT.
