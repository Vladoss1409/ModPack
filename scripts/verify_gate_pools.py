#!/usr/bin/env python3
"""Verify gate quests depend on all 4 wave branches and use checkmark tasks."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "overrides" / "config" / "ftbquests" / "quests" / "chapters"
GATE_POOL_JS = ROOT / "overrides" / "kubejs" / "server_scripts" / "quests" / "coop_gate_pool.js"
GATE_REGISTRY_JS = ROOT / "overrides" / "kubejs" / "server_scripts" / "quests" / "coop_gate_registry.js"

GATE_NUMS = (8, 15, 22)
WAVE_STARTS = {8: 2, 15: 9, 22: 16}


def qid_t0(n: int) -> str:
    return f"5217A{n:011d}"


def qid_tier(tier: int, n: int) -> str:
    return f"522{tier}A{n:011X}"


def expected_branch_ids(tier: int | None, gate_num: int) -> list[str]:
    start = WAVE_STARTS[gate_num]
    if tier is None:
        return [qid_t0(start + i) for i in range(4)]
    return [qid_tier(tier, start + i) for i in range(4)]


def parse_quest_blocks(text: str) -> list[dict]:
    quests: list[dict] = []
    for block in re.findall(r"\{[^{}]*?id: \"(52[12][0-9A]A[0-9A]+)\"[^{}]*?\}", text, re.DOTALL):
        pass
    # Split on quest entries at tab level
    for m in re.finditer(
        r'\t\t\{\s*description:.*?\n\t\t\ty: [0-9.]+d\s*\},',
        text,
        re.DOTALL,
    ):
        chunk = m.group(0)
        qm = re.search(r'id: "(52[12][0-9A]A[0-9A]+)"', chunk)
        if not qm:
            continue
        qid = qm.group(1)
        num = int(qid[-2:], 16) if "522" in qid else int(qid[-2:])
        # T0 uses decimal suffix in id
        nm = re.search(r"A0+([0-9A-F]+)", qid)
        quest_num = int(nm.group(1), 16) if "522" in qid else int(qid[-2:])
        if "5217" in qid:
            quest_num = int(re.search(r"5217A0+(\d+)", qid).group(1))
        deps_m = re.search(r"dependencies: \[(.*?)\]", chunk, re.DOTALL)
        deps = re.findall(r'"([^"]+)"', deps_m.group(1)) if deps_m else []
        task_types = re.findall(r'type: "(custom|checkmark)"', chunk)
        tags_m = re.search(r"tags: \[(.*?)\]", chunk, re.DOTALL)
        tags = re.findall(r'"([^"]+)"', tags_m.group(1)) if tags_m else []
        quests.append(
            {
                "id": qid,
                "num": quest_num,
                "deps": deps,
                "task_types": task_types,
                "tags": tags,
                "chapter": None,
            }
        )
    return quests


def tier_from_chapter(name: str) -> int | None:
    if name == "main_t0_rift.snbt":
        return None
    m = re.match(r"main_t(\d)_", name)
    return int(m.group(1)) if m else None


def scan_chapters() -> tuple[list[dict], dict[str, set[str]]]:
    gates: list[dict] = []
    pool_tags: dict[str, set[str]] = {}
    for ch in sorted(CHAPTERS.glob("main_t*.snbt")):
        tier = tier_from_chapter(ch.name)
        text = ch.read_text(encoding="utf-8")
        for q in parse_quest_blocks(text):
            q["chapter"] = ch.name
            q["tier"] = tier
            if q["num"] in GATE_NUMS:
                gates.append(q)
            for tag in q["tags"]:
                if tag.startswith("pool_") or tag == "branch_pool":
                    pool_tags.setdefault(ch.name, set()).add(tag)
    return gates, pool_tags


def check_removed_kubejs() -> list[str]:
    errors: list[str] = []
    if GATE_POOL_JS.exists():
        errors.append(f"{GATE_POOL_JS.name} should be removed (gate pools disabled)")
    if GATE_REGISTRY_JS.exists():
        errors.append(f"{GATE_REGISTRY_JS.name} should be removed (gate pools disabled)")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(check_removed_kubejs())
    gates, pool_tags = scan_chapters()

    for gate in gates:
        tier = gate["tier"]
        num = gate["num"]
        expected = set(expected_branch_ids(tier, num))
        actual = set(gate["deps"])
        if actual != expected:
            errors.append(
                f"{gate['chapter']} gate {num} ({gate['id']}): "
                f"deps {sorted(actual)} != expected {sorted(expected)}"
            )
        if "custom" in gate["task_types"]:
            errors.append(f"{gate['chapter']} gate {num}: still uses custom task")
        if "checkmark" not in gate["task_types"]:
            errors.append(f"{gate['chapter']} gate {num}: missing checkmark task")

    for ch, tags in pool_tags.items():
        errors.append(f"{ch} still has pool tags: {sorted(tags)}")

    print(f"Gate quests scanned: {len(gates)} (expected {len(GATE_NUMS) * 6})")
    if len(gates) != len(GATE_NUMS) * 6:
        errors.append(f"expected {len(GATE_NUMS) * 6} gate quests, found {len(gates)}")
    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("\nOK: gates depend on all 4 wave branches with checkmark tasks")
    print("OK: pool KubeJS removed, no pool_* / branch_pool tags in main chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
