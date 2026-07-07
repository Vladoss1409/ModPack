---
name: "Applied Mekanistics"
modId: "appmek"
version: "1.4.3"
category: tech
tags:
  - ae2
  - mekanism
  - chemicals
  - integration
links:
  curseforge: "https://www.curseforge.com/minecraft/mc-mods/applied-mekanistics"
  modrinth: "https://modrinth.com/mod/applied-mekanistics"
draft: false
---

## Обзор

**Applied Mekanistics** — официальный мост между [Applied Energistics 2](../appliedenergistics2-forge/) и [Mekanism](../mekanism/). Он позволяет хранить и автокрафтить **химические вещества Mekanism** (газы, жидкости, слизь, пар) прямо в ME-сети — как обычные предметы.

## Ключевые предметы

| Предмет | Назначение |
|---------|-----------|
| **Chemical Storage Cell (1k–256k)** | Ячейки для хранения газов/химикатов в ME-сети |
| **Chemical Portable Cell** | Переносная ячейка под химикаты |
| **Chemical Storage Bus** | Читает содержимое химических баков Mekanism в сеть |
| **Chemical P2P Tunnel** | Передача химикатов через P2P-туннели AE2 |

## Как использовать

1. Соберите **Chemical Storage Cell** и вставьте в обычный **ME Drive** — теперь сеть хранит газы (кислород, водород, хлор и т.д.).
2. Подключайте баки/машины Mekanism через **Chemical Storage Bus** — их содержимое станет видно в терминале.
3. Настраивайте **автокрафт** химии: паттерны с газами работают как обычные рецепты AE2 (например, автопроизводство кислорода/кислот для 3x–5x переработки руды).

## Роль в сборке

Ключевой элемент связки **Mekanism + AE2**: убирает ручное управление газами. Позволяет автоматизировать переработку руды 5x, где нужны кислород и кислоты, без десятков баков.

## Где узнать больше

- Про газы и переработку — [Mekanism](../mekanism/).
- Про ячейки и хранилища — [Applied Energistics 2](../appliedenergistics2-forge/).
