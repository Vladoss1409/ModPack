---
name: "Mekanism Digital Miner"
modId: "mekanism"
modSlug: "mekanism"
structure: "mekanism_digital_miner"
category: multiblock
tags:
  - mekanism
  - mining
  - automation
placement:
  - "Контроллер снизу по центру"
  - "Valve — для энергии и вывода руды"
  - "Над рамой — рабочая зона (воздух)"
draft: false
---

## Назначение

**Digital Miner** — автоматическая добыча руды в заданном радиусе. Ключевой блок для автоматизации добычи в T2.

## Сборка

1. Постройте раму 3×3×4 из **Structural Glass** или **Steel Casing** (упрощённая схема).
2. **Digital Miner** — в центре нижнего ряда.
3. **Valve** — на боковых гранях для кабелей и труб.

## Настройка

- Откройте GUI майнера.
- Задайте радиус (квадратные чанки).
- Настройте фильтр: whitelist/blacklist руд.
- Подайте энергию через Universal Cable.

## Вывод ресурсов

- Подключите Logistical Transporter к Valve.
- Или используйте внутренний буфер и периодическую выгрузку.

## Типичные ошибки

- **Не копает** — проверьте энергию и фильтры.
- **Застревает** — уменьшите радиус или замените блоки в зоне.
