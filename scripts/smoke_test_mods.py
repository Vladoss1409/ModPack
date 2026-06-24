#!/usr/bin/env python3
"""Smoke-test modpack instance: validate JARs and optionally monitor launch log."""
from __future__ import annotations

import argparse
import sys
import time
import zipfile
from pathlib import Path

FORBIDDEN = ('optifine', 'neoforge', 'rubidium-mc', 'rubidium-extra', 'textrues_embeddium_options')


def validate_mods_dir(mods_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    jars = sorted(mods_dir.glob('*.jar'))
    if not jars:
        return ['no JAR files found'], warnings

    for jar in jars:
        name = jar.name.lower()
        for bad in FORBIDDEN:
            if bad in name:
                warnings.append(f'{jar.name}: forbidden pattern "{bad}"')
        try:
            with zipfile.ZipFile(jar) as zf:
                zf.namelist()[:1]
        except zipfile.BadZipFile:
            errors.append(f'{jar.name}: invalid ZIP/JAR')
        except Exception as exc:
            errors.append(f'{jar.name}: {exc}')
    return errors, warnings


def monitor_log(log_path: Path, seconds: int = 90) -> int:
    if not log_path.exists():
        print(f'LOG: waiting for {log_path}')
    start = time.time()
    last_size = 0
    while time.time() - start < seconds:
        if log_path.exists():
            text = log_path.read_text(encoding='utf-8', errors='replace')
            if len(text) != last_size:
                last_size = len(text)
                lines = text.splitlines()
                print(f'LOG: {len(lines)} lines')
                for line in lines[-5:]:
                    print('  ', line[:200])
                joined = text.lower()
                if 'loading complete' in joined or 'finished loading' in joined:
                    print('LOG: loading complete detected')
                    return 0
                if 'crash' in joined and 'crash-reports' in joined:
                    print('LOG: crash detected')
                    return 1
                if 'error' in joined and 'failed to load' in joined:
                    print('LOG: mod load failure detected')
                    return 1
                if 'modlauncher' in joined and 'starting' in joined and len(lines) > 10:
                    print('LOG: passed early ModLauncher stage')
        time.sleep(5)
    print('LOG: monitor timeout (no crash in window)')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mods', type=Path, required=True)
    parser.add_argument('--log', type=Path)
    parser.add_argument('--monitor-seconds', type=int, default=0)
    args = parser.parse_args()

    errors, warnings = validate_mods_dir(args.mods)
    print(f'Checked {len(list(args.mods.glob("*.jar")))} JAR(s) in {args.mods}')
    for w in warnings:
        print(f'WARN: {w}')
    for e in errors:
        print(f'ERROR: {e}')
    if errors:
        return 1

    if args.log and args.monitor_seconds > 0:
        return monitor_log(args.log, args.monitor_seconds)
    print('OK: all JARs readable')
    return 0


if __name__ == '__main__':
    sys.exit(main())
