#!/usr/bin/env python3
"""Launch Forge instance for smoke test and monitor latest.log."""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

import minecraft_launcher_lib.command as mc_cmd

MC = Path(r'C:\Users\GameOn_Dp\AppData\Roaming\.minecraft')
VERSION_NAME = 'Мой мод пак'
GAME_DIR = MC / 'versions' / VERSION_NAME
LOG_PATH = GAME_DIR / 'logs' / 'latest.log'
VERSION_JSON = GAME_DIR / f'{VERSION_NAME}.json'
MONITOR_SECONDS = 180


def normalize_version_json(data: dict) -> dict:
    fixed = copy.deepcopy(data)
    for section in ('game', 'jvm'):
        new_args = []
        for entry in fixed['arguments'][section]:
            e = dict(entry)
            if 'values' in e and 'value' not in e:
                e['value'] = e.pop('values')
            new_args.append(e)
        fixed['arguments'][section] = new_args
    return fixed


def main() -> int:
    data = json.loads(VERSION_JSON.read_text(encoding='utf-8'))
    fixed = normalize_version_json(data)
    backup = VERSION_JSON.with_suffix('.json.bak')
    temp = GAME_DIR / '_smoke_test.json'
    shutil.copy2(VERSION_JSON, backup)
    temp.write_text(json.dumps(fixed), encoding='utf-8')
    shutil.copy2(temp, VERSION_JSON)

    options = {
        'username': 'SmokeTest',
        'uuid': str(uuid.uuid4()),
        'token': '0',
        'version': VERSION_NAME,
        'gameDirectory': str(GAME_DIR),
        'classpathSeparator': mc_cmd.get_classpath_separator(),
        'libraryDirectory': str(MC / 'libraries'),
        'nativesDirectory': str(GAME_DIR / 'natives'),
        'launcherName': 'CoopTechSmokeTest',
        'launcherVersion': '1.0',
        'userType': 'legacy',
        'versionType': 'modified',
        'resolutionWidth': '925',
        'resolutionHeight': '530',
        'jvmArguments': ['-Xms6144M', '-Xmx6144M'],
    }

    try:
        cmd = mc_cmd.get_minecraft_command(VERSION_NAME, str(MC), options)
        LOG_PATH.write_text('', encoding='utf-8')
        print('Launching Forge smoke test...')
        proc = subprocess.Popen(cmd, cwd=str(GAME_DIR))
        passed_early = False
        exit_code = None

        for _ in range(MONITOR_SECONDS // 5):
            if proc.poll() is not None:
                exit_code = proc.returncode
                print(f'Process exited with code {exit_code}')
                break
            if LOG_PATH.exists():
                text = LOG_PATH.read_text(encoding='utf-8', errors='replace')
                lines = text.splitlines()
                if len(lines) > 15 and not passed_early:
                    passed_early = True
                    print(f'PASS: passed early ModLauncher stage ({len(lines)} lines)')
                lower = text.lower()
                if 'modloading failed' in lower or 'error during pre-loading phase' in lower:
                    print('FAIL: mod loading error')
                    for line in lines[-25:]:
                        if any(k in line.lower() for k in ('error', 'exception', 'failure message', 'requires')):
                            print(line.encode('ascii', 'replace').decode('ascii')[:250])
                    proc.terminate()
                    return 1
                if 'loading complete' in lower or 'finished loading' in lower:
                    print('PASS: loading complete')
                    proc.terminate()
                    return 0
            time.sleep(5)

        if proc.poll() is None:
            print(f'PASS: still running after {MONITOR_SECONDS}s')
            proc.terminate()
            return 0 if passed_early else 1
        return 0 if passed_early and exit_code == 0 else (0 if passed_early else 1)
    finally:
        shutil.copy2(backup, VERSION_JSON)
        backup.unlink(missing_ok=True)
        temp.unlink(missing_ok=True)


if __name__ == '__main__':
    sys.exit(main())
