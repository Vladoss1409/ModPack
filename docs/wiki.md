# MyModPack Wiki

Статический справочник по модам сборки. Хостится на GitHub Pages, в игре доступен через `/wiki` (серверный KubeJS, без клиентских модов).

**URL:** https://vladoss1409.github.io/ModPack/

## Локальная разработка

```bash
cd wiki
npm install
npm run dev
```

Сборка (генерирует статический сайт и `search-index.json`):

```bash
npm run build
npm run preview
```

## Добавление контента

### Страница мода

1. Отредактируйте `wiki/src/content/mods/<slug>.md` (или сгенерируйте стабы: `python scripts/wiki_scaffold.py`).
2. Frontmatter: `name`, `modId`, `version`, `category`, `tags`, `links`.

### Текстуры блоков в 3D-схемах

Текстуры извлекаются из jar-файлов модов (локально):

```bash
python scripts/wiki_extract_textures.py
```

Файлы сохраняются в `wiki/public/textures/blocks/` и коммитятся в репозиторий (на CI jar-ов нет).

### Механизм / мультиблок

1. Создайте JSON-схему в `wiki/src/data/structures/<id>.json`.
2. Создайте `wiki/src/content/machines/<slug>.md` с полем `structure: "<id>"`.
3. Опишите правила в `placement` и в теле страницы.

### Деплой

Push в `main` с изменениями в `wiki/` — workflow `.github/workflows/wiki-deploy.yml` публикует на GitHub Pages.

В настройках репозитория: **Settings → Pages → Source: GitHub Actions**.

## Поиск

Собственный поиск по `search-index.json` (совпадение по словам, не по буквам). Deep-link: `?q=mekanism` (также работает `/wiki mekanism` в игре).
