"""Check the real production script and the built in templates."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from attackgen.emitter import render
from attackgen.parser import parse, parse_file
from attackgen.templates import TEMPLATES
from attackgen.validate import validate

REAL_SCRIPT = Path(__file__).resolve().parents[2] / "CSV" / "Attack" / "PHMOD-MeteorMayhem.csv"


def test_real_script_is_caught_bugs() -> None:
    """The production script has four unit names the bot silently ignores.

    This guards the validator: it must keep flagging them until they are fixed.
    """
    script = parse_file(str(REAL_SCRIPT))
    errors = [p for p in validate(script) if p.severity == "error"]
    ignored = {p.message.split("'")[1] for p in errors if "known short name" in p.message}
    assert ignored == {"FireC", "BDrill", "FlamF", "WWreck", "BBlimp"}, ignored
    assert len(script.makes()) == 11


def test_round_trip_keeps_commands() -> None:
    original = parse_file(str(REAL_SCRIPT))
    again = parse(render(original), "roundtrip")
    kinds = lambda s: [type(c).__name__ for c in s.commands if type(c).__name__ != "Raw"]
    assert kinds(again) == kinds(original)
    assert [(d.unit, d.quantity) for d in again.drops()] == [
        (d.unit, d.quantity) for d in original.drops()
    ]


def test_templates_are_valid() -> None:
    for name, builder in TEMPLATES.items():
        problems = [p for p in validate(builder()) if p.severity == "error"]
        assert not problems, f"{name}:\n" + "\n".join(map(str, problems))


def test_case_insensitive_units() -> None:
    script = parse(
        "\n".join(
            [
                "MAKE  |A |FRONT-LEFT |10 |1 |INT-EXT |0 |0 |",
                "DROP  |A |1 |1 |king |128 |0 |16-32 |",
                "DROP  |A |1 |1 |QUEEN |128 |0 |16-32 |",
            ]
        )
    )
    assert not [p for p in validate(script) if p.severity == "error"]


if __name__ == "__main__":
    test_real_script_is_caught_bugs()
    test_round_trip_keeps_commands()
    test_templates_are_valid()
    test_case_insensitive_units()
    script = parse_file(str(REAL_SCRIPT))
    print(f"PHMOD-MeteorMayhem: {len(script.makes())} vectors, {len(script.drops())} drops")
    for problem in validate(script):
        print(" ", problem)
    for name in TEMPLATES:
        print(f"template '{name}': valid")
