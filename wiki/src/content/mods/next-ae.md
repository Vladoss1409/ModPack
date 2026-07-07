---
name: "Next AE"
modId: "next_ae"
version: "1.0.0+1.20.1"
category: tech
tags:
  - ae2
  - autocraft
  - multiblock
  - endgame
links:
  curseforge: "https://www.curseforge.com/minecraft/search?class=mc-mods&search=next_ae"
  modrinth: "https://modrinth.com/mods?q=next_ae"
draft: false
---

## Обзор

**Next AE** — дополнение к [Applied Energistics 2](../appliedenergistics2-forge/), добавляющее **эндгейм-мультиблок для массового автокрафта** — «Massive Crafter». Работает поверх [Next Core](../next-core/).

> Мод нишевый; официальная документация ограничена. Ниже — как он используется в этой сборке. Точные рецепты и ёмкости смотрите в **JEI/EMI** и в квесте Patchouli.

## Массивный сборщик (Massive Crafter)

Это большой многоблочный аналог **Crafting CPU** из AE2 — рассчитан на параллельный крафт огромных объёмов.

Схема сборки, размещение и порядок блоков подробно разобраны в разделе [Механизмы → Massive Crafter](../../machines/next-ae-massive-crafter/).

Кратко:

1. Постройте замкнутый корпус: **каркас + стены + стекло**.
2. Внутри разместите **ядро (контроллер)**, **pattern provider** и **accelerator**.
3. Подключите к **ME-сети** и подайте **энергию**.
4. Загрузите шаблоны — крафт идёт параллельно в большом объёме.

## Роль в сборке

Финальная ступень автокрафта (T5 «Схождение»): когда обычных CPU AE2 уже мало, Massive Crafter обрабатывает массовые заказы.

## Где узнать больше

- Пошаговая сборка мультиблока — [Механизмы → Massive Crafter](../../machines/next-ae-massive-crafter/).
- Базовая библиотека — [Next Core](../next-core/).
- Основы автокрафта — [Applied Energistics 2](../appliedenergistics2-forge/).
