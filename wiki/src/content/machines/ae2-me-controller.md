---
name: "AE2 ME Controller"
modId: "appliedenergistics2"
modSlug: "appliedenergistics2-forge"
structure: "ae2_controller"
category: network
tags:
  - ae2
  - storage
  - network
placement:
  - "Не более 7 контроллеров в одной сети"
  - "Устройства — в пределах 8 блоков от контроллера"
  - "Кабели соединяют все компоненты"
draft: false
---

## Назначение

**ME Controller** — ядро сети Applied Energistics 2. Без него ME Drive, Terminal и автокрафт не работают.

## Минимальная сеть

1. **ME Controller** — центр.
2. **ME Drive** с Storage Cells — хранилище.
3. **ME Terminal** — доступ игрока.
4. **ME Cable** — соединение.

## Правила сети

| Правило | Детали |
|---------|--------|
| Лимит контроллеров | Максимум 7 блоков контроллера (без P2P) |
| Дистанция | Каждое устройство — до 8 кабелей от контроллера |
| Каналы | Базово 8; расширяется P2P и Dense Cable |

## Расширение

- **Molecular Assembler** — автокрафт.
- **ME Pattern Provider** — подача рецептов.
- **P2P Tunnel** — обход лимита каналов на расстоянии.

## Связь с квестами

T3 «Сеть» — основной справочник AE2.
