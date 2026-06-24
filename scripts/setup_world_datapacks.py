#!/usr/bin/env python3
"""Copy CoopTech worldgen datapacks into a Minecraft save folder."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATAPACK_SRC = ROOT / 'overrides' / 'datapacks'
INSTANCE = Path(r'C:\Users\GameOn_Dp\AppData\Roaming\.minecraft\versions\Мой мод пак')
PACKS = (
    'Terralith_1.20.x_v2.5.4',
    'Incendium_1.20.x_v5.3.5',
    'Nullscape_1.20.x_v1.2.8',
)


def latest_save(saves_dir: Path) -> Path | None:
    worlds = [p for p in saves_dir.iterdir() if p.is_dir()]
    if not worlds:
        return None
    return max(worlds, key=lambda p: p.stat().st_mtime)


def install_to_world(world_dir: Path) -> int:
    dst_root = world_dir / 'datapacks'
    dst_root.mkdir(parents=True, exist_ok=True)
    print(f'World: {world_dir.name}')
    for pack in PACKS:
        src = DATAPACK_SRC / pack
        dst = dst_root / pack
        if not src.is_dir():
            print(f'  SKIP missing source: {src}')
            continue
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f'  OK  {pack}')
    print('\nDatapacks copied. Terralith needs a NEW world or first launch with packs enabled.')
    print('If this world was already generated without Terralith — create a new world.')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'world',
        nargs='?',
        help='Save folder name under saves/ (default: newest save)',
    )
    args = parser.parse_args()

    saves = INSTANCE / 'saves'
    if not saves.is_dir():
        print(f'ERROR: saves folder not found:\n  {saves}')
        return 1

    if args.world:
        world_dir = saves / args.world
        if not world_dir.is_dir():
            print(f'ERROR: world not found: {world_dir}')
            print('Available saves:')
            for item in sorted(saves.iterdir()):
                if item.is_dir():
                    print(f'  - {item.name}')
            return 1
    else:
        world_dir = latest_save(saves)
        if world_dir is None:
            print('ERROR: no saves found')
            return 1

    return install_to_world(world_dir)


if __name__ == '__main__':
    sys.exit(main())
