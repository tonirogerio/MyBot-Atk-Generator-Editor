"""Command line interface for the attack generator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .emitter import write
from .parser import parse, parse_file
from .templates import TEMPLATES
from .validate import validate


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="attackgen", description="MyBot CSV attack script generator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list-templates", help="Show available templates")

    p_val = sub.add_parser("validate", help="Validate a script or all scripts in CSV/Attack")
    p_val.add_argument("path", nargs="?", default="", help="File or directory (default: ../CSV/Attack)")

    p_round = sub.add_parser("roundtrip", help="Parse -> emit -> parse and diff")
    p_round.add_argument("file", help="Input CSV")
    p_round.add_argument("-o", "--output", help="Write round-tripped file")

    p_gen = sub.add_parser("gen", help="Generate a new script from a template")
    p_gen.add_argument("--template", choices=sorted(TEMPLATES), required=True)
    p_gen.add_argument("--name", default="", help="Script name (defaults to template name)")
    p_gen.add_argument("-o", "--output", help="Output CSV path (default: prints to stdout)")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.cmd == "list-templates":
        for name in sorted(TEMPLATES):
            print(name)
        return 0

    if args.cmd == "validate":
        target = Path(args.path) if args.path else Path(__file__).resolve().parents[2] / "CSV" / "Attack"
        if target.is_file():
            scripts = [target]
        else:
            scripts = sorted(target.glob("*.csv"))
        if not scripts:
            print("no CSV files found", file=sys.stderr)
            return 1
        ok = True
        for path in scripts:
            script = parse_file(str(path))
            problems = validate(script)
            if problems:
                print(f"--- {path.name} ---")
                for p in problems:
                    print(f"  {p}")
                ok = False
            else:
                print(f"{path.name}: ok")
        return 0 if ok else 2

    if args.cmd == "roundtrip":
        original = parse_file(args.file)
        text = "\n".join(f"{c.kind} {c.cells()}" for c in original.commands)
        roundtrip = parse(render(original), original.name)
        diffs = []
        for i, (o, r) in enumerate(zip(original.commands, roundtrip.commands)):
            if type(o) != type(r) or o.cells() != r.cells():
                diffs.append((i, type(o).__name__, type(r).__name__))
        if diffs:
            print("differences:", diffs)
            return 3
        print("roundtrip: identical")
        if args.output:
            write(roundtrip, args.output)
        return 0

    if args.cmd == "gen":
        builder = TEMPLATES[args.template]
        script = builder(args.name or args.template)
        if args.output:
            write(script, args.output)
            print(f"written to {args.output}")
        else:
            sys.stdout.write(render(script))
        return 0

    return 1


def render(script) -> str:
    from .emitter import render as _render

    return _render(script)


if __name__ == "__main__":
    sys.exit(main())