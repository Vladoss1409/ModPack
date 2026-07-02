"""Quest reward helpers — seed items (~45%) + XP (docs/quest-writing-guide.md)."""
from __future__ import annotations

import re

ITEM_TASK_RE = re.compile(r'item: "([^"]+)"(?:, count: (\d+)L)?')


def first_item_task(tasks: list[str]) -> tuple[str, int] | None:
    for t in tasks:
        m = ITEM_TASK_RE.search(t)
        if m:
            count = int(m.group(2)) if m.group(2) else 1
            return m.group(1), count
    return None


def seed_count(required: int) -> int:
    if required <= 1:
        return 1
    return max(1, min(required - 1, round(required * 0.65)))


RELICS_BY_TIER: dict[int, str] = {
    0: "kubejs:reliquary_field",
    1: "kubejs:reliquary_field",
    2: "kubejs:reliquary_resonant",
    3: "kubejs:reliquary_arcane",
    4: "kubejs:reliquary_primordial",
    5: "kubejs:reliquary_convergence",
}


def reliquary_for_tier(tier: int) -> str:
    return RELICS_BY_TIER.get(tier, "kubejs:reliquary_field")


def should_add_reliquary(
    tier: int,
    quest_num: int,
    *,
    optional: bool = False,
    gate: bool = False,
    finale: bool = False,
    side: bool = False,
) -> bool:
    if finale and side:
        return True
    if gate and tier in (0, 2, 4):
        return True
    if optional and quest_num % 2 == 0:
        return True
    if not optional and not gate and quest_num % 9 == 0:
        return True
    return False


def branch_xp(tier: int, *, optional: bool = False) -> int:
    if optional:
        return 10 + tier * 2
    return 12 + tier * 5


def branch_rewards_from_tasks(
    tasks: list[str],
    tier: int,
    *,
    item_fn,
    xp_fn,
    reliquary_fn,
    rid_item: int,
    rid_xp: int,
    rid_relic: int,
    quest_num: int = 0,
    optional: bool = False,
) -> list[str]:
    rewards: list[str] = []
    if not optional:
        parsed = first_item_task(tasks)
        if parsed:
            item, count = parsed
            rewards.append(item_fn(rid_item, item, seed_count(count)))
    if should_add_reliquary(tier, quest_num, optional=optional):
        rewards.append(reliquary_fn(rid_relic, reliquary_for_tier(tier)))
    rewards.append(xp_fn(rid_xp, branch_xp(tier, optional=optional)))
    return rewards


def gate_rewards(
    tier: int,
    *,
    item_fn,
    xp_fn,
    reliquary_fn,
    page_item: str | None,
    rid_page: int,
    rid_xp: int,
    rid_relic: int,
) -> list[str]:
    rewards: list[str] = []
    if page_item:
        rewards.append(item_fn(rid_page, page_item))
    if should_add_reliquary(tier, 0, gate=True):
        rewards.append(reliquary_fn(rid_relic, reliquary_for_tier(tier)))
    rewards.append(xp_fn(rid_xp, 40 + tier * 5))
    return rewards


def side_rewards_from_item(
    item: str,
    count: int,
    *,
    item_fn,
    xp_fn,
    reliquary_fn,
    rid_item: int,
    rid_xp: int,
    rid_relic: int,
    tier: int,
    quest_num: int,
    finale: bool = False,
) -> list[str]:
    rewards = [item_fn(rid_item, item, seed_count(count))]
    if should_add_reliquary(tier, quest_num, side=True, finale=finale):
        rewards.append(reliquary_fn(rid_relic, reliquary_for_tier(min(tier, 5))))
    rewards.append(xp_fn(rid_xp, 14 + tier * 3 + (20 if finale else 0)))
    return rewards
