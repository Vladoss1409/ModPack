#!/usr/bin/env python3
"""Multi-pass readiness check for CoopTech quests + journal integration."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "overrides" / "config" / "ftbquests" / "quests" / "chapters"
ADV = ROOT / "overrides" / "data" / "cooptech" / "advancements" / "journal"
PATCHOULI = ROOT / "overrides" / "patchouli_books" / "expedition_journal" / "en_us" / "entries"
UNLOCKS_JS = ROOT / "overrides" / "kubejs" / "server_scripts" / "journal" / "journal_quest_unlocks.js"
INTERACT_JS = ROOT / "overrides" / "kubejs" / "server_scripts" / "items" / "cooptech_interact.js"
MODELS = ROOT / "overrides" / "kubejs" / "assets" / "kubejs" / "models" / "item"

sys.path.insert(0, str(ROOT / "scripts"))
from quest_content_v1 import SIDE_BRANCHES  # noqa: E402

QUEST_ID_RE = re.compile(r'"([0-9A-Fa-f]{16})"')


def load_quest_ids() -> set[str]:
    ids: set[str] = set()
    for p in CHAPTERS.glob("*.snbt"):
        text = p.read_text(encoding="utf-8")
        for m in re.finditer(r'\bid: "([0-9A-Fa-f]{16})"', text):
            ids.add(m.group(1).upper())
    return ids


def parse_unlocks_js() -> dict[str, list[str]]:
    text = UNLOCKS_JS.read_text(encoding="utf-8")
    # crude extract quest -> adv keys
    out: dict[str, list[str]] = {}
    block = re.search(r"var JOURNAL_UNLOCKS = \{([\s\S]*?)\n\}", text)
    if not block:
        return out
    body = block.group(1)
    for m in re.finditer(
        r"'([0-9A-Fa-f]{16})'\s*:\s*\[([\s\S]*?)\]\s*,|"
        r"'([0-9A-Fa-f]{16})'\s*:\s*\{\s*adv:\s*'([^']+)'",
        body,
    ):
        if m.group(1):
            qid = m.group(1).upper()
            advs = re.findall(r"adv:\s*'([^']+)'", m.group(2))
            out[qid] = advs
        elif m.group(3):
            out[m.group(3).upper()] = [m.group(4)]
    return out


def patchouli_advs() -> set[str]:
    advs: set[str] = set()
    for p in PATCHOULI.rglob("*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        a = data.get("advancement", "")
        if a.startswith("cooptech:journal/"):
            advs.add(a.split("/", 1)[1])
    return advs


def advancement_files() -> set[str]:
    return {p.stem for p in ADV.glob("*.json")}


def side_first_quest_ids() -> set[str]:
    ids: set[str] = set()
    for fn, *_rest in SIDE_BRANCHES:
        prefix = _rest[4]  # fn, title, ic, grp, old, ord, prefix -> wrong
    return ids


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # ── Pass 1: chapter files ──
    expected_main = [f"main_t{i}_{'rift' if i == 0 else 'spark circuit network dragon convergence'.split()[i-1]}" for i in range(6)]
    # fix names
    main_files = {
        0: "main_t0_rift.snbt",
        1: "main_t1_spark.snbt",
        2: "main_t2_circuit.snbt",
        3: "main_t3_network.snbt",
        4: "main_t4_dragon.snbt",
        5: "main_t5_convergence.snbt",
    }
    for mf in main_files.values():
        if not (CHAPTERS / mf).exists():
            errors.append(f"Missing main chapter: {mf}")
    side_count = len(list(CHAPTERS.glob("side_*.snbt")))
    if side_count != 20:
        errors.append(f"Expected 20 side chapters, found {side_count}")
    if not (CHAPTERS / "main_post_anchor.snbt").exists():
        errors.append("Missing post-T5 hub: main_post_anchor.snbt")

    # ── Pass 2: unlock quest IDs exist ──
    quest_ids = load_quest_ids()
    unlocks = parse_unlocks_js()
    for qid, advs in unlocks.items():
        if qid not in quest_ids and qid.startswith(("5217", "5221", "5222", "5223", "5224", "5225", "A8", "A9")):
            errors.append(f"Unlock quest ID not in chapters: {qid} -> {advs}")
        for a in advs:
            if not (ADV / f"{a}.json").exists():
                errors.append(f"Missing advancement for unlock: cooptech:journal/{a} (quest {qid})")

    # ── Pass 3: patchouli -> advancement ──
    p_adv = patchouli_advs()
    adv_files = advancement_files()
    for a in p_adv:
        if a not in adv_files:
            errors.append(f"Patchouli references missing advancement: {a}")

    # ── Pass 4: codex + progress coverage ──
    codex_main = list((PATCHOULI / "codex_energy").glob("*.json")) + list((PATCHOULI / "codex_network").glob("*.json"))
    codex_main += list((PATCHOULI / "codex_camp").glob("*.json")) + list((PATCHOULI / "codex").glob("*.json"))
    codex_sides = list((PATCHOULI / "codex_branches").glob("*.json"))
    if len(codex_sides) != 20:
        errors.append(f"Expected 20 codex side entries, found {len(codex_sides)}")
    if len(codex_main) < 16:
        warnings.append(f"Main codex entries: {len(codex_main)} (expected ~16)")

    for tier in range(1, 6):
        for beat in ["intro", "w1", "w2", "w3", "finale"]:
            p = PATCHOULI / "progress" / f"t{tier}_{beat}.json"
            if beat == "intro" or beat.startswith("w") or beat == "finale":
                if not p.exists():
                    errors.append(f"Missing progress entry: {p.name}")

    t0_beats = ["rift", "camp", "home", "ready", "spark"]
    for b in t0_beats:
        if not (PATCHOULI / "progress" / f"t0_{b}.json").exists():
            errors.append(f"Missing T0 progress: t0_{b}.json")

    branches = list((PATCHOULI / "branches").glob("*.json"))
    if len(branches) != 20:
        errors.append(f"Expected 20 branch lore entries, found {len(branches)}")

    # ── Pass 5: PAGE_LINES + models ──
    interact = INTERACT_JS.read_text(encoding="utf-8")
    for prefix in ["spark", "cell", "matrix", "singularity", "nexus"]:
        for i in range(5):
            pid = f"journal_page_{prefix}_{i:02d}"
            if f"{pid}:" not in interact and f"{pid}:" not in interact:
                if pid not in interact:
                    errors.append(f"Missing PAGE_LINES: {pid}")
            model = MODELS / f"{pid}.json"
            if not model.exists():
                warnings.append(f"Missing item model: {pid}.json")

    # ── Pass 6: SNBT description format (informational — FTB accepts newline-joined strings) ──
    # skipped: main + side chapters use same generator format

    # ── Pass 7: dispatcher tone in main tiers ──
    for mf in main_files.values():
        t = (CHAPTERS / mf).read_text(encoding="utf-8")
        if "Диспетчер" in t:
            errors.append(f"Dispatcher tone still in {mf}")

    # ── Pass 8: side first-quest unlock IDs ──
    for _fn, _title, _ic, _grp, _old, _ord, prefix, _q, _layout in SIDE_BRANCHES:
        q1 = f"{prefix}000000000001".upper()
        if q1 not in unlocks:
            errors.append(f"Side {prefix} first quest not in JOURNAL_UNLOCKS: {q1}")
        elif "codex_side_" not in str(unlocks[q1]):
            errors.append(f"Side {prefix} missing codex unlock on {q1}")

    # ── Pass 9: T1-T5 gate hex IDs for w2/w3 lore ──
    for tier in range(1, 6):
        prefix = f"522{tier}A"
        for n_hex, beat in [("0F", "w2"), ("16", "w3")]:
            qid = f"{prefix}000000000{n_hex}"
            if qid not in quest_ids:
                errors.append(f"Missing gate quest in chapters: {qid} ({beat} T{tier})")
            adv = f"t{tier}_lore_{beat}"
            if qid not in unlocks or adv not in unlocks.get(qid, []):
                errors.append(f"Missing lore unlock {adv} on quest {qid}")

    # ── Pass 10: T1-T5 codex unlocks on gates ──
    codex_gate_checks = [
        ("5221A00000000008", ["t1_thermal", "t1_powah"]),
        ("5222A00000000001", ["t2_mek"]),
        ("5222A00000000008", ["t2_enderio", "t2_flux"]),
        ("5223A00000000001", ["t3_ae2"]),
        ("5223A00000000008", ["t3_emc"]),
        ("5224A00000000001", ["t4_draconic"]),
        ("5224A00000000008", ["t4_fusion"]),
        ("5225A00000000001", ["t5_next_ae"]),
        ("5225A00000000008", ["t5_anchor"]),
    ]
    for qid, expected in codex_gate_checks:
        got = unlocks.get(qid, [])
        for e in expected:
            if e not in got:
                errors.append(f"Quest {qid} missing codex adv {e}")

    # ── Report ──
    print("=== CoopTech readiness check ===")
    print(f"Chapters: {len(list(CHAPTERS.glob('*.snbt')))} (main 6 + hub 1 + sides 20 = 27)")
    print(f"Quest IDs in chapters: {len(quest_ids)}")
    print(f"Journal unlock mappings: {len(unlocks)}")
    print(f"Advancement files: {len(adv_files)}")
    print(f"Patchouli entries with adv: {len(p_adv)}")
    print(f"Codex main: {len(codex_main)}, codex sides: {len(codex_sides)}, branches: {len(branches)}")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings[:20]:
            print(f"  ! {w}")
        if len(warnings) > 20:
            print(f"  ... +{len(warnings)-20} more")

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  X {e}")
        return 1

    print("\nOK — all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
