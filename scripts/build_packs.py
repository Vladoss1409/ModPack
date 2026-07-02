#!/usr/bin/env python3
"""Build client and server install packs (zip) from repo mods + overrides."""
from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "overrides"
MODS = ROOT / "mods"
DIST = ROOT / "dist"
CACHE = ROOT / ".cache"
MANIFEST = ROOT / "manifest.json"
CLIENT_ONLY_FILE = ROOT / "client-only-mods.txt"

FORGE_MC = "1.20.1"
FORGE_VERSION = "47.4.10"
FORGE_FULL = f"{FORGE_MC}-{FORGE_VERSION}"
FORGE_INSTALLER_URL = (
    f"https://maven.minecraftforge.net/net/minecraftforge/forge/"
    f"{FORGE_FULL}/forge-{FORGE_FULL}-installer.jar"
)
FORGE_SKELETON = CACHE / f"forge-server-{FORGE_FULL}"
FORBIDDEN_MOD_PATTERNS = (
    "rubidium-mc",
    "rubidium-extra",
    "textrues_embeddium_options",
    "optifine",
)

OVERRIDE_DIRS = (
    "config",
    "kubejs",
    "defaultconfigs",
    "datapacks",
    "data",
    "patchouli_books",
    "bootstrap",
)

CLIENT_ONLY_OVERRIDE_DIRS = ("resourcepacks", "shaderpacks")


def run_script(name: str) -> None:
    script = ROOT / "scripts" / name
    if script.is_file():
        print(f"Running {name}...")
        subprocess.run([sys.executable, str(script)], check=True)


def load_manifest() -> tuple[str, str]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return str(data.get("name", "MyModPack")), str(data.get("version", "0.1.0"))


def load_client_only_patterns() -> tuple[str, ...]:
    if not CLIENT_ONLY_FILE.is_file():
        return ()
    patterns: list[str] = []
    for line in CLIENT_ONLY_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line.lower())
    return tuple(patterns)


def is_forbidden_mod(name: str) -> bool:
    low = name.lower()
    return any(p in low for p in FORBIDDEN_MOD_PATTERNS)


def is_client_only_mod(name: str, patterns: tuple[str, ...]) -> bool:
    low = name.lower()
    return any(p in low for p in patterns)


def remove_tree(path: Path) -> None:
    if not path.exists():
        return

    def onerror(func, p, exc_info):  # type: ignore[no-untyped-def]
        try:
            os.chmod(p, stat.S_IWRITE)
            func(p)
        except OSError:
            pass

    shutil.rmtree(path, onexc=onerror)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.is_dir():
        return
    remove_tree(dst)
    shutil.copytree(src, dst)


def copy_mods(target_mods: Path, *, client_only_patterns: tuple[str, ...], include_client_only: bool) -> tuple[int, int]:
    target_mods.mkdir(parents=True, exist_ok=True)
    copied = 0
    skipped = 0
    for jar in sorted(MODS.glob("*.jar")):
        if is_forbidden_mod(jar.name):
            skipped += 1
            continue
        client_only = is_client_only_mod(jar.name, client_only_patterns)
        if client_only and not include_client_only:
            skipped += 1
            continue
        shutil.copy2(jar, target_mods / jar.name)
        copied += 1
    return copied, skipped


def write_install_notes(path: Path, *, kind: str, mod_count: int, skipped: int) -> None:
    if kind == "client":
        text = f"""MyModPack — клієнтський пак (Forge {FORGE_MC}, {FORGE_VERSION})
================================================

1. Створіть профіль Minecraft {FORGE_MC} + Forge {FORGE_VERSION}.
2. Розпакуйте архів у корінь інстансу (у папці мають з'явитися mods/, config/, kubejs/…).
3. Виділіть клієнту 6 GB RAM.
4. Перший запуск може тривати 3–10 хвилин.

Модів у паку: {mod_count}
"""
    else:
        text = f"""MyModPack — серверний пак (Forge {FORGE_MC}, {FORGE_VERSION})
================================================

1. Створіть порожню папку сервера.
2. Розпакуйте архів прямо в неї (mods/, config/, run.bat / run.sh — у корені).
3. Запустіть run.bat (Windows) або ./run.sh (Linux).
4. EULA вже прийнята (eula.txt). RAM: 6G у user_jvm_args.txt.

Модів: {mod_count} (без client-only: {skipped} jar(ів))
Client-only не включено: embeddium, oculus, entityculling, journeymap
"""
    path.write_text(text, encoding="utf-8")


