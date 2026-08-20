#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from research_site.math_audit import audit_math_tree


SITE_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit display math in knowledge Markdown files.")
    parser.add_argument(
        "--root",
        type=Path,
        default=SITE_ROOT / "content" / "knowledge",
        help="Markdown tree to audit",
    )
    args = parser.parse_args()

    issues = audit_math_tree(args.root)
    for issue in issues:
        expression = " ".join(issue.expression.split())
        print(f"{issue.path}:{issue.block}: {issue.rule}: {expression}")
    print(f"math audit: {len(issues)} issue(s)")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
