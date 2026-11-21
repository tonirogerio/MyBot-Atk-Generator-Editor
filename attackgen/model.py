"""Typed model of one attack script.

A script is an ordered list of commands. Only MAKE, DROP, WAIT and RECALC are
executed by the bot; NOTE and unknown rows are kept so round-tripping an
existing script does not lose its documentation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Note:
    kind: ClassVar[str] = "NOTE"
    text: str = ""

    def cells(self) -> list[str]:
        return ["NOTE", self.text]


@dataclass
class Make:
    kind: ClassVar[str] = "MAKE"
    vector: str = "A"
    side: str = "FRONT-LEFT"
    points: int = 10
    add_tiles: int = 1
    versus: str = "INT-EXT"
    random_x: int = 0
    random_y: int = 0
    building: str = ""

    def cells(self) -> list[str]:
        return [
            "MAKE", self.vector, self.side, str(self.points), str(self.add_tiles),
            self.versus, str(self.random_x), str(self.random_y), self.building,
        ]


@dataclass
class Drop:
    kind: ClassVar[str] = "DROP"
    vectors: str = "A"
    index: str = "1"
    quantity: str = "1"
    unit: str = "Barb"
    delay_points: str = "128"
    delay_change: str = "0"
    sleep_after: str = "16-32"

    def cells(self) -> list[str]:
        return [
            "DROP", self.vectors, self.index, self.quantity, self.unit,
            self.delay_points, self.delay_change, self.sleep_after,
        ]


@dataclass
class Wait:
    kind: ClassVar[str] = "WAIT"
    duration: str = "3000"
    conditions: str = ""

    def cells(self) -> list[str]:
        return ["WAIT", self.duration, self.conditions]


@dataclass
class Recalc:
    kind: ClassVar[str] = "RECALC"

    def cells(self) -> list[str]:
        return ["RECALC"]


@dataclass
class Raw:
    """A line the generator does not model, kept verbatim."""

    kind: ClassVar[str] = "RAW"
    raw: str = ""

    def cells(self) -> list[str]:
        return []


@dataclass
class Script:
    name: str = "NewAttack"
    commands: list = field(default_factory=list)

    def makes(self) -> list[Make]:
        return [c for c in self.commands if isinstance(c, Make)]

    def drops(self) -> list[Drop]:
        return [c for c in self.commands if isinstance(c, Drop)]

    def notes(self) -> list[Note]:
        return [c for c in self.commands if isinstance(c, Note)]

    def vector_names(self) -> list[str]:
        names: list[str] = []
        for make in self.makes():
            for letter in make.vector.split("-"):
                letter = letter.strip().upper()
                if letter and letter not in names:
                    names.append(letter)
        return names
