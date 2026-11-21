"""Static vocabulary of the MyBot CSV attack language.

Values mirror COCBot/MBR Global Variables.au3 and
COCBot/functions/Attack/AttackCSV/CheckCSVValues.au3 of MyBot PH MOD v16.4.
Short names are case sensitive and must match exactly.
"""

from __future__ import annotations

SIDES = (
    "FRONT-LEFT",
    "FRONT-RIGHT",
    "RIGHT-FRONT",
    "RIGHT-BACK",
    "LEFT-FRONT",
    "LEFT-BACK",
    "BACK-LEFT",
    "BACK-RIGHT",
    "RANDOM",
)

VERSUS = ("INT-EXT", "EXT-INT", "IGNORE")

# Building targets accepted by CheckCsvValues("MAKE", 8, ...) and by
# MakeTargetDropPoints(). A targeted vector only supports 1 or 5 drop points.
BUILDINGS = (
    "TOWNHALL",
    "EAGLE",
    "FIRESPITTER",
    "INFERNO",
    "XBOW",
    "WIZTOWER",
    "MORTAR",
    "AIRDEFENSE",
    "EX-WALL",
    "IN-WALL",
    "SCATTER",
    "MONOLITH",
    "REVENGE",
)

# Conditions recognised by the WAIT command (value2, comma separated).
WAIT_CONDITIONS = (
    "TH",
    "SIEGE",
    "TH+SIEGE",
    "50%",
    "AQ",
    "BK",
    "GW",
    "RC",
    "DD",
    "AQ+BK",
    "BK+AQ",
)

# The side the bot approaches the village from. It rotates every relative side
# name (FRONT-LEFT and friends) into a fixed screen edge.
MAIN_SIDES = ("BOTTOM-RIGHT", "BOTTOM-LEFT", "TOP-LEFT", "TOP-RIGHT")

# (short name, full name, housing space) for every deployable unit, in the
# exact order of $g_asTroopShortNames / $g_aiTroopSpace in MBR Global Variables.
TROOPS = (
    ("Barb", "Barbarian", 1), ("SBarb", "Super Barbarian", 5),
    ("Arch", "Archer", 1), ("SArch", "Super Archer", 12),
    ("Giant", "Giant", 5), ("SGiant", "Super Giant", 10),
    ("Gobl", "Goblin", 1), ("SGobl", "Sneaky Goblin", 3),
    ("Wall", "Wall Breaker", 2), ("SWall", "Super Wall Breaker", 8),
    ("Ball", "Balloon", 5), ("RBall", "Rocket Balloon", 8),
    ("Wiza", "Wizard", 4), ("SWiza", "Super Wizard", 10),
    ("Heal", "Healer", 14), ("Drag", "Dragon", 20), ("SDrag", "Super Dragon", 40),
    ("Pekk", "P.E.K.K.A", 25), ("BabyD", "Baby Dragon", 10),
    ("InfernoD", "Inferno Dragon", 15), ("Mine", "Miner", 6), ("SMine", "Super Miner", 24),
    ("EDrag", "Electro Dragon", 30), ("Yeti", "Yeti", 18), ("SYeti", "Super Yeti", 35),
    ("RDrag", "Dragon Rider", 25), ("ETitan", "Electro Titan", 32),
    ("RootR", "Root Rider", 20), ("Throw", "Thrower", 16), ("MeteorG", "Meteor Golem", 40),
    ("Mini", "Minion", 2), ("SMini", "Super Minion", 12),
    ("Hogs", "Hog Rider", 5), ("SHogs", "Super Hog Rider", 12),
    ("Valk", "Valkyrie", 8), ("SValk", "Super Valkyrie", 20),
    ("Gole", "Golem", 30), ("Witc", "Witch", 12), ("SWitc", "Super Witch", 40),
    ("Lava", "Lava Hound", 30), ("IceH", "Ice Hound", 40),
    ("Bowl", "Bowler", 6), ("SBowl", "Super Bowler", 30),
    ("IceG", "Ice Golem", 15), ("Hunt", "Headhunter", 6),
    ("AppWard", "Apprentice Warden", 20), ("Druid", "Druid", 16),
    ("Furn", "Furnace", 18), ("RuinW", "Ruin Witch", 26),
    ("Debt", "Debt Collector", 4), ("ERider", "Elephant Rider", 24),
    ("GGiant", "Giant Giant", 50), ("KANE", "KANE", 75),
    ("YEET", "YEETer", 45), ("Disarmer", "The Disarmer", 60),
    ("YUnder", "Yeti Undertaker", 80), ("Kicker", "Barbarian Kicker", 12),
    ("GThrow", "Giant Thrower", 15), ("MOMMA", "M.O.M.M.A", 100),
    ("Broom", "Broom Witch", 20), ("MECHA", "MECHA", 10),
    ("IceMini", "Ice Minion", 4), ("IceWiz", "Ice Wizard", 4),
    ("PartyWiz", "Party Wizard", 4), ("COOKIE", "COOKIE", 10),
    ("Fire", "Firecracker", 10), ("RamR", "Ram Rider", 12),
    ("RoyalG", "Royal Ghost", 8), ("PBarb", "Pumpkin Barbarian", 1),
    ("Barcher", "Barcher", 3), ("HogWiz", "Hog Wizard", 7),
    ("Lavaloon", "Lavaloon", 21), ("TThrow", "Totem Thrower", 28),
    ("WitchG", "Witch Golem", 41), ("GiantS", "Giant Skeleton", 20),
    ("SBarrel", "Skeleton Barrel", 5), ("ADrag", "Azure Dragon", 40),
    ("GDrag", "Golden Dragon", 100),
)

