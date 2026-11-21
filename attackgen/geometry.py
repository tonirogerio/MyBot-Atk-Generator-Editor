"""Approximate the geometry the bot computes at attack time.

The bot derives drop lines from the red zone it detects on each base, so the
exact points only exist during a real attack. This module reproduces the same
shape with a reference diamond so the editor can preview a script and so a
planner can reason about depth and spacing without the game running.

Coordinates are in the game's 860x732 capture space.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# A typical main village diamond, close to the reference used by
# ConvertInternalExternArea().
DIAMOND = {"left": 70, "right": 790, "top": 50, "bottom": 620}

# Relative side name -> fixed edge, for the default approach side
# (BOTTOM-RIGHT). Mirrors __AttackCSV_ApplyMainSideAliases().
SIDE_TO_EDGE = {
    "FRONT-LEFT": "BOTTOM-RIGHT-DOWN",
    "FRONT-RIGHT": "BOTTOM-RIGHT-UP",
    "RIGHT-FRONT": "TOP-RIGHT-DOWN",
    "RIGHT-BACK": "TOP-RIGHT-UP",
    "LEFT-FRONT": "BOTTOM-LEFT-DOWN",
    "LEFT-BACK": "BOTTOM-LEFT-UP",
    "BACK-LEFT": "TOP-LEFT-DOWN",
    "BACK-RIGHT": "TOP-LEFT-UP",
}

# Edge -> the two diamond corners it runs between, ordered so index 1 is the
# corner end and the last index is the middle of the side.
EDGE_CORNERS = {
    "TOP-LEFT-UP": ("left", "top"),
    "TOP-LEFT-DOWN": ("left", "top"),
    "TOP-RIGHT-UP": ("right", "top"),
    "TOP-RIGHT-DOWN": ("right", "top"),
    "BOTTOM-LEFT-UP": ("left", "bottom"),
    "BOTTOM-LEFT-DOWN": ("left", "bottom"),
    "BOTTOM-RIGHT-UP": ("right", "bottom"),
    "BOTTOM-RIGHT-DOWN": ("right", "bottom"),
}

# Direction that points out of the base for each corner. add_tiles moves the
# drop point along this diagonal, matching MakeDropPoints().
OUTWARD = {
    "TOP-LEFT": (-1, -1),
    "TOP-RIGHT": (1, -1),
    "BOTTOM-LEFT": (-1, 1),
    "BOTTOM-RIGHT": (1, 1),
}

PIXELS_PER_TILE = 8


@dataclass
class Point:
    x: float
    y: float


def diamond_corners() -> dict[str, Point]:
    mid_x = (DIAMOND["left"] + DIAMOND["right"]) / 2
    mid_y = (DIAMOND["top"] + DIAMOND["bottom"]) / 2
    return {
        "top": Point(mid_x, DIAMOND["top"]),
        "right": Point(DIAMOND["right"], mid_y),
        "bottom": Point(mid_x, DIAMOND["bottom"]),
        "left": Point(DIAMOND["left"], mid_y),
    }


def drop_points(side: str, count: int, add_tiles: int) -> list[Point]:
    """Evenly spaced points along one side, shifted by add_tiles.

    Positive add_tiles moves the points outside the base, negative moves them
    inside, at 8 pixels per tile. This is the same offset the bot applies.
    """
    edge = SIDE_TO_EDGE.get(side, "BOTTOM-RIGHT-DOWN")
    corner_name, middle_name = EDGE_CORNERS[edge]
    corners = diamond_corners()
    start = corners[corner_name]
    end = corners[middle_name]
    corner = edge.rsplit("-", 1)[0]
    direction = OUTWARD[corner]
    offset = add_tiles * PIXELS_PER_TILE

    count = max(1, count)
    points = []
    for step in range(count):
        fraction = (step + 0.5) / count
        points.append(
            Point(
                start.x + (end.x - start.x) * fraction + direction[0] * offset,
                start.y + (end.y - start.y) * fraction + direction[1] * offset,
            )
        )
    return points


def building_anchor(name: str) -> Point:
    """A plausible position for a defence, used only for the preview.

    Real positions come from the bot's image search during the attack. The
    preview places each defence kind on a ring so targeted spells are visible.
    """
    order = [
        "TOWNHALL", "EAGLE", "MONOLITH", "SCATTER", "INFERNO", "XBOW",
        "AIRDEFENSE", "WIZTOWER", "MORTAR", "FIRESPITTER", "REVENGE",
    ]
    center = diamond_corners()["top"]
    mid_y = (DIAMOND["top"] + DIAMOND["bottom"]) / 2
    center = Point(center.x, mid_y)
    slot = order.index(name) if name in order else len(order)
    angle = -math.pi / 2 + slot * (2 * math.pi / (len(order) + 1))
    radius = 70 + (slot % 3) * 45
    return Point(center.x + math.cos(angle) * radius, center.y + math.sin(angle) * radius)
