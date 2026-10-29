"""Command-line interface: ``ddi-toolkit <calculator> --input value ...``.

Educational use only: every calculator teaches the reasoning in the book with
simplified static models and must not be used for dosing or clinical decisions.
"""

from __future__ import annotations

import argparse
import inspect
import json
import sys
import typing
from typing import List, Optional

from . import __version__
from .registry import CALCULATORS, CAVEAT, PARAM_HELP, Calculator


_ASCII = str.maketrans({
    "–": "-", "—": "-", "−": "-", "×": "x", "·": ".",
    "≈": "~", "Δ": "delta ", "Ω": "Omega", "√": "sqrt", "±": "+/-",
    "≤": "<=", "≥": ">=", "÷": "/", "’": "'", "µ": "u",
})


def _ascii(text: str) -> str:
    """Plain-ASCII text, so that help and results print on any console encoding."""
    return text.translate(_ASCII).encode("ascii", "replace").decode("ascii")


def _arg_type(func, name: str):
    hints = typing.get_type_hints(func)
    hint = hints.get(name, float)
    args = typing.get_args(hint) or (hint,)
    return int if int in args and float not in args else float


def _add_calculator(sub, calc: Calculator) -> None:
    p = sub.add_parser(
        calc.name,
        help=_ascii(calc.summary).replace("%", "%%"),
        description=_ascii(
            f"{calc.summary}\nSource: {calc.source}.\nAssumption: {calc.assumption}\n{CAVEAT}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    for name, param in inspect.signature(calc.func).parameters.items():
        flag = "--" + name.replace("_", "-")
        required = param.default is inspect.Parameter.empty
        help_text = PARAM_HELP.get(name, name)
        if not required and param.default is not None:
            help_text += f" (default {param.default:g})"
        elif not required:
            help_text += " (optional)"
        p.add_argument(
            flag,
            dest=name,
            type=_arg_type(calc.func, name),
            required=required,
            default=None if required else param.default,
            metavar="X",
            help=_ascii(help_text).replace("%", "%%"),
        )
    p.set_defaults(_calc=calc)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ddi-toolkit",
        description=(
            "Calculators from 'Drug-Drug Interactions in Drug Safety and Pharmacovigilance'. "
            + CAVEAT
        ),
        epilog="Run 'ddi-toolkit <calculator> --help' for its inputs, source, and assumption.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    sub = parser.add_subparsers(title="calculators", dest="calculator", metavar="<calculator>")
    for calc in CALCULATORS.values():
        _add_calculator(sub, calc)
    return parser


def _format(value) -> str:
    if value is None:
        return "undefined"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    calc: Optional[Calculator] = getattr(args, "_calc", None)
    if calc is None:
        parser.print_help()
        return 1
    kwargs = {
        name: getattr(args, name)
        for name in inspect.signature(calc.func).parameters
        if getattr(args, name) is not None
    }
    try:
        result = calc.func(**kwargs)
    except ValueError as exc:
        print(_ascii(f"ddi-toolkit {calc.name}: error: {exc}"), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"calculator": calc.name, "inputs": kwargs, "result": result}, indent=2))
        return 0
    print(f"{calc.name}  ({calc.source})")
    width = max(len(k) for k in result)
    for key, value in result.items():
        print(_ascii(f"  {key.ljust(width)}  {_format(value)}"))
    print(_ascii(f"Assumption: {calc.assumption}"))
    print(CAVEAT)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
