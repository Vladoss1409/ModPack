#!/usr/bin/env python3
"""Sync MyModPack overrides to TLauncher test instance."""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / 'overrides'
MC = Path(os.environ.get('APPDATA', '')) / '.minecraft'
VERSION_CANDIDATES = ('ModPack', 'Мой мод пак')

# Jars that must not be in instance (conflict with embeddium / duplicates)
FORBIDDEN_MOD_PATTERNS = (
    'rubidium-mc',
    'rubidium-extra',
    'textrues_embeddium_options',
    'optifine',
)
# When multiple versions exist, remove these older filenames from instance
REMOVE_FROM_INSTANCE = (
    'rubidium-mc1.20.1-0.7.1.jar',
    'item-filters-forge-2001.1.0-build.53.jar',
    'jei-1.20.1-forge-15.20.0.130.jar',
    'textrues_embeddium_options-0.1.5+mc1.20.1.jar',
)


def run_script(name: str) -> None:
    script = ROOT / 'scripts' / name
    if script.is_file():
        subprocess.run([sys.executable, str(script)], check=True)


def unlock_tree(path: Path) -> None:
    if not path.exists():
        return
    for item in path.rglob('*'):
        if item.is_file():
            try:
                os.chmod(item, stat.S_IWRITE | stat.S_IREAD)
            except OSError:
                pass


def lock_snbt_files(path: Path) -> None:
    count = 0
    for snbt in path.rglob('*.snbt'):
        try:
            os.chmod(snbt, stat.S_IREAD)
            count += 1
        except OSError:
            pass
    print(f'  quest SNBT: {count} files set read-only (editor cannot corrupt)')


def _robocopy_mirror(src: Path, dst: Path) -> bool:
    """Mirror src -> dst via robocopy (Windows). Returns True on success."""
    if sys.platform != 'win32':
        return False
    dst.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ['robocopy', str(src), str(dst), '/MIR', '/R:2', '/W:2', '/NFL', '/NDL', '/NJH', '/NJS'],
        capture_output=True,
        text=True,
    )
    # robocopy: 0 = nothing copied, 1 = copied, 2+ = extra; >=8 = failure
    return result.returncode < 8


def replace_tree(src: Path, dst: Path, label: str) -> None:
    if not src.is_dir():
        print(f'  skip {label}: {src} not found')
        return
    unlock_tree(dst)
    if _robocopy_mirror(src, dst):
        print(f'  {label}: mirrored (robocopy)')
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f'  {label}: replaced')


def copy_tree(src: Path, dst: Path, label: str) -> None:
    if not src.is_dir():
        print(f'  skip {label}: {src} not found')
        return
    if _robocopy_mirror(src, dst):
        print(f'  {label}: mirrored (robocopy)')
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f'  {label}: copied')


def merge_tree(src: Path, dst: Path, label: str) -> None:
    if not src.is_dir():
        print(f'  skip {label}: {src} not found')
        return
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.rglob('*'):
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
    print(f'  {label}: merged')


def copy_file(src: Path, dst: Path, label: str) -> None:
    if not src.is_file():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f'  {label}: copied')


def resolve_instance() -> Path | None:
    versions = MC / 'versions'
    for name in VERSION_CANDIDATES:
        inst = versions / name
        if inst.is_dir():
            return inst
    return None


