#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from research_site.build import build_site
from research_site.catalog import CatalogError, load_catalog


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the static research site")
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--base-url", default="/research/")
    args = parser.parse_args()
    site_root = args.site_root.resolve()
    output = args.output.resolve() if args.output else site_root / "_site"
    try:
        catalog = load_catalog(site_root / "content")
        build_site(catalog, site_root, output, args.base_url)
    except CatalogError as exc:
        parser.error(str(exc))
    print(
        f"built {len(catalog.projects)} projects, {len(catalog.studies)} studies, "
        f"and {len(catalog.reports)} reports at {output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
