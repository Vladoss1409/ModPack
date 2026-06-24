#!/usr/bin/env python3
"""Deploy CoopTech camp datapack + CNPC dialogs into a world save (Minecraft closed)."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTANCE = Path(r'C:\Users\GameOn_Dp\AppData\Roaming\.minecraft\versions\Мой мод пак')
CAMP_PACK = ROOT / 'overrides' / 'datapacks' / 'CoopTechCamp'
DIALOG_SRC = ROOT / 'overrides' / 'bootstrap' / 'customnpcs' / 'dialogs'
WORLDS = ROOT / 'overrides' / 'bootstrap' / 'worlds'


def wait_unlock(world: Path, timeout: float = 30.0) -> bool:
    lock = world / 'session.lock'
    if not lock.is_file():
        return True
    print('  Minecraft open (session.lock). Close the game...')
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not lock.is_file():
            return True
        time.sleep(1)
    return not lock.is_file()


def read_spawn(world: Path) -> tuple[int, int, int]:
    import nbtlib

    nbt = nbtlib.load(str(world / 'level.dat'))
    data = nbt['Data']
    return int(data['SpawnX']), int(data['SpawnY']), int(data['SpawnZ'])


def set_world_spawn(world: Path, x: int, y: int, z: int) -> None:
    import nbtlib
    from nbtlib import Int

    level = world / 'level.dat'
    nbt = nbtlib.load(str(level))
    data = nbt['Data']
    data['SpawnX'] = Int(x)
    data['SpawnY'] = Int(y)
    data['SpawnZ'] = Int(z)
    nbt.save(str(level))
    print(f'  OK  world spawn -> {x} {y} {z}')


def patch_deploy_coords(world: Path, camp: tuple[int, int, int], preset: dict | None = None) -> None:
    x, y, z = camp
    dst = (
        world
        / 'datapacks'
        / 'CoopTechCamp'
        / 'data'
        / 'cooptech_world'
        / 'functions'
        / 'camp'
        / 'deploy.mcfunction'
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = f"""# Auto-deploy — datapack surface scan
data remove storage cooptech_world:config camp_built
tellraw @a [{{"text":"[CoopTech] ","color":"light_purple"}},{{"text":"Building expedition camp...","color":"white"}}]
function cooptech_world:camp/find_surface_build
data merge storage cooptech_world:config {{camp_built:1b}}
tellraw @a [{{"text":"[CoopTech] ","color":"light_purple"}},{{"text":"Camp ready.","color":"green"}}]
"""
    dst.write_text(text, encoding='utf-8')
    print(f'  OK  deploy at {x} {y} {z}')


def copy_camp_pack(world: Path) -> None:
    dst = world / 'datapacks' / 'CoopTechCamp'
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(CAMP_PACK, dst)
    print(f'  OK  datapack -> {dst.name}')


def install_dialogs(world: Path) -> None:
    src = DIALOG_SRC / 'CoopTech'
    if not src.is_dir():
        print('  SKIP dialogs: missing CoopTech templates')
        return
    dst = world / 'customnpcs' / 'dialogs' / 'CoopTech'
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.glob('*.json'):
        shutil.copy2(f, dst / f.name)
    print('  OK  CNPC dialogs CoopTech/')


def enable_datapack(world: Path, pack_name: str = 'CoopTechCamp') -> None:
    import nbtlib
    from nbtlib import String

    level = world / 'level.dat'
    nbt = nbtlib.load(str(level))
    data = nbt['Data']
    if 'DataPacks' not in data:
        print('  SKIP level.dat DataPacks missing')
        return
    dp = data['DataPacks']
    enabled = list(dp['Enabled'])
    tag = f'file/{pack_name}'
    if tag not in [str(x) for x in enabled]:
        enabled.append(String(tag))
        dp['Enabled'] = nbtlib.List[String](enabled)
        nbt.save(str(level))
    print(f'  OK  enabled {tag}')


def load_preset(name: str) -> dict:
    path = WORLDS / f'{name}.json'
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding='utf-8'))


def find_world(preset: dict, world_name: str | None) -> Path | None:
    saves = INSTANCE / 'saves'
    if world_name:
        direct = saves / world_name
        if direct.is_dir():
            return direct
    folder = preset.get('save_folder')
    if folder and (saves / folder).is_dir():
        return saves / folder
    target_seed = preset.get('seed')
    if target_seed is not None:
        import nbtlib

        want = int(target_seed)
        for p in saves.iterdir():
            if not p.is_dir() or not (p / 'level.dat').exists():
                continue
            d = nbtlib.load(str(p / 'level.dat'))['Data']
            seed = int(d.get('WorldGenSettings', {}).get('seed', d.get('RandomSeed', 0)))
            if seed == want:
                return p
    level_want = preset.get('world_name') or world_name
    if level_want:
        import nbtlib

        for p in saves.iterdir():
            if not p.is_dir() or not (p / 'level.dat').exists():
                continue
            d = nbtlib.load(str(p / 'level.dat'))['Data']
            if str(d.get('LevelName', '')) == level_want:
                return p
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('world', nargs='?', help='Save folder name')
    parser.add_argument('--preset', default='test1', help='Bootstrap preset (default: test1)')
    parser.add_argument('--camp', nargs=3, type=int, metavar=('X', 'Y', 'Z'), help='Camp center block')
    parser.add_argument('--set-spawn', action='store_true', help='Set world spawn to camp coords')
    parser.add_argument('--force', action='store_true', help='Deploy even if session.lock exists')
    parser.add_argument('--install-cnpc', action='store_true', help='Copy CNPC dialogs (deprecated; quest-only pack)')
    args = parser.parse_args()

    preset = load_preset(args.preset) if args.preset else {}
    world_name = args.world or preset.get('world_name', 'Тест1')
    world = find_world(preset, args.world)
    if world is None:
        print(f'ERROR: world not found (name={world_name}, seed={preset.get("seed")})')
        print(f'Create world with seed {preset.get("seed", "?")}, then run again.')
        return 1

    if not args.force and not wait_unlock(world):
        print('ERROR: close Minecraft and retry.')
        return 1

    if args.camp:
        camp = tuple(args.camp)
    elif 'camp' in preset:
        c = preset['camp']
        camp = (int(c['x']), int(c['y']), int(c['z']))
    else:
        camp = read_spawn(world)

    print(f'World: {world_name} (folder: {world.name})')
    print(f'Seed (preset): {preset.get("seed", "n/a")}')
    print(f'Camp: {camp[0]} {camp[1]} {camp[2]}')

    copy_camp_pack(world)
    patch_deploy_coords(world, camp, preset)
    enable_datapack(world)
    if args.install_cnpc:
        install_dialogs(world)
    if args.set_spawn or preset.get('set_spawn', True):
        set_world_spawn(world, *camp)

    print('\nDone.')
    print(f'1. Open world "{world_name}" — camp builds at {camp[0]} {camp[1]} {camp[2]}')
    print('2. Or: /function cooptech_world:camp/deploy')
    print('3. Journal + FTB Quests at camp (no NPC markers)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
