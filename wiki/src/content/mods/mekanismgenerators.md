---
name: "Mekanism Generators"
modId: "mekanismgenerators"
version: "10.4.16"
category: tech
tags:
  - mekanism
  - energy
  - generators
links:
  curseforge: "https://www.curseforge.com/minecraft/mc-mods/mekanism-generators"
  modrinth: "https://modrinth.com/mod/mekanism-generators"
draft: false
---

## Обзор

**Mekanism Generators** — официальный модуль генерации энергии для [Mekanism](../mekanism/). Даёт всё: от простого сжигания топлива до **термоядерного реактора**. Энергия в **Joule (J)**, но совместима с RF/FE.

## Генераторы

| Генератор | Источник энергии |
|-----------|------------------|
| **Heat Generator** | Сжигание топлива/лава (стартовый) |
| **Gas-Burning Generator** | Горючие газы (водород, этилен) — очень мощный |
| **Bio-Generator** | Биотопливо |
| **Solar / Advanced Solar Generator** | Солнечная энергия |
| **Wind Generator** | Ветер (эффективнее на высоте) |
| **Fission Reactor** (многоблок) | Ядерное деление — огромная мощность, требует охлаждения и контроля |
| **Fusion Reactor** (многоблок) | Термоядерный синтез — эндгейм, нужен D-T-топливо и лазерный поджиг |
| **Industrial Turbine** (многоблок) | Превращает пар (в т.ч. от реактора) в энергию |

## Прогрессия энергетики

1. **Heat Generator** — на старте.
2. **Gas-Burning** на этилене (Bio → Substrate → Ethylene) — мощный средний этап.
3. **Fission Reactor + Industrial Turbine** — промышленная мощность (осторожно: перегрев = взрыв/радиация).
4. **Fusion Reactor** — вершина: стабильная гигантская мощность.

## Как использовать

- Ставьте генератор, подавайте топливо/газ, снимайте энергию кабелями Mekanism или через [Flux Networks](../fluxnetworks/).
- Многоблоки (Fission/Fusion/Turbine) строятся по схемам — следите за охлаждением и безопасностью.

## Роль в сборке

Основная «электростанция» технической ветки: от первых машин Mekanism до питания AE2 и эндгейм-производств.

## Где узнать больше

- База Mekanism, газы, безопасность реакторов — [Mekanism](../mekanism/).
- Беспроводная раздача энергии — [Flux Networks](../fluxnetworks/).
- Схемы многоблоков — **JEI/EMI** и встроенные подсказки.
