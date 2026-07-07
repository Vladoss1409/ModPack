---
name: "Applied Energistics 2"
modId: "ae2"
version: "15.4.10"
category: tech
tags:
  - ae2
  - storage
  - automation
  - network
links:
  curseforge: "https://www.curseforge.com/minecraft/mc-mods/applied-energistics-2"
  modrinth: "https://modrinth.com/mod/ae2"
  wiki: "https://guide.appliedenergistics.org/"
draft: false
---

## Обзор

**Applied Energistics 2 (AE2)** — цифровая система хранения и автоматизации. Все предметы хранятся в виде «данных» на ячейках памяти внутри ME-сети, доступ — через терминалы. Основа T3 «Сеть».

## С чего начать

1. Соберите **Certus Quartz** и вырастите кристаллы (Crystal Growth Accelerator ускоряет).
2. Скрафтите **ME Drive**, **Storage Cells (1k–256k)**, **ME Terminal**, **ME Controller**.
3. Свяжите всё кабелями и подайте энергию (FE/RF через Energy Acceptor).

## Ключевые механики

| Понятие | Зачем |
|---------|-------|
| Каналы | Каждое устройство требует канал; базовый кабель даёт 8, Dense — 32 |
| ME Controller | Ядро сети, снимает лимит на каналы (см. схему ниже) |
| Autocrafting | Pattern Provider + Molecular Assembler собирают предметы по запросу |
| P2P Tunnel | Передача каналов/энергии/жидкостей на расстояние |

## Мультиблок

Схема и правила сборки контроллера: [ME Controller](../../machines/ae2-me-controller/).

## Связь с квестами

Открывается в T3 «Сеть» — основной справочник AE2 и сайд-ветка «Молекулярная сеть».

## Советы

- Не превышайте 7 блоков контроллера в одной сети (без P2P).
- Для больших баз используйте Dense Cable и P2P, чтобы не упираться в каналы.
- Официальный гайд: [guide.appliedenergistics.org](https://guide.appliedenergistics.org/).
