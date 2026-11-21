"""Summarise what an attack script deploys.

Useful both for the editor sidebar and for the bandit, which records the shape
of a script alongside its results.
"""

from __future__ import annotations

from .model import Drop, Script
from .schema import UNITS


def _quantity(value: str) -> int:
    """Upper bound of a quantity, which may be a single number or a range."""
    parts = [int(part) for part in value.split("-") if part.strip().isdigit()]
    return max(parts) if parts else 0


def deployment_summary(script: Script) -> list[tuple[str, str, int]]:
    """Return (unit, kind, total quantity) in drop order, REMAIN excluded."""
    totals: dict[str, int] = {}
    order: list[str] = []
    for drop in script.drops():
        if drop.unit in ("REMAIN", "AnyS"):
            continue
        if drop.unit not in totals:
            totals[drop.unit] = 0
            order.append(drop.unit)
        totals[drop.unit] += _quantity(drop.quantity)
    rows = []
    for unit in order:
        info = UNITS.get(unit, {"name": unit, "kind": "unknown"})
        rows.append((unit, info["kind"], totals[unit]))
    return rows


def housing_used(script: Script) -> int:
    """Housing space of the troops the script deploys. Heroes and spells are free."""
    used = 0
    for unit, kind, quantity in deployment_summary(script):
        if kind == "troop":
            used += UNITS[unit]["space"] * quantity
    return used
