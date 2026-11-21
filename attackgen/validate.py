"""Check a script against the rules enforced by the bot parser.

Every problem reported here corresponds to a row the bot would discard or a
unit it would fail to deploy.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import Drop, Make, Script, Wait
from .schema import BUILDINGS, SIDES, VERSUS, WAIT_CONDITIONS, lookup_unit, suggest_unit


@dataclass
class Problem:
    index: int  # command position, -1 for whole-script issues
    severity: str  # "error" or "warning"
    message: str

    def __str__(self) -> str:
        where = f"command {self.index + 1}" if self.index >= 0 else "script"
        return f"[{self.severity}] {where}: {self.message}"


def validate(script: Script) -> list[Problem]:
    problems: list[Problem] = []
    defined: dict[str, int] = {}
    for make in script.makes():
        for letter in _split(make.vector):
            defined[letter.upper()] = make.points

    for index, command in enumerate(script.commands):
        if isinstance(command, Make):
            problems.extend(_check_make(index, command))
        elif isinstance(command, Drop):
            problems.extend(_check_drop(index, command, defined))
        elif isinstance(command, Wait):
            problems.extend(_check_wait(index, command))

    return problems


def _check_make(index: int, make: Make) -> list[Problem]:
    problems = []
    if not _letters(make.vector):
        problems.append(Problem(index, "error", f"MAKE vector '{make.vector}' must be a single letter A-Z"))
    if make.side not in SIDES:
        problems.append(Problem(index, "error", f"MAKE side '{make.side}' is not a known side"))
    if make.versus not in VERSUS:
        problems.append(Problem(index, "error", f"MAKE versus '{make.versus}' must be INT-EXT, EXT-INT or IGNORE"))
    if make.points < 1:
        problems.append(Problem(index, "error", "MAKE drop point count must be at least 1"))
    if make.building:
        if make.building not in BUILDINGS:
            problems.append(Problem(index, "error", f"MAKE building target '{make.building}' is not recognised"))
        elif make.points not in (1, 5):
            problems.append(Problem(index, "error", "a building targeted MAKE only accepts 1 or 5 drop points"))
    return problems


def _check_drop(index: int, drop: Drop, defined: dict[str, int]) -> list[Problem]:
    problems = []
    for letter in _split(drop.vectors):
        key = letter.upper()
        if key not in defined:
            problems.append(Problem(index, "error", f"DROP uses vector '{letter}' which no MAKE defines"))
        else:
            highest = _highest_index(drop.index)
            if highest is not None and highest > defined[key]:
                problems.append(
                    Problem(
                        index,
                        "warning",
                        f"DROP index {highest} is beyond the {defined[key]} points of vector '{letter}'",
                    )
                )
    if not _range_or_list(drop.index):
        problems.append(Problem(index, "error", f"DROP index '{drop.index}' is not a number, range or list"))

    canonical = lookup_unit(drop.unit)
    if canonical is None:
        hint = suggest_unit(drop.unit)
        suffix = f" (did you mean '{hint}'?)" if hint else ""
        problems.append(
            Problem(
                index,
                "error",
                f"DROP unit '{drop.unit}' is not a known short name and will be ignored{suffix}",
            )
        )
    elif canonical != "REMAIN" and not _range_or_number(drop.quantity):
        problems.append(Problem(index, "error", f"DROP quantity '{drop.quantity}' is not a number or range"))

    for label, value in (
        ("delay", drop.delay_points),
        ("delay change", drop.delay_change),
        ("sleep", drop.sleep_after),
    ):
        if not _range_or_number(value, allow_zero=True):
            problems.append(Problem(index, "error", f"DROP {label} '{value}' is not a number or range"))
    return problems


def _check_wait(index: int, wait: Wait) -> list[Problem]:
    problems = []
    if not _range_or_number(wait.duration):
        problems.append(Problem(index, "error", f"WAIT duration '{wait.duration}' is not a number or range"))
    if wait.conditions:
        for condition in _split(wait.conditions, ","):
            if condition not in WAIT_CONDITIONS:
                problems.append(Problem(index, "warning", f"WAIT condition '{condition}' is ignored by the bot"))
    return problems


def _letters(value: str) -> bool:
    return len(value) == 1 and "A" <= value <= "Z"


def _split(value: str, separator: str = "-") -> list[str]:
    return [part.strip() for part in value.split(separator) if part.strip()]


def _highest_index(value: str) -> int | None:
    if "," in value:
        numbers = [int(part) for part in value.split(",") if part.strip().isdigit()]
    else:
        numbers = [int(part) for part in value.split("-") if part.strip().isdigit()]
    return max(numbers) if numbers else None


def _range_or_number(value: str, allow_zero: bool = False) -> bool:
    parts = value.split("-")
    if len(parts) > 2:
        return False
    floor = 0 if allow_zero else 1
    return all(part.strip().isdigit() and int(part) >= floor for part in parts if part.strip())


def _range_or_list(value: str) -> bool:
    if "," in value:
        return all(part.strip().isdigit() and int(part) >= 1 for part in value.split(","))
    return _range_or_number(value)
