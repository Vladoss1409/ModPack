#!/usr/bin/env python3
"""Validate all JAR files in mods/."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS = ROOT / 'mods'

errors: list[str] = []
warnings: list[str] = []


def is_valid_jar(path: Path) -> bool:
    with path.open('rb') as f:
        header = f.read(2)
    return header == b'PK'


def main() -> int:
    if not MODS.is_dir():
        print(f'ERROR: mods directory not found: {MODS}')
        return 1

    jars = sorted(MODS.glob('*.jar'))
    if not jars:
        print(f'ERROR: no JAR files in {MODS}')
        return 1

    for jar in jars:
        name = jar.name.lower()
        if not is_valid_jar(jar):
            errors.append(f'{jar.name}: not a valid JAR (expected PK zip header)')
        if 'neoforge' in name:
            warnings.append(f'{jar.name}: NeoForge build on Forge 47 modpack')
        if 'optifine' in name:
            warnings.append(f'{jar.name}: OptiFine conflicts with Embeddium/Oculus')

    print(f'Checked {len(jars)} JAR(s) in {MODS}')
    for w in warnings:
        print(f'WARN: {w}')
    for e in errors:
        print(f'ERROR: {e}')

    if errors:
        return 1
    if warnings:
        print(f'OK with {len(warnings)} warning(s)')
    else:
        print('OK: all JARs valid')
    return 0


if __name__ == '__main__':
    sys.exit(main())
