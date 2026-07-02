#!/usr/bin/env python3
"""Find default crafting recipe JSON paths for gate-locked outputs."""
from __future__ import annotations

import json
import os
import zipfile
from pathlib import Path

MC = Path(os.environ.get("APPDATA", "")) / ".minecraft/versions/ModPack/mods"
TARGETS = [
    "thermal:machine_frame",
    "mekanism:steel_casing",
    "ae2:inscriber",
    "projecte:philosophers_stone",
    "draconicevolution:draconium_core",
]


def item_in_result(data: dict, item_id: str) -> bool:
    result = data.get("result")
    if isinstance(result, str):
        return result == item_id
    if isinstance(result, dict):
        if result.get("item") == item_id:
            return True
        if result.get("id") == item_id:
            return True
    if "results" in data:
        for r in data["results"]:
            if isinstance(r, dict) and (r.get("item") == item_id or r.get("id") == item_id):
                return True
    return False


def main() -> None:
    for item_id in TARGETS:
        ns = item_id.split(":")[0]
        print(f"\n=== {item_id} ===")
        for jar in sorted(MC.glob("*.jar")):
            if ns not in jar.name.lower() and not (
                ns == "ae2" and "appliedenergistics" in jar.name.lower()
            ):
                continue
            with zipfile.ZipFile(jar) as zf:
                for name in zf.namelist():
                    if "/recipes/" not in name or not name.endswith(".json"):
                        continue
                    try:
                        data = json.loads(zf.read(name))
                    except Exception:
                        continue
                    if item_in_result(data, item_id) or item_id.split(":")[1] in name:
                        rid = name.split("data/")[-1].replace(".json", "").replace("/", ":")
                        if item_id.split(":")[1] in name or item_in_result(data, item_id):
                            print(f"  {rid}")


if __name__ == "__main__":
    main()
