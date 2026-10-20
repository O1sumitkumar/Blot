"""blot: history-aware pre-commit checks.

Commands:
    index         build or refresh the local history index (.git/blot.db)
    check         run all checks against staged changes (pre-commit) or a commit range
    why           show the history behind a line: fix commits, PR, linked issues
    install-hook  add blot to .git/hooks/pre-commit
    bench         score the checks against bench/cases.json
"""

from __future__ import annotations

import argparse
import sys

from blot import __version__
from blot.checks import all_checks
from blot.config import load_config
from blot.report import render


def _cmd_index(args: argparse.Namespace) -> int:
    from blot.index import build_index

    build_index(args.repo, full=args.full, github=args.github)
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    from blot.diff import read_changes
    from blot.store import Store

    config = load_config(args.repo)
    store = Store.open(args.repo)
    if store is None:
        # Never break a commit because the index is missing; just say how to fix it.
        print("blot: no index yet, run `blot index` (commit allowed)", file=sys.stderr)
        return 0

    changes = read_changes(args.repo, rev_range=args.range)
    findings = [f for check in all_checks(config) for f in check.run(changes, store, config)]
    print(render(findings, fmt=args.format), end="")
    return 1 if (args.strict and findings) else 0


def _cmd_why(args: argparse.Namespace) -> int:
    raise NotImplementedError("TODO(M3): trace a line to its explaining commits")


def _cmd_install_hook(args: argparse.Namespace) -> int:
    raise NotImplementedError("TODO(M1): write .git/hooks/pre-commit without clobbering existing hooks")


def _cmd_bench(args: argparse.Namespace) -> int:
    raise NotImplementedError("TODO(M4): run bench/cases.json and print precision/recall per check")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="blot", description="History-aware pre-commit checks.")
    parser.add_argument("--version", action="version", version=f"blot {__version__}")
    parser.add_argument("--repo", default=".", help="path to the git repository (default: .)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("index", help="build or refresh the local history index")
    p.add_argument("--full", action="store_true", help="rebuild from scratch instead of incrementally")
    p.add_argument("--github", action="store_true", help="add PR/issue data via the gh CLI")
    p.set_defaults(func=_cmd_index)

    p = sub.add_parser("check", help="run history checks on staged changes or a commit range")
    p.add_argument("--staged", action="store_true", help="check staged changes (the default)")
    p.add_argument("--range", metavar="A..B", help="check a commit range instead, e.g. origin/main..HEAD")
    p.add_argument("--strict", action="store_true", help="exit 1 when there are findings (blocks the commit)")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.set_defaults(func=_cmd_check)

    p = sub.add_parser("why", help="show the history behind a line")
    p.add_argument("location", metavar="FILE:LINE")
    p.set_defaults(func=_cmd_why)

    p = sub.add_parser("install-hook", help="add blot to .git/hooks/pre-commit")
    p.set_defaults(func=_cmd_install_hook)

    p = sub.add_parser("bench", help="score checks against bench/cases.json")
    p.set_defaults(func=_cmd_bench)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
