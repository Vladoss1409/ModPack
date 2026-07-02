# CoopTech Quests — статус реализации

**План:** [Квестовое дерево.md](Квестовое%20дерево.md) · **Актуальная модель:** T0–T5 + 17 сайд-веток + post-T5 (хаб + 3 сайди)

## Готово

### Основная линия (T0–T5)
- `main_t0_rift.snbt` … `main_t5_convergence.snbt` — ~28 квестов на тир
- Шаблон: intro → 3 волни (4 pool + gate 2/4) → prep → finale
- **Блокировка веток:** волна N+1 залежить від gate + квест тієї ж колонки
- **Ланцюжок тирів:** інтро T(n) залежить від фіналу T(n−1) (`…26` для T0, `…1A` для T1+)
- Журнал T0 + заглушки T1–T5 у `journal_quest_unlocks.js`
- Записки-нагороди на маяках, лор у описах квестів

### Сайд-ветки (17 глав)
- Генератор: `scripts/quests_build_sides.py`
- Гібридний lock: квест «Рубеж не пройден» + дерево `hide_quest_until_deps_visible`
- Прив'язка до рубежів main-тиру (див. `SIDE_TIER_GATES` у скрипті)

| Сайд | Відкривається після |
|------|---------------------|
| Kitchen, Storage | T0 · gate 1 |
| Bestiary | T0 · gate 2 |
| Thermal, Powah | T1 · gate 1 |
| IE, Apotheosis, Silent Gear | T1 · gate 2 |
| Flux, Mekanism, Ender IO | T2 · gate 1 |
| Arcane | T2 · gate 2 |
| Network (AE2) | T3 · gate 1 |
| Twilight | T3 · gate 2 |
| Draconic | T4 · gate 1 |
| Cataclysm, Relics | T4 · gate 2 |

### Після якоря (post-T5)
- Генератор: `scripts/quests_build_post_anchor.py`
- Група FTB: `Після якоря` (`B100000000000006`)
- Хаб `main_post_anchor.snbt` — після фіналу T5 (`reality_anchor_core`)
- Три ветки (кожна потребує відповідну гілку хаба + фінал T5):

| Сайд | Відкривається |
|------|----------------|
| Печери розлому | Хаб → «Печери» |
| Бос-фарм якоря | Хаб → «Бос-фарм» |
| Епілог модів | Хаб → «Епілог» |

### UX
- `default_hide_dependency_lines: true` — лінії при hover
- `progression_mode: "default"` на всіх главах
- Тема: `ftb_quests_theme.txt` (тонкі лінії)

## В роботі / далі

1. **Patchouli-справочник** T1–T5 (механізми по таймінгу квестів)
2. **Повні лор-тексти** записок T1–T5 (`cooptechReadJournalPage`)
3. **Російські назви** квестів у сайдах (зараз EN з manifest)
4. **Welcome / Guides** — опційно повернути як вступні вкладки
5. **Валідатор item ID** у квестах (next_ae, cataclysm, silentgear)
6. `sync_to_tlauncher.py` — шлях інстансу vlado/ModPack

## Збірка (важливо)

```bash
python scripts/quests_build_tiers.py   # T1–T5 (не чіпає T0)
python scripts/quests_build_sides.py   # 17 сайдів
python scripts/quests_build_post_anchor.py  # хаб + 3 post-T5 сайди
```

**Не запускати** `quests_build_v1.py` без потреби — перезапише старі `main_*` і видалить `main_t*`.

Після змін: скопіювати `overrides/config/ftbquests/` в інстанс → закрити гру → `/ftbquests reload`.

**Не включати Editing Mode** в FTB Quests — ламає SNBT.
