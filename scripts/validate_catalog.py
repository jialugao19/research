#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from research_site.catalog import CatalogError, load_catalog


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate project and report manifests")
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        catalog = load_catalog(args.site_root.resolve() / "content")
    except CatalogError as exc:
        parser.error(str(exc))
    print(
        f"catalog valid: {len(catalog.projects)} projects, "
        f"{len(catalog.studies)} studies, {len(catalog.reports)} reports"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
