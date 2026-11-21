"""Read a MyBot attack CSV into a Script."""

from __future__ import annotations

import re

from .model import Drop, Make, Note, Raw, Recalc, Script, Wait

# The bot splits every line on "|" and requires at least 8 cells before it
# treats the row as a command (ParseAttackCSV.au3).
_MIN_CELLS = 8


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.split("|")]


def parse(text: str, name: str = "") -> Script:
    script = Script(name=name)
    for line in text.splitlines():
        cells = _cells(line)
        first = cells[0].upper() if cells else ""
        # The bot treats every NOTE line as a comment, even when it has fewer
        # than the eight cells a command row needs.
        if first == "NOTE":
            script.commands.append(Note(text=_cell(cells, 1)))
            continue
        if len(cells) < _MIN_CELLS:
            if line.strip():
                script.commands.append(Raw(raw=line))
            continue
        command = first
        if command in ("", "TRAIN", "WMODE", "REDLN", "DRPLN", "CCREQ", "CCSPL"):
            script.commands.append(Raw(raw=line))
        elif command == "MAKE":
            script.commands.append(_make(cells))
        elif command == "DROP":
            script.commands.append(_drop(cells))
        elif command == "WAIT":
            script.commands.append(Wait(duration=cells[1], conditions=_cell(cells, 2)))
        elif command == "RECALC":
            script.commands.append(Recalc())
        else:
            script.commands.append(Raw(raw=line))
    return script


def parse_file(path: str) -> Script:
    with open(path, encoding="utf-8-sig") as handle:
        text = handle.read()
    name = re.sub(r"\.csv$", "", path.replace("\\", "/").rsplit("/", 1)[-1])
    return parse(text, name)


def _cell(cells: list[str], index: int) -> str:
    return cells[index] if index < len(cells) else ""


def _make(cells: list[str]) -> Make:
    return Make(
        vector=_cell(cells, 1),
        side=_cell(cells, 2),
        points=_int(_cell(cells, 3), 1),
        add_tiles=_int(_cell(cells, 4), 0),
        versus=_cell(cells, 5) or "INT-EXT",
        random_x=_int(_cell(cells, 6), 0),
        random_y=_int(_cell(cells, 7), 0),
        building=_cell(cells, 8),
    )


def _drop(cells: list[str]) -> Drop:
    return Drop(
        vectors=_cell(cells, 1),
        index=_cell(cells, 2) or "1",
        quantity=_cell(cells, 3) or "1",
        unit=_cell(cells, 4),
        delay_points=_cell(cells, 5) or "0",
        delay_change=_cell(cells, 6) or "0",
        sleep_after=_cell(cells, 7) or "0",
    )


def _int(value: str, default: int) -> int:
    try:
        return int(value)
    except ValueError:
        return default
