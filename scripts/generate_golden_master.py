#!/usr/bin/env python
"""Generate or approve tests/golden_master_expected.txt from current solver output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
_TESTS = _ROOT / "tests"
for path in (_SRC, _TESTS):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from boundary.screen_boundary import ScreenBoundary  # noqa: E402
from control.solve import resolve  # noqa: E402
from golden_master_support import (  # noqa: E402
    GOLDEN_MASTER_PATH,
    build_golden_document,
    write_golden_master,
)


def main() -> int:
    """Build golden master baseline from ScreenBoundary + resolve pipeline."""
    parser = argparse.ArgumentParser(
        description="Generate MagicSquare_xx golden master expected output.",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Overwrite the baseline file with current solver output.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=GOLDEN_MASTER_PATH,
        help=f"Output path (default: {GOLDEN_MASTER_PATH})",
    )
    args = parser.parse_args()

    boundary = ScreenBoundary(resolve=resolve)
    document = build_golden_document(boundary)

    if args.approve or not args.output.exists():
        path = write_golden_master(document, args.output)
        action = "approved" if args.approve else "created"
        print(f"Golden master {action}: {path}")
        return 0

    existing = args.output.read_text(encoding="utf-8")
    if existing == document:
        print(f"Golden master unchanged: {args.output}")
        return 0

    print(
        "Golden master differs from current output. "
        "Re-run with --approve to update.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
