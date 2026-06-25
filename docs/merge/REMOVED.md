# Журнал видалених модів (technomagic → MyModPack)

Зведений журнал переносу. Гілка: `merge/technomagic`.
Джерело: `C:\Users\vlado\Desktop\ТехноМагия\ТехноМагия`. Схема: `technomagic-modmap.canvas.tsx`.

Статуси: `planned` → `manifest` (EXCLUDE/REWRITE складено) → `applied` (застосовано під час pull).

| Дата | Мод (modId) | Гілка видалення (залежні) | Маніфест | Коміти | Статус |
|---|---|---|---|---|---|
| 2026-06-25 | `botania` | `aiotbotania`, `extrabotany`, `mythicbotany`, `appbot`, `kubejs_botania` | [botania.md](botania.md) | `00b5108`, `ec5343f` | manifest |

---

## Легенда

- **Гілка видалення** — мод + усі, хто від нього hard-залежить (за `dependency-graph`), що виключаються разом.
- **Маніфест** — `docs/merge/<mod>.md` з EXCLUDE (не тягнемо) / REWRITE (тягнемо без посилань) / modlist.
- **Коміти** — записи на гілці `merge/technomagic` (`git log main..merge/technomagic`).
- **applied** ставиться лише після фінального pull-у з застосуванням EXCLUDE/REWRITE.
