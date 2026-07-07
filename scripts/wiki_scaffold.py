#!/usr/bin/env python3
"""Generate idempotent mod pages for the wiki from modlist.txt.

Auto-fills every page with a category-based description and clickable
CurseForge/Modrinth search links, so no page is empty. Pages with the
"<!-- scaffold -->" marker are regenerated; hand-written pages (without the
marker) are preserved.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
MODLIST = ROOT / "modlist.txt"
OUT_DIR = ROOT / "wiki" / "src" / "content" / "mods"

# Heuristic category + modId from jar filename
CATEGORY_RULES: list[tuple[str, str]] = [
    (r"embeddium|oculus|entityculling|journeymap|jei|emi|jade|mouse|controlling|searchables|inventorysorter|trashslot|toolstats|tl_skin", "client"),
    (r"architectury|bookshelf|balm|cloth|codechicken|curios|geckolib|kotlin|lionfish|moonlight|octolib|placebo|puzzles|rhino|resourceful|silent-lib|citadel|cerbons|corgilib|glodium|collective|yungsapi|structure_gel|bwncr|canary|clumps|ferritecore|modernfix|attribute|player-animation", "library"),
    (r"terralith|incendium|nullscape|amplified|repurposed|dungeonsarise|blue_skies|undergarden|aether|twilight", "worldgen"),
    (r"apotheosis|irons_spell|relics|silent-gear|cataclysm|bomd|mowzie|alexsmobs|alexscaves", "combat"),
    (r"ae2|applied|mekanism|thermal|powah|enderio|flux|draconic|brandon|immersive|ironfurnaces|projecte|sophisticated|storage|elevator|oreexcavation|farmers|supplementaries|amendments|data_anchor|next_", "tech"),
    (r"ftb-|luckperms|kubejs|lootjs|spark|guideme|patchouli", "utility"),
    (r"explorers|natures|solcarrot|enhanced", "exploration"),
]

TAG_RULES: list[tuple[str, list[str]]] = [
    (r"ae2|applied", ["ae2", "storage", "automation"]),
    (r"mekanism", ["mekanism", "processing", "energy"]),
    (r"thermal", ["thermal", "machines"]),
    (r"powah", ["powah", "energy", "generators"]),
    (r"draconic|brandon", ["draconic", "endgame"]),
    (r"enderio", ["enderio", "logistics"]),
    (r"flux", ["flux", "wireless"]),
    (r"immersive", ["immersive", "multiblock"]),
    (r"apotheosis", ["apotheosis", "gear"]),
    (r"twilight", ["twilight", "dimension"]),
    (r"ftb-quests", ["quests"]),
    (r"kubejs", ["scripting"]),
]


CATEGORY_DESC: dict[str, str] = {
    "tech": "Технический мод: машины, автоматизация и энергетика.",
    "magic": "Магический мод: заклинания, ритуалы и артефакты.",
    "exploration": "Исследование мира: структуры, биомы и навигация.",
    "combat": "Бой и снаряжение: мобы, боссы, оружие и броня.",
    "utility": "Утилита: улучшает игровой процесс, интерфейс и управление.",
    "worldgen": "Генерация мира: биомы, измерения и структуры.",
    "library": "Библиотека: зависимость для других модов, сама по себе почти не добавляет контента.",
    "client": "Клиентский мод: интерфейс, отображение и оптимизация (на сервере не требуется).",
    "other": "Дополнение к сборке.",
}

CATEGORY_ROLE: dict[str, list[str]] = {
    "tech": [
        "Добавляет блоки и машины для автоматизации и переработки.",
        "Обычно работает на энергии (RF/FE) — подключается к общей энергосети.",
        "Связан с технической прогрессией сборки (тиры T1–T5).",
    ],
    "magic": [
        "Добавляет магические механики: заклинания, ритуалы или артефакты.",
        "Часто требует особых ресурсов и прокачки.",
    ],
    "exploration": [
        "Расширяет исследование: новые структуры, биомы или инструменты навигации.",
        "Полезен для поиска ресурсов и точек интереса.",
    ],
    "combat": [
        "Добавляет мобов, боссов и/или боевое снаряжение.",
        "Влияет на сложность и лут сборки.",
    ],
    "utility": [
        "Улучшает удобство игры: интерфейс, сортировка, информация.",
        "Не меняет прогрессию напрямую, но экономит время.",
    ],
    "worldgen": [
        "Меняет генерацию мира: биомы, измерения, структуры.",
        "Влияет на исследование и добычу ресурсов.",
    ],
    "library": [
        "Устанавливается как зависимость других модов.",
        "Отдельного игрового контента, как правило, не добавляет.",
    ],
    "client": [
        "Работает на стороне клиента (интерфейс/оптимизация).",
        "В серверную сборку не входит.",
    ],
    "other": [
        "Дополняет сборку вспомогательным контентом.",
    ],
}


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "mod"


def jar_to_mod_id(jar: str) -> str:
    base = jar.removesuffix(".jar")
    base = re.sub(r"-\d.*$", "", base)
    base = re.sub(r"_(forge|mc\d.*|universal|all|beta).*$", "", base, flags=re.I)
    return base.lower().replace("-", "_").replace(" ", "_")


def jar_to_name(jar: str) -> str:
    base = jar.removesuffix(".jar")
    # strip version tail
    base = re.sub(
        r"[-_](?:forge|mc)?\d.*$",
        "",
        base,
        flags=re.I,
    )
    base = base.replace("_", " ").replace("-", " ")
    return " ".join(w.capitalize() for w in base.split())


def jar_to_version(jar: str) -> str:
    m = re.search(r"(\d+\.\d+(?:\.\d+)?(?:[+.-][\w.]+)?)", jar)
    return m.group(1) if m else "unknown"


def guess_category(jar: str) -> str:
    low = jar.lower()
    for pattern, cat in CATEGORY_RULES:
        if re.search(pattern, low):
            return cat
    return "other"


def guess_tags(jar: str) -> list[str]:
    low = jar.lower()
    tags: list[str] = []
    for pattern, tlist in TAG_RULES:
        if re.search(pattern, low):
            tags.extend(tlist)
    return list(dict.fromkeys(tags))[:5]


def is_stub_content(body: str) -> bool:
    markers = ("<!-- scaffold -->", "Страница в разработке", "TODO")
    return any(m in body for m in markers)


def curseforge_search(name: str) -> str:
    return f"https://www.curseforge.com/minecraft/search?class=mc-mods&search={quote(name)}"


def modrinth_search(name: str) -> str:
    return f"https://modrinth.com/mods?q={quote(name)}"


def build_frontmatter(jar: str) -> str:
    name = jar_to_name(jar)
    mod_id = jar_to_mod_id(jar)
    version = jar_to_version(jar)
    category = guess_category(jar)
    tags = guess_tags(jar)
    tags_yaml = "\n".join(f"  - {t}" for t in tags) if tags else "  []"

    desc = CATEGORY_DESC.get(category, CATEGORY_DESC["other"])
    role_lines = "\n".join(f"- {line}" for line in CATEGORY_ROLE.get(category, CATEGORY_ROLE["other"]))
    cf = curseforge_search(name)
    mr = modrinth_search(name)

    return f"""---
