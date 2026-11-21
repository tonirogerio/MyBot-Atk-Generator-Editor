"""Write a Script back to the pipe format the bot reads."""

from __future__ import annotations

from .model import Note, Raw, Script

# Column widths chosen so a generated file lines up like the hand written
# scripts shipped with the bot.
_WIDTHS = (6, 11, 11, 11, 11, 11, 11, 11, 11)


def render(script: Script) -> str:
    lines = []
    for command in script.commands:
        if isinstance(command, Raw):
            lines.append(command.raw)
        elif isinstance(command, Note):
            lines.append(f"NOTE  |{command.text}")
        else:
            lines.append(_row(command.cells()))
    text = "\n".join(lines)
    if not text.endswith("\n"):
        text += "\n"
    return text


def write(script: Script, path: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(render(script))


def _row(cells: list[str]) -> str:
    # The bot needs at least eight cells before it treats a line as a command,
    # so short commands such as WAIT are padded out to nine columns.
    cells = list(cells) + [""] * (9 - len(cells))
    padded = [
        cell.ljust(_WIDTHS[index] if index < len(_WIDTHS) else 11)
        for index, cell in enumerate(cells)
    ]
    return "|".join(padded) + "|"
