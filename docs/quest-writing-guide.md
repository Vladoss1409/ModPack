# CoopTech — guide-first описания квестов

## Шаблон

```
[Сюжет 1–2 предложения]

Цель: …

Как выполнить:
1. …
2. …

Кооп: …

Подсказка: JEI → «…»

Не делайте: …

Награда поможет: …
```

## Чеклист

- [ ] Нумерованные шаги
- [ ] Имя для JEI / Compass
- [ ] Блок «Не делайте» где нужно
- [ ] Кооп указан
- [ ] Награда не пустая + «Награда поможет»
- [ ] Seed ≥40% следующего крафта
- [ ] Без ссылок на вики

## Pool 2 из 4

На вкладке: «Выполните любые 2 из 4 заданий ниже». Gate-квест: `dependencies: [4 pool IDs]`, `min_required_dependencies: 2`.

**Блокировка:** в каждой главе включены `progression_mode: "linear"`, `hide_quest_until_deps_complete: true` — квест не виден, пока не выполнены зависимости (для gate — минимум 2 из 4). Глобально в `data.snbt`: `progression_mode: "linear"`.

Полный шаблон главы (много квестов, волны, «выплывание» веток): см. **`docs/chapter-structure.md`**.

## Иконки

- Кастомные предметы: `kubejs:…` (текстуры в `kubejs/assets/kubejs/textures/item/`)
- Служебные иконки квестов: `cooptech:textures/quests/gate.png`, `pool.png`, `finale.png`, `chapter_start.png`, `wave.png`
- Регенерация: `python scripts/generate_cooptech_assets.py`

## Награды

- **Seed** — 40–70% материалов следующего квеста
- **Плюшка** — reliquary / XP / utility (не обязательна)