name: "{name}"
modId: "{mod_id}"
version: "{version}"
category: {category}
tags:
{tags_yaml}
links:
  curseforge: "{cf}"
  modrinth: "{mr}"
draft: false
---

<!-- scaffold -->

## Обзор

**{name}** (`{mod_id}`, v{version}) — {desc}

Часть кооп-сборки MyModPack (Forge 1.20.1). Кнопки CurseForge и Modrinth выше ведут на поиск мода — там официальное описание, скриншоты и вики.

## Роль в сборке

{role_lines}

## Где узнать больше

- Рецепты и предметы — в **JEI/EMI** в игре.
- Официальное описание и скриншоты — по ссылкам CurseForge/Modrinth выше.
- Мультиблоки сборки — в разделе [Механизмы](../../machines/).
"""


def main() -> int:
    if not MODLIST.is_file():
        print(f"ERROR: {MODLIST} not found")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    jars = [ln.strip() for ln in MODLIST.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]

    created = 0
    skipped = 0
    for jar in jars:
        slug = slugify(jar_to_mod_id(jar))
        path = OUT_DIR / f"{slug}.md"
        if path.is_file():
            existing = path.read_text(encoding="utf-8")
            if not is_stub_content(existing):
                skipped += 1
                continue
        content = build_frontmatter(jar)
        path.write_text(content, encoding="utf-8")
        created += 1

    print(f"Wiki scaffold: {created} written, {skipped} skipped (custom content), {len(jars)} total jars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
