#!/usr/bin/env python3
"""Fix invalid Patchouli color tokens in patchouli_books JSON."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'overrides' / 'patchouli_books'

REPLACEMENTS = [
    (re.compile(r'\$\(5\)'), '$(#DD55DD)'),
    (re.compile(r'\$\(6\)'), '$(#FFAA00)'),
    (re.compile(r'\$\(c\)(?!:)'), '$(#FF5555)'),
    (re.compile(r'\$\(o\)'), '$(italic)'),
]


def fix_text(text: str) -> str:
    for pattern, repl in REPLACEMENTS:
        text = pattern.sub(repl, text)
    return text.replace('• ', '- ')


def main() -> None:
    for path in ROOT.rglob('*.json'):
        original = path.read_text(encoding='utf-8')
        updated = fix_text(original)
        if updated != original:
            path.write_text(updated, encoding='utf-8')
            print(f'fixed: {path.relative_to(ROOT.parent.parent)}')


if __name__ == '__main__':
    main()