def main() -> int:
    instance = resolve_instance()
    if instance is None:
        print('ERROR: TLauncher instance not found. Expected one of:')
        for name in VERSION_CANDIDATES:
            print(f'  {MC / "versions" / name}')
        return 1

    print('Preparing assets...')
    run_script('generate_cooptech_assets.py')

    tex_dir = OVERRIDES / 'kubejs' / 'assets' / 'kubejs' / 'textures' / 'item'
    png_count = len(list(tex_dir.glob('*.png')))
    if png_count < 10:
        print(f'ERROR: expected item PNG textures, found {png_count}')
        return 1
    print(f'  textures OK: {png_count} PNG in repo\n')

    if not instance.is_dir():
        print(f'ERROR: TLauncher instance not found:\n  {instance}')
        return 1

    print(f'CoopTech sync -> {instance}\n')

    replace_tree(
        OVERRIDES / 'config' / 'ftbquests',
        instance / 'config' / 'ftbquests',
        'config/ftbquests',
    )

    copy_tree(
        OVERRIDES / 'kubejs',
        instance / 'kubejs',
        'kubejs',
    )

    copy_tree(
        OVERRIDES / 'resourcepacks' / 'CoopTechTheme',
        instance / 'resourcepacks' / 'CoopTechTheme',
        'resourcepacks/CoopTechTheme',
    )

    copy_tree(
        OVERRIDES / 'shaderpacks',
        instance / 'shaderpacks',
        'shaderpacks',
    )

    merge_tree(
        OVERRIDES / 'defaultconfigs',
        instance / 'defaultconfigs',
        'defaultconfigs',
    )

    merge_tree(
        OVERRIDES / 'data',
        instance / 'data',
        'data',
    )

    # KubeJS loads kubejs/data as a datapack; instance/data/ is not picked up by Forge.
    cooptech_data = OVERRIDES / 'data' / 'cooptech'
    if cooptech_data.is_dir():
        merge_tree(
            cooptech_data,
            instance / 'kubejs' / 'data' / 'cooptech',
            'kubejs/data/cooptech (from overrides/data)',
        )

    merge_tree(
        OVERRIDES / 'datapacks',
        instance / 'datapacks',
        'datapacks',
    )

    copy_tree(
        OVERRIDES / 'patchouli_books',
        instance / 'patchouli_books',
        'patchouli_books',
    )

    copy_file(
        OVERRIDES / 'config' / 'ftbquests-client.snbt',
        instance / 'config' / 'ftbquests-client.snbt',
        'config/ftbquests-client.snbt',
    )

    copy_file(
        OVERRIDES / 'config' / 'oculus.properties',
        instance / 'config' / 'oculus.properties',
        'config/oculus.properties',
    )

    for stray in (instance / 'config' / 'ftbquests' / 'quests' / 'chapters').glob('*.snbt.snbt'):
        stray.unlink(missing_ok=True)

    legacy_main = [
        'main_00_welcome.snbt',
        'main_02_ch1_anchor.snbt',
        'main_03_ch2_surface.snbt',
        'main_04_ch3_flux.snbt',
        'main_05_ch4_production.snbt',
        'main_06_ch5_nano.snbt',
        'main_07_ch6_finale.snbt',
    ]
    chapters_dir = instance / 'config' / 'ftbquests' / 'quests' / 'chapters'
    for name in legacy_main:
        stale = chapters_dir / name
        if stale.is_file():
            stale.unlink()
            print(f'  removed stale chapter: {name}')

    sync_mods_from_repo(instance)

    inst_tex = instance / 'kubejs' / 'assets' / 'kubejs' / 'textures' / 'item'
    inst_png = len(list(inst_tex.glob('*.png')))
    print(f'  instance textures: {inst_png} PNG')

    print('\nDone. Close Minecraft completely, then restart.')
    print('Quest SNBT is writable — use /ftbquests reload after in-game edits.')
    return 0


def cleanup_forbidden_mods(mods_dir: Path) -> None:
    if not mods_dir.is_dir():
        return
    removed = 0
    for name in REMOVE_FROM_INSTANCE:
        path = mods_dir / name
        if path.is_file():
            path.unlink()
            removed += 1
            print(f'  mods: removed conflict {name}')
    for jar in mods_dir.glob('*.jar'):
        low = jar.name.lower()
        if any(p in low for p in FORBIDDEN_MOD_PATTERNS):
            jar.unlink()
            removed += 1
            print(f'  mods: removed forbidden {jar.name}')
    if removed == 0:
        print('  mods: no forbidden jars found')


def sync_mods_from_repo(instance: Path) -> None:
    mods_src = ROOT / 'mods'
    mods_dst = instance / 'mods'
    cleanup_forbidden_mods(mods_dst)
    if not mods_src.is_dir():
        return
    copied = 0
    for jar in mods_src.glob('*.jar'):
        low = jar.name.lower()
        if any(p in low for p in FORBIDDEN_MOD_PATTERNS):
            continue
        dest = mods_dst / jar.name
        if not dest.exists() or jar.stat().st_mtime > dest.stat().st_mtime:
            shutil.copy2(jar, dest)
            copied += 1
    print(f'  mods: synced {copied} updated jar(s) from repo')


if __name__ == '__main__':
    sys.exit(main())
