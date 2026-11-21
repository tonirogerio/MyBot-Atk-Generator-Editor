"""Parametric attack templates.

Each template returns a Script built from the same command model the parser
produces, so anything generated here passes through the same validator and
emitter as a hand written script.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .model import Drop, Make, Note, Script, Wait


def meteor_mayhem(name: str = "MeteorMayhem") -> Script:
    """A ground smash built around Meteor Golems, Throwers and Totem spells.

    Mirrors the structure of the PHMOD-MeteorMayhem script: a wide troop line,
    support directly behind it, totems and earthquakes dropped deeper in, and
    the remaining army committed after the funnel is open.
    """
    script = Script(name=name)
    script.commands += [
        Note(text=f"Author: attack-generator"),
        Note(text="Army: Meteor Golems, Throwers, Healers, Balloons, Apprentice Warden"),
        Note(text="Spells: Rage, Totem, Earthquake"),
        Note(text="Siege: Log Launcher"),
        Make("A", "FRONT-LEFT", 10, 1, "INT-EXT"),
        Make("B", "FRONT-RIGHT", 10, 1, "INT-EXT"),
        Make("C", "FRONT-LEFT", 10, -8, "INT-EXT"),
        Make("D", "FRONT-RIGHT", 10, -8, "INT-EXT"),
        Make("E", "FRONT-LEFT", 10, -22, "INT-EXT"),
        Make("F", "FRONT-RIGHT", 10, -22, "INT-EXT"),
        Make("Z", "FRONT-RIGHT", 10, 1, "EXT-INT"),
        Drop("A-B", "1-10", "4", "MeteorG", "128", "0", "16-32"),
        Drop("A", "1", "5", "RootR", "128", "0", "16-32"),
        Drop("A", "1", "4", "Throw", "128", "0", "16-32"),
        Drop("A", "1", "5", "Heal", "128", "0", "16-32"),
        Drop("A", "1", "1", "LogL", "128", "0", "16-32"),
        Drop("A", "1", "1", "AppWard", "128", "0", "16-32"),
        Drop("A", "1", "1", "Warden", "128", "0", "16-32"),
        Drop("C", "1", "1", "TSpell", "256", "0", "128-256"),
        Drop("D", "4", "1", "TSpell", "256", "0", "128-256"),
        Drop("C", "2", "1", "ESpell", "128", "0", "16-32"),
        Drop("D", "2", "1", "ESpell", "128", "0", "16-32"),
        Drop("A", "1", "1", "King", "128", "0", "16-32"),
        Drop("A", "1", "1", "Queen", "128", "0", "16-32"),
        Drop("Z", "5", "1", "Champion", "128", "0", "16-32"),
        Wait("8000-12000"),
        Drop("E", "3", "1", "RSpell", "256", "0", "128-256"),
        Drop("F", "3", "1", "RSpell", "256", "0", "128-256"),
        Wait("10000-15000"),
        Drop("Z", "3", "10", "REMAIN", "128", "0", "16-32"),
    ]
    return script


def edrag_loon(name: str = "EDragLoon") -> Script:
    """Electro Dragons and Balloons spread across both front edges.

    Balloons go down first to soak seeking air mines, then the dragons in a
    staggered line with rage spells dropped ahead of them.
    """
    script = Script(name=name)
    script.commands += [
        Note(text="Author: attack-generator"),
        Note(text="Army: Electro Dragons, Balloons, Rage, Freeze"),
        Note(text="Siege: Battle Blimp"),
        Make("A", "FRONT-LEFT", 10, 2, "INT-EXT"),
        Make("B", "FRONT-RIGHT", 10, 2, "INT-EXT"),
        Make("C", "FRONT-LEFT", 10, -6, "INT-EXT"),
        Make("D", "FRONT-RIGHT", 10, -6, "INT-EXT"),
        Make("H", "FRONT-LEFT", 1, 0, "IGNORE", building="EAGLE"),
        Drop("A", "5", "2", "Ball", "60-90", "2-4", "15-25"),
        Drop("B", "5", "2", "Ball", "60-90", "2-4", "15-25"),
        Drop("A", "6,4,2", "3", "EDrag", "80-120", "2-5", "20-30"),
        Drop("B", "2,4,6", "3", "EDrag", "80-120", "2-5", "20-30"),
        Drop("C", "3", "1", "RSpell", "50-80", "0", "10-20"),
        Drop("D", "3", "1", "RSpell", "50-80", "0", "10-20"),
        Drop("B", "1", "1", "BattleB", "50-80", "0", "10-20"),
        Drop("B", "1", "1", "Castle", "50-80", "0", "10-20"),
        Drop("B", "1", "1", "Warden", "50-80", "0", "10-20"),
        Drop("H", "1", "1", "FSpell", "50-80", "0", "10-20"),
        Wait("6000-8000", "AQ"),
        Drop("A", "1", "1", "King", "50-80", "0", "10-20"),
        Drop("A", "1", "1", "Queen", "50-80", "0", "10-20"),
        Drop("A", "1", "1", "Champion", "50-80", "0", "10-20"),
        Drop("C", "6", "1", "RSpell", "50-80", "0", "10-20"),
        Drop("D", "6", "1", "RSpell", "50-80", "0", "10-20"),
        Wait("12000-16000", "50%"),
        Drop("A-B", "1-10", "10", "REMAIN", "60-90", "0", "10-20"),
    ]
    return script


def queen_charge(name: str = "QueenCharge") -> Script:
    """A queen walk from one corner into a hybrid of miners and hog riders.

    The queen, healers and a wall opener start at the corner. Once she has
    worked into the base the hybrid goes through the opened wall with heal
    spells behind it.
    """
    script = Script(name=name)
    script.commands += [
        Note(text="Author: attack-generator"),
        Note(text="Army: Queen walk into Miners and Hog Riders"),
        Note(text="Spells: Heal, Rage, Freeze"),
        Make("A", "LEFT-FRONT", 6, 2, "EXT-INT"),
        Make("B", "LEFT-FRONT", 4, -10, "INT-EXT"),
        Make("C", "FRONT-LEFT", 10, 1, "INT-EXT"),
        Make("D", "FRONT-RIGHT", 10, 1, "INT-EXT"),
        Make("E", "FRONT-LEFT", 8, -12, "INT-EXT"),
        Make("F", "FRONT-RIGHT", 8, -12, "INT-EXT"),
        Make("H", "FRONT-LEFT", 1, 0, "IGNORE", building="TOWNHALL"),
        Drop("A", "1", "5", "Heal", "200-300", "0", "100-200"),
        Drop("A", "1", "1", "Queen", "200", "0", "100-200"),
        Drop("A", "2", "4", "Wall", "150-250", "0", "50-100"),
        Drop("B", "2", "1", "RSpell", "100-150", "0", "50-100"),
        Wait("14000-18000"),
        Drop("C-D", "1-8", "6", "Mine", "80-120", "0", "20-40"),
        Drop("C-D", "1-8", "6", "Hogs", "80-120", "0", "20-40"),
        Drop("C", "1", "1", "SiegeB", "80-120", "0", "20-40"),
        Drop("C", "1", "1", "King", "80-120", "0", "20-40"),
        Drop("C", "1", "1", "Warden", "80-120", "0", "20-40"),
        Drop("E", "3", "1", "HSpell", "100-150", "0", "50-100"),
        Drop("F", "3", "1", "HSpell", "100-150", "0", "50-100"),
        Drop("H", "1", "1", "FSpell", "80-120", "0", "20-40"),
        Wait("10000-14000", "50%"),
        Drop("E", "5", "1", "HSpell", "100-150", "0", "50-100"),
        Drop("F", "5", "1", "HSpell", "100-150", "0", "50-100"),
        Drop("C-D", "1-10", "10", "REMAIN", "80-120", "0", "20-40"),
    ]
    return script


# Built-in templates
_BUILTIN_TEMPLATES = {
    "Meteor Mayhem": meteor_mayhem,
    "Electro Dragon Loons": edrag_loon,
    "Queen Charge Hybrid": queen_charge,
}

# User templates folder
_TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"


def _load_user_templates() -> dict:
    """Load custom templates from the templates folder."""
    templates = {}
    if not _TEMPLATES_DIR.exists():
        _TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        return templates
    for path in _TEMPLATES_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            name = data.get("name", path.stem)
            commands = data.get("commands", [])
            if commands:
                def make_builder(commands=commands):
                    script = Script(name=name)
                    for c in commands:
                        kind = c.get("kind", "").upper()
                        if kind == "MAKE":
                            script.commands.append(Make(
                                vector=c.get("vector", "A"),
                                side=c.get("side", "FRONT-LEFT"),
                                points=int(c.get("points", 10)),
                                add_tiles=int(c.get("add_tiles", 0)),
                                versus=c.get("versus", "INT-EXT"),
                                random_x=int(c.get("random_x", 0)),
                                random_y=int(c.get("random_y", 0)),
                                building=c.get("building", ""),
                            ))
                        elif kind == "DROP":
                            script.commands.append(Drop(
                                vectors=c.get("vectors", "A"),
                                index=c.get("index", "1"),
                                quantity=c.get("quantity", "1"),
                                unit=c.get("unit", "Barb"),
                                delay_points=c.get("delay_points", "128"),
                                delay_change=c.get("delay_change", "0"),
                                sleep_after=c.get("sleep_after", "16-32"),
                            ))
                        elif kind == "WAIT":
                            script.commands.append(Wait(
                                duration=c.get("duration", "3000"),
                                conditions=c.get("conditions", ""),
                            ))
                        elif kind == "NOTE":
                            script.commands.append(Note(text=c.get("text", "")))
                        elif kind == "RECALC":
                            script.commands.append(Recalc())
                    return script
                templates[name] = make_builder
        except Exception:
            pass
    return templates


def get_all_templates() -> dict:
    """Return merged dict of built-in + user templates."""
    result = dict(_BUILTIN_TEMPLATES)
    result.update(_load_user_templates())
    return result


def save_template(name: str, script: Script) -> Path:
    """Save a script as a user template JSON file."""
    _TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    path = _TEMPLATES_DIR / f"{name}.json"
    data = {
        "name": name,
        "commands": [
            {"kind": c.kind} | (
                {"vector": c.vector, "side": c.side, "points": c.points,
                 "add_tiles": c.add_tiles, "versus": c.versus,
                 "random_x": c.random_x, "random_y": c.random_y,
                 "building": c.building} if isinstance(c, Make) else
                {"vectors": c.vectors, "index": c.index, "quantity": c.quantity,
                 "unit": c.unit, "delay_points": c.delay_points,
                 "delay_change": c.delay_change, "sleep_after": c.sleep_after} if isinstance(c, Drop) else
                {"duration": c.duration, "conditions": c.conditions} if isinstance(c, Wait) else
                {"text": c.text} if isinstance(c, Note) else
                {} if isinstance(c, Recalc) else {}
            )
            for c in script.commands
        ],
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path