SPELLS = (
    ("LSpell", "Lightning", 1), ("HSpell", "Heal", 2), ("RSpell", "Rage", 2),
    ("JSpell", "Jump", 2), ("FSpell", "Freeze", 1), ("CSpell", "Clone", 3),
    ("ISpell", "Invisibility", 1), ("ReSpell", "Recall", 2), ("RvSpell", "Revive", 2),
    ("TSpell", "Totem", 1), ("PSpell", "Poison", 1), ("ESpell", "Earthquake", 1),
    ("HaSpell", "Haste", 1), ("SkSpell", "Skeleton", 1), ("BtSpell", "Bat", 1),
    ("OgSpell", "Overgrowth", 2), ("IBSpell", "Ice", 1), ("ASpell", "Angry", 1),
    ("HeSpell", "Heroic", 2),
)

HEROES = (
    ("King", "Barbarian King"), ("Queen", "Archer Queen"), ("Prince", "Minion Prince"),
    ("Warden", "Grand Warden"), ("Champion", "Royal Champion"), ("Duke", "Dragon Duke"),
)

SIEGES = (
    ("WallW", "Wall Wrecker"), ("BattleB", "Battle Blimp"), ("StoneS", "Stone Slammer"),
    ("SiegeB", "Siege Barracks"), ("LogL", "Log Launcher"), ("FlameF", "Flame Flinger"),
    ("BattleD", "Battle Drill"), ("TroopL", "Troop Launcher"), ("SkyW", "Sky Wagon"),
)

# Names accepted by DROP that are not a real unit.
SPECIAL_UNITS = ("REMAIN", "AnyS", "Castle")


def unit_catalog() -> dict[str, dict]:
    """Map every deployable short name to its metadata."""
    catalog: dict[str, dict] = {}
    for short, name, space in TROOPS:
        catalog[short] = {"name": name, "kind": "troop", "space": space}
    for short, name, space in SPELLS:
        catalog[short] = {"name": name, "kind": "spell", "space": space}
    for short, name in HEROES:
        catalog[short] = {"name": name, "kind": "hero", "space": 0}
    for short, name in SIEGES:
        catalog[short] = {"name": name, "kind": "siege", "space": 1}
    for short in SPECIAL_UNITS:
        catalog[short] = {"name": short, "kind": "special", "space": 0}
    return catalog


UNITS = unit_catalog()

# AutoIt compares strings case insensitively with "=", so the bot accepts any
# casing of a short name. The lookup table mirrors that behaviour.
_UNITS_BY_LOWER = {short.lower(): short for short in UNITS}


def lookup_unit(value: str) -> str | None:
    """Return the canonical short name, or None if the bot would discard it."""
    return _UNITS_BY_LOWER.get(value.strip().lower())


def suggest_unit(value: str) -> str | None:
    """Closest known short name, used to explain a discarded DROP row."""
    import difflib

    matches = difflib.get_close_matches(value, list(UNITS), n=1, cutoff=0.6)
    return matches[0] if matches else None
