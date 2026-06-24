#!/usr/bin/env python3
from __future__ import annotations
import json, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS_DIR = ROOT / "mods"
DATAPACKS_DIR = ROOT / "overrides" / "datapacks"
REPORT_PATH = ROOT / "install-report.json"
MC, LOADER = "1.20.1", "forge"
UA = "MyModPack/1.0"

CORE_MODS = [
    ("thermal-foundation", False), ("thermal-expansion", False), ("thermal-dynamics", False),
    ("thermal-innovation", False), ("thermal-cultivation", False), ("immersive-engineering", False),
    ("mekanism", False), ("mekanism-generators", False), ("mekanism-tools", False),
    ("powah", False), ("enderio", False), ("ae2", False), ("applied-mekanistics", False),
    ("ae2-things", False), ("guideme", False), ("sophisticated-storage", False),
    ("storage-drawers", False), ("iron-furnaces", False), ("irons-spells-n-spellbooks", False),
    ("relics-mod", False), ("apotheosis", False), ("twilightforest", False), ("aether", False),
    ("undergarden", False), ("blue-skies", False), ("cataclysm", False),
    ("bosses-of-mass-destruction", False), ("mowzies-mobs", False), ("alexs-mobs", False),
    ("alexscaves", False), ("when-dungeons-arise", False), ("yungs-api", False),
    ("yungs-better-strongholds", False), ("yungs-better-dungeons", False),
    ("yungs-better-mineshafts", False), ("yungs-better-nether-fortresses", False),
    ("yungs-better-end-island", False), ("explorers-compass", False), ("natures-compass", False),
    ("farmers-delight", False), ("supplementaries", False), ("amendments", False),
    ("spice-of-life-carrot-edition", False), ("enhanced-celestials", False), ("attributefix", False),
    ("bwc", False), ("ftb-quests-forge", False), ("ftb-teams-forge", False),
    ("ftb-library-forge", False), ("ftb-xmod-compat", False), ("item-filters", False),
    ("kubejs", False), ("rhino", False), ("ftb-chunks-forge", False), ("elevator-mod", False),
    ("jei", False), ("just-enough-resources-jer", False), ("jade", False), ("journeymap", True),
    ("tool-stats", False), ("mouse-tweaks", False), ("controlling", False), ("inventory-sorter", False),
    ("clumps", False), ("trashslot", False), ("embeddium", True),
    ("oculus", True), ("entityculling", True), ("modernfix", False), ("ferritecore", False),
    ("canary", False), ("polymorph", False), ("architectury-api", False), ("balm", False),
    ("bookshelf", False), ("citadel", False), ("cloth-config", False), ("curios", False),
    ("geckolib", False), ("patchouli", False), ("placebo", False), ("puzzles-lib", False),
    ("resourceful-lib", False), ("terrablender", False), ("terralith", False), ("incendium", False), ("nullscape", False), ("collective", False), ("moonlight", False),
    ("kotlin-for-forge", False), ("spark", False),
    ("ore-excavation", False),     ("lootjs", False),
    ("flux-networks", False), ("draconic-evolution", False), ("brandons-core", False),
    ("silent-gear", False), ("silent-lib", False),
]
DATAPACKS = ["terralith", "incendium", "nullscape", "repurposed-structures"]

# CurseForge-only mods (no Modrinth Forge build) — file_id from curseforge.com/.../files/FILE_ID
CURSEFORGE_FILES = [
    (248020, 5234697, "FluxNetworks-1.20.1-7.2.1.15.jar"),
]

def api_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def pick_version(slug):
    q = urllib.parse.urlencode([("loaders", json.dumps([LOADER])), ("game_versions", json.dumps([MC]))])
    try:
        versions = api_get(f"https://api.modrinth.com/v2/project/{slug}/version?{q}")
    except urllib.error.HTTPError as e:
        return None if e.code == 404 else (_ for _ in ()).throw(e)
    if not versions:
        return None
    for v in versions:
        if v.get("version_type") == "release":
            return v
    return versions[0]