def download_forge_installer(target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.is_file():
        print(f"  downloading Forge installer {FORGE_FULL}...")
        urllib.request.urlretrieve(FORGE_INSTALLER_URL, target)
    return target


def ensure_forge_server_skeleton() -> Path:
    marker = FORGE_SKELETON / "run.bat"
    if marker.is_file():
        return FORGE_SKELETON

    installer = download_forge_installer(CACHE / f"forge-{FORGE_FULL}-installer.jar")
    work = CACHE / f"forge-install-{FORGE_FULL}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    print(f"  installing Forge server {FORGE_FULL} (one-time cache)...")
    subprocess.run(
        ["java", "-jar", str(installer), "--installServer"],
        cwd=work,
        check=True,
    )

    if FORGE_SKELETON.exists():
        shutil.rmtree(FORGE_SKELETON)
    shutil.copytree(work, FORGE_SKELETON)
    shutil.rmtree(work)
    return FORGE_SKELETON


def write_server_bootstrap(stage: Path) -> None:
    (stage / "eula.txt").write_text(
        "#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n"
        "eula=true\n",
        encoding="utf-8",
    )

    (stage / "server.properties").write_text(
        "\n".join(
            [
                "enable-jmx-monitoring=false",
                "rcon.port=25575",
                "level-seed=",
                "gamemode=survival",
                "enable-command-block=true",
                "enable-query=false",
                "generator-settings={}",
                "enforce-secure-profile=true",
                "level-name=world",
                "motd=MyModPack Coop Server",
                "query.port=25565",
                "pvp=true",
                "generate-structures=true",
                "max-chained-neighbor-updates=1000000",
                "difficulty=hard",
                "network-compression-threshold=256",
                "max-tick-time=60000",
                "require-resource-pack=false",
                "max-players=2",
                "use-native-transport=true",
                "online-mode=true",
                "enable-status=true",
                "allow-flight=false",
                "initial-disabled-packs=",
                "broadcast-rcon-to-ops=true",
                "view-distance=10",
                "server-ip=",
                "resource-pack-prompt=",
                "allow-nether=true",
                "server-port=25565",
                "enable-rcon=false",
                "sync-chunk-writes=true",
                "op-permission-level=4",
                "prevent-proxy-connections=false",
                "hide-online-players=false",
                "resource-pack=",
                "entity-broadcast-range-percentage=100",
                "simulation-distance=10",
                "rcon.password=",
                "player-idle-timeout=0",
                "force-gamemode=false",
                "rate-limit=0",
                "hardcore=false",
                "white-list=false",
                "broadcast-console-to-ops=true",
                "spawn-npcs=true",
                "spawn-animals=true",
                "function-permission-level=2",
                "level-type=minecraft\\:normal",
                "text-filtering-config=",
                "spawn-monsters=true",
                "enforce-whitelist=false",
                "spawn-protection=0",
                "resource-pack-sha1=",
                "max-world-size=29999984",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    jvm_args = stage / "user_jvm_args.txt"
    lines = jvm_args.read_text(encoding="utf-8").splitlines() if jvm_args.is_file() else []
    if not any(line.strip().startswith("-Xmx") for line in lines):
        lines.extend(["", "-Xms6G", "-Xmx6G"])
        jvm_args.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_zip(source_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for file in sorted(source_dir.rglob("*")):
            if file.is_file():
                zf.write(file, file.relative_to(source_dir).as_posix())


def build_pack(*, label: str, include_client_only: bool, client_only_patterns: tuple[str, ...]) -> Path:
    name, version = load_manifest()
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", name)
    stage = DIST / f"{slug}-{version}-{label}"
    remove_tree(stage)
    stage.mkdir(parents=True)

    if label == "server":
        print("  installing Forge server bootstrap...")
        skeleton = ensure_forge_server_skeleton()
        for item in skeleton.iterdir():
            dest = stage / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

    for folder in OVERRIDE_DIRS:
        copy_tree(OVERRIDES / folder, stage / folder)

    if include_client_only:
        for folder in CLIENT_ONLY_OVERRIDE_DIRS:
            copy_tree(OVERRIDES / folder, stage / folder)

    copied, skipped = copy_mods(
        stage / "mods",
        client_only_patterns=client_only_patterns,
        include_client_only=include_client_only,
    )

    if label == "server":
        write_server_bootstrap(stage)
        for log_file in stage.glob("*.log"):
            log_file.unlink(missing_ok=True)

    write_install_notes(
        stage / f"INSTALL-{label.upper()}.txt",
        kind=label,
        mod_count=copied,
        skipped=skipped,
    )

    if label == "client" and (ROOT / "README.md").is_file():
        shutil.copy2(ROOT / "README.md", stage / "README.md")
    if label == "server" and (ROOT / "server-setup.md").is_file():
        shutil.copy2(ROOT / "server-setup.md", stage / "server-setup.md")
    if (ROOT / "client-only-mods.txt").is_file():
        shutil.copy2(ROOT / "client-only-mods.txt", stage / "client-only-mods.txt")

    zip_path = DIST / f"{slug}-{version}-{label}.zip"
    make_zip(stage, zip_path)
    print(f"  staged: {stage}")
    print(f"  archive: {zip_path} ({copied} mods, skipped {skipped})")
    return zip_path


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Build MyModPack install zips")
    parser.add_argument("--target", choices=("client", "server", "both"), default="both")
    parser.add_argument("--skip-prep", action="store_true", help="Skip asset/quest regeneration")
    args = parser.parse_args()

    if not MODS.is_dir():
        print(f"ERROR: mods/ not found at {MODS}")
        return 1
    if not OVERRIDES.is_dir():
        print(f"ERROR: overrides/ not found at {OVERRIDES}")
        return 1

    if not args.skip_prep:
        run_script("generate_cooptech_assets.py")
        run_script("quests_build_v1.py")

    client_only = load_client_only_patterns()
    DIST.mkdir(parents=True, exist_ok=True)

    client_zip = server_zip = None
    if args.target in ("client", "both"):
        print("\nBuilding client pack...")
        client_zip = build_pack(label="client", include_client_only=True, client_only_patterns=client_only)

    if args.target in ("server", "both"):
        print("\nBuilding server pack...")
        server_zip = build_pack(label="server", include_client_only=False, client_only_patterns=client_only)

    print("\nDone.")
    if client_zip:
        print(f"  Client: {client_zip}")
    if server_zip:
        print(f"  Server: {server_zip}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
