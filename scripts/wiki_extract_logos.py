#!/usr/bin/env python3
"""Extract mod logos/icons from mod jars for the wiki.

For every article in wiki/src/content/mods/*.md we try to find the matching
mod jar (by declared modId or a fuzzy name/slug match), pull its logo image
(logoFile from mods.toml, or a pack.png / icon.png / logo.png fallback) and
save it to wiki/public/logos/<slug>.png. A manifest keyed by article slug is
written to wiki/src/data/logos.json so the site can render it.
"""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS = ROOT / "mods"
CONTENT = ROOT / "wiki" / "src" / "content" / "mods"
OUT = ROOT / "wiki" / "public" / "logos"
MANIFEST = ROOT / "wiki" / "src" / "data" / "logos.json"

SKIP_MODIDS = {"forge", "minecraft", "mod_id", "examplemod"}
ROOT_FALLBACKS = ["logo.png", "icon.png", "pack.png", "logoFile.png"]


def nrm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def parse_toml(jar: zipfile.ZipFile) -> tuple[list[str], str | None]:
    """Return (list of real modIds, logoFile) from META-INF/mods.toml."""
    try:
        text = jar.read("META-INF/mods.toml").decode("utf-8", "ignore")
    except KeyError:
        return [], None
    modids: list[str] = []
    logo: str | None = None
    for line in text.splitlines():
        m = re.search(r'modId\s*=\s*"([^"]+)"', line)
        if m and m.group(1) not in SKIP_MODIDS:
            modids.append(m.group(1))
        m = re.search(r'logoFile\s*=\s*"([^"]+)"', line)
        if m and not logo:
            logo = m.group(1)
    return modids, logo


def read_frontmatter(md: Path) -> dict[str, str]:
    text = md.read_text(encoding="utf-8")
    data: dict[str, str] = {}
    if not text.startswith("---"):
        return data
    end = text.find("\n---", 3)
    if end == -1:
        return data
    for line in text[3:end].splitlines():
        m = re.match(r'^(\w+):\s*"?([^"\n]*)"?\s*$', line)
        if m:
            data[m.group(1)] = m.group(2).strip()
    return data


def index_jars() -> list[dict]:
    jars: list[dict] = []
    for jar_path in sorted(MODS.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar_path) as zf:
                modids, logo = parse_toml(zf)
                names = zf.namelist()
        except zipfile.BadZipFile:
            continue
        jars.append(
            {
                "path": jar_path,
                "modids": modids,
                "logo": logo,
                "names": names,
                "nname": nrm(jar_path.stem),
            }
        )
    return jars


def find_logo_bytes(
    jar_path: Path, names: list[str], logo: str | None, modids: list[str]
) -> bytes | None:
    pngs = [n for n in names if n.lower().endswith(".png")]
    # exclude in-game texture/gui noise from the fuzzy searches
    clean = [
        n
        for n in pngs
        if "/textures/" not in n.lower() and "/gui/" not in n.lower()
    ]
    candidates: list[str] = []

    # 1. declared logoFile (basename match, anywhere in the jar)
    if logo and logo.lower().endswith(".png"):
        lf = logo.replace("\\", "/").lower()
        base = lf.rsplit("/", 1)[-1]
        candidates += [n for n in pngs if n.lower() == lf or n.lower().endswith("/" + base)]

    # 2. explicit logo/icon files under assets/<modid>/ (shallow) or assets root
    for mid in modids:
        candidates += [n for n in clean if n.lower() == f"assets/{mid.lower()}/logo.png"]
        candidates += [n for n in clean if n.lower() == f"assets/{mid.lower()}/icon.png"]
    candidates += [n for n in clean if n.lower() in ("assets/logo.png", "assets/icon.png")]

    # 3. any *logo*.png (prefer non-wide), then any *icon*.png outside textures
    logo_like = [n for n in clean if "logo" in n.lower()]
    logo_like.sort(key=lambda n: ("wide" in n.lower(), len(n)))
    candidates += logo_like
    candidates += [n for n in clean if "icon" in n.lower()]

    # 4. root fallbacks / any root png
    for fb in ROOT_FALLBACKS:
        candidates += [n for n in pngs if n.lower() == fb.lower()]
    candidates += [n for n in pngs if "/" not in n]

    with zipfile.ZipFile(jar_path) as zf:
        seen: set[str] = set()
        for n in candidates:
            if n in seen:
                continue
            seen.add(n)
            try:
                data = zf.read(n)
            except KeyError:
                continue
            if len(data) > 100:
                return data
    return None


def match_jar(article_modid: str, slug: str, name: str, jars: list[dict]) -> dict | None:
    amod = nrm(article_modid)
    nslug = nrm(slug)
    nname = nrm(name)
    # 1. exact modId
    for j in jars:
        if any(nrm(m) == amod for m in j["modids"]) and amod:
            return j
    # 2. modId substring of jar declared ids or vice versa
    for j in jars:
        for m in j["modids"]:
            nm = nrm(m)
            if amod and (amod in nm or nm in amod):
                return j
    # 3. slug/name vs jar filename
    for j in jars:
        if nslug and (nslug in j["nname"] or j["nname"] in nslug):
            return j
    for j in jars:
        if nname and (nname in j["nname"] or j["nname"] in nname):
            return j
    return None


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    jars = index_jars()
    manifest: dict[str, str] = {}
    ok = 0
    miss = 0
    missing: list[str] = []

    for md in sorted(CONTENT.glob("*.md")):
        slug = md.stem
        fm = read_frontmatter(md)
        article_modid = fm.get("modId", "")
        name = fm.get("name", slug)
        j = match_jar(article_modid, slug, name, jars)
        if not j:
            miss += 1
            missing.append(slug)
            continue
        data = find_logo_bytes(j["path"], j["names"], j["logo"], j["modids"])
        if not data:
            miss += 1
            missing.append(slug)
            continue
        (OUT / f"{slug}.png").write_bytes(data)
        manifest[slug] = f"logos/{slug}.png"
        ok += 1

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Logos extracted: {ok}, missing: {miss}")
    if missing:
        print("Missing:", ", ".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