def download_file(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())

def install_mod(slug, client_only, installed, report):
    if slug in installed:
        return
    installed.add(slug)
    version = pick_version(slug)
    if not version:
        report["failed"].append({"slug": slug, "reason": "no 1.20.1 forge version"})
        print(f"  FAIL {slug}: no version")
        return
    for dep in version.get("dependencies", []):
        if dep.get("dependency_type") == "optional":
            continue
        pid = dep.get("project_id")
        if not pid:
            continue
        try:
            dep_slug = api_get(f"https://api.modrinth.com/v2/project/{pid}")["slug"]
            install_mod(dep_slug, False, installed, report)
        except Exception:
            pass
    primary = version["files"][0]
    dest = MODS_DIR / primary["filename"]
    if dest.exists():
        report["skipped"].append({"slug": slug, "file": primary["filename"]})
        return
    try:
        download_file(primary["url"], dest)
        report["ok"].append({"slug": slug, "file": primary["filename"], "version": version["version_number"], "client_only": client_only})
        print(f"  OK  {slug} -> {primary['filename']}")
    except Exception as exc:
        report["failed"].append({"slug": slug, "reason": str(exc)})
        print(f"  FAIL {slug}: {exc}")
    time.sleep(0.12)

def install_curseforge_file(file_id: int, filename: str, report: dict) -> None:
    dest = MODS_DIR / filename
    if dest.exists():
        report.setdefault("curseforge_skipped", []).append(filename)
        return
    fid = str(file_id)
    folder = f"{fid[:-3]}/{fid[-3:]}"
    urls = [
        f"https://edge.forgecdn.net/files/{folder}/{filename}",
        f"https://mediafilez.forgecdn.net/files/{folder}/{filename}",
    ]
    for url in urls:
        try:
            download_file(url, dest)
            report.setdefault("curseforge_ok", []).append({"file": filename, "url": url})
            print(f"  OK  curseforge -> {filename}")
            return
        except Exception:
            continue
    report.setdefault("curseforge_failed", []).append({
        "file": filename,
        "manual": f"https://www.curseforge.com/minecraft/mc-mods/flux-networks/files/{file_id}",
    })
    print(f"  MANUAL flux: download {filename} from CurseForge file {file_id}")

def install_datapack(slug, report):
    version = pick_version(slug)
    if not version:
        report["datapack_failed"].append(slug)
        print(f"  FAIL datapack {slug}")
        return
    dest = DATAPACKS_DIR / version["files"][0]["filename"]
    if dest.exists():
        report["datapack_skipped"].append(slug)
        return
    try:
        download_file(version["files"][0]["url"], dest)
        report["datapack_ok"].append({"slug": slug, "file": dest.name})
        print(f"  OK  datapack {slug}")
    except Exception as exc:
        report["datapack_failed"].append({"slug": slug, "reason": str(exc)})

def main():
    MODS_DIR.mkdir(parents=True, exist_ok=True)
    DATAPACKS_DIR.mkdir(parents=True, exist_ok=True)
    report = {"minecraft": MC, "loader": LOADER, "ok": [], "skipped": [], "failed": [], "datapack_ok": [], "datapack_skipped": [], "datapack_failed": []}
    installed = set()
    print("Downloading mods...")
    for slug, co in CORE_MODS:
        install_mod(slug, co, installed, report)
    print("CurseForge-only mods...")
    for _pid, file_id, fname in CURSEFORGE_FILES:
        install_curseforge_file(file_id, fname, report)
    print("Downloading datapacks...")
    for slug in DATAPACKS:
        install_datapack(slug, report)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Done: {len(report['ok'])} new, {len(report['skipped'])} skipped, {len(report['failed'])} failed")
    return 1 if report["failed"] else 0

if __name__ == "__main__":
    sys.exit(main())
